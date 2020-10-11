import os
import logging
from pathlib import Path
from services.logger_service import init_logger
from services.cache_service import CacheService
from services.downloads_service import DownloadsService
from services.files_service import FilesService
from services.windows_service import WindowsService
from config.config import CONFIG


class BackupSystem:
    def __init__(self):
        self.logger = init_logger()
        self.cache_service = CacheService()
        self.downloads_service = DownloadsService(self.cache_service)
        self.files_service = FilesService(self.cache_service)
        self.windows_service = WindowsService()

    def update_local_files(self):
        try:
            # Filter Microsoft Excel files on local machine
            local_microsoft_excel_files = self.files_service.get_files_by_types(
                CONFIG['local']['Microsoft Word'])

            # Filter Google Sheet files on Google Drive Stream folder
            drive_stream_google_sheet_files = self.files_service.get_files_by_types(
                CONFIG['local']['Google Doc'])

            # Download all Google Sheet documents from Google Drive
            drive_google_sheet_files = self.downloads_service.download_all_files_by_type(
                CONFIG['drive']['Google Doc'])

            # self.__replace_local_files_with_drive_files(
            #     drive_google_sheet_files)
        except Exception as err:
            self.logger.error(err)

    def __replace_local_files_with_drive_files(self, downloaded_drive_files):
        tmp_directory_path = os.path.abspath('tmp')

        for drive_file in downloaded_drive_files:
            drive_file_backslash = drive_file.replace('/', '\\')
            tmp_file_path = f"{tmp_directory_path}\\My Drive\\{drive_file_backslash}"
            if not os.path.isfile(tmp_file_path):
                self.logger.error(
                    f"Failed to find tmp file: '{tmp_file_path}'")
                continue

            local_file_to_replace = f"D:\\Yam Bakshi\\{drive_file_backslash}"
            if os.path.isfile(local_file_to_replace):
                self.__replace_local_file(local_file_to_replace, tmp_file_path)
            else:
                self.__add_new_drive_file(local_file_to_replace, tmp_file_path)

    def __replace_local_file(self, local_file_to_replace, drive_file):
        self.logger.debug(
            f"Moving old file '{local_file_to_replace}' to 'Recycle Bin'")
        self.windows_service.move_to_recycle_bin(local_file_to_replace)

        local_file_to_replace_parent = '\\'.join(
            local_file_to_replace.split('\\')[:-1])
        self.logger.debug(
            f"Moving new file '{drive_file}' into '{local_file_to_replace_parent}'")
        os.rename(drive_file, local_file_to_replace)

    def __add_new_drive_file(self, missing_local_file, drive_file):
        missing_local_file_parent = '\\'.join(
            missing_local_file.split('\\')[-1])
        self.logger.debug(
            f"Creating new local destination path: '{missing_local_file_parent}'")
        Path(missing_local_file_parent).mkdir(parents=True, exist_ok=True)

        self.logger.debug(
            f"Moving new file '{drive_file}' to '{missing_local_file_parent}'")
        os.rename(drive_file, missing_local_file)
