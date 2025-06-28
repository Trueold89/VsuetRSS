from fastapi import APIRouter
from vsuetrssfeed import version
from vsuetrssfeed.services import AppService
from vsuetrssfeed.api.routers.feed_router import feed_service

service = APIRouter(prefix="/service", tags=["service"])


@service.get("/version")
async def server_version() -> str:
    """
    Возвращает версию сервера
    """
    return version


@service.get("/health")
async def health() -> str | int:
    """
    Проверка здоровья
    """
    redis, scrapper = feed_service.redis, feed_service.scrapper
    app = AppService(redis, scrapper)
    return await app.health
