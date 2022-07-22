import io
import logging


class CacheService:
    def __init__(self):
        self.logger = logging.getLogger('backup_system')

    def load(self, cache_file_path: str):
        with io.open(cache_file_path, "r", encoding="utf8") as f:
            contents = f.read()
            return contents

    def cache(self, scan_results, cache_file_path: str):
        lines = []
        for file_path, file_data in scan_results.items():
            file_data_str = ''.join(
                [f"|{val}" for val in file_data.values()])
            lines.append(f"{file_path}{file_data_str}")

        with io.open(cache_file_path, "w", encoding="utf8") as f:
            f.writelines(line + '\n' for line in lines)
