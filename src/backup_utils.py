from services.log_service import LogService
from services.downloads_service import DownloadsService
from services.filter_service import FilterService
from config.config import CONFIG


class BackupUtils:
    def __init__(self):
        self.log_service = LogService()
        self.downloads_service = DownloadsService(self.log_service)
        self.filter_service = FilterService(self.log_service)

    def update_local_files(self):
        # Filter Microsoft Excel files in local machine
        filtered_local_microsoft_excel_files = self.filter_service.filter_files_by_types(
            CONFIG['Microsoft Excel']['filter'], True, [r'D:/Yam Bakshi/Careers/Hi-Tech/Portfolio/Python/Backup Utils/tmp'])

        # Filter Google Sheet files in Google Drive Stream folder
        filtered_drive_stream_google_sheet_files = self.filter_service.filter_files_by_types(
            CONFIG['Google Sheets']['filter'], True, [])

        # Download all Google Sheet documents from Google Drive
        downloaded_drive_google_sheet_files = self.downloads_service.download_files_by_type(
            CONFIG['Google Sheets']['download'], True)

        # Download 3 Google Sheet documents from Google Drive
        # downloads_service.download_files(CONFIG['Google Sheets']['download'], False, 3)

        self.check_missing_files(
            downloaded_drive_google_sheet_files, filtered_drive_stream_google_sheet_files)

    def check_missing_files(self, downloaded_files, local_files):
        missing_files_counter = 0
        for file_path in downloaded_files:
            if not file_path in local_files:
                missing_files_counter += 1
                missing_file_message = f"Downloaded file is missing from local machine: {file_path}"
                self.log_service.log(missing_file_message)

        if missing_files_counter == 0:
            self.log_service.log(
                'All downloaded files paths are found in local machine')
        else:
            self.log_service.log(
                f"{missing_files_counter} downloaded files are missing in local machine")
