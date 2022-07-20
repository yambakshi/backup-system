import io
import os
import logging
from pathlib import Path
from config.config import CONFIG


class FileIOService:
    def __init__(self, file_io_type: str):
        self.logger = logging.getLogger('backup_system')
        self.file_io_type = file_io_type
        self.files_directory = f"{file_io_type}s"
        if not os.path.exists(self.files_directory):
            Path(self.files_directory).mkdir(parents=True, exist_ok=True)

    def read(self, file_path: str):
        full_file_path = f"{self.files_directory}/{file_path}"
        try:
            with io.open(full_file_path, "r", encoding="utf8") as f:
                contents = f.read()
                return contents
        except FileNotFoundError as err:
            self.logger.error(f"Couldn't find file: '{full_file_path}'")
            return ''

    def save(self, files_paths: {}):
        for space, files_types in files_paths.items():
            for file_type, paths in files_types.items():
                lines = []
                for file_path, file_data in paths.items():
                    file_data_str = ''.join(
                        [f"|{val}" for val in file_data.values()])
                    lines.append(f"{file_path}{file_data_str}")

                file_io_path = CONFIG[space][file_type][f"{self.file_io_type}_file"]
                self.logger.debug(
                    f"Saving '{space}/{file_type}' {self.file_io_type} to {file_io_path}")
                with io.open(f"{self.files_directory}/{file_io_path}", "w", encoding="utf8") as f:
                    f.writelines(line + '\n' for line in lines)
