CONFIG = {
    'local': {
        'root_directory_path': r'D:/Yam Bakshi',
        'file_types': {
            'Microsoft Word': {
                'file_extensions': ['docx'],
                'cache_file': r'local.microsoft-word.cache',
                'excluded_directories': [r'tmp']
            },
            'Microsoft Excel': {
                'file_extensions': ['xlsx'],
                'cache_file': r'local.microsoft-excel.cache',
                'excluded_directories': [r'tmp']
            },
            'PDF': {
                'file_extensions': ['pdf'],
                'cache_file': r'local.pdf.cache',
                'excluded_directories': [r'tmp']
            }
        }
    },
    'drive_stream': {
        'root_directory_path': r'G:/My Drive',
        'file_types': {
            'Google Doc': {
                'file_extensions': ['gdoc'],
                'cache_file': r'drive_stream.google-docs.cache',
                'excluded_directories': []
            },
            'Google Sheet': {
                'file_extensions': ['gsheet'],
                'cache_file': r'drive_stream.google-sheets.cache',
                'excluded_directories': []
            },
            'PDF': {
                'file_extensions': ['pdf'],
                'cache_file': r'drive_stream.pdf.cache',
                'excluded_directories': []
            }
        }
    },
    'downloads': {
        'Google Doc': {
            'file_type': 'application/vnd.google-apps.document',
            'download_as': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'save_as': 'docx',
            # 'download_as': 'application/pdf',
            # 'save_as': 'pdf',
            'cache_file': r'downloads.google-docs.cache',
        },
        'Google Sheet': {
            'file_type': 'application/vnd.google-apps.spreadsheet',
            'download_as': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'save_as': 'xlsx',
            # 'download_as': 'application/pdf',
            # 'save_as': 'pdf',
            'cache_file': r'downloads.google-sheets.cache',
        },
        'PDF': {
            'file_type': 'application/pdf',
            'download_as': 'application/pdf',
            'cache_file': r'downloads.pdf.cache',
        },
    }
}
