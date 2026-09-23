"""
Shared logging setup for the pipeline.

Every acquisition run gets its own timestamped log file under logs/, in
addition to console output. The point is reproducibility: Methods needs
retrieval dates for every live web source pulled, and "when did I run this"
should never depend on memory or file mtimes.
"""

import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"


def get_logger(name: str) -> logging.Logger:
    """Return a logger that writes to both console and a run-scoped file.

    File is named <name>_<UTC timestamp>.log so each run is independently
    auditable and citable by retrieval date.
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    run_stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_path = LOG_DIR / f"{name}_{run_stamp}.log"

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.handlers:
        logger.handlers.clear()

    formatter = logging.Formatter(
        fmt="%(asctime)s.%(msecs)03dZ [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    formatter.converter = lambda *args: datetime.now(timezone.utc).timetuple()

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.info("Log file for this run: %s", log_path)
    return logger


def log_retrieval(logger: logging.Logger, source: str, url: str, note: str = "") -> None:
    """Standardized line for citing a data pull in the paper's Methods section.

    Emits a single grep-able RETRIEVED line with a UTC ISO-8601 timestamp,
    the source name, the URL, and an optional note (e.g. snapshot date used,
    row count, HTTP status).
    """
    retrieved_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    msg = f"RETRIEVED source={source} url={url} retrieved_at={retrieved_at}"
    if note:
        msg += f" note={note}"
    logger.info(msg)
