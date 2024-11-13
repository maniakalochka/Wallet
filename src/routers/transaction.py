from schemas.transaction import TransactionCreate
from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from repositories.transaction import TransactionRepo


router = APIRouter(prefix='/transaction', tags=['transaction'])

@router.post('/')
async def add_transaction(
    transaction: TransactionCreate,
):
    transaction_dict = transaction.model_dump()
    transaction_id = await TransactionRepo().add_one(transaction_dict)
    return {
        "transaction_id": transaction_id  
    }

@router.get('/all')
async def get_transactions():
    transactions = await TransactionRepo().find_all()
    return transactions

@router.get('/{id}')
async def get_transaction_by_id(id: int):
    transaction = await TransactionRepo().find_by_id(id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction
