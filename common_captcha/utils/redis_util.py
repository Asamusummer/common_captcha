#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import annotations

import redis
import json


class RedisUtil:

    def __init__(self, redis_url: str = "redis://xxxxxx:xxxxxx@xxxxx:xxx/11") -> None:
        self.redis_url = redis_url

    @property
    def redis(self):
        if not self.redis_url:
            raise KeyError("Must set a redis connection URL in app config.")
        return redis.StrictRedis.from_url(self.redis_url)

    def setex(self, cache_key: str, cache_value: str, expire_time: int) -> None:
        if isinstance(cache_value, dict):
            cache_value = json.dumps(cache_value)

        self.redis.setex(cache_key, expire_time, cache_value)
        return None

    def set(self, cache_key: str, cache_value: str, expire_time: int) -> None:
        self.redis.set(cache_key, cache_value, expire_time)
        return None

    def get(self, cache_key: str) -> str | None:
        return self.redis.get(cache_key)

    def delete(self, cache_key) -> None:
        self.redis.delete(cache_key)
        return None
