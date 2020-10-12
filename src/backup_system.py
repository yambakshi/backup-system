import os
import logging
import shutil
from utils.logger import init_logger
from services.cache_service import CacheService
from services.google_drive_service import GoogleDriveService
from services.search_service import SearchService
from services.merge_service import MergeService


class BackupSystem:
    def __init__(self):
        self.logger = init_logger()
        self.cache_service = CacheService()
        self.merge_service = MergeService()
        self.google_drive_service = GoogleDriveService(self.cache_service)
        self.search_service = SearchService(self.cache_service)

    def backup_google_drive_files(self):
        # TODO: Remove from/Prevent storing on Google Drive downloads cache files paths that don't exist in Google Drive stream
        # TODO: Replace local files only if modification date changed from previous merge
        # TODO: Don't replace non-Google Drive types such as PDF or PNG. ONLY add if missing
        # TODO: Implement 'backup_local_machine_files' method
        # TODO: Implement copying non-Google Drive types from Google Drive Stream instead of downloading them

        try:
            files_paths = {}

            # Search local machine
            files_paths['local'] = self.search_service.search_files(
                'local', r'D:/Yam Bakshi')

            # Search Google Drive Stream
            files_paths['drive_stream'] = self.search_service.search_files(
                'drive_stream', r'G:/My Drive')

            # Download Google Drive files
            self.__delete_tmp_folder()
            files_paths['downloads'] = self.google_drive_service.download_all_files(
                ['Google Doc', 'Google Sheet'])

            # Compare downloads and local files paths
            self.merge_service.set_files_paths(files_paths)
            self.merge_service.compare_local_and_downloads('Google Doc')
            self.merge_service.compare_local_and_downloads('Google Sheet')
            self.merge_service.compare_local_and_downloads('PDF')

            # Update local machine
            self.merge_service.merge_downloads_into_local(
                ['Google Doc', 'Google Sheet', 'PDF'])

            # Cleanup
            self.__delete_tmp_folder()
            self.cache_service.delete_cache_folder()
        except Exception as err:
            self.logger.error(err)

    def backup_local_machine_files(self):
        try:
            pass
        except Exception as err:
            self.logger.error(err)

    def __delete_tmp_folder(self):
        if os.path.exists('./tmp'):
            shutil.rmtree(r'tmp')
