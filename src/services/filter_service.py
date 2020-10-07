import os
import io
from datetime import datetime


class FilterService:
    def __init__(self):
        pass

    def filter_files_by_types(self, filter_config):
        current_date = datetime.today().strftime('%Y-%m-%d')
        filter_config['log_file'] = f"logs/filter/{current_date} - {filter_config['log_file']}"

        # Clear log file
        open(filter_config['log_file'], 'w').close()

        # Recursively iterate files and filter by types
        files_counter = self.iterate_files(filter_config)

        with io.open(filter_config['log_file'], "a", encoding="utf-8") as f:
            f.write(f"{files_counter} files found")

        print(f"{files_counter} files found")


    def iterate_files(self, filter_config, files_counter = 0):
        for filename in os.listdir(filter_config['root_directory_path']):
            file_path = f"{filter_config['root_directory_path']}/{filename}"
            if os.path.isdir(file_path):
                files_counter = self.iterate_files({**filter_config, 'root_directory_path': file_path}, files_counter)

            extension = os.path.splitext(filename)[1][1:]
            if extension in filter_config['file_extensions']:
                files_counter += 1
                with io.open(filter_config['log_file'], "a", encoding="utf-8") as f:
                    f.write(f"{file_path}\n")

        return files_counter
