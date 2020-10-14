import os
import logging
import shutil
from utils.logger import init_logger
from services.google_drive_service import GoogleDriveService
from services.scan_service import ScanService
from services.cache_service import CacheService
from services.diff_service import DiffService
from config.config import CONFIG


class BackupSystem:
    def __init__(self):
        self.logger = init_logger()
        self.cache_service = CacheService()
        self.scan_service = ScanService()
        self.google_drive_service = GoogleDriveService()
        self.diff_service = DiffService(self.cache_service)

    def backup_google_drive_files(self):
        # TODO: Implement 'backup_local_machine_files' method
        # TODO: Update cache upon move/copy files
        # TODO: Add argparse
        # TODO: Handle 'remove' files

        try:
            self.logger.debug("Backing-up 'Google Drive' files")
            self.__delete_tmp_folder()
            files_paths = {
                'drive_stream': self.scan_service.scan('drive_stream', r'G:/My Drive'),
                'local': self.scan_service.scan('local', r'D:/Yam Bakshi'),
                'drive': self.google_drive_service.scan(['Google Doc', 'Google Sheet', 'PDF'])
            }

            diff = self.diff_service.get_diff(files_paths)
            downloads = self.google_drive_service.download_changes(diff)
            self.diff_service.merge_downloads(downloads)
            # self.cache_service.update_cache(files_paths)

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
