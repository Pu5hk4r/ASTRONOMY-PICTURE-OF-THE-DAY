"""
WHY a cache service?

NASA's free API key: 1,000 requests/day.
If 50 users visit your site and each triggers a NASA fetch, you burn 50 requests
for the same data. Caching stores the result the first time and serves it
instantly for subsequent requests — protecting your rate limit and speeding up responses.

The pattern used here is Cache-Aside (also called Lazy Loading):
  1. Check cache → hit? return immediately
  2. Miss? fetch from NASA → store in cache → return
  3. Cache expires after TTL → next request re-fetches fresh data

HOW Redis TTL works:
  When you SET a key with EX (expiry), Redis automatically deletes it after
  that many seconds. You never have to manually clean up stale data.
"""
 #also no dependencies on your DB layer. Just Redis.

import json
from typing import Any, Optional

import redis.asyncio as aioredis

from app.core.config import settings


class CacheService:
    def __init__(self):
        # WHY decode_responses=True?
        # Redis stores bytes. decode_responses converts them to str automatically
        # so you don't have to call .decode() everywhere.
        self.client = aioredis.from_url(
            settings.redis_url,
            decode_responses=True,
        )

    async def get(self, key: str) -> Optional[Any]:
        """Return cached value or None if missing/expired."""
        value = await self.client.get(key)
        if value is None:
            return None
        return json.loads(value)

    async def set(self, key: str, value: Any, ttl: int = settings.apod_cache_ttl) -> None:
        """
        Store value as JSON with a TTL (time-to-live) in seconds.
        After TTL seconds, Redis deletes the key automatically.
        """
        await self.client.set(key, json.dumps(value, default=str), ex=ttl)

    async def delete(self, key: str) -> None:
        """Manually invalidate a cache entry — useful when data is updated."""
        await self.client.delete(key)

    async def exists(self, key: str) -> bool:
        return bool(await self.client.exists(key))

    # --- Key builders ---
    # WHY methods for keys? String keys scattered across your codebase are
    # impossible to refactor. One typo and you have two keys for the same data.
    # Centralise key construction here.

    @staticmethod
    def apod_today_key() -> str:
        return "apod:today"

    @staticmethod
    def apod_date_key(date_str: str) -> str:
        return f"apod:date:{date_str}"

    @staticmethod
    def apod_search_key(keyword: str, page: int) -> str:
        return f"apod:search:{keyword}:page:{page}"

    async def close(self):
        await self.client.aclose()


# Singleton instance
cache = CacheService()
