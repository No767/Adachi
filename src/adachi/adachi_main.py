from typing import Optional

import redis.asyncio as redis

from adachi import defaultKeyBuilder


class Adachi:
    def __init__(self, url):
        self.self = self
        self.url = url

    async def setCache(
        self,
        key: Optional[str] = defaultKeyBuilder(
            prefix="adachi", namespace="cache", user_id=None
        ),
        value: Optional[str] = None,
        ttl: Optional[int] = 30,
    ) -> None:
        """Sets the cache on Redis

        Args:
            key (Optional[str], optional): Key to set on Redis. Defaults to `defaultKeyBuilder(prefix="adachi", namespace="cache", user_id=None)`.
            value (Optional[str], optional): Value to set on Redis. Defaults to None.
            ttl (Optional[int], optional): TTL for the key-value pair. Defaults to 30.
        """
        conn = redis.from_url(self.url, decode_responses=True)
        await conn.set(key, value, ttl)
        await conn.close()

    async def getUserCacheKey(self, pattern: str) -> list:
        """Gets the user's cache on Redis

        This uses Redis's `SCAN` command, and iterates through the keys to find the user's cache.

        Args:
            pattern (str): Pattern to search for user's cache.

        Returns:
            list: A `list` of `str` containing the user's cache key.
        """
        conn = redis.from_url(self.url, decode_responses=True)
        returnKey = conn.scan_iter(match=pattern, _type="STRING")
        await conn.close()
        return [items async for items in returnKey]

    async def getUserCache(self, key: str) -> list:
        conn = redis.from_url(self.url, decode_responses=True)
        returnKey = await conn.get(key)
        await conn.close()
        return returnKey
