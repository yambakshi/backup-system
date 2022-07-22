import os
import logging
from config.config import CONFIG
from services.cache_service import CacheService


class ScanService:
    def __init__(self):
        self.logger = logging.getLogger('backup_system')
        self.cache_service = CacheService()

    def scan(self, space: str, root_directory_path: str):
        files_paths = {}
        for file_type, config in CONFIG[space].items():
            cache_file_path = f"caches/{config['cache_file']}"

            # If cache file exists load scan from cache
            if os.path.isfile(cache_file_path):
                files_paths[file_type] = self.__load_cache(config)
            else:
                self.logger.debug(
                    f"Scanning '{space}' ('{root_directory_path}') for '{config['extension']}' files...")
                files_paths[file_type] = self.__iterate_files(
                    root_directory_path, {}, config)
                self.logger.debug(
                    f"Scanned {len(files_paths[file_type])} '{config['extension']}' files in '{space}' ('{root_directory_path}')")

                self.logger.debug(
                    f"Caching scan results in '{cache_file_path}'")
                self.cache_service.cache(
                    files_paths[file_type], cache_file_path)

        return files_paths

    def __iterate_files(self, parent_directory, files_paths: {}, config):
        for filename in os.listdir(parent_directory):
            if filename in config['excluded_directories']:
                return files_paths

            file_path = f"{parent_directory}\\{filename}"
            if os.path.isdir(file_path):
                files_paths = self.__iterate_files(
                    file_path, files_paths, config)

            extension = os.path.splitext(filename)[1][1:]
            if extension == config['extension']:
                file_path_no_root = '\\'.join(file_path.split('\\')[2:])
                file_last_modified = os.stat(file_path).st_mtime
                files_paths[file_path_no_root] = {
                    'last_modified': file_last_modified
                }

                self.logger.debug(f"Found file: '{file_path}'")

        return files_paths

    def __load_cache(self, config: {}):
        self.logger.debug(
            f"Loading '{config['extension']}' files from scan results cache 'caches/{config['cache_file']}'")
        cache_contents = self.cache_service.load(
            f"caches/{config['cache_file']}")
        cache_lines = cache_contents.split('\n')[:-1]
        files_paths = {}
        for line in cache_lines:
            file_path, file_last_modified = line.split('|')
            files_paths[file_path] = {
                'last_modified': float(file_last_modified)
            }

        self.logger.debug(
            f"Loaded {len(files_paths)} '{config['extension']}' files from 'caches/{config['cache_file']}'")
        return files_paths
