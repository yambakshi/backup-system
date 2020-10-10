import os
import logging
import sys
from services.cache_service import CacheService
from services.downloads_service import DownloadsService
from services.filter_service import FilterService
from services.windows_service import WindowsService
from config.config import CONFIG
from pathlib import Path


class BackupUtils:
    def __init__(self):
        self.init_logging()
        self.cache_service = CacheService()
        self.downloads_service = DownloadsService(self.cache_service)
        self.filter_service = FilterService(self.cache_service)
        self.windows_service = WindowsService()

    def init_logging(self):
        if not os.path.exists('./logs'):
            Path(r'logs').mkdir(parents=True, exist_ok=True)

        logging.basicConfig(filename='logs/backup_system.log',
                            format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    def update_local_files(self):
        try:
            # Filter Microsoft Excel files in local machine
            local_microsoft_excel_files = self.filter_service.get_files_by_types(
                CONFIG['Microsoft Excel']['filter'], True, [r'D:/Yam Bakshi/Careers/Hi-Tech/Portfolio/Python/Backup Utils/tmp'])

            # Filter Google Sheet files in Google Drive Stream folder
            drive_stream_google_sheet_files = self.filter_service.get_files_by_types(
                CONFIG['Google Sheets']['filter'], True, [])

            # Download all Google Sheet documents from Google Drive
            drive_google_sheet_files = self.downloads_service.download_files_by_type(
                CONFIG['Google Sheets']['download'], True)

            # Get a list of files found in Google Drive but missing from local machine
            missing_files = self.__get_missing_files(
                local_microsoft_excel_files, drive_google_sheet_files)

            for missing_file in missing_files:
                parent_folder = '/'.join(missing_file.split('/')[:-1])
                local_path_to_folder = f"D:/Yam Bakshi/{parent_folder}"
                if not os.path.isdir(local_path_to_folder):
                    Path(parent_folder).mkdir(parents=True, exist_ok=True)
        except Exception as err:
            logging.error(err)

    def __get_missing_files(self, local_files, downloaded_files):
        missing_files = []
        for file_path in downloaded_files:
            if not file_path in local_files:
                missing_files.append(file_path)
                logging.debug(
                    f"Downloaded file is missing from local machine: '{file_path}'")

        if len(missing_files) == 0:
            logging.debug(
                'All downloaded files paths are found in local machine')
        else:
            logging.debug(
                f"{len(missing_files)} downloaded files are missing in local machine")

        return missing_files
