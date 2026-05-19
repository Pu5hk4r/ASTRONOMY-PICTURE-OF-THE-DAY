'''
DATABASE CONNECTION--engine , session , base

Why before models? Models inherit from Base. 
Base lives here. If you write 
the model first you have nothing to inherit from. Also test the connection here — confirm Postgres is reachable before writing a single query

WHY async SQLALCHEMY?

Fastapi is async - it handles many requests concurrently using python's event loop.
If your DB calls a synchronous (blocking), they freeze the event loop while waiting
for Postgres to respond , killing your concurrency advantage.

Async SQLAlchemy + aysync lets your app handle other rqeuests while waiting for DB I/O
How the session works:
 -AsyncEngine: the raw connection pool to postgres (created once at startup)
 -AsyncSession: a single unit-of-work. Open one per request, close it when done.
 -get_db(): a FastAPI dependency that yields a fresh session per request,
  the commits or rolls back automatically 

'''

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

#WHY pool_pre_ping?
#If Postgres restarts, old connections in the pool are dead
#pool_pre_ping sends a lightweight "SELECT 1" before using a connection
#so SQLAlchemy detects and replaces deads one automatically.

engine= create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
    echo=settings.debug,  #logs evety sql query in debug mode
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit = False, #WHY? After commit, don't expire objects attributes.
                              # Without this, accessing obj.title after commit.
                              #triggers another SELECT - unexpected and slow.

)

class Base(DeclarativeBase):
    '''
    ALL your SQLAlchemy models inherits from this,
    Why? a single BAse? Alembic(migrations) needs to discover all  models
    Importing Base imports all models registered to it - one import, full picture
    
    '''

    pass

async def get_db():
    '''
    FastAPI dependency - inject a DB session into any route with:
      db: AsyncSession = Depends (get_db)
    
    The 'async with' guarantees the session close even if an exception occurs
    '''

    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise 