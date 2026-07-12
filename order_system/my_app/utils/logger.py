import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Log directory
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)

# Log file
log_file = log_dir / "app.log"

# Configure logger
logger = logging.getLogger("my_app")
logger.setLevel(logging.INFO)

# Rotating file handler (5 MB per file, keep 5 backups)
handler = RotatingFileHandler(
    log_file,
    maxBytes=5 * 1024 * 1024,
    backupCount=5
)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

handler.setFormatter(formatter)
logger.addHandler(handler)


def log_info(message: str):
    logger.info(message)


def log_warning(message: str):
    logger.warning(message)


def log_error(message: str):
    logger.error(message)
