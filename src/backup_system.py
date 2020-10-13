import os
import logging
import shutil
from utils.logger import init_logger
from services.google_drive_service import GoogleDriveService
from services.scan_service import ScanService
from services.cache_service import CacheService
from services.merge_service import MergeService
from config.config import CONFIG


class BackupSystem:
    def __init__(self):
        self.logger = init_logger()
        self.cache_service = CacheService()
        self.scan_service = ScanService(self.cache_service)
        self.google_drive_service = GoogleDriveService(self.cache_service)
        self.merge_service = MergeService()

    def backup_google_drive_files(self):
        # TODO: Implement 'backup_local_machine_files' method
        # TODO: Update cache upon move/copy files
        # TODO: Add argparse
        # TODO: Handle new/deleted files
        # TODO: Copy non-Google Drive files from file stream instead of downloading them and verify modification date upon copy

        try:
            self.logger.debug("Backing-up 'Google Drive' files")
            self.__delete_tmp_folder()
            files_paths = {
                'drive_stream': self.scan_service.scan('drive_stream', r'G:/My Drive', False),
                'local': self.scan_service.scan('local', r'D:/Yam Bakshi', True),
                'drive': self.google_drive_service.scan(['Google Doc', 'Google Sheet', 'PDF'], False)
            }

            # Check 'drive_stream' for new files that don't exist on 'local'
            self.merge_service.compare_spaces(
                'local', 'drive_stream', files_paths)
            downloads = self.google_drive_service.download_changes(files_paths)
            self.merge_service.merge_downloads_into_local(downloads)
            self.merge_service.merge_drive_stream_into_local(['PDF'])

            # Cleanup
            self.__delete_tmp_folder()
            self.cache_service.delete_cache_folder()
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
