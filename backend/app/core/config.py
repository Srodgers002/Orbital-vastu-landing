from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'Global AI Intelligence Portal API'
    environment: str = 'development'

    database_url: str = Field(default='postgresql+psycopg://postgres:postgres@db:5432/ai_portal')
    redis_url: str = Field(default='redis://redis:6379/0')
    chroma_persist_dir: str = Field(default='/data/chroma')

    openai_api_key: str = Field(default='')
    openai_model: str = Field(default='gpt-4o-mini')
    embedding_model: str = Field(default='text-embedding-3-small')

    newsapi_key: str = ''
    newsdata_key: str = ''
    gnews_key: str = ''

    fetch_interval_minutes: int = 15
    embedding_rebuild_cron: str = '0 3 * * *'


@lru_cache
def get_settings() -> Settings:
    return Settings()
