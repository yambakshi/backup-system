import os
from pathlib import Path
from services.downloads_service import DownloadsService
from services.filter_service import FilterService
from config.config import CONFIG


def init_folders():
    # Create log folders
    if not os.path.exists('./logs'):
        Path(r'logs/filter').mkdir(parents=True, exist_ok=True)
        Path(r'logs/download').mkdir(parents=True, exist_ok=True)
    
    # Create tmp folder for the downloads
    if not os.path.exists('./tmp'):
        os.makedirs('./tmp')

def main():
    init_folders()
    downloads_service = DownloadsService()
    filter_service = FilterService()

    downloads_service.download_files_by_type(CONFIG['Google Sheets']['download'])
    # filter_service.filter_files_by_types(CONFIG['Microsoft Excel']['filter'])


if __name__ == '__main__':
    main()
