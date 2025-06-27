from redis.asyncio import Redis
from redis.exceptions import ConnectionError as RedisConError


class RedisCache(object):
    url: str
    _default_expire: int

    def __init__(self, url: str, default_expire_time: int = 60):
        self.url = url
        self._default_expire = default_expire_time

    @staticmethod
    def _redis(func):
        async def wrapper(self, *args, **kwargs):
            try:
                async with Redis.from_url(self.url) as redis:
                    return await func(self, *args, **kwargs, redis=redis)
            except RedisConError:
                raise ConnectionError("Нет связи с Redis")

        return wrapper

    @_redis
    async def save(
        self, key: str, value: str, redis: Redis, expire: int | None = None
    ) -> None:
        if expire is None:
            expire = self._default_expire
        await redis.set(key, value, ex=expire)

    @_redis
    async def get(self, key: str, redis: Redis) -> str:
        return (await redis.get(key)).decode("utf-8")

    @_redis
    async def ping(self, redis: Redis) -> bool:
        return await redis.ping()

    @_redis
    async def is_exist(self, key: str, redis: Redis) -> bool:
        return await redis.exists(key) > 0


