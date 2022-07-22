import os
import logging
from pathlib import Path
from send2trash import send2trash
from shutil import copyfile
from config.config import CONFIG


class DiffService:
    def __init__(self):
        self.logger = logging.getLogger('backup_system')

    def compare_drive_and_local(self, scan_results):
        self.logger.debug("Comparing 'drive' and 'local'")
        diff = {
            'new': [],
            'modified': [],
            'removed': []
        }

        prev_diff_lengths = {
            'new': 0,
            'modified': 0,
            'removed': 0
        }

        # Iterating 'local' file types
        for file_type, local_files_paths in scan_results['local'].items():
            drive_files_paths = scan_results['drive'][file_type]

            # Get 'drive' and 'local' extensions
            drive_ext = CONFIG['drive'][file_type]['extension']
            local_ext = CONFIG['local'][file_type]['extension']

            # Iterating 'local' files
            for file_path, file_data in local_files_paths.items():
                # Replace 'local' extension with 'drive' extension
                drive_file_path = file_path.replace(local_ext, drive_ext)

                # If local file isn't found in Google Drive it should be removed locally
                if drive_file_path not in drive_files_paths:
                    diff['removed'].append({
                        'type': file_type,
                        'path': drive_file_path,
                        **file_data
                    })
                    self.logger.debug(
                        f"Removed file: '{file_path}'")
                    continue

            self.logger.debug(
                f"Found {len(diff['removed']) - prev_diff_lengths['removed']} removed '{file_type}' files in 'drive'")
            prev_diff_lengths['removed'] = len(diff['removed'])

        # Iterating 'drive' file types
        for file_type, drive_files_paths in scan_results['drive'].items():
            local_files_paths = scan_results['local'][file_type]

            # Get 'drive' and 'local' extensions
            drive_ext = CONFIG['drive'][file_type]['extension']
            local_ext = CONFIG['local'][file_type]['extension']

            # Iterating 'drive' files
            for file_path, file_data in drive_files_paths.items():
                # Replace 'drive' extension with 'local' extension
                local_file_path = file_path.replace(drive_ext, local_ext)

                # If Google Drive file isn't found locally it should be added locally
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
                f"Found {len(diff['new']) - prev_diff_lengths['new']} new '{file_type}' files in 'drive'")
            prev_diff_lengths['new'] = len(diff['new'])

            self.logger.debug(
                f"Found {len(diff['modified']) - prev_diff_lengths['modified']} modified '{file_type}' files in 'drive'")
            prev_diff_lengths['modified'] = len(diff['modified'])

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

                # If the file type is 'gsheet' or 'gdoc' or any other Google file type,
                # it means that it was downloaded and saved in the tmp folder as 'xlsx' or 'docx' or any other Microsoft Office equivalent.
                # Else, the file is a 'pdf' or 'txt' and is available for copying directly from the Google Drive stream (G:/ drive)
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
