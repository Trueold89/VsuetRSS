from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import Field


class ApiSettings(BaseSettings):
    vsuetrss_api_docs: Optional[bool] = Field(
        default=False, description="Вкл/выкл документацию API"
    )
    vsuetrss_api_root: Optional[str] = Field(
        default="/", description="Основной эндпоинт API"
    )


class ScrapperSettings(BaseSettings):
    vsuetrss_scrapper_base: Optional[str] = Field(
        default="https://vsuet.ru", description="Базовый адрес ресурса Vsuet"
    )
    vsuetrss_scrapper_news_endpoint: Optional[str] = Field(
        default="/news", description="Эндпоинт раздела с новостями"
    )


class ChannelSettings(BaseSettings):
    vsuetrss_rss_title: Optional[str] = Field(
        default="Новости ВГУИТ", description="Название RSS-канала"
    )
    vsuetess_rss_link: Optional[str] = Field(
        default="https://vsuet.ru/news", description="Ссылка на изначальный ресурс"
    )
    vsuetess_rss_description: Optional[str] = Field(
        default="Обновляемая лента новостей ВГУИТ", description="Описание RSS-канала"
    )
    vsuetess_rss_language: Optional[str] = Field(
        default="ru", description="Язык RSS-канала"
    )


class RedisSettings(BaseSettings):
    vsuetrss_redis_url: str = Field(description="Ссылка подключения к Redis серверу")
    vsuetrss_redis_expire: Optional[int] = Field(
        default=60, description="Время истечения кэширования"
    )


api_settings = ApiSettings()
scrapper_settings = ScrapperSettings()
channel_settings = ChannelSettings()
redis_settings = RedisSettings()
version = "dev0"
