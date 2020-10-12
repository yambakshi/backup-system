import os
import logging
from pathlib import Path
from services.windows_service import WindowsService
from config.config import CONFIG


class MergeService:
    def __init__(self):
        self.logger = logging.getLogger('backup_system')
        self.windows_service = WindowsService()
        self.files_paths = {'local': [], 'downloads': []}

    def set_files_paths(self, files_paths):
        self.files_paths = files_paths

    def compare_local_and_downloads(self, file_type: str):
        missing_paths_counter = 0
        local_files_paths = self.files_paths['local'][file_type]
        for downloads_file_path in self.files_paths['downloads'][file_type]:
            if not downloads_file_path in local_files_paths:
                missing_paths_counter += 1
                self.logger.debug(
                    f"Downloaded file path '{downloads_file_path}' could not be found on local machine")

        if missing_paths_counter == 0:
            self.logger.debug(
                f"All downloaded '{file_type}' files paths were found on local machine")
        else:
            self.logger.debug(
                f"{missing_paths_counter} downloaded '{file_type}' files paths were not found on local machine")

    def merge_downloads_into_local(self, files_types: []):
        tmp_directory_path = os.path.abspath('tmp')

        for files_type in files_types:
            for file_path in self.files_paths['downloads'][files_type]:
                file_path = file_path.replace('/', '\\')
                tmp_file_path = f"{tmp_directory_path}\\My Drive\\{file_path}"
                if not os.path.isfile(tmp_file_path):
                    self.logger.error(
                        f"Failed to find tmp file: '{tmp_file_path}'")
                    continue

                local_file_path = f"D:\\Yam Bakshi\\{file_path}"
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
