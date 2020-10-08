import io, os
from pathlib import Path
from datetime import datetime
from config.config import CONFIG


class LogService:
    def __init__(self):
        if not os.path.exists('./logs'):
            Path(r'logs').mkdir(parents=True, exist_ok=True)

        current_date = datetime.today().strftime('%Y-%m-%d')
        self.log_file = f"logs/{current_date} - {CONFIG['Log']['log_file']}"
        self.clear_log()
        

    def clear_log(self):
        open(self.log_file, 'w').close()


    def log(self, message: str):
        print(message)
        with io.open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"{message}\n")
