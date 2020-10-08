import os
import io
from datetime import datetime
from .cache_service import CacheService
from config.config import CONFIG


class FilterService:
    def __init__(self, log_service):
        self.filtered_files = []
        self.log_service = log_service
        self.cache_service = CacheService(CONFIG['Cache']['filter_cache_file'])


    def filter_files_by_types(self, filter_config, excluded_paths=[]):
        files_counter = self.__iterate_files(filter_config, excluded_paths)
        self.log_service.log(f"{files_counter} files found")


    def __iterate_files(self, filter_config, excluded_paths=[], files_counter=0):
        if filter_config['root_directory_path'] in excluded_paths:
            return files_counter

        for filename in os.listdir(filter_config['root_directory_path']):
            file_path = f"{filter_config['root_directory_path']}/{filename}"
            if os.path.isdir(file_path):
                files_counter = self.__iterate_files(
                    {**filter_config, 'root_directory_path': file_path}, excluded_paths, files_counter)

            extension = os.path.splitext(filename)[1][1:]
            if extension in filter_config['file_extensions']:
                files_counter += 1
                self.filtered_files.append('/'.join(file_path.split('/')[2:]))
                self.cache_service.write('/'.join(file_path.split('/')[2:]))
                self.log_service.log(f"Filtered file: {file_path}")

        return files_counter
