import logging
import os
import traceback

LOGS_DIR = "logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

LOG_FILE = os.path.join(LOGS_DIR, "api.log")

# ✅ Dynamic Log Level (Can switch to DEBUG easily)
LOG_LEVEL = logging.DEBUG  # Change to logging.INFO for production

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),  # ✅ Force UTF-8 encoding
        logging.StreamHandler(),  # ✅ Show logs in terminal
    ],
)

logger = logging.getLogger("api_logger")


def log_exception(exc: Exception):
    """Logs detailed exception traceback."""
    error_message = "".join(traceback.format_exception(None, exc, exc.__traceback__))
    logger.error(f"Exception: {error_message}")


def log_request(request, response, duration):
    """Logs API request and response details with correct error handling."""

    # Extract the request body safely
    try:
        body = request.body.decode('utf-8') if hasattr(request, "body") and request.body else "No Body"
    except Exception:
        body = "Could not decode body"

    logger.info(
        f"REQUEST: {request.client.host} {request.method} {request.url.path} "
        f"| Body: {body}"
    )

    # ✅ Correctly log errors as ERROR
    if response.status_code >= 400:
        logger.error(
            f"RESPONSE: {request.client.host} {request.method} {request.url.path} "
            f"| Status: {response.status_code} | Time: {duration:.4f}s"
        )
    else:
        logger.info(
            f"RESPONSE: {request.client.host} {request.method} {request.url.path} "
            f"| Status: {response.status_code} | Time: {duration:.4f}s"
        )
