from fastapi import APIRouter, Response

from vsuetrssfeed import scrapper_settings, redis_settings
from vsuetrssfeed.services import FeedService
from vsuetrssfeed.utils import VsuetScrapper, RedisCache

feed_router = APIRouter(prefix="/feed", tags=["rss"])


def init_feed_service() -> FeedService:
    scrap = VsuetScrapper(scrapper_settings.vsuetrss_scrapper_base, scrapper_settings.vsuetrss_scrapper_news_endpoint)
    redis = RedisCache(redis_settings.vsuetrss_redis_url, redis_settings.vsuetrss_redis_expire)
    return FeedService(scrap, redis)


feed_service = init_feed_service()


@feed_router.get("")
async def feed(pages: int | None = None):
    return Response(content=await feed_service.get_feed(pages), media_type="application/xml")
