import logging
import os
from typing import Any

from config import LOG_FILE


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def setup_logger() -> None:
    ensure_dir(os.path.dirname(LOG_FILE) or ".")
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        encoding="utf-8",
        force=True,
    )


def log_info(message: Any) -> None:
    logging.info(message)


def log_error(message: Any) -> None:
    logging.error(message)


