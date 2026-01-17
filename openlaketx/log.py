import logging
import os
from logging import Logger
from typing import Optional


# Default log directory and file
LOG_DIR = "logs"
LOG_FILE = "openlaketx.log"


# Default log format
LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def _ensure_log_directory(path: str) -> None:
    """
    Ensure that the log directory exists.
    Logging should never fail if directory creation fails.
    """
    try:
        os.makedirs(path, exist_ok=True)
    except Exception:
        # Fail silently - logging must never crash the app
        pass

def get_logger(
        name: str,
        level: int = logging.INFO,
        log_to_file: bool = True
) -> Logger:
    """
    Returns a configured logger instance.

    Args:
        name (str): Logger name (usually __name__)
        level (int): Logging level
        log_to_file (bool): Enable file logging

    Returns:
        logging.Logger
    """

    logger = logging.getLogger(name)

    # Prevent reconfiguration if already set up
    if logger.handlers:
        return logger
    

    logger.setLevel(level)
    logger.propagate = False    # Prevent duplicate logs

    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


    # File Handler (optional)
    if log_to_file:
        _ensure_log_directory(LOG_DIR)
        log_path = os.path.join(LOG_DIR, LOG_FILE)

        try:
            file_handler = logging.FileHandler(log_path)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        except Exception:
            # Fail silently; console logging still works
            pass

    return logger