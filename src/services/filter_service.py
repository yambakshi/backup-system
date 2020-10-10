import os
import io
import logging


class FilterService:
    def __init__(self, cache_service):
        self.cache_service = cache_service

    def get_files_by_types(self, config: {}, use_cache: bool, excluded_paths: []):
        logging.debug(
            f"Searching '{','.join(config['file_extensions'])}' files in '{config['root_directory_path']}'")

        if use_cache:
            filtered_files = self.__load_cache(config)
            logging.debug(
                f"{len(filtered_files)} '{','.join(config['file_extensions'])}' files loaded from 'cache/{config['cache_file']}'")
        else:
            filtered_files = self.__iterate_files(config, excluded_paths)
            logging.debug(
                f"{len(filtered_files)} '{','.join(config['file_extensions'])}' files found in '{config['root_directory_path']}'")

        return filtered_files

    def __iterate_files(self, config: {}, excluded_paths: [], filtered_files=[]):
        if config['root_directory_path'] in excluded_paths:
            return filtered_files

        for filename in os.listdir(config['root_directory_path']):
            file_path = f"{config['root_directory_path']}/{filename}"
            if os.path.isdir(file_path):
                filtered_files = self.__iterate_files(
                    {**config, 'root_directory_path': file_path}, excluded_paths, filtered_files)

            extension = os.path.splitext(filename)[1][1:]
            if extension in config['file_extensions']:
                filtered_files.append('/'.join(file_path.split('/')[2:]))
                self.cache_service.write(
                    config['cache_file'], '/'.join(file_path.split('/')[2:]))
                logging.debug(f"Found file: '{file_path}'")

        return filtered_files

    def __load_cache(self, config):
        cache = self.cache_service.read(config['cache_file'])
        return cache.split('\n')[:-1]
