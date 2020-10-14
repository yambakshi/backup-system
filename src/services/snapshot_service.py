import io
import os
import logging
import shutil
from pathlib import Path


class SnapshotService:
    def __init__(self):
        self.logger = logging.getLogger('backup_system')
        if not os.path.exists('./snapshots'):
            Path(r'snapshots').mkdir(parents=True, exist_ok=True)

    def clear_snapshot(self, snapshot_file):
        if os.path.isfile(f"snapshots/{snapshot_file}"):
            self.logger.debug(f"Clearing snapshot: '{snapshot_file}'")
            open(snapshot_file, 'w').close()

    def delete_snapshots_folder(self):
        if not os.path.exists('./snapshots'):
            shutil.rmtree(r'snapshots')

    def write(self, snapshot_file: str, item: str):
        with io.open(f"snapshots/{snapshot_file}", "a", encoding="utf-8") as f:
            f.write(f"{item}\n")

    def read(self, snapshot_file: str):
        with io.open(f"snapshots/{snapshot_file}", "r", encoding="utf8") as f:
            contents = f.read()
            return contents

    def update(self, update: []):
        for snapshot in update:
            snapshot_file = snapshot['snapshot_file']
            lines = self.read(snapshot_file).split('\n')[:-1]
            for line in snapshot['remove_lines']:
                lines.remove(line)

            lines += [line.replace('\\', '/') for line in snapshot['add_lines']]
            with io.open(f"snapshots/{snapshot_file}", "w", encoding="utf8") as f:
                f.writelines(line + '\n' for line in lines)

    def snapshot_exists(self, snapshot_file: str):
        return os.path.isfile(f"snapshots/{snapshot_file}")
