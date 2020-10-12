import os
import logging
import shutil
from utils.logger import init_logger
from services.cache_service import CacheService
from services.google_drive_service import GoogleDriveService
from services.scan_service import ScanService
from services.merge_service import MergeService


class BackupSystem:
    def __init__(self):
        self.logger = init_logger()
        self.cache_service = CacheService()
        self.merge_service = MergeService(self.cache_service)
        self.google_drive_service = GoogleDriveService(self.cache_service)
        self.scan_service = ScanService(self.cache_service)

    def backup_google_drive_files(self):
        # TODO: Replace local files only if modification date changed from previous merge
        # TODO: Implement 'backup_local_machine_files' method
        # TODO: Update cache upon move/copy files
        # TODO: Add argparse

        try:
            self.logger.debug("Backing-up 'Google Drive' files")
            self.__delete_tmp_folder()
            files_paths = {
                'local': self.scan_service.scan('local', r'D:/Yam Bakshi'),
                'drive_stream': self.scan_service.scan('drive_stream', r'G:/My Drive'),
                'downloads': self.google_drive_service.download_all_files(['Google Doc', 'Google Sheet'])
            }

            # Compare downloads and drive_stream to local files paths
            self.merge_service.set_files_paths(files_paths)
            self.merge_service.compare_spaces('local', 'downloads', [
                                              'Google Doc', 'Google Sheet'])
            self.merge_service.compare_spaces('local', 'drive_stream', ['PDF'])

            # Merge new and modified files into local
            self.merge_service.merge_downloads_into_local(
                ['Google Doc', 'Google Sheet'])
            self.merge_service.add_missing_drive_stream_files_to_local(['PDF'])

            # # Cleanup
            self.__delete_tmp_folder()
            self.cache_service.delete_cache_folder()
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
