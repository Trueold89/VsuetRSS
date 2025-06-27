from pydantic_settings import BaseSettings
from typing import Optional


class ApiSettings(BaseSettings):
    vsuetrss_api_docs: Optional[bool] = False
    vsuetrss_api_root: Optional[str] = "/"


class ScrapperSettings(BaseSettings):
    vsuetrss_scrapper_base: Optional[str] = "https://vsuet.ru"
    vsuetrss_scrapper_news_endpoint: Optional[str] = "/news"


class ChannelSettings(BaseSettings):
    vsuetrss_rss_title: Optional[str] = "vsuet.ru"
    vsuetess_rss_link: Optional[str] = "https://vsuet.ru/news"
    vsuetess_rss_description: Optional[str] = "Обновляемая лента новостей ВГУИТ"
    vsuetess_rss_language: Optional[str] = "ru"


class RedisSettings(BaseSettings):
    vsuetrss_redis_url: str
    vsuetrss_redis_expire: Optional[int] = 60


api_settings = ApiSettings()
scrapper_settings = ScrapperSettings()
channel_settings = ChannelSettings()
redis_settings = RedisSettings()
version = "dev0"
