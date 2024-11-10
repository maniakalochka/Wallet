import os
from src.core.config import settings

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = settings.DB_URL
ECHO = settings.ECHO
EXPIRE_ON_COMMIT = settings.EXPIRE_ON_COMMIT

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=ECHO)

# Session Factory
async_session = sessionmaker(
    bind=engine, class_=AsyncSession, autoflush=True, expire_on_commit=EXPIRE_ON_COMMIT
)

Base = declarative_base()  # Base class for ORM models


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
