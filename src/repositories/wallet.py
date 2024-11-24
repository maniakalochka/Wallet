from utils.repository import SQLAlchemyRepository
from models.wallet import Wallet
from database.db import async_session
from sqlalchemy import select


class WalletRepo(SQLAlchemyRepository):
    model = Wallet

    async def find_all(self, user_id):
        async with async_session() as session:
            async with session.begin():
                stmt = select(self.model).where(self.model.user_id == user_id)
                res = await session.execute(stmt)
                wallets = res.scalars().all()
                return wallets
