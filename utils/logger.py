import logging
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)


def get_logger():

    logger = logging.getLogger("framework_logger")

    if not logger.handlers:

        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "[%(levelname)s] %(asctime)s | %(message)s",
            datefmt="%H:%M:%S"
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(
            os.path.join(LOGS_DIR, "test_run.log"),
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger