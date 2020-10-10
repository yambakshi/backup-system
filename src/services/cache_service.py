import io
import os
import logging
from pathlib import Path


class CacheService:
    def __init__(self):
        if not os.path.exists('./cache'):
            Path(r'cache').mkdir(parents=True, exist_ok=True)

    def write(self, cache_file: str, item: str):
        with io.open(f"cache/{cache_file}", "a", encoding="utf-8") as f:
            f.write(f"{item}\n")

    def read(self, cache_file: str):
        with io.open(f"cache/{cache_file}", "r") as f:
            contents = f.read()
            return contents
