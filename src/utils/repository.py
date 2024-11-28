from abc import ABC, abstractmethod
from database.db import async_session
from sqlalchemy import insert, select, or_, update
from fastapi import status


class AbstractRepository(ABC):

    @abstractmethod
    async def add_one():
        """
        Add one item to the database
        """
        raise NotImplementedError

    @abstractmethod
    async def find_all():
        """
        Find all items in the database
        """
        raise NotImplementedError

    @abstractmethod
    async def check_exists():
        """
        Check if the item exists in the database
        """
        raise NotImplementedError

    @abstractmethod
    async def deactivate_user():
        """
        Ban user by ID
        """
        raise NotImplementedError

    @abstractmethod
    async def find_by_id():
        """
        Find item by ID
        """
        raise NotImplementedError

    @abstractmethod
    async def find_by_username():
        """
        Find item by username
        """
        raise NotImplementedError

    @abstractmethod
    async def add_by_user_id():
        """
        Add item by user ID
        """
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def check_exists(self, **kwargs):
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
