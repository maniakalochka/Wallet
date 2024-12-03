from core.config import settings

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
)
from models.base import Base

DATABASE_URL = settings.DB_URL
ECHO = settings.ECHO
EXPIRE_ON_COMMIT = settings.EXPIRE_ON_COMMIT

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=ECHO)

# Session Factory
async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, autoflush=True, expire_on_commit=EXPIRE_ON_COMMIT
)


async def get_db():
    """Create async session"""
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Init database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
