import os
from pathlib import Path
from services.log_service import LogService
from services.downloads_service import DownloadsService
from services.filter_service import FilterService
from config.config import CONFIG


def init_folders():    
    # Create tmp folder for the downloads
    if not os.path.exists('./tmp'):
        os.makedirs('./tmp')


def update_local_files():
    log_service = LogService()
    downloads_service = DownloadsService()
    filter_service = FilterService(log_service)

    filter_service.filter_files_by_types(CONFIG['Microsoft Excel']['filter'])
    # downloads_service.download_files_by_type(CONFIG['Google Sheets']['download'])

    for file_path in downloads_service.files_paths:
        if not file_path in filter_service.files_paths:
            missing_file_message = f"Downloaded file is missing from local machine: {file_path}"
            log_service.log(missing_file_message)


def main():
    init_folders()
    update_local_files()


if __name__ == '__main__':
    main()
