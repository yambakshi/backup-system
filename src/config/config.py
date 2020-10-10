CONFIG = {
    'local': {
        'Google Doc': {
            'root_directory_path': r'G:/My Drive',
            'file_extensions': ['gdoc'],
            'cache_file': r'local.google-docs.cache',
            'excluded_directories': []
        },
        'Google Sheet': {
            'root_directory_path': r'G:/My Drive',
            'file_extensions': ['gsheet'],
            'cache_file': r'local.google-sheets.cache',
            'excluded_directories': []
        },
        'PDF': {
            'root_directory_path': r'G:/My Drive',
            'file_extensions': ['pdf'],
            'cache_file': r'local.pdf.cache',
            'excluded_directories': []
        },
        'Microsoft Word': {
            'root_directory_path': r'D:/Yam Bakshi',
            'file_extensions': ['docx'],
            'cache_file': r'local.microsoft-word.cache',
            'excluded_directories': [r'tmp']
        },
        'Microsoft Excel': {
            'root_directory_path': r'D:/Yam Bakshi',
            'file_extensions': ['xlsx'],
            'cache_file': r'local.microsoft-excel.cache',
            'excluded_directories': [r'tmp']
        }
    },
    'drive': {
        'Google Doc': {
            'file_type': 'application/vnd.google-apps.document',
            'download_as': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'save_as': 'docx',
            # 'download_as': 'application/pdf',
            # 'save_as': 'pdf',
            'cache_file': r'drive.google-docs.cache',
        },
        'Google Sheet': {
            'file_type': 'application/vnd.google-apps.spreadsheet',
            'download_as': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'save_as': 'xlsx',
            # 'download_as': 'application/pdf',
            # 'save_as': 'pdf',
            'cache_file': r'drive.google-sheets.cache',
        },
        'PDF': {
            'file_type': 'application/pdf',
            'download_as': 'application/pdf',
            'save_as': 'pdf',
            'cache_file': r'drive.pdf.cache',
        },
    }
}
