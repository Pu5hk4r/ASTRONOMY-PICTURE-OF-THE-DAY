"""
WHY are routes so thin?

A route handler's only job is:
  1. Accept the HTTP request
  2. Call services to do the actual work
  3. Return the HTTP response

Business logic (caching strategy, DB upsert, NASA fetch) lives in services.
This makes routes easy to read, test, and change independently.

HOW FastAPI routing works:
  @router.get("/today")           → maps GET /api/apod/today to this function
  response_model=ApodResponse     → FastAPI validates + serializes the return value
  Depends(get_db)                 → FastAPI creates a DB session and injects it
"""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.apod import ApodListResponse, ApodResponse
from app.services.apod import apod_service
from app.services.cache import cache
from app.services.nasa import nasa_service

router = APIRouter(prefix="/apod", tags=["APOD"])


@router.get("/today", response_model=ApodResponse)
async def get_today(db: AsyncSession = Depends(get_db)):
    """
    Cache-aside pattern in action:
      1. Check Redis → cache hit? Return immediately (fast path)
      2. Check DB → already fetched today? Cache it, return it
      3. Fetch from NASA → store in DB → cache → return (slow path, runs once/day)
    """
    cache_key = cache.apod_today_key()

    # Step 1: Cache check
    cached = await cache.get(cache_key)
    if cached:
        return ApodResponse(**cached)

    # Step 2: DB check
    db_apod = await apod_service.get_today(db)
    if db_apod:
        response = ApodResponse.model_validate(db_apod)
        await cache.set(cache_key, response.model_dump())
        return response

    # Step 3: Fetch from NASA
    try:
        raw = await nasa_service.get_apod_today()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"NASA API unavailable: {e}")

    db_apod = await apod_service.upsert(db, raw)
    response = ApodResponse.model_validate(db_apod)
    await cache.set(cache_key, response.model_dump())
    return response


@router.get("/date/{date_str}", response_model=ApodResponse)
async def get_by_date(date_str: str, db: AsyncSession = Depends(get_db)):
    """
    Fetch APOD for a specific date (YYYY-MM-DD).
    Historical APODs never change — cache them longer (24h).
    """
    try:
        target_date = date.fromisoformat(date_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Date must be YYYY-MM-DD format")

    cache_key = cache.apod_date_key(date_str)
    cached = await cache.get(cache_key)
    if cached:
        return ApodResponse(**cached)

    db_apod = await apod_service.get_by_date(db, target_date)
    if not db_apod:
        # Not in our DB yet — fetch from NASA and store
        try:
            raw = await nasa_service.get_apod_for_date(target_date)
            db_apod = await apod_service.upsert(db, raw)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"APOD not found: {e}")

    response = ApodResponse.model_validate(db_apod)
    # Historical APODs never change — cache for 24 hours
    await cache.set(cache_key, response.model_dump(), ttl=86400)
    return response


@router.get("/search", response_model=ApodListResponse)
async def search(
    keyword: str | None = Query(None, description="Search in title and explanation"),
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    media_type: str | None = Query(None, pattern="^(image|video)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """
    Search stored APODs by keyword, date range, or media type.
    Only searches what's in our DB — run the backfill worker to populate it.

    WHY Query(ge=1)? FastAPI validates page >= 1 automatically.
    Invalid values return 422 Unprocessable Entity before your code runs.
    """
    items, total = await apod_service.search(
        db,
        keyword=keyword,
        start_date=start_date,
        end_date=end_date,
        media_type=media_type,
        page=page,
        page_size=page_size,
    )

    return ApodListResponse(
        items=[ApodResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
        has_next=(page * page_size) < total,
    )


@router.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    """
    Returns archive statistics for the dashboard.
    No caching here — this is a cheap query and it's fun to see live numbers.
    """
    from sqlalchemy import func, select
    from app.models.apod import Apod

    result = await db.execute(
        select(
            func.count(Apod.id).label("total"),
            func.min(Apod.date).label("oldest"),
            func.max(Apod.date).label("newest"),
        )
    )
    row = result.one()
    return {
        "total_apods": row.total,
        "oldest_date": row.oldest,
        "newest_date": row.newest,
    }
