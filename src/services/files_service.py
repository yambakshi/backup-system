import os
import io
import logging
from config.config import CONFIG


class FilesService:
    def __init__(self, cache_service):
        self.logger = logging.getLogger('backup_system')
        self.cache_service = cache_service

    def get_files(self, space: str, file_type: str):
        config = {
            'root_directory_path': CONFIG[space]['root_directory_path'],
            **CONFIG[space]['file_types'][file_type]
        }
        
        if self.cache_service.cache_exists(config['cache_file']):
            files = self.__load_cache(config)
        else:
            file_extensions = ','.join(config['file_extensions'])
            self.logger.debug(
                f"Searching '{file_extensions}' files in '{config['root_directory_path']}'")
            files = self.__iterate_files(config, [])
            self.logger.debug(
                f"Found {len(files)} '{file_extensions}' files in '{config['root_directory_path']}'")

        return files

    def __iterate_files(self, config: {}, files: []):
        for filename in os.listdir(config['root_directory_path']):
            if filename in config['excluded_directories']:
                return files

            file_path = f"{config['root_directory_path']}/{filename}"
            if os.path.isdir(file_path):
                files = self.__iterate_files(
                    {**config, 'root_directory_path': file_path}, files)

            extension = os.path.splitext(filename)[1][1:]
            if extension in config['file_extensions']:
                file_path_no_root = '/'.join(file_path.split('/')[2:])
                files.append(file_path_no_root)
                self.cache_service.write(
                    config['cache_file'], file_path_no_root)
                self.logger.debug(f"Found file: '{file_path}'")

        return files

    def __load_cache(self, config):
        file_extensions = ','.join(config['file_extensions'])
        self.logger.debug(
            f"Loading '{file_extensions}' files from 'cache/{config['cache_file']}'")
        cache = self.cache_service.read(config['cache_file'])
        files = cache.split('\n')[:-1]
        self.logger.debug(
            f"Loaded {len(files)} '{file_extensions}' files from 'cache/{config['cache_file']}'")

        return files
