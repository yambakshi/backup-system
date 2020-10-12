import os
import sys
import logging
from pathlib import Path


def init_logger():
    if not os.path.exists('./logs'):
        Path(r'logs').mkdir(parents=True, exist_ok=True)

    # Set the root logger to minimum log level of ERROR
    # This way only log messages from severities ERROR and CRITICAL from imported modules will be logged
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                        level=logging.ERROR)

    # Init the backup_system logger
    logger = logging.getLogger('backup_system')

    # Set minimum log level to the lowest (DEBUG)
    logger.setLevel(logging.DEBUG)

    # File mode 'a' means append to existsing log file
    # File mode 'w' means clearing log file before writing to it
    file_handler = logging.FileHandler(
        'logs/backup_system.log', 'a', 'utf-8')
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s %(message)s'))

    logger.addHandler(file_handler)
    return logger
