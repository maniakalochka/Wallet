from core.config import settings
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
)
from models.base import Base

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DB_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DB_URL
    DATABASE_PARAMS = {"poolclass": NullPool}


engine: AsyncEngine = create_async_engine(
    url=DATABASE_URL, echo=True, **DATABASE_PARAMS
)

# Session Factory
async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, autoflush=True, expire_on_commit=False
)


async def get_db():
    """Create async session"""
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


async def init_db() -> None:
    """Init database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
