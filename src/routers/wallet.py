from fastapi import APIRouter, Depends, HTTPException, status
from schemas.wallet import WalletCreate, WalletUpdate
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from repositories.wallet import WalletRepo
from .auth_helper import get_current_user
from models.wallet import Wallet

router = APIRouter(prefix="/wallet", tags=["wallet"])


@router.post("/")
async def add_wallet(
    wallet: WalletCreate,
    current_user: dict = Depends(get_current_user),
):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user"
        )
    wallet_holder_id = current_user.id
    wallet_dict = wallet.model_dump()
    await WalletRepo().add_by_user_id(wallet_holder_id, wallet_dict)
    return {
        "status": "success",
    }


@router.get("/all")
async def get_wallets(
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user"
        )
    user_id = current_user.id
    wallets = await WalletRepo().find_all(user_id)
    return wallets
