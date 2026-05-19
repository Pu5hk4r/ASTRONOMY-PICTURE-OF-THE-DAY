"""
WHY lifespan instead of @app.on_event?

FastAPI deprecated on_event in favour of the `lifespan` context manager.
lifespan handles both startup AND shutdown in one place, which is cleaner.

Everything before `yield` runs at startup.
Everything after `yield` runs at shutdown (cleanup).

HOW CORS works:
  Your React app runs on http://localhost:5173 (Vite default).
  Your FastAPI runs on http://localhost:8000.
  Browsers block cross-origin requests by default (CORS policy).
  CORSMiddleware tells the browser: "yes, localhost:5173 is allowed to call me."
  In production you'd replace the origin with your real frontend URL.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import apod as apod_router
from app.core.config import settings
from app.workers.scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP ---
    start_scheduler()
    yield
    # --- SHUTDOWN ---
    stop_scheduler()


app = FastAPI(
    title=settings.app_title,
    description="Astronomy Picture of the Day — archiver and explorer",
    version="1.0.0",
    lifespan=lifespan,
    # docs_url="/docs" by default — visit http://localhost:8000/docs
    # FastAPI auto-generates this from your route + schema definitions
)

# CORS — allow the React dev server to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route groups
# WHY prefix="/api"? All API routes live under /api/...
# This makes it easy to serve the React frontend on the same domain
# and route /api/* to FastAPI, /* to React.
app.include_router(apod_router.router, prefix="/api")


@app.get("/health")
async def health():
    """
    Simple health check endpoint.
    WHY? Load balancers, Docker, and monitoring tools ping this to know
    if the app is alive. Return 200 = healthy, anything else = problem.
    """
    return {"status": "ok"}
