import io
import os
import logging
import shutil
from pathlib import Path


class CacheService:
    def __init__(self):
        self.logger = logging.getLogger('backup_system')
        if not os.path.exists('./cache'):
            Path(r'cache').mkdir(parents=True, exist_ok=True)

    def clear_cache(self, cache_file):
        if os.path.isfile(f"cache/{cache_file}"):
            self.logger.debug(f"Clearing cache: '{cache_file}'")
            open(cache_file, 'w').close()

    def delete_cache_folder(self):
        if not os.path.exists('./cache'):
            shutil.rmtree(r'cache')

    def write(self, cache_file: str, item: str):
        with io.open(f"cache/{cache_file}", "a", encoding="utf-8") as f:
            f.write(f"{item}\n")

    def read(self, cache_file: str):
        with io.open(f"cache/{cache_file}", "r", encoding="utf8") as f:
            contents = f.read()
            return contents

    def update(self, update: []):
        for cache in update:
            cache_file = cache['cache_file']
            lines = self.read(cache_file).split('\n')[:-1]
            for line in cache['remove_lines']:
                lines.remove(line)

            lines += [line.replace('\\', '/') for line in cache['add_lines']]
            with io.open(f"cache/{cache_file}", "w", encoding="utf8") as f:
                f.writelines(line + '\n' for line in lines)

    def cache_exists(self, cache_file: str):
        return os.path.isfile(f"cache/{cache_file}")
