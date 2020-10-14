CONFIG = {
    'local': {
        'Google Doc': {
            'extension': 'docx',
            'snapshot_file': r'local.google-docs.snapshot',
            'cache_file': r'local.google-docs.cache',
            'excluded_directories': [r'tmp']
        },
        'Google Sheet': {
            'extension': 'xlsx',
            'snapshot_file': r'local.google-sheets.snapshot',
            'cache_file': r'local.google-sheets.cache',
            'excluded_directories': [r'tmp']
        },
        'PDF': {
            'extension': 'pdf',
            'snapshot_file': r'local.pdf.snapshot',
            'cache_file': r'local.pdf.cache',
            'excluded_directories': [r'tmp']
        }
    },
    'drive_stream': {
        'Google Doc': {
            'extension': 'gdoc',
            'snapshot_file': r'drive_stream.google-docs.snapshot',
            'cache_file': r'drive_stream.google-docs.cache',
            'excluded_directories': []
        },
        'Google Sheet': {
            'extension': 'gsheet',
            'snapshot_file': r'drive_stream.google-sheets.snapshot',
            'cache_file': r'drive_stream.google-sheets.cache',
            'excluded_directories': []
        },
        'PDF': {
            'extension': 'pdf',
            'snapshot_file': r'drive_stream.pdf.snapshot',
            'cache_file': r'drive_stream.pdf.cache',
            'excluded_directories': []
        }
    },
    'drive': {
        'Google Doc': {
            'extension': 'gdoc',
            'file_type': 'application/vnd.google-apps.document',
            'download_as': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            # 'download_as': 'application/pdf',
            # 'extension': 'pdf',
            'snapshot_file': r'drive.google-docs.snapshot',
            'cache_file': r'drive.google-docs.cache'
        },
        'Google Sheet': {
            'extension': 'gsheet',
            'file_type': 'application/vnd.google-apps.spreadsheet',
            'download_as': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            # 'download_as': 'application/pdf',
            # 'extension': 'pdf',
            'snapshot_file': r'drive.google-sheets.snapshot',
            'cache_file': r'drive.google-sheets.cache'
        },
        'PDF': {
            'extension': 'pdf',
            'file_type': 'application/pdf',
            'snapshot_file': r'drive.pdf.snapshot',
            'cache_file': r'drive.pdf.cache',
        },
    }
}
