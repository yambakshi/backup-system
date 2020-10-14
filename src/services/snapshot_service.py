import io
import os
import logging
from pathlib import Path
from config.config import CONFIG


class SnapshotService:
    def __init__(self):
        self.logger = logging.getLogger('backup_system')
        if not os.path.exists('./snapshots'):
            Path(r'snapshots').mkdir(parents=True, exist_ok=True)

    def read(self, snapshot_file: str):
        with io.open(f"snapshots/{snapshot_file}", "r", encoding="utf8") as f:
            contents = f.read()
            return contents

    def save(self, files_paths: {}):
        self.logger.debug("Saving snapshots")
        for space, files_types in files_paths.items():
            for file_type, paths in files_types.items():
                lines = []
                for file_path, file_data in paths.items():
                    file_data_str = ''.join(
                        [f"|{val}" for val in file_data.values()])
                    lines.append(f"{file_path}{file_data_str}")

                snapshot_file = CONFIG[space][file_type]['snapshot_file']
                self.logger.debug(
                    f"Saving '{space}/{file_type}' snapshot to {snapshot_file}")
                with io.open(f"snapshots/{snapshot_file}", "w", encoding="utf8") as f:
                    f.writelines(line + '\n' for line in lines)

    def snapshot_exists(self, snapshot_file: str):
        return os.path.isfile(f"snapshots/{snapshot_file}")
