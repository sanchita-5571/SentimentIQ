import json
from typing import Any

import redis.asyncio as redis

from core.config import settings


redis_client: redis.Redis | None = None


async def init_redis() -> redis.Redis | None:
    global redis_client
    try:
        redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
        await redis_client.ping()
        return redis_client
    except Exception:
        redis_client = None
        return None


async def cache_get(key: str) -> Any | None:
    if redis_client is None:
        return None
    payload = await redis_client.get(key)
    return json.loads(payload) if payload else None


async def cache_set(key: str, value: Any, ttl_seconds: int | None = None) -> None:
    if redis_client is None:
        return
    await redis_client.set(
        key,
        json.dumps(value, default=str),
        ex=ttl_seconds or settings.CACHE_TTL_SECONDS,
    )


async def cache_delete_pattern(prefix: str) -> None:
    if redis_client is None:
        return
    cursor = 0
    pattern = f"{prefix}*"
    while True:
        cursor, keys = await redis_client.scan(cursor=cursor, match=pattern, count=100)
        if keys:
            await redis_client.delete(*keys)
        if cursor == 0:
            break


async def close_redis() -> None:
    global redis_client
    if redis_client is not None:
        await redis_client.close()
    redis_client = None
