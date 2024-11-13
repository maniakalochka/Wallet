from schemas.transaction import TransactionCreate
from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from repositories.transaction import TransactionRepo
from models.user import User
from .auth import get_current_user


router = APIRouter(prefix='/transaction', tags=['transaction'])

@router.post('/')
async def add_transaction(
    transaction: TransactionCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    transaction_dict = transaction.model_dump()
    transaction_id = await TransactionRepo().add_one(transaction_dict)
    return {
        "transaction_id": transaction_id  
    }

@router.get('/all')
async def get_transactions(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    transactions = await TransactionRepo().find_all()
    return transactions

@router.get('/my')
async def get_my_transactions(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    transactions = await TransactionRepo().find_by_user_id(current_user.id)
    return transactions

@router.get('/{id}')
async def get_transaction_by_id(
    id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    transaction = await TransactionRepo().find_by_id(id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    if not current_user.is_admin and (transaction.sender_wallet_id != current_user.wallet.id and transaction.receiver_wallet_id != current_user.wallet.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return transaction
