import io
import os
from pathlib import Path
from datetime import datetime
from config.config import CONFIG


class CacheService:
    def __init__(self):
        if not os.path.exists('./cache'):
            Path(r'cache').mkdir(parents=True, exist_ok=True)

    def set_file(self, filename, use_cache=False):
        current_date = datetime.today().strftime('%Y-%m-%d')
        self.cache_file = f"cache/{current_date} - {filename}"
        if not use_cache:
            open(self.cache_file, 'w').close()

    def write(self, item: str):
        with io.open(self.cache_file, "a", encoding="utf-8") as f:
            f.write(f"{item}\n")

    def read(self):
        with io.open(self.cache_file, "r") as f:
            contents = f.read()
            return contents
