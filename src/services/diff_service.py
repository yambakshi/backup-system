import os
import logging
from pathlib import Path
from shutil import copyfile
from services.windows_service import WindowsService
from config.config import CONFIG


class DiffService:
    def __init__(self, snapshot_service):
        self.logger = logging.getLogger('backup_system')
        self.windows_service = WindowsService()
        self.snapshot_service = snapshot_service

    def get_diff(self, files_paths):
        self.logger.debug("Comparing 'drive' and 'local'")
        diff = {
            'new': {},
            'modified': {},
            'removed': {}
        }

        for file_type, files in files_paths['drive'].items():
            # Get a list of 'drive_stream' files paths
            drive_stream = list(files_paths['drive_stream'][file_type].keys())

            cache_contents = self.snapshot_service.read(
                CONFIG['drive'][file_type]['cache_file'])
            cache_files = [cache_file.split(
                '|')[0] for cache_file in cache_contents.split('\n')[:-1]]

            for file_path, file_data in files.items():
                # Only files found in 'drive_stream' are counted as diffs
                if file_path not in drive_stream:
                    continue

                drive_extension = CONFIG['drive'][file_type]['extension']
                local_extension = CONFIG['local'][file_type]['extension']
                local_file_path = file_path.replace(
                    drive_extension, local_extension)

                if local_file_path not in files_paths['local'][file_type]:
                    if file_type not in diff['new']:
                        diff['new'][file_type] = {}
                    diff['new'][file_type][file_path] = file_data
                    self.logger.debug(
                        f"New file '{file_path}' on 'drive'")
                    continue

                if file_data['last_modified'] > files_paths['local'][file_type][local_file_path]['last_modified']:
                    if file_type not in diff['modified']:
                        diff['modified'][file_type] = {}
                    diff['modified'][file_type][file_path] = file_data
                    self.logger.debug(
                        f"Modified file '{file_path}' on 'drive'")
                    continue

                if file_path not in cache_files:
                    if file_type not in diff['remove']:
                        diff['remove'][file_type] = {}
                    diff['remove'][file_type][file_path] = file_data
                    self.logger.debug(
                        f"Removed file '{file_path}' on 'drive'")

        self.logger.debug(
            f"Diff is: {len(diff['new'])} new files, {len(diff['modified'])} modified files, {len(diff['removed'])} removed files")
        return diff

    def merge_downloads(self, downloads):
        self.logger.debug("Merging changes into 'local'")
        tmp_abs_path = os.path.abspath('tmp')
        for diff_type in downloads.keys():
            for file_type, files_paths in downloads[diff_type].items():
                for file_path, file_data in files_paths.items():
                    self.logger.debug(
                        f"Merging file '{file_path}' into 'local'")

                    copy_file = False
                    file_path = file_path.replace('/', '\\')
                    if file_type == 'google_type':
                        downloads_file_path = f"{tmp_abs_path}\\{file_path}"
                    else:
                        downloads_file_path = f"G:\\My Drive\\{file_path}"
                        copy_file = True

                    local_file_path = f"D:\\Yam Bakshi\\{file_path}"
                    if diff_type == 'modified':
                        self.__replace_file(
                            local_file_path, downloads_file_path, copy_file)
                    else:
                        self.__add_file(local_file_path,
                                        downloads_file_path, copy_file)

                    os.utime(local_file_path,
                             (file_data['last_modified'], file_data['last_modified']))

    def __replace_file(self, old_file_path: str, new_file_path: str, copy_new_file: bool):
        self.logger.debug(
            f"Replacing '{old_file_path}' with '{new_file_path}'")
        self.windows_service.move_to_recycle_bin(old_file_path)
        if copy_new_file:
            copyfile(new_file_path, old_file_path)
        else:
            os.rename(new_file_path, old_file_path)

    def __add_file(self, old_file_path: str, new_file_path: str, copy_new_file: bool):
        old_file_path_parent = '\\'.join(old_file_path.split('\\')[:-1])
        self.logger.debug(
            f"Adding file '{new_file_path}' to '{old_file_path_parent}'")
        Path(old_file_path_parent).mkdir(parents=True, exist_ok=True)
        if copy_new_file:
            copyfile(new_file_path, old_file_path)
        else:
            os.rename(new_file_path, old_file_path)
