import os
import io
import datetime
import shutil
import logging
from googleapiclient.http import MediaIoBaseDownload
from pathlib import Path
from utils.google_drive import init_drive
from config.config import CONFIG


GOOGLE_FILE_TYPES = [
    'application/vnd.google-apps.document',
    'application/vnd.google-apps.spreadsheet'
]


class GoogleDriveService:
    def __init__(self, cache_service):
        self.logger = logging.getLogger('backup_system')
        self.drive = init_drive()
        self.cache_service = cache_service

    def download_changes(self, files_paths: {}):
        self.logger.debug("Downloading modified files from 'Google Drive'")
        self.files_paths = files_paths
        downloads = {
            'new': [],
            'modified': []
        }

        # Reset tmp folder
        if os.path.isdir('./tmp'):
            shutil.rmtree(r'tmp')
        os.mkdir('tmp')

        for file_type, files in files_paths['drive'].items():
            for file_path, file_data in files.items():
                # Make sure only files in 'drive_stream' that are Google Drive types (Google Doc, Google Sheet etc.) are downloaded
                if not self.__file_in_space('drive_stream', file_path, file_type) or CONFIG['drive'][file_type]['file_type'] not in GOOGLE_FILE_TYPES:
                    continue

                file_id, file_last_modified = file_data.values()
                if not self.__file_in_space('local', file_path, file_type):
                    downloads['new'].append(file_path)
                    self.__download_file(file_id, file_type,
                                         file_path, file_last_modified)
                    continue

                local_file_last_modified = files_paths['local'][file_type][file_path]['last_modified']
                if file_last_modified <= local_file_last_modified:
                    continue

                self.__download_file(file_id, file_type,
                                     file_path, file_last_modified)
                downloads['modified'].append(file_path)

        modified_len = len(downloads['modified'])
        if modified_len == 0:
            self.logger.debug(
                "Nothing to download. All 'local' files are up-to-date")
        else:
            self.logger.debug(f"Downloaded {modified_len} modified files")

        new_len = len(downloads['new'])
        if new_len == 0:
            self.logger.debug(
                "Nothing to download. No new files were found on 'Google Drive'")
        else:
            self.logger.debug(f"Downloaded {new_len} new files")

        return downloads

    def scan(self, files_types: [], cache_scan: bool):
        files_paths = {}
        for file_type in files_types:
            self.logger.debug(
                f"Searching '{file_type}' files on  'Google Drive'")
            self.config = CONFIG['drive'][file_type]
            if self.cache_service.cache_exists(self.config['cache_file']):
                files_paths[file_type] = self.__load_cache()
            else:
                files_paths[file_type] = self.__iterate_files(
                    file_type, cache_scan)

        return files_paths

    def __file_in_space(self, space, file_path: str, file_type: str):
        # Create a list of all paths in the specified space for the specified file type
        files_paths = list(self.files_paths[space][file_type].keys())
        return file_path in files_paths

    def __iterate_files(self, file_type: str, cache_scan: bool):
        files_paths = {}
        page_token = None

        self.logger.debug(
            f"Searching '{file_type}' files on 'Google Drive'")

        # Iterate files
        while True:
            results = self.__search_drive(None, page_token)
            files_paths = {
                **files_paths,
                **self.__process_results(results, cache_scan)
            }
            page_token = results.get('nextPageToken', None)
            if page_token is None:
                break

        self.logger.debug(
            f"Downloaded {len(files_paths)} '{file_type}' files from 'Google Drive'")
        return files_paths

    def __search_drive(self, page_size: int, page_token):
        search_params = {
            'pageSize': page_size,
            'q': f"mimeType='{self.config['file_type']}' and 'yambakshi@gmail.com' in owners and trashed = false",
            'spaces': 'drive',
            'fields': '*',
            'pageToken': page_token
        }

        results = self.drive.files().list(**search_params).execute()
        return results

    def __process_results(self, results, cache_scan: bool):
        files_paths = {}
        for file in results.get('files', []):
            file_id = file.get('id')
            file_name = file.get('name')
            file_parents = file.get('parents')
            file_last_modified = file.get('modifiedTime')
            file_last_modified_timestamp = datetime.datetime.strptime(
                file_last_modified, '%Y-%m-%dT%H:%M:%S.%f%z').timestamp()
            file_directory_path = self.__get_file_directory_path(
                file_parents[0])
            file_directory_path = '/'.join(file_directory_path.split('/')[1:])
            file_path = f"{file_directory_path}{file_name}"
            if self.config['file_type'] in GOOGLE_FILE_TYPES:
                file_path = f"{file_path}.{self.config['extension']}"

            self.logger.debug(f"Found file: '{file_path}'")

            if cache_scan:
                self.cache_service.write(
                    self.config['cache_file'], f"{file_path}|{file_last_modified_timestamp}|{file_id}")
            files_paths[file_path] = {
                'id': file_id,
                'last_modified': file_last_modified_timestamp
            }

        return files_paths

    def __load_cache(self):
        self.logger.debug(
            f"Loading '{self.config['extension']}' files paths from 'cache/{self.config['cache_file']}'")
        cache_contents = self.cache_service.read(self.config['cache_file'])
        cache_lines = cache_contents.split('\n')[:-1]
        files_paths = {}
        for line in cache_lines:
            file_path, file_last_modified, file_id = line.split('|')

            files_paths[file_path] = {'id': file_id,
                                      'last_modified': float(file_last_modified)}
        self.logger.debug(
            f"Loaded {len(files_paths)} '{self.config['extension']}' files from 'cache/{self.config['cache_file']}'")

        return files_paths

    def __download_file(self, file_id: str, file_type: str, file_path: str, file_last_modified: float):
        tmp_abs_path = os.path.abspath('tmp')
        request = self.drive.files().export_media(fileId=file_id,
                                                  mimeType=CONFIG['drive'][file_type]['download_as'])
        file_directory_path = '/'.join(file_path.split('/')[:-1])
        Path(f"tmp/{file_directory_path}").mkdir(parents=True,
                                                 exist_ok=True)
        fh = io.FileIO(f"tmp/{file_path}", 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            download_progress = "%d%%" % int(status.progress() * 100)

            file_path_backslash = file_path.replace('/', '\\')
            file_abs_path = f"{tmp_abs_path}\\{file_path_backslash}"
            os.utime(file_abs_path, (file_last_modified, file_last_modified))
            self.logger.debug(
                f"Downloaded {download_progress} of '{file_path}'")

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
            directories_path = f"{directory['name']}/{directories_path}"

        return f"{directories_path}"
