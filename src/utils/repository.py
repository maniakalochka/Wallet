from fastapi import status
from sqlalchemy import insert, or_, select, update
from sqlalchemy.exc import SQLAlchemyError

from database.db import async_session

from logger import logger
from .abstract_repo import AbstractRepository


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def check_exists(self, **kwargs):
        try:
            async with async_session() as session:
                stmt = select(self.model).where(
                    or_(
                        self.model.username == kwargs["username"],
                        self.model.email == kwargs["email"],
                    )
                )
                result = await session.execute(stmt)
                res = result.scalars().first()
            return res
        except (SQLAlchemyError, Exception) as e:
            logger.error("", exc_info=True)
            if isinstance(e, SQLAlchemyError):
                msg = "Database error:"
            else:
                msg = "Unexpected error:"
            extra = {**kwargs}
            msg += ": can't check user exists"
            logger.error(msg, extra=extra, exc_info=True)

    async def deactivate_user(self, id):
        async with async_session() as session:
            stmt = update(self.model).where(self.model.id == id).values(is_active=False)
            await session.execute(stmt)
            await session.commit()
            return {"status_code": status.HTTP_200_OK, "transaction": "Successful"}

    async def add_one(self, data: dict):
        async with async_session() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def find_all(self):
        async with async_session() as session:
            stmt = select(self.model)
            result = await session.execute(stmt)
            res = [row[0] for row in result.fetchall()]
            return res

    async def find_by_id(self, id: int):
        async with async_session() as session:
            stmt = select(self.model).where(self.model.id == id)
            result = await session.execute(stmt)
            res = result.scalars().first()
            return res

    async def find_by_username(self, username: str):
        async with async_session() as session:
            stmt = select(self.model).where(self.model.username == username)
            result = await session.execute(stmt)
            res = result.scalars().first()
            return res

    async def add_by_user_id(self, user_id: int, data: dict):
        async with async_session() as session:
            wallet_data = {"user_id": user_id, **data}
            stmt = insert(self.model).values(**wallet_data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()
