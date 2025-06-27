from typing import List
from pydantic import BaseModel


class News(BaseModel):
    title: str
    link: str
    description: str
    pubdate: str
    guid: str
    categories: List[str]
