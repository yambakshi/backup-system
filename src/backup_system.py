import os
import logging
from utils.logger import init_logger
from services.cache_service import CacheService
from services.google_drive_service import GoogleDriveService
from services.search_service import SearchService
from services.merge_service import MergeService


class BackupSystem:
    def __init__(self):
        self.logger = init_logger()
        self.cache_service = CacheService()
        self.google_drive_service = GoogleDriveService(self.cache_service)
        self.search_service = SearchService(self.cache_service)

    def update_local_machine(self):
        try:
            files_paths = {}

            # Search local machine
            files_paths['local'] = self.search_service.search_files(
                'local', ['Microsoft Word', 'Microsoft Excel', 'PDF'])

            # Search Google Drive Stream
            files_paths['drive_stream'] = self.search_service.search_files(
                'drive_stream', ['Google Doc', 'Google Sheet', 'PDF'])

            # Download Google Drive files
            files_paths['downloads'] = self.google_drive_service.download_all_files(
                ['Google Doc', 'Google Sheet', 'PDF'])

            # Check downloaded files
            self.merge_service = MergeService(files_paths)
            self.merge_service.compare_local_and_downloads(
                'Microsoft Word', 'Google Doc')
            self.merge_service.compare_local_and_downloads(
                'Microsoft Excel', 'Google Sheet')
            self.merge_service.compare_local_and_downloads('PDF', 'PDF')

            # Update local machine
            self.merge_service.merge_downloads_into_local(
                ['Google Doc', 'Google Sheet', 'PDF'])

            # Cleanup
            self.google_drive_service.delete_tmp_folder()
            self.cache_service.delete_cache_folder()
        except Exception as err:
            self.logger.error(err)

    def update_external_backup(self):
        try:
            pass
        except Exception as err:
            self.logger.error(err)
