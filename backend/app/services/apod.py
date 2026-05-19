"""
WHY a DB service layer?

Same reason as the NASA service: keep SQL out of your route handlers.
Routes should read like English: "get today's APOD, cache it, return it."
Not like SQL queries embedded in HTTP handlers.

This layer owns all database operations for APOD data.
It's also the right place to learn SQLAlchemy's query patterns.
"""
#depends on the model and schemas. Upsert, search, get_by_date.

from datetime import date
from typing import Optional

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.apod import Apod
from app.schemas.apod import NasaApodRaw


class ApodService:

    async def get_by_date(self, db: AsyncSession, target_date: date) -> Optional[Apod]:
        """
        HOW SQLAlchemy 2.0 queries work:
          select(Model)           → SELECT * FROM apods
          .where(condition)       → WHERE date = :date
          scalar_one_or_none()    → returns one row or None (raises if multiple)
        """
        result = await db.execute(
            select(Apod).where(Apod.date == target_date)
        )
        return result.scalar_one_or_none()

    async def get_today(self, db: AsyncSession) -> Optional[Apod]:
        from datetime import date as date_type
        return await self.get_by_date(db, date_type.today())

    async def create_from_nasa(self, db: AsyncSession, raw: NasaApodRaw) -> Apod:
        """
        Convert a NASA API response into a DB row.
        WHY not insert the raw dict directly?
        NASA's field names and types don't perfectly match our schema.
        (e.g. NASA returns date as a string, our DB column is a DATE type)
        """
        from datetime import date as date_type
        apod = Apod(
            date=date_type.fromisoformat(raw.date),
            title=raw.title,
            explanation=raw.explanation,
            url=raw.url,
            hdurl=raw.hdurl,
            media_type=raw.media_type,
            copyright=raw.copyright,
        )
        db.add(apod)
        await db.flush()   # WHY flush not commit? flush sends SQL to Postgres
                           # but doesn't commit the transaction. The caller
                           # (get_db dependency) commits when the request succeeds.
                           # This lets multiple DB operations share one transaction.
        await db.refresh(apod)   # load the auto-generated id back into the object
        return apod

    async def upsert(self, db: AsyncSession, raw: NasaApodRaw) -> Apod:
        """
        Insert if not exists, skip if already stored.
        WHY upsert? The daily cron job runs every day. If it runs twice
        (restart, redeploy), you don't want duplicate rows.
        """
        existing = await self.get_by_date(db, __import__('datetime').date.fromisoformat(raw.date))
        if existing:
            return existing
        return await self.create_from_nasa(db, raw)

    async def search(
        self,
        db: AsyncSession,
        keyword: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        media_type: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Apod], int]:
        """
        Full search with optional filters and pagination.

        HOW pagination works:
          .offset((page-1) * page_size)  → skip rows from previous pages
          .limit(page_size)              → take only one page worth
          count_query                    → separate query to get total (for UI)
        """
        query = select(Apod)

        if keyword:
            # Search in both title and explanation
            # WHY ilike? Case-insensitive LIKE. `%keyword%` matches anywhere in string.
            query = query.where(
                or_(
                    Apod.title.ilike(f"%{keyword}%"),
                    Apod.explanation.ilike(f"%{keyword}%"),
                )
            )
        if start_date:
            query = query.where(Apod.date >= start_date)
        if end_date:
            query = query.where(Apod.date <= end_date)
        if media_type:
            query = query.where(Apod.media_type == media_type)

        # Count total matching rows (for pagination metadata)
        count_result = await db.execute(
            select(func.count()).select_from(query.subquery())
        )
        total = count_result.scalar_one()

        # Fetch the actual page
        query = query.order_by(Apod.date.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await db.execute(query)
        items = list(result.scalars().all())

        return items, total


apod_service = ApodService()
