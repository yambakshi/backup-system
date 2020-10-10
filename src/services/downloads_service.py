import os
import io
import shutil
import logging
from .google_drive_service import GoogleDriveService
from pathlib import Path
from googleapiclient.http import MediaIoBaseDownload


class DownloadsService:
    def __init__(self, cache_service):
        self.cache_service = cache_service
        self.drive = GoogleDriveService().get_drive()
        self.query_conditions = {
            'im_in_owners': "'yambakshi@gmail.com' in owners",
            'visibility': "visibility != 'anyoneCanFind' and visibility != 'anyoneWithLink' and visibility != 'domainCanFind' and visibility != 'domainWithLink' and visibility != 'limited'",
            'not_in_trash': "trashed = false"
        }

    def download_files_by_type(self, config: {}, use_cache: bool):
        logging.debug(
            f"Downloading '{config['drive_file_type']}' files from 'Google Drive'")

        if use_cache:
            downloaded_files = self.__load_cache(config)
            logging.debug(
                f"{len(downloaded_files)} '{config['drive_file_type']}' files loaded from 'cache/{config['cache_file']}'")
        else:
            downloaded_files = self.__download_all_files(config)
            logging.debug(
                f"{len(downloaded_files)} '{config['drive_file_type']}' files downloaded from 'Google Drive'")

        return downloaded_files

    def download_files(self, config: {}, use_cache: bool, page_size: int):
        # Create tmp folder for the downloads
        self.__reset_tmp_folder()

        files_query = f"mimeType='{config['drive_file_type']}' and {self.query_conditions['im_in_owners']} and {self.query_conditions['not_in_trash']}"
        response = self.drive.files().list(pageSize=page_size,
                                           q=files_query,
                                           spaces='drive',
                                           fields="*").execute()

        downloaded_files = self.__process_response(config, response)
        logging.debug(f"{len(downloaded_files)} files downloaded")
        return downloaded_files

    def __download_all_files(self, config):
        downloaded_files = []
        page_token = None

        # Create tmp folder for the downloads
        self.__reset_tmp_folder()

        # Iterate all file pages
        while True:
            files_query = f"mimeType='{config['drive_file_type']}' and {self.query_conditions['im_in_owners']} and {self.query_conditions['not_in_trash']}"
            response = self.drive.files().list(q=files_query,
                                               spaces='drive',
                                               fields="*",
                                               pageToken=page_token).execute()

            downloaded_files += self.__process_response(config, response)
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        return downloaded_files

    def __process_response(self, config, response):
        downloaded_files = []
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

                downloaded_files.append(
                    '/'.join(file_path_and_name.split('/')[1:]))
                self.cache_service.write(config['cache_file'],
                                         '/'.join(file_path_and_name.split('/')[1:]))
                logging.debug(
                    f"{file_id} - {download_progress} - {file_path_and_name}")

        return downloaded_files

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

    def __load_cache(self, config):
        cache = self.cache_service.read(config['cache_file'])
        return cache.split('\n')[:-1]

    def __reset_tmp_folder(self):
        shutil.rmtree(r'tmp')
        if not os.path.exists('./tmp'):
            os.makedirs('./tmp')
