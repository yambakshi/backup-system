ROOT = r'D:/Yam Bakshi/Careers/Hi-Tech/Portfolio/Python/Backup Utils'

CONFIG = {
    'Google Docs': {
        'filter': {
            'root_directory_path': r"G:/My Drive",
            'file_extensions': ['gdoc'],
            'log_file': 'google-docs.log'
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
            'file_extensions': ['gsheet'],
            'log_file': 'google-sheets.log'
        },
        'download': {
            'drive_file_type': 'application/vnd.google-apps.spreadsheet',
            'download_as': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'save_as': 'xlsx',
            # 'download_as': 'application/pdf',
            # 'save_as': 'pdf'
            'log_file': 'google-sheets.log',
        }
    },
    'Google PDFs': {
        'filter': {
            'root_directory_path': r"G:/My Drive",
            'file_extensions': ['pdf'],
            'log_file': 'pdfs.log'
        },
        'download': {
            'drive_file_type': 'application/pdf',
            'download_as': 'application/pdf',
            'save_as': 'pdf'
        }
    },
    'Microsoft Word': {
        'filter': {
            'root_directory_path': 'f"{ROOT}/tmp"',
            'file_extensions': ['docx'],
            'log_file': 'microsoft-word.log'
        }
    },
    'Microsoft Excel': {
        'filter': {
            'root_directory_path': f"{ROOT}/tmp",
            'file_extensions': ['xlsx'],
            'log_file': 'microsoft-excel.log'
        }
    },
}
