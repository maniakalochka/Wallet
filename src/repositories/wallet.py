from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import async_session
from models.wallet import Wallet
from utils.repository import SQLAlchemyRepository


class WalletRepo(SQLAlchemyRepository):
    model = Wallet

    async def find_all(self, user_id):
        """
        override the find_all method to filter by user_id
        """
        async with async_session() as session:
            async with session.begin():
                stmt = select(self.model).where(self.model.user_id == user_id)
                res = await session.execute(stmt)
                wallets = res.scalars().all()
                return wallets

    async def get_balance(self, wallet_id: int, db: AsyncSession):
        stmt = select(self.model).where(self.model.id == wallet_id)
        res = await db.execute(stmt)
        wallet = res.scalar_one_or_none()
        if wallet is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Wallet {wallet_id} not found",
            )
        return wallet.balance


    async def update_balance(
        self, wallet_id: int, new_balance: float, db: AsyncSession
    ):
        stmt = select(self.model).where(self.model.id == wallet_id)
        res = await db.execute(stmt)
        wallet = res.scalar_one_or_none()
        if wallet is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Wallet {wallet_id} not found",
            )
        wallet.balance = new_balance
        db.add(wallet)
        await db.commit()

