import os
import logging
from pathlib import Path
from send2trash import send2trash
from shutil import copyfile
from config.config import CONFIG


class DiffService:
    def __init__(self, snapshot_service):
        self.logger = logging.getLogger('backup_system')
        self.snapshot_service = snapshot_service

    def get_diff(self, files_paths):
        self.logger.debug("Comparing 'drive' and 'local'")
        diff = {
            'new': [],
            'modified': [],
            'removed': []
        }

        for file_type, drive_files_paths in files_paths['drive'].items():
            drive_stream_files_paths = files_paths['drive_stream'][file_type]
            local_files_paths = files_paths['local'][file_type]

            # Get 'drive' and 'local' extensions
            drive_ext = CONFIG['drive'][file_type]['extension']
            local_ext = CONFIG['local'][file_type]['extension']

            # Get last 'drive' snapshot for the current file type
            snapshot_contents = self.snapshot_service.read(
                CONFIG['drive'][file_type]['snapshot_file'])
            snapshot_files_paths = [snapshot_file.split(
                '|')[0] for snapshot_file in snapshot_contents.split('\n')[:-1]]

            # Iterating 'drive' snapshot files
            for file_path in snapshot_files_paths:
                # If snapshot file path is not in 'drive' files paths, it should be removed locally
                if file_path not in drive_files_paths:
                    local_file_path = file_path.replace(drive_ext, local_ext)
                    diff['removed'].append({
                        'type': file_type,
                        'path': local_file_path
                    })
                    self.logger.debug(
                        f"Removed file: '{file_path}'")

            # Iterating 'drive' files
            for file_path, file_data in drive_files_paths.items():
                # Only files found in 'drive_stream' are counted as diffs
                if file_path not in drive_stream_files_paths:
                    continue

                # Replace 'drive' extension with 'local' extension
                local_file_path = file_path.replace(drive_ext, local_ext)

                # If file isn't found locally it's should be added locally
                if local_file_path not in local_files_paths:
                    diff['new'].append({
                        'type': file_type,
                        'path': local_file_path,
                        **file_data
                    })
                    self.logger.debug(
                        f"New file: '{file_path}'")
                    continue

                # If file is found locally and its 'last_modified' date is before the 'drive' file's 'last_modified', it's modified
                if file_data['last_modified'] > local_files_paths[local_file_path]['last_modified']:
                    diff['modified'].append({
                        'type': file_type,
                        'path': local_file_path,
                        **file_data
                    })
                    self.logger.debug(
                        f"Modified file: '{file_path}'")
                    continue

        self.logger.debug(
            f"Diff is: {len(diff['new'])} new files, {len(diff['modified'])} modified files, {len(diff['removed'])} removed files")
        return diff

    def merge_changes(self, diff):
        self.logger.debug("Merging changes into 'local'")
        tmp_abs_path = os.path.abspath('tmp')
        for diff_type, files_data in diff.items():
            for file_data in files_data:
                file_path = file_data['path']

                local_file_path = f"D:\\Yam Bakshi\\{file_path}"
                if diff_type == 'removed':
                    self.__remove_file(local_file_path)
                    continue

                if file_data['is_google_type']:
                    downloads_file_path = f"{tmp_abs_path}\\{file_path}"
                else:
                    downloads_file_path = f"G:\\My Drive\\{file_path}"

                if diff_type == 'modified':
                    self.__replace_file(
                        local_file_path, downloads_file_path, not file_data['is_google_type'])
                elif diff_type == 'new':
                    self.__add_file(
                        local_file_path, downloads_file_path, not file_data['is_google_type'])
                else:
                    continue

                os.utime(local_file_path,
                         (file_data['last_modified'], file_data['last_modified']))

    def __replace_file(self, old_file_path: str, new_file_path: str, copy_new_file: bool):
        self.logger.debug(
            f"Replacing file: '{old_file_path}'")
        send2trash(old_file_path)
        if copy_new_file:
            copyfile(new_file_path, old_file_path)
        else:
            os.rename(new_file_path, old_file_path)

    def __add_file(self, old_file_path: str, new_file_path: str, copy_new_file: bool):
        old_file_path_parent = '\\'.join(old_file_path.split('\\')[:-1])
        self.logger.debug(
            f"Adding file '{new_file_path}' to '{old_file_path_parent}'")

        if os.path.isfile(new_file_path):
            self.logger.debug(f"File already exists: '{new_file_path}'")
            return

        Path(old_file_path_parent).mkdir(parents=True, exist_ok=True)
        if copy_new_file:
            copyfile(new_file_path, old_file_path)
        else:
            os.rename(new_file_path, old_file_path)

    def __remove_file(self, file_path):
        self.logger.debug(f"Removing file: '{file_path}'")
        if os.path.isfile(file_path):
            send2trash(file_path)
        else:
            self.logger.error(f"Couldn't find file: '{file_path}'")
