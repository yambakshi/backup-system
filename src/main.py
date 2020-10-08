from pathlib import Path
from services.log_service import LogService
from services.downloads_service import DownloadsService
from services.filter_service import FilterService
from config.config import CONFIG


def update_local_files():
    log_service = LogService()
    downloads_service = DownloadsService(log_service)
    filter_service = FilterService(log_service)

    # Filter Microsoft Excel files in local machine
    # filter_service.filter_files_by_types(CONFIG['Microsoft Excel']['filter'], [
    #                                      r'D:/Yam Bakshi/Careers/Hi-Tech/Portfolio/Python/Backup Utils/tmp'])

    # Download all Google Sheet documents from Google Drive
    downloads_service.download_files_by_type(
        CONFIG['Google Sheets']['download'])

    # Download 3 Google Sheet documents from Google Drive
    # downloads_service.download_files(CONFIG['Google Sheets']['download'], 3)

    missing_files_counter = 0
    for file_path in downloads_service.downloaded_files:
        if not file_path in filter_service.filtered_files:
            missing_files_counter += 0
            missing_file_message = f"Downloaded file is missing from local machine: {file_path}"
            log_service.log(missing_file_message)

    if missing_files_counter == 0:
        log_service.log('All downloaded files paths are found in local machine')
    else:
        log_service.log(f"{missing_files_counter} downloaded files are missing in local machine")


def main():
    update_local_files()


if __name__ == '__main__':
    main()
