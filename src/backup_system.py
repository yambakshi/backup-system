import os
import logging
import sys
from services.cache_service import CacheService
from services.downloads_service import DownloadsService
from services.files_service import FilesService
from services.windows_service import WindowsService
from config.config import CONFIG
from pathlib import Path


class BackupSystem:
    def __init__(self):
        self.logger = self.init_logger()
        self.cache_service = CacheService()
        self.downloads_service = DownloadsService(self.cache_service)
        self.files_service = FilesService(self.cache_service)
        self.windows_service = WindowsService()

    def init_logger(self):
        if not os.path.exists('./logs'):
            Path(r'logs').mkdir(parents=True, exist_ok=True)

        # Set the root logger to minimum log level of ERROR
        # This way only log messages from severities ERROR and CRITICAL from imported modules will be logged
        logging.basicConfig(filename='logs/backup_system.log',
                            format='%(asctime)s %(levelname)s %(message)s',
                            level=logging.ERROR)

        # Init the backup_system logger
        logger = logging.getLogger('backup_system')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.StreamHandler(sys.stdout))
        return logger

    def update_local_files(self):
        try:
            # Filter Microsoft Excel files on local machine
            local_microsoft_excel_files = self.files_service.get_files_by_types(
                CONFIG['local']['Microsoft Excel'])

            # Filter Google Sheet files on Google Drive Stream folder
            drive_stream_google_sheet_files = self.files_service.get_files_by_types(
                CONFIG['local']['Google Sheet'])

            # Download all Google Sheet documents from Google Drive
            drive_google_sheet_files = self.downloads_service.download_all_files_by_type(
                CONFIG['drive']['Google Sheet'])

            # Get a list of files found on Google Drive but missing from local machine
            missing_files = self.__get_missing_files(
                local_microsoft_excel_files, drive_google_sheet_files)

            # for missing_file in missing_files:
            #     parent_folder = '/'.join(missing_file.split('/')[:-1])
            #     local_path_to_folder = f"D:/Yam Bakshi/{parent_folder}"
            #     if not os.path.isdir(local_path_to_folder):
            #         Path(parent_folder).mkdir(parents=True, exist_ok=True)
        except Exception as err:
            self.logger.error(err)

    def __get_missing_files(self, local_files, downloaded_files):
        missing_files = []
        for file_path in downloaded_files:
            if not file_path in local_files:
                missing_files.append(file_path)
                self.logger.debug(
                    f"Downloaded file is missing from local machine: '{file_path}'")

        if len(missing_files) == 0:
            self.logger.debug(
                'All downloaded files paths are found on local machine')
        else:
            self.logger.debug(
                f"{len(missing_files)} downloaded files are missing from local machine")

        return missing_files
