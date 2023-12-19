#!/usr/bin/env python
# -*- coding:utf-8 -*-
import redis
import json
from typing import Union


class RedisHelperUtil:

    def __init__(
            self, redis_host: str = 'localhost', redis_username: str = None,
            redis_password: str = None,
            redis_port: int = 6379, redis_db: int = 0
    ) -> None:
        self.redis = redis.StrictRedis(
            host=redis_host,
            port=redis_port,
            username=redis_username,
            password=redis_password,
            db=redis_db,
        )

    def setex(self, cache_key: str, cache_value: str, expire_time: int) -> None:
        if isinstance(cache_value, dict):
            cache_value = json.dumps(cache_value)

        self.redis.setex(cache_key, expire_time, cache_value)
        return None

    def set(self, cache_key: str, cache_value: str, expire_time: int) -> None:
        self.redis.set(cache_key, cache_value, expire_time)
        return None

    def get(self, cache_key: str) -> Union[str, None]:
        return self.redis.get(cache_key)

    def delete(self, cache_keys) -> None:
        self.redis.delete(cache_keys if isinstance(cache_keys, list) else [cache_keys])
        return None


def init_redis(redis_client=None, redis_host='139.196.199.182',
               redis_port=6379, redis_username=None, redis_password=None, redis_db=0):
    if not redis_client:
        redis_client = RedisHelperUtil(
            redis_host=redis_host,
            redis_port=redis_port,
            redis_username=redis_username,
            redis_password=redis_password,
            redis_db=redis_db,
        )
    return redis_client


if __name__ == '__main__':
    r = RedisHelperUtil(
        redis_host='139.196.199.182',
    )
    r.redis.set('wl', 23)
    print(r.redis.keys())
    print(r.redis.get('SimpleCaptcha:4ef8c24331af458690194ac9b15021e8'))
