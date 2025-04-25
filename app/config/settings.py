"""
Author: sg.kim
Date: 2025-04-24
Description:
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    youtube_api_base_url: str
    youtube_api_key: str

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="YOUTUBE_",
        env_file=".env",
        extra="ignore",
    )

class DatabaseSettings(BaseSettings):

    DBAPI: str = "postgresql+asyncpg"

    database_url: str
    postgres_db: str
    postgres_user: str
    postgres_password: str

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        extra="ignore",
    )

    def get_connect_url(self):
        return f"{self.DBAPI}://{self.postgres_user}:{self.postgres_password}@{self.database_url}/{self.postgres_db}"