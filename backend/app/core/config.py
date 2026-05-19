'''

Why before DB? Every layer below needs secrets — DB password, NASA key, Redis URL. 
Config must exist before anything that uses it. You'll import settings everywhere.
Why pydantic-setting?
your app needs secretes (API KEYS ,DB PASSWORDS) and config (port numbers, cache TTLs).
hardcoding them is dangerous (they leak into git) and inflexible (different values in dev vs prod)

pydantic-settings read from .env file, validates each values's type, and gives you a typed python object
If NASA_API_KEY is missing, it crashes
at startup- not silently at 3am when cron job runs.

HOW IT WORK:
 1.you define a class with field names + types
 2.pydantic-settings reads matching keys from .env
 3.you get a typed, validated settings objects anywhere in your app
 
'''
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # NASA API
    nasa_api_key: str

    # Database
    database_url: str

    # Redis
    redis_url: str

    # Cache TTL (seconds)
    apod_cache_ttl: int = 3600

    # App
    app_title: str = "APOD Explorer"
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent / ".env",
        env_file_encoding="utf-8"
    )

settings = Settings()