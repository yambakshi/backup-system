import os
import logging
from pathlib import Path
from shutil import copyfile
from services.windows_service import WindowsService
from config.config import CONFIG


GOOGLE_FILE_TYPES = [
    'Google Doc',
    'Google Sheet'
]


class DiffService:
    def __init__(self, snapshot_service):
        self.logger = logging.getLogger('backup_system')
        self.windows_service = WindowsService()
        self.snapshot_service = snapshot_service

    def get_diff(self, files_paths):
        self.logger.debug("Comparing 'drive' and 'local'")
        diff = {
            'new': [],
            'modified': [],
            'removed': []
        }

        for file_type, files in files_paths['drive'].items():
            # Get a list of 'drive_stream' files paths
            drive_stream = list(files_paths['drive_stream'][file_type].keys())

            snapshot_contents = self.snapshot_service.read(
                CONFIG['drive'][file_type]['snapshot_file'])
            snapshot_files_paths = [snapshot_file.split(
                '|')[0] for snapshot_file in snapshot_contents.split('\n')[:-1]]

            for file_path, file_data in files.items():
                # Only files found in 'drive_stream' are counted as diffs
                if file_path not in drive_stream:
                    continue

                drive_extension = CONFIG['drive'][file_type]['extension']
                local_extension = CONFIG['local'][file_type]['extension']
                local_file_path = file_path.replace(
                    drive_extension, local_extension)

                if local_file_path not in files_paths['local'][file_type]:
                    diff['new'].append({
                        'type': file_type,
                        'path': file_path,
                        'is_google_type': file_type in GOOGLE_FILE_TYPES,
                        **file_data
                    })
                    self.logger.debug(
                        f"New file '{file_path}' on 'drive'")
                    continue

                if file_data['last_modified'] > files_paths['local'][file_type][local_file_path]['last_modified']:
                    diff['modified'].append({
                        'type': file_type,
                        'path': file_path,
                        'is_google_type': file_type in GOOGLE_FILE_TYPES,
                        **file_data
                    })
                    self.logger.debug(
                        f"Modified file '{file_path}' on 'drive'")
                    continue

                if file_path not in snapshot_files_paths:
                    diff['removed'].append({
                        'type': file_type,
                        'path': file_path,
                        'is_google_type': file_type in GOOGLE_FILE_TYPES,
                        **file_data
                    })
                    self.logger.debug(
                        f"Removed file '{file_path}' on 'drive'")

        self.logger.debug(
            f"Diff is: {len(diff['new'])} new files, {len(diff['modified'])} modified files, {len(diff['removed'])} removed files")
        return diff

    def merge_changes(self, diff):
        self.logger.debug("Merging changes into 'local'")
        tmp_abs_path = os.path.abspath('tmp')
        for diff_type, file_data in diff.items():
            file_path = file_data['path'].replace('/', '\\')
            if file_data['is_google_type']:
                downloads_file_path = f"{tmp_abs_path}\\{file_path}"
            else:
                downloads_file_path = f"G:\\My Drive\\{file_path}"

            local_file_path = f"D:\\Yam Bakshi\\{file_path}"
            if diff_type == 'removed':
                self.__remove_file(local_file_path)
                continue

            if diff_type == 'modified':
                self.__replace_file(
                    local_file_path, downloads_file_path, file_data['is_google_type'])
                continue

            if diff_type == 'new':
                self.__add_file(local_file_path,
                                downloads_file_path, file_data['is_google_type'])

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

    def __remove_file(self, file_path):
        self.logger.debug(f"Removing file: {file_path}")
        self.windows_service.move_to_recycle_bin(file_path)
