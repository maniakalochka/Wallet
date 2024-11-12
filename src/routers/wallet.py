from fastapi import APIRouter, Depends, HTTPException, status
from schemas.wallet import WalletCreate
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from repositories.wallet import WalletRepo


router = APIRouter(prefix='/wallet', tags=['wallet'])


@router.post('/')
async def add_wallet(
    wallet: WalletCreate,
):
    wallet_dict = wallet.model_dump()
    wallet_id = await WalletRepo().add_one(wallet_dict)
    return {
        "wallet_id": wallet_id  # /TODO add succes status
    }
    