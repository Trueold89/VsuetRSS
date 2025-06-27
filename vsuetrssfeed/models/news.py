from typing import List
from pydantic import BaseModel, Field


class News(BaseModel):
    title: str = Field(description="Заголовок новости")
    link: str = Field(description="Ссылка на статью")
    description: str = Field(description="Краткая сводка новости")
    pubdate: str = Field(description="Дата публикации")
    guid: str = Field(description="Идентификатор новости")
    categories: List[str] = Field(description="Список категорий")
