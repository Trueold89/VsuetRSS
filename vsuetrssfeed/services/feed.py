from vsuetrssfeed.utils import VsuetScrapper, gen_xml, RedisCache
from vsuetrssfeed.models import Feed
from vsuetrssfeed import channel_settings
from datetime import datetime


class FeedService(object):
    """
    Менеджер генератора фида
    """
    scrapper: VsuetScrapper
    redis: RedisCache

    @staticmethod
    def redis_cache(func):
        async def wrapper(self, *args, **kwargs):
            key = func.__name__
            if await self.redis.is_exist(key):
                return await self.redis.get(key)
            value = await func(self, *args, **kwargs)
            await self.redis.save(key, value)
            return value

        return wrapper

    def __init__(self, scrapper: VsuetScrapper, redis: RedisCache) -> None:
        """
        Менеджер генератора фида
        :param scrapper: Парсер ресурса
        """
        self.scrapper = scrapper
        self.redis = redis

    @redis_cache
    async def get_feed(self, pages: int | None = None) -> str:
        """
        Получает ленту новостей в rss формате
        :param pages: Кол-во страниц
        :return: RSS-фид
        """
        feed_settings = {
            "title": channel_settings.vsuetrss_rss_title,
            "link": channel_settings.vsuetess_rss_link,
            "description": channel_settings.vsuetess_rss_description,
            "language": channel_settings.vsuetess_rss_language,
            "pubDate": datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT'),
            "items": await self.scrapper.get_feed(pages)
        }
        feed = Feed(**feed_settings)
        return gen_xml(feed)
