import os
import logging
from pathlib import Path
from shutil import copyfile
from services.windows_service import WindowsService
from config.config import CONFIG


class MergeService:
    def __init__(self):
        self.logger = logging.getLogger('backup_system')
        self.windows_service = WindowsService()
        self.files_paths = {'local': [], 'drive': []}

    def compare_spaces(self, space1: str, space2: str, files_paths: {}):
        missing_files_paths = {}
        for file_type, space1_files_paths in files_paths[space1].items():
            missing_files_paths[file_type] = []
            for space2_file_path in files_paths[space2][file_type]:
                space1_extension = CONFIG[space1][file_type]['extension']
                space2_extension = CONFIG[space2][file_type]['extension']
                space2_file_path = space2_file_path.replace(
                    space2_extension, space1_extension)

                if not space2_file_path in space1_files_paths:
                    missing_files_paths[file_type].append(space2_file_path)
                    self.logger.debug(
                        f"'{space2}' file path '{space2_file_path}' could not be found on '{space1}'")

            if len(missing_files_paths[file_type]) == 0:
                self.logger.debug(
                    f"All '{file_type}' files paths from '{space2}' were found on '{space1}'")
            else:
                self.logger.debug(
                    f"{len(missing_files_paths[file_type])} '{file_type}' files paths from '{space2}' were not found on '{space1}'")

        return missing_files_paths

    def merge_downloads_into_local(self, downloads: {}):
        tmp_abs_path = os.path.abspath('tmp')
        for files_paths in downloads.values():
            for file_path in files_paths:
                self.logger.debug(
                    f"Merging downloaded file '{file_path}' into 'local'")
                file_path = file_path.replace('/', '\\')
                downloads_file_path = f"{tmp_abs_path}\\{file_path}"
                local_file_path = f"D:\\Yam Bakshi\\{file_path}"
                if os.path.isfile(local_file_path):
                    self.__replace_file(local_file_path, downloads_file_path)
                else:
                    self.__add_file(local_file_path, downloads_file_path)

    def merge_drive_stream_into_local(self, file_types: []):
        for file_type in file_types:
            self.logger.debug(
                f"Adding all '{file_type}' files from 'drive_stream' to 'local'")

            missing_files_paths = self.compare_spaces(
                'local', 'drive_stream', [file_type])
            for file_path in missing_files_paths:
                file_path = file_path.replace('/', '\\')
                drive_stream_file_path = f"G:\\My Drive\\{file_path}"
                local_file_path = f"D:\\Yam Bakshi\\{file_path}"
                self.__add_file(local_file_path, drive_stream_file_path, True)

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
