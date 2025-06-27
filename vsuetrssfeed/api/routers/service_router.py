from fastapi import APIRouter
from vsuetrssfeed import version

service = APIRouter(prefix="/service", tags=["service"])


@service.get("/version")
async def server_version() -> str:
    """
    Возвращает версию сервера
    """
    return version
