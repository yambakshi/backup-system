import os
import io
import datetime
import shutil
import logging
from googleapiclient.http import MediaIoBaseDownload
from pathlib import Path
from utils.google_drive import init_drive
from config.config import CONFIG, GOOGLE_FILE_TYPES


class GoogleDriveService:
    def __init__(self, cache_service):
        self.logger = logging.getLogger('backup_system')
        self.drive = init_drive()
        self.cache_service = cache_service

    def scan(self, load_cache: bool):
        files_paths = {}
        for file_type, config in CONFIG['drive'].items():
            if load_cache and os.path.isfile(f"caches/{config['cache_file']}"):
                files_paths[file_type] = self.__load_cache(config)
            else:
                files_paths[file_type] = self.__iterate_files(file_type)

        return files_paths

    def download_changes(self, diff: {}):
        self.logger.debug("Downloading changes from 'drive'")

        # Reset tmp folder
        if os.path.isdir('./tmp'):
            shutil.rmtree(r'tmp')
        os.mkdir('tmp')

        for diff_type, files_data in diff.items():
            if diff_type == 'removed':
                continue

            for file_data in files_data:
                # Skipping files that were removed or Non-Google types (Google Doc, Google Sheet etc.)
                if not file_data['is_google_type']:
                    continue

                # Download file
                self.__download_file(file_data)

        new_len = len(
            list(filter(lambda file_data: file_data['is_google_type'], diff['new'])))
        modified_len = len(
            list(filter(lambda file_data: file_data['is_google_type'], diff['modified'])))
        if new_len == 0 and modified_len == 0:
            self.logger.debug(f"Nothing to download")
        else:
            if new_len > 0:
                self.logger.debug(f"Downloaded {new_len} new files")
            if modified_len > 0:
                self.logger.debug(f"Downloaded {modified_len} modified files")

    def __iterate_files(self, file_type: str):
        files_paths = {}
        page_token = None

        file_extension = CONFIG['drive'][file_type]['extension']
        search_file_type = CONFIG['drive'][file_type]['file_type']
        self.logger.debug(
            f"Searching '{file_extension}' files on 'Google Drive'")

        # Iterate files
        while True:
            results = self.__search_drive(search_file_type, None, page_token)
            new_files_paths = self.__process_results(
                file_type, file_extension, results)
            files_paths = {**files_paths, **new_files_paths}

            page_token = results.get('nextPageToken', None)
            if page_token is None:
                break

        self.logger.debug(
            f"Found {len(files_paths)} '{file_extension}' files from 'Google Drive'")
        return files_paths

    def __search_drive(self, file_type: str, page_size: int, page_token):
        search_params = {
            'pageSize': page_size,
            'q': f"mimeType='{file_type}' and 'yambakshi@gmail.com' in owners and trashed = false",
            'spaces': 'drive',
            'fields': '*',
            'pageToken': page_token
        }

        results = self.drive.files().list(**search_params).execute()
        return results

    def __process_results(self, file_type: str, file_extension: str, results):
        files_paths = {}
        for file in results.get('files', []):
            file_id = file.get('id')
            file_name = file.get('name')
            file_parents = file.get('parents')
            file_last_modified = file.get('modifiedTime')

            # Get file's last modified timestamp
            file_last_modified_timestamp = datetime.datetime.strptime(
                file_last_modified, '%Y-%m-%dT%H:%M:%S.%f%z').timestamp()

            # Get file's directory path
            file_directory_path = self.__get_file_directory_path(
                file_parents[0])
            file_directory_path = '\\'.join(
                file_directory_path.split('\\')[1:])

            # Check if file's type is a google file type
            file_path = f"{file_directory_path}{file_name}"
            is_google_type = file_type in GOOGLE_FILE_TYPES
            if is_google_type:
                file_path = f"{file_path}.{file_extension}"

            self.logger.debug(f"Found file: '{file_path}'")
            files_paths[file_path] = {
                'id': file_id,
                'last_modified': file_last_modified_timestamp,
                'is_google_type': is_google_type
            }

        return files_paths

    def __download_file(self, file_data: {}):
        file_type = file_data['type']
        file_path = file_data['path']

        self.logger.debug(f"Downloading '{file_path}'...")
        request = self.drive.files().export_media(fileId=file_data['id'],
                                                  mimeType=CONFIG['drive'][file_type]['download_as'])

        file_directory_path = '\\'.join(file_path.split('\\')[:-1])
        Path(f"tmp\\{file_directory_path}").mkdir(parents=True,
                                                  exist_ok=True)
        fh = io.FileIO(f"tmp\\{file_path}", 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()

    def __query_directories_path(self, parent_directory_id: str, file_path: str):
        parent_directory = self.drive.files().get(
            fileId=parent_directory_id, fields='id, name, parents').execute()
        parent_directory_parents = parent_directory.get('parents')
        if parent_directory_parents:
            file_path.append({
                'id': parent_directory.get('id'),
                'name': parent_directory.get('name'),
                'parents': parent_directory_parents[0]
            })

            return self.__query_directories_path(parent_directory_parents[0], file_path)

        file_path.append({
            'id': parent_directory.get('id'),
            'name': parent_directory.get('name')
        })

        return file_path

    def __get_file_directory_path(self, parent_directory_id: str):
        raw_directories_path = self.__query_directories_path(
            parent_directory_id, [])
        directories_path = ''
        for directory in raw_directories_path:
            directories_path = f"{directory['name']}\\{directories_path}"

        return f"{directories_path}"

    def __load_cache(self, config: {}):
        self.logger.debug(
            f"Loading '{config['extension']}' files from 'caches/{config['cache_file']}'")
        cache_contents = self.cache_service.read(config['cache_file'])
        cache_lines = cache_contents.split('\n')[:-1]
        files_paths = {}
        for line in cache_lines:
            file_path, file_id, file_last_modified = line.split('|')
            files_paths[file_path] = {
                'id': file_id,
                'last_modified': float(file_last_modified)
            }

        self.logger.debug(
            f"Loaded {len(files_paths)} '{config['extension']}' files from 'caches/{config['cache_file']}'")
        return files_paths
