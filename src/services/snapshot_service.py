import logging
from services.file_io_service import FileIOService


class SnapshotService(FileIOService):
    def __init__(self):
        self.logger = logging.getLogger('backup_system')
        super().__init__('snapshot')

    def read(self, snapshot_file: str):
        return super().read(snapshot_file)

    def save(self, files_paths: {}):
        self.logger.debug("Saving snapshots")
        super().save(files_paths)
