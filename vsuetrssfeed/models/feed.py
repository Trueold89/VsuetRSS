from typing import Optional, List
from pydantic import BaseModel

from vsuetrssfeed.models import News


class Feed(BaseModel):
    rss_version: Optional[str] = "2.0"
    title: str
    link: str
    description: str
    language: str
    pubDate: str
    items: List[News]
