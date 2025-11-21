import logging
from .config import LOG_FILE

logger = logging.getLogger("personal_finance")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

# file handler
fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)
