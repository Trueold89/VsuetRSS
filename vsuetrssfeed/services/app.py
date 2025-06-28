from asyncio import gather

from vsuetrssfeed.utils import RedisCache, VsuetScrapper


class AppService(object):
    redis: RedisCache
    scrapper: VsuetScrapper

    def __init__(self, redis: RedisCache, scrapper: VsuetScrapper) -> None:
        self.redis = redis
        self.scrapper = scrapper

    @property
    async def health(self) -> int | str:
        try:
            tests = await gather(self.redis.ping(), self.scrapper.ping())
            if False in tests:
                raise RuntimeError("HealthCheck error")
            return 1
        except Exception as e:
            return f"Ошибка: {e}"
