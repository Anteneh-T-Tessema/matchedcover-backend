""""
Redis client configuration for MatchedCover.

This module handles Redis connections for caching, sessions,
and message queuing.
""""

import json
import logging
from typing import Any, Optional, Union

import redis.asyncio as redis
from redis.asyncio import Redis

from src.core.config import settings

logger = logging.getLogger(__name__)

# Global Redis client instance
redis_client: Optional[Redis] = None


async def init_redis() -> None:
    """Initialize Redis connection."""
global redis_client

    try:
        redis_client = redis.from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
        socket_connect_timeout=5,
        socket_timeout=5,
        retry_on_timeout=True,
        health_check_interval=30,
    )

        # Test connection
    await redis_client.ping()
    logger.info("Redis connection established successfully")

    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
    raise


async def get_redis() -> Redis:
    """Get Redis client instance."""
if redis_client is None:
        await init_redis()
return redis_client


async def close_redis() -> None:
    """Close Redis connection."""
if redis_client:
        await redis_client.close()


class RedisService:
    """Redis service for common operations."""

    def __init__(self, client: Optional[Redis] = None):
        self.client = client or redis_client

    async def set(
        self,
    key: str,
    value: Union[str, dict, list],
    expire: Optional[int] = None,
) -> bool:
        """Set a key-value pair in Redis."""
    try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)

            result = await self.client.set(key, value, ex=expire)
        return bool(result)
    except Exception as e:
            logger.error(f"Redis SET error for key {key}: {e}")
        return False

    async def get(self, key: str) -> Optional[Any]:
        """Get a value from Redis."""
    try:
            value = await self.client.get(key)
        if value is None:
                return None

            # Try to parse as JSON
        try:
                return json.loads(value)
        except json.JSONDecodeError:
                return value

        except Exception as e:
            logger.error(f"Redis GET error for key {key}: {e}")
        return None

    async def delete(self, key: str) -> bool:
        """Delete a key from Redis."""
    try:
            result = await self.client.delete(key)
        return bool(result)
    except Exception as e:
            logger.error(f"Redis DELETE error for key {key}: {e}")
        return False

    async def exists(self, key: str) -> bool:
        """Check if a key exists in Redis."""
    try:
            result = await self.client.exists(key)
        return bool(result)
    except Exception as e:
            logger.error(f"Redis EXISTS error for key {key}: {e}")
        return False

    async def expire(self, key: str, seconds: int) -> bool:
        """Set expiration for a key."""
    try:
            result = await self.client.expire(key, seconds)
        return bool(result)
    except Exception as e:
            logger.error(f"Redis EXPIRE error for key {key}: {e}")
        return False

    async def increment(self, key: str, amount: int = 1) -> Optional[int]:
        """Increment a counter."""
    try:
            result = await self.client.incrby(key, amount)
        return result
    except Exception as e:
            logger.error(f"Redis INCR error for key {key}: {e}")
        return None

    async def push_to_list(self, key: str, value: Any) -> bool:
        """Push value to a list."""
    try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)

            await self.client.lpush(key, value)
        return True
    except Exception as e:
            logger.error(f"Redis LPUSH error for key {key}: {e}")
        return False

    async def pop_from_list(self, key: str, timeout: int = 0) -> Optional[Any]:
        """Pop value from a list."""
    try:
            if timeout > 0:
                result = await self.client.brpop(key, timeout=timeout)
            if result:
                    _, value = result
            else:
                    return None
        else:
                value = await self.client.rpop(key)

            if value is None:
                return None

            # Try to parse as JSON
        try:
                return json.loads(value)
        except json.JSONDecodeError:
                return value

        except Exception as e:
            logger.error(f"Redis POP error for key {key}: {e}")
        return None

    async def add_to_set(self, key: str, value: Any) -> bool:
        """Add value to a set."""
    try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)

            await self.client.sadd(key, value)
        return True
    except Exception as e:
            logger.error(f"Redis SADD error for key {key}: {e}")
        return False

    async def is_member_of_set(self, key: str, value: Any) -> bool:
        """Check if value is member of set."""
    try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)

            result = await self.client.sismember(key, value)
        return bool(result)
    except Exception as e:
            logger.error(f"Redis SISMEMBER error for key {key}: {e}")
        return False
