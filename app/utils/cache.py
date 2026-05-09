import redis
import json

from app.core.config import settings
from app.utils.logger import logger


# Establish connection to the Redis server
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5
)


# Verify Redis connection during application startup
try:
    redis_client.ping()
    logger.info("Redis connection established successfully.")
except redis.exceptions.ConnectionError:
    logger.warning("Redis server is unavailable during startup.")


def get_cached_data(key: str):
    """
    Retrieve data from the Redis cache based on the provided key.
    Returns None if the key does not exist or if Redis is unavailable.
    """

    try:
        data = redis_client.get(key)

        if data:
            logger.info(f"Cache HIT: {key}")
            return json.loads(data)

        logger.info(f"Cache MISS: {key}")
        return None

    except redis.exceptions.ConnectionError:
        logger.warning("Redis is not available, skipping cache read.")
        return None

    except Exception as e:
        logger.error(f"Unexpected Redis read error: {str(e)}")
        return None


def set_cached_data(key: str, value: dict, expire: int = 300):
    """
    Store data in the Redis cache with an expiration time.
    Default expiration time: 300 seconds.
    """

    try:
        redis_client.setex(key, expire, json.dumps(value))

        logger.info(f"Cache SET: {key} (expires in {expire}s)")

    except redis.exceptions.ConnectionError:
        logger.warning("Redis is not available, skipping cache write.")

    except Exception as e:
        logger.error(f"Unexpected Redis write error: {str(e)}")


def invalidate_cache(key_prefix: str):
    """
    Remove all cached entries that match a specific key prefix.
    Used to keep data consistent after mutations.
    """

    try:
        deleted_count = 0

        for key in redis_client.scan_iter(f"{key_prefix}*"):
            redis_client.delete(key)
            deleted_count += 1

        logger.info(
            f"Cache invalidation completed for prefix '{key_prefix}' "
            f"({deleted_count} keys removed)"
        )

    except redis.exceptions.ConnectionError:
        logger.warning("Redis is not available, skipping cache invalidation.")

    except Exception as e:
        logger.error(f"Unexpected Redis invalidation error: {str(e)}")