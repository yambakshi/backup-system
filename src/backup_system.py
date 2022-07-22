import os
import logging
import shutil
import sys
import traceback
from utils.logger import init_logger
from services.google_drive_service import GoogleDriveService
from services.scan_service import ScanService
from services.diff_service import DiffService
from pathlib import Path


class BackupSystem:
    def __init__(self):
        self.logger = init_logger()
        self.scan_service = ScanService()
        self.google_drive_service = GoogleDriveService()
        self.diff_service = DiffService()

        if not os.path.exists('caches'):
            Path('caches').mkdir(parents=True, exist_ok=True)

    def backup_google_drive_files(self):
        try:
            self.logger.debug("Backing-up Google Drive files")

            # Scan spaces
            scan_results = {
                'drive_stream': self.scan_service.scan('drive_stream', 'G:\My Drive'),
                'local': self.scan_service.scan('local', 'D:\Yam Bakshi'),
                'drive': self.google_drive_service.scan()
            }

            # Get the diff between 'drive' to 'local'
            diff = self.diff_service.compare_drive_and_local(scan_results)
            if len(diff['new']) > 0 or len(diff['modified']) > 0:
                self.google_drive_service.download_changes(diff)
            elif len(diff['removed']) == 0:
                self.logger.debug(
                    "Nothing to do. 'local' is synced with 'drive'")
                return

            # Merge diff to 'local'
            # self.diff_service.merge_changes(diff)

            # Cleanup
            self.__delete_tmp_folder()
            self.logger.debug('Backup completed succesfully')
        except Exception as err:
            self.logger.exception(err)

    def backup_local_files(self):
        try:
            self.logger.debug("Backing-up local files")
        except Exception as err:
            self.logger.exception(err)

    def __delete_tmp_folder(self):
        if os.path.exists('./tmp'):
            shutil.rmtree(r'tmp')
