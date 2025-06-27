from vsuetrssfeed.utils import VsuetScrapper, gen_xml
from vsuetrssfeed.models import Feed
from vsuetrssfeed import channel_settings
from datetime import datetime


class FeedService(object):
    """
    Менеджер генератора фида
    """
    scrapper: VsuetScrapper

    def __init__(self, scrapper: VsuetScrapper) -> None:
        """
        Менеджер генератора фида
        :param scrapper: Парсер ресурса
        """
        self.scrapper = scrapper

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
