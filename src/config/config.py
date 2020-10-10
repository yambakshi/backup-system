CONFIG = {
    'Google Docs': {
        'local': {
            'root_directory_path': r'G:/My Drive',
            'file_extensions': ['gdoc'],
            'cache_file': r'google-docs.local.cache',
        },
        'drive': {
            'file_type': 'application/vnd.google-apps.document',
            'download_as': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'save_as': 'docx',
            # 'download_as': 'application/pdf',
            # 'save_as': 'pdf',
            'cache_file': r'google-docs.drive.cache',
        }
    },
    'Google Sheets': {
        'local': {
            'root_directory_path': r'G:/My Drive',
            'file_extensions': ['gsheet'],
            'cache_file': r'google-sheets.local.cache',
        },
        'drive': {
            'file_type': 'application/vnd.google-apps.spreadsheet',
            'download_as': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'save_as': 'xlsx',
            # 'download_as': 'application/pdf',
            # 'save_as': 'pdf',
            'cache_file': r'google-sheets.drive.cache',
        }
    },
    'Google PDFs': {
        'local': {
            'root_directory_path': r'G:/My Drive',
            'file_extensions': ['pdf'],
            'cache_file': r'google-pdf.local.cache',
        },
        'drive': {
            'file_type': 'application/pdf',
            'download_as': 'application/pdf',
            'save_as': 'pdf',
            'cache_file': r'google-pdf.drive.cache',
        }
    },
    'Microsoft Word': {
        'local': {
            'root_directory_path': r'D:/Yam Bakshi',
            'file_extensions': ['docx'],
            'cache_file': r'microsoft-word.local.cache',
        }
    },
    'Microsoft Excel': {
        'local': {
            'root_directory_path': r'D:/Yam Bakshi',
            'file_extensions': ['xlsx'],
            'cache_file': r'microsoft-excel.local.cache',
        }
    }
}
