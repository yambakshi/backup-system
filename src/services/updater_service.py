import os
import logging
from pathlib import Path
from services.windows_service import WindowsService


class UpdaterService:
    def __init__(self, files_paths: {}):
        self.logger = logging.getLogger('backup_system')
        self.windows_service = WindowsService()
        self.files_paths = files_paths

    def check_downloaded_files_paths(self, downloads_file_type: str, local_file_type: str):
        missing_paths_counter = 0
        local_files = self.files_paths['local'][local_file_type]
        for downloaded_file in self.files_paths['downloads'][downloads_file_type]:
            if not downloaded_file in local_files:
                missing_paths_counter += 1
                self.logger.debug(
                    f"Downloaded file path '{downloaded_file}' could not be found on local machine")

        if missing_paths_counter == 0:
            self.logger.debug(
                f"All downloaded '{local_file_type}' files paths were found on local machine")
        else:
            self.logger.debug(
                f"{missing_paths_counter} downloaded '{local_file_type}' files paths were not found on local machine")

    def update_local_machine(self, downloads_files_types: []):
        tmp_directory_path = os.path.abspath('tmp')

        for downloads_files_type in downloads_files_types:
            for downloaded_file in self.files_paths['downloads'][downloads_files_type]:
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

    def __replace_local_file(self, dst_local_file: str, downloaded_file: str):
        self.logger.debug(
            f"Moving old file '{dst_local_file}' to 'Recycle Bin'")
        self.windows_service.move_to_recycle_bin(dst_local_file)

        dst_local_file_parent = '\\'.join(dst_local_file.split('\\')[:-1])
        self.logger.debug(
            f"Moving new file '{downloaded_file}' into '{dst_local_file_parent}'")
        os.rename(downloaded_file, dst_local_file)

    def __add_new_file(self, dst_local_file: str, downloaded_file: str):
        dst_local_file_parent = '\\'.join(
            dst_local_file.split('\\')[:-1])
        self.logger.debug(
            f"Creating new local destination path: '{dst_local_file_parent}'")
        Path(dst_local_file_parent).mkdir(parents=True, exist_ok=True)

        self.logger.debug(
            f"Moving new file '{downloaded_file}' to '{dst_local_file_parent}'")
        os.rename(downloaded_file, dst_local_file)
