from pydantic_settings import BaseSettings
from typing import Optional


class ApiSettings(BaseSettings):
    vsuetrss_api_docs: Optional[bool] = False
    vsuetrss_api_root: Optional[str] = "/"


api_settings = ApiSettings()
version = "dev0"
