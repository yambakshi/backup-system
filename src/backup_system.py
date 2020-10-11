import os
import logging
from pathlib import Path
from services.logger_service import init_logger
from services.cache_service import CacheService
from services.downloads_service import DownloadsService
from services.files_service import FilesService
from services.windows_service import WindowsService


class BackupSystem:
    def __init__(self):
        self.logger = init_logger()
        self.cache_service = CacheService()
        self.downloads_service = DownloadsService(self.cache_service)
        self.files_service = FilesService(self.cache_service)
        self.windows_service = WindowsService()

    def update_local_machine(self):
        try:
            files = {
                'local': {
                    'Microsoft Word': [],
                    'Microsoft Excel': [],
                    'PDF': []
                },
                'drive_stream': {
                    'Google Doc': [],
                    'Google Sheet': [],
                    'PDF': []
                },
                'downloads': {
                    'Microsoft Word': [],
                    'Microsoft Excel': [],
                    'PDF': []
                }
            }

            # Get local machine file paths
            files['local']['Microsoft Word'] = self.files_service.get_files(
                'local', 'Microsoft Word')
            files['local']['Microsoft Excel'] = self.files_service.get_files(
                'local', 'Microsoft Excel')
            files['local']['PDF'] = self.files_service.get_files(
                'local', 'PDF')

            # Get Google Drive Stream files paths
            files['drive_stream']['Google Doc'] = self.files_service.get_files(
                'drive_stream', 'Google Doc')
            files['drive_stream']['Google Sheet'] = self.files_service.get_files(
                'drive_stream', 'Google Sheet')
            files['drive_stream']['PDF'] = self.files_service.get_files(
                'drive_stream', 'PDF')

            # Download Google Drive files
            files['downloads']['Google Doc'] = self.downloads_service.download_all_files(
                'Google Doc')
            files['downloads']['Google Sheet'] = self.downloads_service.download_all_files(
                'Google Sheet')
            files['downloads']['PDF'] = self.downloads_service.download_all_files(
                'PDF')

            # Check downloaded files
            self.__check_downloaded_files_paths(
                files['downloads']['Google Doc'], files['local']['Microsoft Word'])
            self.__check_downloaded_files_paths(
                files['downloads']['Google Sheet'], files['local']['Microsoft Excel'])
            self.__check_downloaded_files_paths(
                files['downloads']['PDF'], files['local']['PDF'])

            # Update local machine
            self.__update_local_machine(files['downloads']['Google Doc'])
            self.__update_local_machine(files['downloads']['Google Sheet'])
            self.__update_local_machine(files['downloads']['PDF'])

            # Delete tmp folder
            self.downloads_service.delete_tmp_folder()
        except Exception as err:
            self.logger.error(err)

    def __check_downloaded_files_paths(self, downloaded_files, local_files):
        missing_paths_counter = 0
        for downloaded_file in downloaded_files:
            if not downloaded_file in local_files:
                missing_paths_counter += 1
                self.logger.debug(
                    f"Downloaded file path '{downloaded_file}' could not be found on local machine")

        if missing_paths_counter == 0:
            self.logger.debug(
                'All downloaded files paths were found on local machine')
        else:
            self.logger.debug(
                f"{missing_paths_counter} downloaded files paths were not found on local machine")

    def __update_local_machine(self, downloaded_files):
        tmp_directory_path = os.path.abspath('tmp')
        for downloaded_file in downloaded_files:
            downloaded_file_backslash = downloaded_file.replace('/', '\\')
            tmp_file_path = f"{tmp_directory_path}\\My Drive\\{downloaded_file_backslash}"
            if not os.path.isfile(tmp_file_path):
                self.logger.error(
                    f"Failed to find tmp file: '{tmp_file_path}'")
                continue

            local_file_path = f"D:\\Yam Bakshi\\{downloaded_file_backslash}"
            if os.path.isfile(local_file_path):
                self.__replace_local_file(local_file_path, tmp_file_path)
            else:
                self.__add_new_file(local_file_path, tmp_file_path)

    def __replace_local_file(self, dst_local_file, downloaded_file):
        self.logger.debug(
            f"Moving old file '{dst_local_file}' to 'Recycle Bin'")
        self.windows_service.move_to_recycle_bin(dst_local_file)

        dst_local_file_parent = '\\'.join(dst_local_file.split('\\')[:-1])
        self.logger.debug(
            f"Moving new file '{downloaded_file}' into '{dst_local_file_parent}'")
        os.rename(downloaded_file, dst_local_file)

    def __add_new_file(self, dst_local_file, downloaded_file):
        dst_local_file_parent = '\\'.join(
            dst_local_file.split('\\')[:-1])
        self.logger.debug(
            f"Creating new local destination path: '{dst_local_file_parent}'")
        Path(dst_local_file_parent).mkdir(parents=True, exist_ok=True)

        self.logger.debug(
            f"Moving new file '{downloaded_file}' to '{dst_local_file_parent}'")
        os.rename(downloaded_file, dst_local_file)
