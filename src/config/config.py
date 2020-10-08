CONFIG = {
    'Google Docs': {
        'filter': {
            'root_directory_path': r"G:/My Drive",
            'file_extensions': ['gdoc'],
            'cache_file': r'google-docs.filter.cache',
        },
        'download': {
            'drive_file_type': 'application/vnd.google-apps.document',
            'download_as': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'save_as': 'docx',
            # 'download_as': 'application/pdf',
            # 'save_as': 'pdf',
            'cache_file': r'google-docs.download.cache',
        }
    },
    'Google Sheets': {
        'filter': {
            'root_directory_path': r"G:/My Drive",
            'file_extensions': ['gsheet'],
            'cache_file': r'google-sheets.filter.cache',
        },
        'download': {
            'drive_file_type': 'application/vnd.google-apps.spreadsheet',
            'download_as': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'save_as': 'xlsx',
            # 'download_as': 'application/pdf',
            # 'save_as': 'pdf',
            'cache_file': r'google-sheets.download.cache',
        }
    },
    'Google PDFs': {
        'filter': {
            'root_directory_path': r'G:/My Drive',
            'file_extensions': ['pdf'],
            'cache_file': r'google-pdf.filter.cache',
        },
        'download': {
            'drive_file_type': 'application/pdf',
            'download_as': 'application/pdf',
            'save_as': 'pdf',
            'cache_file': r'google-pdf.download.cache',
        }
    },
    'Microsoft Word': {
        'filter': {
            'root_directory_path': r'D:/Yam Bakshi',
            'file_extensions': ['docx'],
            'cache_file': r'microsoft-word.filter.cache',
        }
    },
    'Microsoft Excel': {
        'filter': {
            'root_directory_path': r'D:/Yam Bakshi',
            'file_extensions': ['xlsx'],
            'cache_file': r'microsoft-excel.filter.cache',
        }
    },
    'Log': {
        'log_file': r'backup.log'
    }
}
