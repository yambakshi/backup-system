import os
import logging
from pathlib import Path
from services.windows_service import WindowsService


class MergeService:
    def __init__(self, files_paths: {}):
        self.logger = logging.getLogger('backup_system')
        self.windows_service = WindowsService()
        self.files_paths = files_paths

    def compare_local_and_downloads(self, local_file_type: str, downloads_file_type: str):
        missing_paths_counter = 0
        local_files_paths = self.files_paths['local'][local_file_type]
        for downloads_file_path in self.files_paths['downloads'][downloads_file_type]:
            if not downloads_file_path in local_files_paths:
                missing_paths_counter += 1
                self.logger.debug(
                    f"Downloaded file path '{downloads_file_path}' could not be found on local machine")

        if missing_paths_counter == 0:
            self.logger.debug(
                f"All downloaded '{local_file_type}' files paths were found on local machine")
        else:
            self.logger.debug(
                f"{missing_paths_counter} downloaded '{local_file_type}' files paths were not found on local machine")

    def merge_downloads_into_local(self, downloads_files_types: []):
        tmp_directory_path = os.path.abspath('tmp')

        for downloads_files_type in downloads_files_types:
            for downloads_file_path in self.files_paths['downloads'][downloads_files_type]:
                downloads_file_path = downloads_file_path.replace('/', '\\')
                tmp_file_path = f"{tmp_directory_path}\\My Drive\\{downloads_file_path}"
                if not os.path.isfile(tmp_file_path):
                    self.logger.error(
                        f"Failed to find tmp file: '{tmp_file_path}'")
                    continue

                local_file_path = f"D:\\Yam Bakshi\\{downloads_file_path}"
                if os.path.isfile(local_file_path):
                    self.__replace_local_file(tmp_file_path, local_file_path)
                else:
                    self.__add_new_file(tmp_file_path, local_file_path)

    def __replace_local_file(self, downloads_file_path: str, local_file_path: str):
        self.logger.debug(
            f"Replacing '{local_file_path}' with '{downloads_file_path}'")
        self.windows_service.move_to_recycle_bin(local_file_path)
        os.rename(downloads_file_path, local_file_path)

    def __add_new_file(self, downloads_file_path: str, local_file: str):
        local_file_parent = '\\'.join(local_file.split('\\')[:-1])
        self.logger.debug(
            f"Moving new file '{downloads_file_path}' to '{local_file_parent}'")
        Path(local_file_parent).mkdir(parents=True, exist_ok=True)
        os.rename(downloads_file_path, local_file)
