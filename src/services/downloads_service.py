import io
from pathlib import Path
from datetime import datetime
from .google_drive_service import GoogleDriveService
from googleapiclient.http import MediaIoBaseDownload


class DownloadsService:
    def __init__(self):
        self.drive = GoogleDriveService().get_drive()


    def query_file_path(self, driver_service, parent_directory_id: str, file_path):
        parent_directory = driver_service.files().get(
            fileId=parent_directory_id, fields='id, name, parents').execute()
        parent_directory_parents = parent_directory.get('parents')
        if parent_directory_parents:
            file_path.append({
                'id': parent_directory.get('id'),
                'name': parent_directory.get('name'),
                'parents': parent_directory_parents[0]
            })

            return self.query_file_path(driver_service, parent_directory_parents[0], file_path)

        file_path.append({
            'id': parent_directory.get('id'),
            'name': parent_directory.get('name')
        })

        return file_path


    def get_file_path(self, driver_service, parent_directory_id: str):
        raw_file_path = self.query_file_path(
            driver_service, parent_directory_id, [])
        file_path = ''
        for directory in raw_file_path:
            file_path = f"{directory['name']}/{file_path}"

        return f"{file_path}"


    def download_all_files_in_page(self, config: {}, page_token):
        im_in_owners = "'yambakshi@gmail.com' in owners"
        # visibility = "visibility != 'anyoneCanFind' and visibility != 'anyoneWithLink' and visibility != 'domainCanFind' and visibility != 'domainWithLink' and visibility != 'limited'"
        not_in_trash = "trashed = false"
        # files_query = f"mimeType='{config['drive_file_type']}' and (({im_in_owners}) and ({visibility})) and {not_in_trash}"
        files_query = f"mimeType='{config['drive_file_type']}' and {im_in_owners} and {not_in_trash}"

        response = self.drive.files().list(q=files_query,
                                           spaces='drive',
                                           fields="*",
                                           pageToken=page_token).execute()

        page_files_counter = self.process_response(config, response)
        return response, page_files_counter


    def download_files(self, config: {}, page_size):
        im_in_owners = "'yambakshi@gmail.com' in owners"
        not_in_trash = "trashed = false"
        current_date = datetime.today().strftime('%Y-%m-%d')

        # Clear log file
        config['log_file'] = f"logs/download/{current_date} - {config['log_file']}"
        open(config['log_file'], 'w').close()

        response = self.drive.files().list(pageSize=page_size,
                                              q=f"mimeType='{config['drive_file_type']}' and {im_in_owners} and {not_in_trash}",
                                              spaces='drive',
                                              fields="*").execute()

        files_counter = self.process_response(config, response)
        with io.open(config['log_file'], "a", encoding="utf-8") as f:
            f.write(f"{files_counter} files downloaded")

        print(f"{files_counter} files downloaded")


    def process_response(self, config, response):
        files_counter = 0

        for file in response.get('files', []):
            # Get file info
            file_id = file.get('id')
            file_name = file.get('name')
            file_parents = file.get('parents')

            # Print and log status
            print('Found file: %s (%s)' % (file_name, file_id))
            file_path = self.get_file_path(self.drive, file_parents[0])
            with io.open(config['log_file'], "a", encoding="utf-8") as f:
                f.write(file_id)

            # Create file folders by its path
            Path(f"tmp/{file_path}").mkdir(parents=True, exist_ok=True)

            # Download file by id
            request = self.drive.files().export_media(fileId=file_id,
                                                         mimeType=config['download_as'])
            fh = io.FileIO(
                f"tmp/{file_path}{file_name}.{config['save_as']}", 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                download_progress = "Download %d%%" % int(
                    status.progress() * 100)

                # Print and log status
                print(download_progress)
                with io.open(config['log_file'], "a", encoding="utf-8") as f:
                    f.write(f" - {download_progress} - {file_path}{file_name}.{config['save_as']}\n")

                files_counter += 1

        return files_counter


    def download_files_by_type(self, config: {}):
        files_counter = 0
        current_date = datetime.today().strftime('%Y-%m-%d')

        # Clear log file
        config['log_file'] = f"logs/download/{current_date} - {config['log_file']}"
        open(config['log_file'], 'w').close()

        page_token = None

        # Iterate all file pages
        while True:
            response, page_files_counter = self.download_all_files_in_page(
                config, page_token)
            files_counter += page_files_counter
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        with io.open(config['log_file'], "a", encoding="utf-8") as f:
            f.write(f"{files_counter} files downloaded")

        print(f"{files_counter} files downloaded")
