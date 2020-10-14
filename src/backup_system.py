import os
import logging
import shutil
from utils.logger import init_logger
from services.snapshot_service import SnapshotService
from services.google_drive_service import GoogleDriveService
from services.scan_service import ScanService
from services.diff_service import DiffService


class BackupSystem:
    def __init__(self):
        self.logger = init_logger()
        self.snapshot_service = SnapshotService()
        self.scan_service = ScanService()
        self.google_drive_service = GoogleDriveService()
        self.diff_service = DiffService(self.snapshot_service)

    def backup_google_drive_files(self):
        # TODO: Implement 'backup_local_machine_files' method
        # TODO: Add argparse
        # TODO: Handle 'remove' files

        try:
            self.logger.debug("Backing-up 'Google Drive' files")
            files_paths = {
                'drive_stream': self.scan_service.scan('drive_stream', r'G:/My Drive'),
                'local': self.scan_service.scan('local', r'D:/Yam Bakshi'),
                'drive': self.google_drive_service.scan(['Google Doc', 'Google Sheet', 'PDF'])
            }

            diff = self.diff_service.get_diff(files_paths)
            downloads = self.google_drive_service.download_changes(diff)
            self.diff_service.merge_downloads(downloads)
            self.snapshot_service.save(files_paths)

            # Cleanup
            self.__delete_tmp_folder()
            self.logger.debug('Backup completed succesfully')
        except Exception as err:
            self.logger.error(err)

    def backup_local_machine_files(self):
        try:
            self.logger.debug("Backing-up local files")
        except Exception as err:
            self.logger.error(err)

    def __delete_tmp_folder(self):
        if os.path.exists('./tmp'):
            shutil.rmtree(r'tmp')
