import os
import io
import shutil
from pathlib import Path
from datetime import datetime
from .google_drive_service import GoogleDriveService
from .cache_service import CacheService
from googleapiclient.http import MediaIoBaseDownload
from config.config import CONFIG


class DownloadsService:
    def __init__(self, log_service):
        self.drive = GoogleDriveService().get_drive()
        self.downloaded_files = []
        self.log_service = log_service
        self.cache_service = CacheService(
            CONFIG['Cache']['downloads_cache_file'])
        self.query_conditions = {
            'im_in_owners': "'yambakshi@gmail.com' in owners",
            'visibility': "visibility != 'anyoneCanFind' and visibility != 'anyoneWithLink' and visibility != 'domainCanFind' and visibility != 'domainWithLink' and visibility != 'limited'",
            'not_in_trash': "trashed = false"
        }

    def download_files_by_type(self, config: {}):
        files_counter = 0
        page_token = None

        # Create tmp folder for the downloads
        shutil.rmtree(r'tmp')
        if not os.path.exists('./tmp'):
            os.makedirs('./tmp')

        # Iterate all file pages
        while True:
            response, page_files_counter = self.__download_all_files_in_page(
                config, page_token)
            files_counter += page_files_counter
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        self.log_service.log(f"{files_counter} files downloaded")

    def download_files(self, config: {}, page_size):
        files_query = f"mimeType='{config['drive_file_type']}' and {self.query_conditions['im_in_owners']} and {self.query_conditions['not_in_trash']}"
        response = self.drive.files().list(pageSize=page_size,
                                           q=files_query,
                                           spaces='drive',
                                           fields="*").execute()

        files_counter = self.__process_response(config, response)
        self.log_service.log(f"{files_counter} files downloaded")

    def __download_all_files_in_page(self, config: {}, page_token):
        # files_query = f"mimeType='{config['drive_file_type']}' and (({im_in_owners}) and ({visibility})) and {not_in_trash}"
        files_query = f"mimeType='{config['drive_file_type']}' and {self.query_conditions['im_in_owners']} and {self.query_conditions['not_in_trash']}"

        response = self.drive.files().list(q=files_query,
                                           spaces='drive',
                                           fields="*",
                                           pageToken=page_token).execute()

        page_files_counter = self.__process_response(config, response)
        return response, page_files_counter

    def __process_response(self, config, response):
        files_counter = 0

        for file in response.get('files', []):
            # Get file info
            file_id = file.get('id')
            file_name = file.get('name')
            file_parents = file.get('parents')
            file_path = self.__get_file_path(self.drive, file_parents[0])

            # Create file folders by its path
            Path(f"tmp/{file_path}").mkdir(parents=True, exist_ok=True)

            # Download file by id
            request = self.drive.files().export_media(fileId=file_id,
                                                      mimeType=config['download_as'])
            file_path_and_name = f"{file_path}{file_name}.{config['save_as']}"
            fh = io.FileIO(f"tmp/{file_path_and_name}", 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                download_progress = "Download %d%%" % int(
                    status.progress() * 100)

                self.downloaded_files.append(
                    '/'.join(file_path_and_name.split('/')[1:]))
                self.cache_service.write(
                    '/'.join(file_path_and_name.split('/')[1:]))
                self.log_service.log(
                    f"{file_id} - {download_progress} - {file_path_and_name}")
                files_counter += 1

        return files_counter

    def __query_file_path(self, driver_service, parent_directory_id: str, file_path):
        parent_directory = driver_service.files().get(
            fileId=parent_directory_id, fields='id, name, parents').execute()
        parent_directory_parents = parent_directory.get('parents')
        if parent_directory_parents:
            file_path.append({
                'id': parent_directory.get('id'),
                'name': parent_directory.get('name'),
                'parents': parent_directory_parents[0]
            })

            return self.__query_file_path(driver_service, parent_directory_parents[0], file_path)

        file_path.append({
            'id': parent_directory.get('id'),
            'name': parent_directory.get('name')
        })

        return file_path

    def __get_file_path(self, driver_service, parent_directory_id: str):
        raw_file_path = self.__query_file_path(
            driver_service, parent_directory_id, [])
        file_path = ''
        for directory in raw_file_path:
            file_path = f"{directory['name']}/{file_path}"

        return f"{file_path}"
