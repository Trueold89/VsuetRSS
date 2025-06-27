from redis.asyncio import Redis
from redis.exceptions import ConnectionError as RedisConError


class RedisCache(object):
    """
    Утилита управления взаимодействия с Redis
    """

    url: str
    _default_expire: int

    def __init__(self, url: str, default_expire_time: int = 60):
        """
        Утилита управления взаимодействия с Redis
        :param url: URL Redis сервера
        :param default_expire_time: Время истчения кэширования
        """
        self.url = url
        self._default_expire = default_expire_time

    @staticmethod
    def _redis(func):
        """
        Создаёт сессию для работы с Redis
        """

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
        """
        Сохраняет значение в Redis
        :param key: Ключ
        :param value: Значение
        :param redis: Сессия Redis
        :param expire: Время истечения
        """
        if expire is None:
            expire = self._default_expire
        await redis.set(key, value, ex=expire)

    @_redis
    async def get(self, key: str, redis: Redis) -> str:
        """
        Получает значение из Redis
        :param key: Ключ
        :param redis: Сессия Redis
        """
        return (await redis.get(key)).decode("utf-8")

    @_redis
    async def ping(self, redis: Redis) -> bool:
        """
        Проверяет подключение с сервером Redis
        :param redis: Сессия Redis
        """
        return await redis.ping()

    @_redis
    async def is_exist(self, key: str, redis: Redis) -> bool:
        """
        Проверяет наличие поля в Redis
        :param key: Ключ
        :param redis: Сессия Redis
        """
        return await redis.exists(key) > 0
