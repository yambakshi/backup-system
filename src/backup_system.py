import os
import logging
import shutil
from utils.logger import init_logger
from services.snapshot_service import SnapshotService
from services.cache_service import CacheService
from services.google_drive_service import GoogleDriveService
from services.scan_service import ScanService
from services.diff_service import DiffService


class BackupSystem:
    # TODO: Build project to an EXE

    def __init__(self):
        self.logger = init_logger()
        self.cache_service = CacheService()
        self.snapshot_service = SnapshotService()
        self.scan_service = ScanService(self.cache_service)
        self.google_drive_service = GoogleDriveService(self.cache_service)
        self.diff_service = DiffService(self.snapshot_service)
        self.load_cache = False

    def backup_google_drive_files(self):
        try:
            self.logger.debug("Backing-up Google Drive files")
            files_paths = {
                'drive_stream': self.scan_service.scan('drive_stream', 'G:\My Drive', self.load_cache),
                'local': self.scan_service.scan('local', 'D:\Yam Bakshi', self.load_cache),
                'drive': self.google_drive_service.scan(self.load_cache)
            }

            # If files_paths were loaded from cache no need to save them to cache
            if not self.load_cache:
                self.cache_service.save(files_paths)

            # Get the diff between 'drive' to 'local'
            diff = self.diff_service.get_diff(files_paths)
            if len(diff['new']) > 0 or len(diff['modified']) > 0:
                self.google_drive_service.download_changes(diff)
            elif len(diff['removed']) == 0:
                self.logger.debug(
                    "Nothing to do. 'local' is synced with 'drive'")
                return
            
            # Merge diff to 'local'
            self.diff_service.merge_changes(diff)

            # Save files paths snapshots of all spaces
            self.snapshot_service.save(files_paths)

            # Cleanup
            self.__delete_tmp_folder()
            self.logger.debug('Backup completed succesfully')
        except Exception as err:
            self.logger.error(err)

    def backup_local_files(self):
        try:
            self.logger.debug("Backing-up local files")
        except Exception as err:
            self.logger.error(err)

    def __delete_tmp_folder(self):
        if os.path.exists('./tmp'):
            shutil.rmtree(r'tmp')
