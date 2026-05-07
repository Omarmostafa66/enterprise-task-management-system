import sys
import os
from loguru import logger

# Configure Logger to output to both console and an external file
logger.remove()
logger.add(sys.stdout, format="{time} | {level} | {message}", level="INFO")
logger.add("app_log.log", rotation="10 MB", level="DEBUG", compression="zip")


def log_api_event(method: str, endpoint: str, status_code: int, user: str = "Anonymous"):
    """
    Standardized API event logging.
    Records system activity into the application log file.
    """
    logger.info(f"User: {user} | Method: {method} | Endpoint: {endpoint} | Status: {status_code}")


def get_recent_logs(lines: int = 50):
    """
    Read recent lines from the log file for the Admin Audit Dashboard.
    Returns a list of parsed log string entries.
    """
    log_file_path = "app_log.log"

    if not os.path.exists(log_file_path):
        return ["No system activity recorded yet."]

    try:
        with open(log_file_path, "r", encoding="utf-8") as f:
            all_lines = f.readlines()
            # Retrieve only the most recent N lines to avoid heavy payloads
            return all_lines[-lines:]
    except Exception as e:
        return [f"Error reading logs: {str(e)}"]