from typing import Optional, List
from pydantic import BaseModel, Field

from vsuetrssfeed.models import News


class Feed(BaseModel):
    rss_version: Optional[str] = Field(default="2.0", description="Версия RSS")
    title: str = Field(description="Заголовок канала")
    link: str = Field(description="Ссылка на оригинальный ресурс")
    description: str = Field(description="Описание канала")
    language: str = Field(description="Язык канала")
    pubDate: str = Field(description="Последняя дата публикации")
    items: List[News] = Field(description="Список новостей")
