import redis
import json
from app.core.config import settings
from app.utils.logger import logger

# الاتصال بـ Redis
redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)

def get_cached_data(key: str):
    try:
        data = redis_client.get(key)
        return json.loads(data) if data else None
    except redis.exceptions.ConnectionError:
        logger.warning("Redis is not available, skipping cache read.")
        return None

def set_cached_data(key: str, value: dict, expire: int = 300):
    try:
        redis_client.setex(key, expire, json.dumps(value))
    except redis.exceptions.ConnectionError:
        logger.warning("Redis is not available, skipping cache write.")

def invalidate_cache(key_prefix: str):
    try:
        for key in redis_client.scan_iter(f"{key_prefix}*"):
            redis_client.delete(key)
    except redis.exceptions.ConnectionError:
        logger.warning("Redis is not available, skipping cache invalidation.")