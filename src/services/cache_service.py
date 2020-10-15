import logging
from services.file_io_service import FileIOService


class CacheService(FileIOService):
    def __init__(self):
        self.logger = logging.getLogger('backup_system')
        super().__init__('cache')

    def read(self, cache_file: str):
        super().read(cache_file)

    def save(self, files_paths: {}):
        self.logger.debug("Saving caches")
        super().save(files_paths)
