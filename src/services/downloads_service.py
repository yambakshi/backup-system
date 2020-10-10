import os
import io
import shutil
import logging
from .google_drive_service import GoogleDriveService
from pathlib import Path
from googleapiclient.http import MediaIoBaseDownload


class DownloadsService:
    def __init__(self, cache_service):
        self.logger = logging.getLogger('backup_system')
        self.cache_service = cache_service
        self.drive = GoogleDriveService().get_drive()
        self.query_conditions = {
            'im_in_owners': "'yambakshi@gmail.com' in owners",
            'visibility': "visibility != 'anyoneCanFind' and visibility != 'anyoneWithLink' and visibility != 'domainCanFind' and visibility != 'domainWithLink' and visibility != 'limited'",
            'not_in_trash': "trashed = false"
        }

    def download_all_files_by_type(self, config: {}):
        if self.cache_service.cache_exists(config['cache_file']):
            downloaded_files = self.__load_cache(config)
        else:
            downloaded_files = self.__download_all_files(config)

        return downloaded_files

    def __load_cache(self, config):
        self.logger.debug(
            f"Loading '{config['file_type']}' files from 'cache/{config['cache_file']}'")
        cache = self.cache_service.read(config['cache_file'])
        downloaded_files = cache.split('\n')[:-1]
        self.logger.debug(
            f"{len(downloaded_files)} '{config['file_type']}' files loaded from 'cache/{config['cache_file']}'")
        return downloaded_files

    def download_files_by_type(self, config: {}, page_size: int):
        self.logger.debug(
            f"Downloading '{config['file_type']}' files from 'Google Drive'")
        self.__reset_tmp_folder()
        results = self.__search_drive(config, page_size, None)
        downloaded_files = self.__download_files(config, results, False)
        self.logger.debug(f"{len(downloaded_files)} files downloaded")
        return downloaded_files

    def __download_all_files(self, config):
        downloaded_files = []
        page_token = None

        self.__reset_tmp_folder()
        self.cache_service.clear_cache(config['cache_file'])
        self.logger.debug(
            f"Downloading all '{config['file_type']}' files from 'Google Drive'")

        # Iterate all pages
        while True:
            results = self.__search_drive(config, None, page_token)
            downloaded_files += self.__download_files(config, results)
            page_token = results.get('nextPageToken', None)
            if page_token is None:
                break

        self.logger.debug(
            f"{len(downloaded_files)} '{config['file_type']}' files downloaded from 'Google Drive'")
        return downloaded_files

    def __download_files(self, config, results, cache_files=True):
        downloaded_files = []
        for file in results.get('files', []):
            file_id = file.get('id')
            file_name = file.get('name')
            file_parents = file.get('parents')
            file_directories_path = self.__get_file_directories_path(
                self.drive, file_parents[0])

            # Create file folders by its path
            Path(f"tmp/{file_directories_path}").mkdir(parents=True,
                                                       exist_ok=True)

            # Download file by id
            request = self.drive.files().export_media(fileId=file_id,
                                                      mimeType=config['download_as'])
            file_path = f"{file_directories_path}{file_name}.{config['save_as']}"
            fh = io.FileIO(f"tmp/{file_path}", 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                download_progress = "%d%%" % int(status.progress() * 100)

                file_path_no_root = '/'.join(file_path.split('/')[1:])
                downloaded_files.append(file_path_no_root)
                if cache_files:
                    self.cache_service.write(
                        config['cache_file'], file_path_no_root)
                self.logger.debug(
                    f"Downloaded {download_progress} of '{file_path}' ({file_id})")

        return downloaded_files

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

    def __query_directories_path(self, driver_service, parent_directory_id: str, file_path):
        parent_directory = driver_service.files().get(
            fileId=parent_directory_id, fields='id, name, parents').execute()
        parent_directory_parents = parent_directory.get('parents')
        if parent_directory_parents:
            file_path.append({
                'id': parent_directory.get('id'),
                'name': parent_directory.get('name'),
                'parents': parent_directory_parents[0]
            })

            return self.__query_directories_path(driver_service, parent_directory_parents[0], file_path)

        file_path.append({
            'id': parent_directory.get('id'),
            'name': parent_directory.get('name')
        })

        return file_path

    def __get_file_directories_path(self, driver_service, parent_directory_id: str):
        raw_directories_path = self.__query_directories_path(
            driver_service, parent_directory_id, [])
        directories_path = ''
        for directory in raw_directories_path:
            directories_path = f"{directory['name']}/{directories_path}"

        return f"{directories_path}"

    def __reset_tmp_folder(self):
        if os.path.exists('./tmp'):
            shutil.rmtree(r'tmp')
        os.makedirs('./tmp')
