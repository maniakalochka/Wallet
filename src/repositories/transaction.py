import models
from utils.repository import SQLAlchemyRepository
from models.transaction import Transaction
from database.db import async_session
from fastapi import select


class TransactionRepo(SQLAlchemyRepository):
    model = Transaction

    async def find_all(self, user_id):
        """
        override the find_all method to filter by user_id
        """
        async with async_session() as session:
            async with session.begin():
                stmt = select(self.model).where(self.model.user_id == user_id)
                res = await session.execute(stmt)
                transaction = res.scalars().all()
                return transaction
