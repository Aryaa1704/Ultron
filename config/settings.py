from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "JARVIS-OS"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    secret_key: str
    database_url: str
    redis_url: str = "redis://localhost:6379/0"
    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-3-5-sonnet-latest"
    chroma_persist_directory: str = "./chroma_data"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
