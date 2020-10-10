import os
import io
import logging


class FilesService:
    def __init__(self, cache_service):
        self.logger = logging.getLogger('backup_system')
        self.cache_service = cache_service

    def get_files_by_types(self, config: {}, excluded_paths: []):
        self.logger.debug(
            f"Searching '{','.join(config['file_extensions'])}' files in '{config['root_directory_path']}'")

        if self.cache_service.cache_exists(config['cache_file']):
            files = self.__load_cache(config)
            self.logger.debug(
                f"{len(files)} '{','.join(config['file_extensions'])}' files loaded from 'cache/{config['cache_file']}'")
        else:
            files = self.__iterate_files(config, excluded_paths, [])
            self.logger.debug(
                f"{len(files)} '{','.join(config['file_extensions'])}' files found in '{config['root_directory_path']}'")

        return files

    def __iterate_files(self, config: {}, excluded_paths: [], files: []):
        if config['root_directory_path'] in excluded_paths:
            return files

        for filename in os.listdir(config['root_directory_path']):
            file_path = f"{config['root_directory_path']}/{filename}"
            if os.path.isdir(file_path):
                files = self.__iterate_files(
                    {**config, 'root_directory_path': file_path}, excluded_paths, files)

            extension = os.path.splitext(filename)[1][1:]
            if extension in config['file_extensions']:
                file_path_no_root = '/'.join(file_path.split('/')[2:])
                files.append(file_path_no_root)
                self.cache_service.write(
                    config['cache_file'], file_path_no_root)
                self.logger.debug(f"Found file: '{file_path}'")

        return files

    def __load_cache(self, config):
        cache = self.cache_service.read(config['cache_file'])
        return cache.split('\n')[:-1]
