from sqlalchemy import insert, select

from database.db import async_session
from models.user import User
from utils.repository import SQLAlchemyRepository


class UserRepo(SQLAlchemyRepository):
    model = User

    async def add_one(self, data: dict):
        """
        Override the add_one method to return the newly created user
        """
        async with async_session() as session:
            async with session.begin():
                stmt = insert(self.model).values(**data).returning(self.model.id)
                res = await session.execute(stmt)
                user_id = res.scalar_one()

                # Получаем объект пользователя по его ID
                stmt = select(self.model).where(self.model.id == user_id)
                res = await session.execute(stmt)
                new_user = res.scalar_one()

                return new_user
