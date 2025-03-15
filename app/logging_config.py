import logging
import os
import traceback

LOGS_DIR = "logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

LOG_FILE = os.path.join(LOGS_DIR, "api.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),  # ✅ Ensure UTF-8 encoding
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("api_logger")


def log_exception(exc: Exception):
    error_message = "".join(traceback.format_exception(None, exc, exc.__traceback__))
    logger.error(f"EXCEPTION: {error_message}")
