import os
import io
import logging
import time
from datetime import datetime
from config.config import CONFIG


class ScanService:
    def __init__(self):
        self.logger = logging.getLogger('backup_system')

    def scan(self, space: str, root_directory_path: str):
        all_files_paths = {}
        for file_type, file_type_data in CONFIG[space].items():
            self.config = file_type_data
            self.logger.debug(
                f"Searching '{file_type_data['extension']}' files in '{root_directory_path}'")
            files_paths = self.__iterate_files(root_directory_path, {})
            self.logger.debug(
                f"Found {len(files_paths)} '{file_type_data['extension']}' files in '{root_directory_path}'")

            all_files_paths[file_type] = files_paths

        return all_files_paths

    def __iterate_files(self, parent_directory, files_paths: {}):
        for filename in os.listdir(parent_directory):
            if filename in self.config['excluded_directories']:
                return files_paths

            file_path = f"{parent_directory}/{filename}"
            if os.path.isdir(file_path):
                files_paths = self.__iterate_files(file_path, files_paths)

            extension = os.path.splitext(filename)[1][1:]
            if extension == self.config['extension']:
                file_path_no_root = '/'.join(file_path.split('/')[2:])
                file_last_modified = os.stat(file_path).st_mtime
                files_paths[file_path_no_root] = {
                    'last_modified': file_last_modified
                }
                # if self.cache_scan:
                #     self.cache_service.write(
                #         self.config['cache_file'], f"{file_path_no_root}|{file_last_modified}")
                self.logger.debug(f"Found file: '{file_path}'")

        return files_paths

    # def __load_cache(self):
    #     self.logger.debug(
    #         f"Loading '{self.config['extension']}' files from 'cache/{self.config['cache_file']}'")
    #     cache_contents = self.cache_service.read(self.config['cache_file'])
    #     cache_lines = cache_contents.split('\n')[:-1]
    #     files_paths = {}
    #     for line in cache_lines:
    #         file_path, file_last_modified = line.split('|')
    #         files_paths[file_path] = {
    #             'last_modified': float(file_last_modified)
    #         }
    #     self.logger.debug(
    #         f"Loaded {len(files_paths)} '{self.config['extension']}' files from 'cache/{self.config['cache_file']}'")

    #     return files_paths
