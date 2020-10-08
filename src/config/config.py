ROOT = r'D:/Yam Bakshi/Careers/Hi-Tech/Portfolio/Python/Backup Utils'

CONFIG = {
    'Google Docs': {
        'filter': {
            'root_directory_path': r"G:/My Drive",
            'file_extensions': ['gdoc']
        },
        'download': {
            'drive_file_type': 'application/vnd.google-apps.document',
            'download_as': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'save_as': 'docx'
            # 'download_as': 'application/pdf',
            # 'save_as': 'pdf'
        }
    },
    'Google Sheets': {
        'filter': {
            'root_directory_path': r"G:/My Drive",
            'file_extensions': ['gsheet']
        },
        'download': {
            'drive_file_type': 'application/vnd.google-apps.spreadsheet',
            'download_as': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'save_as': 'xlsx',
            # 'download_as': 'application/pdf',
            # 'save_as': 'pdf'
        }
    },
    'Google PDFs': {
        'filter': {
            'root_directory_path': r'G:/My Drive',
            'file_extensions': ['pdf']
        },
        'download': {
            'drive_file_type': 'application/pdf',
            'download_as': 'application/pdf',
            'save_as': 'pdf'
        }
    },
    'Microsoft Word': {
        'filter': {
            'root_directory_path': f"{ROOT}/tmp",
            'file_extensions': ['docx']
        }
    },
    'Microsoft Excel': {
        'filter': {
            'root_directory_path': r'D:/Yam Bakshi',
            'file_extensions': ['xlsx']
        }
    },
    'Log': {
        'log_file': r'backup.log'
    }
}
