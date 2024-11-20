import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIRECTORY = "logs"
LOG_FILE = f"{LOG_DIRECTORY}/api_logs.log"

def setup_logger():
    os.makedirs(LOG_DIRECTORY, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = RotatingFileHandler(
        filename=LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5 MB per file
        backupCount=3,  # Keep only 3 files for example purpose
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info("Logger configured and ready to use.")
