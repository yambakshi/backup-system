from re import M


GOOGLE_FILE_TYPES = [
    'Google Doc',
    'Google Sheet',
    'Google Slides'
]


CONFIG = {
    'local': {
        'Google Doc': {
            'extension': 'docx',
            'cache_file': r'local.google-docs.cache',
            'excluded_directories': [r'tmp', r'tmp_old']
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
        },
        # 'PNG': {
        #     'extension': 'png',
        #     'file_type': '',
        #     'cache_file': r'local.png.cache',
        # },
        # 'JPG': {
        #     'extension': 'jpg',
        #     'file_type': '',
        #     'cache_file': r'local.jpg.cache',
        # },
        # 'TXT': {
        #     'extension': 'txt',
        #     'file_type': '',
        #     'cache_file': r'local.txt.cache',
        # },
        # 'GP7': {
        #     'extension': 'gp7',
        #     'file_type': '',
        #     'cache_file': r'drive.gp7.cache',
        # },
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
        },
        # 'PNG': {
        #     'extension': 'png',
        #     'file_type': '',
        #     'cache_file': r'drive_stream.png.cache',
        # },
        # 'JPG': {
        #     'extension': 'jpg',
        #     'file_type': '',
        #     'cache_file': r'drive_stream.jpg.cache',
        # },
        # 'TXT': {
        #     'extension': 'txt',
        #     'file_type': '',
        #     'cache_file': r'drive_stream.txt.cache',
        # },
        # 'GP7': {
        #     'extension': 'gp7',
        #     'file_type': '',
        #     'cache_file': r'drive_stream.gp7.cache',
        # },
    },
    'drive': {
        'Google Doc': {
            'extension': 'gdoc',
            'file_type': 'application/vnd.google-apps.document',
            'download_as': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            # 'download_as': 'application/pdf',
            # 'extension': 'pdf',
            'cache_file': r'drive.google-docs.cache'
        },
        'Google Sheet': {
            'extension': 'gsheet',
            'file_type': 'application/vnd.google-apps.spreadsheet',
            'download_as': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            # 'download_as': 'application/pdf',
            # 'extension': 'pdf',
            'cache_file': r'drive.google-sheets.cache'
        },
        'PDF': {
            'extension': 'pdf',
            'file_type': 'application/pdf',
            'cache_file': r'drive.pdf.cache',
        },
        # 'PNG': {
        #     'extension': 'png',
        #     'file_type': '',
        #     'cache_file': r'drive.png.cache',
        # },
        # 'JPG': {
        #     'extension': 'jpg',
        #     'file_type': '',
        #     'cache_file': r'drive.jpg.cache',
        # },
        # 'TXT': {
        #     'extension': 'txt',
        #     'file_type': '',
        #     'cache_file': r'drive.txt.cache',
        # },
        # 'GP7': {
        #     'extension': 'gp7',
        #     'file_type': '',
        #     'cache_file': r'drive.gp7.cache',
        # },
    }
}
