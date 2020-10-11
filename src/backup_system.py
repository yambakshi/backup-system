import os
import logging
from services.logger_service import init_logger
from services.cache_service import CacheService
from services.downloads_service import DownloadsService
from services.files_service import FilesService
from services.updater_service import UpdaterService


class BackupSystem:
    def __init__(self):
        self.logger = init_logger()
        self.cache_service = CacheService()
        self.downloads_service = DownloadsService(self.cache_service)
        self.files_service = FilesService(self.cache_service)

    def update_local_machine(self):
        try:
            files_paths = {}

            # Get local machine file paths
            files_paths['local'] = self.files_service.get_files(
                'local', ['Microsoft Word', 'Microsoft Excel', 'PDF'])

            # Get Google Drive Stream files paths
            files_paths['drive_stream'] = self.files_service.get_files(
                'drive_stream', ['Google Doc', 'Google Sheet', 'PDF'])

            # Download Google Drive files
            self.downloads_service.reset_tmp_folder()
            files_paths['downloads'] = self.downloads_service.download_all_files(
                ['Google Doc', 'Google Sheet', 'PDF'])

            # Check downloaded files
            self.updater_service = UpdaterService(files_paths)
            self.updater_service.check_downloaded_files_paths(
                'Google Doc', 'Microsoft Word')
            self.updater_service.check_downloaded_files_paths(
                'Google Sheet', 'Microsoft Excel')
            self.updater_service.check_downloaded_files_paths('PDF', 'PDF')

            # Update local machine
            # self.updater_service.update_local_machine(
            #     ['Google Doc', 'Google Sheet', 'PDF'])

            # # Delete tmp folder
            # self.downloads_service.delete_tmp_folder()
        except Exception as err:
            self.logger.error(err)
