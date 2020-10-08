import os
import io
from datetime import datetime


class FilterService:
    def __init__(self, log_service):
        self.files_paths = []
        self.log_service = log_service

    def filter_files_by_types(self, filter_config):
        files_counter = self.iterate_files(filter_config)
        self.log_service.log(f"{files_counter} files found")


    def iterate_files(self, filter_config, files_counter = 0):
        for filename in os.listdir(filter_config['root_directory_path']):
            file_path = f"{filter_config['root_directory_path']}/{filename}"
            if os.path.isdir(file_path):
                files_counter = self.iterate_files({**filter_config, 'root_directory_path': file_path}, files_counter)

            extension = os.path.splitext(filename)[1][1:]
            if extension in filter_config['file_extensions']:
                files_counter += 1
                self.files_paths.append('/'.join(file_path.split('/')[2:]))
                self.log_service.log(file_path)

        return files_counter
