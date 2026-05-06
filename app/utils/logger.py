import sys
from loguru import logger

# إعداد الـ Logger ليطبع في الكونسول وفي ملف خارجي
logger.remove()
logger.add(sys.stdout, format="{time} | {level} | {message}", level="INFO")
logger.add("app_log.log", rotation="10 MB", level="DEBUG", compression="zip")

def log_api_event(method: str, endpoint: str, status_code: int, user: str = "Anonymous"):
    logger.info(f"User: {user} | Method: {method} | Endpoint: {endpoint} | Status: {status_code}")