import os
import logging
from pathlib import Path
from shutil import copyfile
from services.windows_service import WindowsService
from config.config import CONFIG


class MergeService:
    def __init__(self, cache_service):
        self.logger = logging.getLogger('backup_system')
        self.windows_service = WindowsService()
        self.cache_service = cache_service
        self.files_paths = {'local': [], 'downloads': []}

    def set_files_paths(self, files_paths):
        self.files_paths = files_paths

    def compare_spaces(self, space1: str, space2: str, file_types: []):
        for file_type in file_types:
            missing_files_paths = []
            local_files_paths = self.files_paths[space1][file_type]
            for space2_file_path in self.files_paths[space2][file_type]:
                if not space2_file_path in local_files_paths:
                    missing_files_paths.append(space2_file_path)
                    self.logger.debug(
                        f"'{space2}' file path '{space2_file_path}' could not be found on '{space1}'")

            if len(missing_files_paths) == 0:
                self.logger.debug(
                    f"All '{file_type}' files paths from '{space2}' were found on '{space1}'")
            else:
                self.logger.debug(
                    f"{len(missing_files_paths)} '{file_type}' files paths from '{space2}' were not found on '{space1}'")

            return missing_files_paths

    def merge_downloads_into_local(self, file_types: []):
        tmp_directory_path = os.path.abspath('tmp')
        for file_type in file_types:
            self.logger.debug(
                f"Merging all downloaded '{file_type}' files into 'local'")
            for file_path in self.files_paths['downloads'][file_type]:
                file_path = file_path.replace('/', '\\')
                downloads_file_path = f"{tmp_directory_path}\\My Drive\\{file_path}"
                local_file_path = f"D:\\Yam Bakshi\\{file_path}"
                if os.path.isfile(local_file_path):
                    self.__replace_file(local_file_path, downloads_file_path)
                else:
                    self.__add_file(local_file_path, downloads_file_path)

    def add_missing_drive_stream_files_to_local(self, file_types: []):
        for file_type in file_types:
            self.logger.debug(
                f"Adding all '{file_type}' files from 'Google Drive Stream' to 'local'")

            missing_files_paths = self.compare_spaces(
                'local', 'drive_stream', [file_type])
            for file_path in missing_files_paths:
                file_path = file_path.replace('/', '\\')
                drive_stream_file_path = f"G:\\My Drive\\{file_path}"
                local_file_path = f"D:\\Yam Bakshi\\{file_path}"
                self.__add_file(local_file_path, drive_stream_file_path, True)
                self.cache_service.update([
                    {
                        'cache_file': CONFIG['local'][file_type]['cache_file'],
                        'remove_lines': [],
                        'add_lines': [file_path]
                    }
                ])

    def __replace_file(self, old_file_path: str, new_file_path: str):
        self.logger.debug(
            f"Replacing '{old_file_path}' with '{new_file_path}'")
        self.windows_service.move_to_recycle_bin(old_file_path)
        os.rename(new_file_path, old_file_path)

    def __add_file(self, old_file_path: str, new_file_path: str, copy_new_file: bool = False):
        old_file_path_parent = '\\'.join(old_file_path.split('\\')[:-1])
        self.logger.debug(
            f"Adding file '{new_file_path}' to '{old_file_path_parent}'")
        Path(old_file_path_parent).mkdir(parents=True, exist_ok=True)
        if copy_new_file:
            copyfile(new_file_path, old_file_path)
        else:
            os.rename(new_file_path, old_file_path)
