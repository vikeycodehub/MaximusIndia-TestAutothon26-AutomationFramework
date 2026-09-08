"""Centralized logging so every layer (pages, API client, tests) logs consistently."""
import logging
import sys
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parents[2] / "reports" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # already configured, avoid duplicate handlers

    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(_FORMAT))

    file_handler = logging.FileHandler(LOG_DIR / "run.log", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(_FORMAT))

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger
