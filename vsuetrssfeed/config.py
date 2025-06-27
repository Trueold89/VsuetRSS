from pydantic_settings import BaseSettings
from typing import Optional


class ApiSettings(BaseSettings):
    vsuetrss_api_docs: Optional[bool] = False
    vsuetrss_api_root: Optional[str] = "/"


class ScrapperSettings(BaseSettings):
    vsuetrss_scrapper_base: Optional[str] = "https://vsuet.ru"
    vsuetrss_scrapper_news_endpoint: Optional[str] = "/news"


api_settings = ApiSettings()
scrapper_settings = ScrapperSettings()
version = "dev0"
