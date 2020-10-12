import os
import io
import logging
from config.config import CONFIG


class SearchService:
    def __init__(self, cache_service):
        self.logger = logging.getLogger('backup_system')
        self.cache_service = cache_service

    def search_files(self, space: str, root_directory_path: str):
        all_files_paths = {}
        for file_type, file_type_data in CONFIG[space].items():
            config = {
                'root_directory_path': root_directory_path,
                **file_type_data
            }

            if self.cache_service.cache_exists(config['cache_file']):
                files_paths = self.__load_cache(config)
            else:
                file_extensions = ','.join(config['file_extensions'])
                self.logger.debug(
                    f"Searching '{file_extensions}' files in '{config['root_directory_path']}'")
                files_paths = self.__iterate_files(config, [])
                self.logger.debug(
                    f"Found {len(files_paths)} '{file_extensions}' files in '{config['root_directory_path']}'")

            all_files_paths[file_type] = files_paths

        return all_files_paths

    def __iterate_files(self, config: {}, files_paths: []):
        for filename in os.listdir(config['root_directory_path']):
            if filename in config['excluded_directories']:
                return files_paths

            file_path = f"{config['root_directory_path']}/{filename}"
            if os.path.isdir(file_path):
                files_paths = self.__iterate_files(
                    {**config, 'root_directory_path': file_path}, files_paths)

            extension = os.path.splitext(filename)[1][1:]
            if extension in config['file_extensions']:
                file_path_no_root = '/'.join(file_path.split('/')[2:])
                files_paths.append(file_path_no_root)
                self.cache_service.write(
                    config['cache_file'], file_path_no_root)
                self.logger.debug(f"Found file: '{file_path}'")

        return files_paths

    def __load_cache(self, config):
        file_extensions = ','.join(config['file_extensions'])
        self.logger.debug(
            f"Loading '{file_extensions}' files from 'cache/{config['cache_file']}'")
        cache = self.cache_service.read(config['cache_file'])
        files_paths = cache.split('\n')[:-1]
        self.logger.debug(
            f"Loaded {len(files_paths)} '{file_extensions}' files from 'cache/{config['cache_file']}'")

        return files_paths
