from abc import ABC, abstractmethod
from database.db import async_session
from sqlalchemy import insert, select


class AbstractRepository(ABC):
    
    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def find_all():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None
    
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