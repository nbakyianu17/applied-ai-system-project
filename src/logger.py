import logging
import os
from typing import List, Tuple, Dict

_LOG_DIR = "logs"
_LOG_FILE = os.path.join(_LOG_DIR, "session.log")


def get_logger() -> logging.Logger:
    os.makedirs(_LOG_DIR, exist_ok=True)
    logger = logging.getLogger("vibefinder")
    if logger.handlers:
        return logger
    handler = logging.FileHandler(_LOG_FILE, encoding="utf-8")
    handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(message)s",
                          datefmt="%Y-%m-%d %H:%M:%S")
    )
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def log_session(
    label: str,
    prefs: Dict,
    results: List[Tuple[Dict, float, str]],
) -> None:
    log = get_logger()
    genre = prefs.get("genre", "?")
    mood = prefs.get("mood", "?")
    log.info("RUN | profile=%r | genre=%s | mood=%s", label, genre, mood)
    for rank, (song, score, _) in enumerate(results, 1):
        log.info(
            "  #%d | %s — %s | score=%.2f | genre=%s | mood=%s",
            rank, song["title"], song["artist"], score, song["genre"], song["mood"],
        )


def log_error(context: str, exc: Exception) -> None:
    get_logger().error("ERROR | context=%r | %s: %s", context, type(exc).__name__, exc)
