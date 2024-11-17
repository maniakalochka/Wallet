from fastapi import APIRouter, Depends, HTTPException, status
from schemas.wallet import WalletCreate, WalletUpdate
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from repositories.wallet import WalletRepo


router = APIRouter(prefix="/wallet", tags=["wallet"])


@router.post("/")
async def add_wallet(
    wallet: WalletCreate,
):
    wallet_dict = wallet.model_dump()
    wallet_id = await WalletRepo().add_one(wallet_dict)
    return {"wallet_id": wallet_id}  # /TODO add succes status


@router.get("/all")
async def get_wallets():
    wallets = await WalletRepo().find_all()
    return wallets


@router.get("/{id}")
async def get_wallet_by_id(id: int):
    wallet = await WalletRepo().find_by_id(id)
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet
