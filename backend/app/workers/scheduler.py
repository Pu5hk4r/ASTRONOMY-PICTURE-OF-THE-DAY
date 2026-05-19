"""
WHY a background worker?

You want fresh APOD data every day without a user triggering it.
APScheduler runs inside your FastAPI process and fires a function on a schedule.

HOW it works:
  - At app startup, we register a job: "run fetch_daily_apod() every day at 07:00 UTC"
  - APScheduler keeps an internal clock and calls the function when the time comes
  - The function fetches from NASA and upserts to DB
  - No user request needed

WHY 07:00 UTC?
  NASA publishes APOD around midnight US Eastern time (05:00 UTC).
  07:00 UTC gives a buffer so the image is definitely live before we fetch.

WHEN to use APScheduler vs an external queue (Celery, BullMQ)?
  APScheduler: simple, single-process, no extra infra. Perfect for learning.
  External queue: needed when tasks are heavy, need retries, or run across multiple servers.
  For this project, APScheduler is the right choice.

  Why after routes? The cron job does exactly 
  what your /today route does — fetch from NASA, upsert to DB. 
  By now both services exist and are tested. The scheduler is just a timer that calls them.
"""

import logging
from datetime import date

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.db.database import AsyncSessionLocal
from app.services.apod import apod_service
from app.services.cache import cache
from app.services.nasa import nasa_service

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def fetch_daily_apod():
    """
    Fetches today's APOD from NASA and stores it.
    Called by the scheduler — no HTTP request, no user involved.
    """
    logger.info("Cron: fetching today's APOD from NASA...")

    try:
        raw = await nasa_service.get_apod_today()
    except Exception as e:
        logger.error(f"Cron: NASA fetch failed: {e}")
        return

    async with AsyncSessionLocal() as db:
        try:
            apod = await apod_service.upsert(db, raw)
            await db.commit()
            logger.info(f"Cron: saved APOD for {apod.date} — '{apod.title}'")

            # Invalidate the today cache so the next request gets fresh data
            await cache.delete(cache.apod_today_key())
        except Exception as e:
            await db.rollback()
            logger.error(f"Cron: DB save failed: {e}")


def start_scheduler():
    scheduler.add_job(
        fetch_daily_apod,
        trigger=CronTrigger(hour=7, minute=0, timezone="UTC"),
        id="daily_apod_fetch",
        replace_existing=True,      # safe to call start_scheduler() multiple times
        misfire_grace_time=3600,    # if server was down, run the job up to 1h late
    )
    scheduler.start()
    logger.info("Scheduler started — daily APOD fetch at 07:00 UTC")


def stop_scheduler():
    scheduler.shutdown()
