import os
import io
from copy import deepcopy
from datetime import datetime
from .cache_service import CacheService
from config.config import CONFIG


class FilterService:
    def __init__(self, log_service):
        self.filtered_files = []
        self.log_service = log_service
        self.cache_service = CacheService()

    def filter_files_by_types(self, config: {}, use_cache: bool, excluded_paths: []):
        self.log_service.log(f"Filtering files in {config['root_directory_path']}")
        self.filtered_files.clear()
        self.cache_service.set_file(config['cache_file'], use_cache)
        if use_cache:
            self.__load_cache(config)
            self.log_service.log(f"{len(self.filtered_files)} already filtered")
        else:
            self.__iterate_files(config, excluded_paths)
            self.log_service.log(f"{len(self.filtered_files)} files filtered")

        return deepcopy(self.filtered_files)

    def __iterate_files(self, config: {}, excluded_paths=[]):
        if config['root_directory_path'] in excluded_paths:
            return

        for filename in os.listdir(config['root_directory_path']):
            file_path = f"{config['root_directory_path']}/{filename}"
            if os.path.isdir(file_path):
                self.__iterate_files(
                    {**config, 'root_directory_path': file_path}, excluded_paths)

            extension = os.path.splitext(filename)[1][1:]
            if extension in config['file_extensions']:
                self.filtered_files.append('/'.join(file_path.split('/')[2:]))
                self.cache_service.write('/'.join(file_path.split('/')[2:]))
                self.log_service.log(f"Filtered file: {file_path}")

    def __load_cache(self, config):
        cache = self.cache_service.read()
        self.filtered_files = cache.split('\n')[:-1]
