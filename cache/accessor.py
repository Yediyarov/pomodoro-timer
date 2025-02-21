from redis import Redis, RedisError
from settings import settings


def get_redis_connection() -> Redis:
    try:
        return Redis(
            host=settings.CACHE_HOST,
            port=settings.CACHE_PORT,
            db=settings.CACHE_DB,
            socket_timeout=5,
            socket_connect_timeout=5
        )
    except RedisError as e:
        # Log the error or handle it as needed
        print(f"Error connecting to Redis: {e}")
        raise
