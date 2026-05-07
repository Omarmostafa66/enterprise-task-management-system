import redis
import json
from app.core.config import settings
from app.utils.logger import logger


# Establish connection to the Redis server
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True
)


def get_cached_data(key: str):
    """
    Retrieve data from the Redis cache based on the provided key.
    Returns None if the key does not exist or if Redis is unavailable.
    """
    try:
        data = redis_client.get(key)
        return json.loads(data) if data else None
    except redis.exceptions.ConnectionError:
        logger.warning("Redis is not available, skipping cache read.")
        return None


def set_cached_data(key: str, value: dict, expire: int = 300):
    """
    Store data in the Redis cache with an expiration time (default: 300 seconds).
    """
    try:
        redis_client.setex(key, expire, json.dumps(value))
    except redis.exceptions.ConnectionError:
        logger.warning("Redis is not available, skipping cache write.")


def invalidate_cache(key_prefix: str):
    """
    Remove all cached entries that match a specific key prefix.
    Used to keep data consistent after mutations.
    """
    try:
        for key in redis_client.scan_iter(f"{key_prefix}*"):
            redis_client.delete(key)
    except redis.exceptions.ConnectionError:
        logger.warning("Redis is not available, skipping cache invalidation.")