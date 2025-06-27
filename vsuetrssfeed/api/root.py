from fastapi import FastAPI
from vsuetrssfeed import api_settings


def init_api():
    sets = {
        "root_path": api_settings.vsuetrss_api_root,
        "docs_url": "/docs" if api_settings.vsuetrss_api_docs else None,
        "redoc_url": "/redoc" if api_settings.vsuetrss_api_docs else None
    }
    return FastAPI(**sets)


api = init_api()


@api.get("")
async def root():
    return "Server up and running"
