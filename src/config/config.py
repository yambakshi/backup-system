CONFIG = {
    'local': {
        'Google Doc': {
            'extension': 'docx',
            'cache_file': r'local.google-docs.cache',
            'excluded_directories': [r'tmp']
        },
        'Google Sheet': {
            'extension': 'xlsx',
            'cache_file': r'local.google-sheets.cache',
            'excluded_directories': [r'tmp']
        },
        'PDF': {
            'extension': 'pdf',
            'cache_file': r'local.pdf.cache',
            'excluded_directories': [r'tmp']
        }
    },
    'drive_stream': {
        'Google Doc': {
            'extension': 'gdoc',
            'cache_file': r'drive_stream.google-docs.cache',
            'excluded_directories': []
        },
        'Google Sheet': {
            'extension': 'gsheet',
            'cache_file': r'drive_stream.google-sheets.cache',
            'excluded_directories': []
        },
        'PDF': {
            'extension': 'pdf',
            'cache_file': r'drive_stream.pdf.cache',
            'excluded_directories': []
        }
    },
    'drive': {
        'Google Doc': {
            'file_type': 'application/vnd.google-apps.document',
            'download_as': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'extension': 'docx',
            # 'download_as': 'application/pdf',
            # 'extension': 'pdf',
            'cache_file': r'drive.google-docs.cache',
        },
        'Google Sheet': {
            'file_type': 'application/vnd.google-apps.spreadsheet',
            'download_as': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'extension': 'xlsx',
            # 'download_as': 'application/pdf',
            # 'extension': 'pdf',
            'cache_file': r'drive.google-sheets.cache',
        },
        'PDF': {
            'file_type': 'application/pdf',
            'extension': 'pdf',
            'cache_file': r'drive.pdf.cache',
        },
    }
}
