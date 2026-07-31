#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：cached.py
@IDE     ：PyCharm 

@Date    ：2025/4/17 16:06 
'''
from loguru import logger
from redis.asyncio import Redis, ConnectionPool


class RedisClient:
    def __init__(
            self,
            redis_url,
            **kwargs
    ):
        self._pool = None
        self._redis = None
        self.redis_url = redis_url
        self.kwargs = kwargs

    async def init(self):
        """初始化连接池"""
        self._pool = ConnectionPool.from_url(
            f"{self.redis_url}",
            **self.kwargs
        )
        self._redis = Redis(connection_pool=self._pool)

    async def close(self):
        """关闭连接池"""
        if self._redis:
            await self._redis.close()
        if self._pool:
            await self._pool.aclose()

    async def execute(self, command: str, *args, **kwargs):

        return await self._redis.execute_command(command, *args, **kwargs)

    async def exists(self, key: str) -> bool:

        return await self._redis.exists(key)

    async def expire(self, key: str, seconds: int) -> bool:

        return await self._redis.expire(key, seconds)

    async def delete(self, *keys) -> int:

        return await self._redis.delete(*keys)

    # ----------- String 操作 -----------
    async def get(self, key: str) -> str:

        return await self._redis.get(key)

    async def set(self, key: str, value, ex: int = None) -> bool:

        return await self._redis.set(key, value, ex=ex)

    # ----------- Hash 操作 -----------
    async def hget(self, name: str, key: str) -> str:

        return await self._redis.hget(name, key)

    async def hset(self, name: str, key: str, value) -> int:

        return await self._redis.hset(name, key, value)

    async def hgetall(self, name: str) -> dict:

        return await self._redis.hgetall(name)

    async def incr(self, key: str) -> int:

        return await self._redis.incr(key)

    async def lpush(self, name: str, *values) -> int:

        return await self._redis.lpush(name, *values)

    async def rpop(self, name: str) -> str:

        return await self._redis.rpop(name)

    async def randomkey(self) -> str:

        return await self._redis.randomkey()

    async def ping(self) -> bool:

        try:
            return await self._redis.ping()
        except (ConnectionError, AttributeError):
            return False

    async def type(self, key: str) -> str:

        return await self._redis.type(key)

    async def check_connection(self) -> bool:

        if not self._redis:
            return False

        try:
            return await self._redis.ping()
        except (ConnectionError, TimeoutError):
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return False
