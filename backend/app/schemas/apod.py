"""
WHY schemas separate from models?

This is one of the most important patterns to understand.

Your SQLAlchemy MODEL defines what's in the DATABASE.
Your Pydantic SCHEMA defines what goes in/out of your API.

They are intentionally separate because:
  1. You never want to expose raw DB rows to the outside world
     (internal IDs, sensitive fields, related objects you didn't load)
  2. Request payloads don't always match your DB shape
  3. You might return computed fields that aren't in the DB at all

HOW FastAPI uses schemas:
  - Input schemas (like ApodSearchParams) validate and parse incoming query params
  - Output schemas (like ApodResponse) control exactly what JSON the client receives
  - FastAPI auto-generates OpenAPI docs from these schemas — visit /docs to see it
"""
from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, HttpUrl


class ApodResponse(BaseModel):
    """
    What the API returns for a single APOD entry.
    Notice: no `id` field — clients don't need our internal DB id.
    """
    date : date
    title : str
    explanation : str
    url : str
    hdurl : Optional[str] = None
    media_type : str
    copyright : Optional[str] = None

    # WHY model_config with from_attributes?
    # By default Pydantic expects a dict. SQLAlchemy returns objects.
    # from_attributes=True tells Pydantic to read object attributes
    # so you can do: ApodResponse.model_validate(db_apod_object)

    model_config = ConfigDict(from_attributes = True)

class ApodListResponse(BaseModel):
    ''' Paginated list of APODS'''
    items: list[ApodResponse]
    total : int
    page : int
    page_size : int
    has_next : bool


class ApodSearchParams(BaseModel):
    """
    Query parameters for search endpoint.
    FastAPI reads these from the URL: /api/apod/search?keyword=galaxy&page=2
    """
    keyword : Optional[str] = None
    start_date : Optional[date] = None
    end_date : Optional[date] = None
    media_type : Optional[str] = None
    page : int = 1
    page_size : int = 20

class NasaApodRaw(BaseModel):
     """
    Matches the exact shape NASA returns.
    WHY? When you fetch from NASA, validate their response against this.
    If NASA changes their API, your app fails loudly here instead of
    silently storing garbage in your DB.
    """
     date : str
     title : str
     explanation : str
     url : str
     hdurl : Optional[str] = None
     media_type : str
     copyright : Optional[str] = None






    