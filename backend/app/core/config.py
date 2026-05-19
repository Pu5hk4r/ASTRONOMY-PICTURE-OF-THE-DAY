'''
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
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    #NASA_API
     nasa_api_key: str

     #Database
     database_url: str 

     #Redis
     redis_url: str

     #Cache TTL (Seconds)
     #why 3600? APOD updates once in a day. Caching for 1 hour means
     #24 request/day max to NASA instead of one per user visit.

     apod_cache_ttl: int = 3600

     #APP
     app_title: str = "APOD Explorer"
     debug : bool = False

     model_config = SettingsConfigDict(
          env_files=".env",
          env_file_emcoding= "utf-8"
     )

# Singleton - import this everywhere,never instantiate Settings() again
settings= Settings()



