import os
import io
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
        self.query_conditions = {
            'im_in_owners': "'yambakshi@gmail.com' in owners",
            'not_in_trash': "trashed = false"
        }

    def download_all_files(self, file_types: []):
        all_files_paths = {}
        for file_type in file_types:
            config = CONFIG['downloads'][file_type]
            if self.cache_service.cache_exists(config['cache_file']):
                files_paths = self.__load_cache(config)
            else:
                files_paths = self.__iterate_all_files(config)
            all_files_paths[file_type] = files_paths

        return all_files_paths

    def download_files(self, file_type: str, page_size: int):
        config = CONFIG['downloads'][file_type]
        self.logger.debug(f"Downloading '{config['file_type']}' files from 'Google Drive'")
        results = self.__search_drive(config, page_size, None)
        files_paths = self.__iterate_files(config, results, False)
        self.logger.debug(f"{len(files_paths)} files downloaded")
        return files_paths

    def __load_cache(self, config: {}):
        if hasattr(config, 'save_as'):
            file_type = config['save_as']
        else:
            file_type = config['download_as']

        self.logger.debug(
            f"Loading '{file_type}' files from 'cache/{config['cache_file']}'")
        cache = self.cache_service.read(config['cache_file'])
        files_paths = cache.split('\n')[:-1]
        self.logger.debug(
            f"Loaded {len(files_paths)} '{file_type}' files from 'cache/{config['cache_file']}'")
        return files_paths

    def __iterate_all_files(self, config: {}):
        files_paths = []
        page_token = None

        self.logger.debug(
            f"Downloading all '{config['file_type']}' files from 'Google Drive'")

        # Download preparation
        Path(r'tmp').mkdir(parents=True, exist_ok=True)
        self.cache_service.clear_cache(config['cache_file'])

        # Iterate all pages
        while True:
            results = self.__search_drive(config, None, page_token)
            files_paths += self.__iterate_files(config, results)
            page_token = results.get('nextPageToken', None)
            if page_token is None:
                break

        self.logger.debug(
            f"Downloaded {len(files_paths)} '{config['file_type']}' files from 'Google Drive'")
        return files_paths

    def __iterate_files(self, config: {}, results, cache_files=True):
        files_paths = []
        for file in results.get('files', []):
            file_id = file.get('id')
            file_name = file.get('name')
            file_parents = file.get('parents')
            file_directories_path = self.__get_file_directories_path(
                file_parents[0])

            # Create file folders by its path
            Path(f"tmp/{file_directories_path}").mkdir(parents=True,
                                                       exist_ok=True)

            # Download file by id
            if config['file_type'] in GOOGLE_FILE_TYPES:
                request = self.drive.files().export_media(fileId=file_id,
                                                          mimeType=config['download_as'])
                file_path = f"{file_directories_path}{file_name}.{config['save_as']}"
            else:
                request = self.drive.files().get_media(fileId=file_id)
                file_path = f"{file_directories_path}{file_name}"

            fh = io.FileIO(f"tmp/{file_path}", 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                download_progress = "%d%%" % int(status.progress() * 100)

                file_path_no_root = '/'.join(file_path.split('/')[1:])
                files_paths.append(file_path_no_root)
                if cache_files:
                    self.cache_service.write(
                        config['cache_file'], file_path_no_root)
                self.logger.debug(
                    f"Downloaded {download_progress} of '{file_path}'")

        return files_paths

    def __search_drive(self, config: {}, page_size: int, page_token):
        search_params = {
            'pageSize': page_size,
            'q': f"mimeType='{config['file_type']}' and {self.query_conditions['im_in_owners']} and {self.query_conditions['not_in_trash']}",
            'spaces': 'drive',
            'fields': '*',
            'pageToken': page_token
        }

        results = self.drive.files().list(**search_params).execute()
        return results

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

    def __get_file_directories_path(self, parent_directory_id: str):
        raw_directories_path = self.__query_directories_path(
            parent_directory_id, [])
        directories_path = ''
        for directory in raw_directories_path:
            directories_path = f"{directory['name']}/{directories_path}"

        return f"{directories_path}"
