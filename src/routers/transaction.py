from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from models.user import User
from repositories.transaction import TransactionRepo
from repositories.wallet import WalletRepo
from schemas.transaction import TransactionCreate

from .auth_helper import get_current_user

transaction_router = APIRouter(prefix="/transaction", tags=["transaction"])


@transaction_router.post("/")
async def add_transaction(
    transaction: TransactionCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Создает транзакцию (перевод с одного счета на другой)
    """
    wallet_repo = WalletRepo()
    sender_balance = await wallet_repo.get_balance(transaction.sender_wallet_id, db)

    if sender_balance < transaction.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds in the sender's wallet.",
        )

    # Атомарное выполнение транзакции
    # Списываем средства у отправителя
    await wallet_repo.update_balance(
        transaction.sender_wallet_id,
        sender_balance - transaction.amount,
        db,
    )

    # Получаем текущий баланс получателя
    receiver_balance = await wallet_repo.get_balance(transaction.receiver_wallet_id, db)

    # Зачисляем средства на счёт получателя
    await wallet_repo.update_balance(
        transaction.receiver_wallet_id,
        receiver_balance + transaction.amount,
        db,
    )

    # Создаём запись о транзакции
    transaction_dict = transaction.model_dump()
    transaction_dict["user_id"] = current_user.id
    transaction_id = await TransactionRepo().add_one(transaction_dict)

    return {"transaction_id": transaction_id}


@transaction_router.get("/all")
@cache(expire=60)
async def get_transactions(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Получает все транзакции конкретного пользователя
    Работает только для администарторов
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    transactions = await TransactionRepo().find_all(user_id)
    return transactions


@transaction_router.get("/my")
@cache(expire=60)
async def get_my_transactions(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    transactions = await TransactionRepo().find_all(current_user.id)
    return transactions


# @transaction_router.get("/{id}")
# @cache(expire=60)
# async def get_transaction_by_id(
#     id: int,
#     db: Annotated[AsyncSession, Depends(get_db)],
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     transaction = await TransactionRepo().find_by_id(id)
#     if transaction is None:
#         raise HTTPException(status_code=404, detail="Transaction not found")
#     if not current_user.is_admin and (
#         transaction.sender_wallet_id != current_user.wallet.id
#         and transaction.receiver_wallet_id != current_user.wallet.id
#     ):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
#         )
#     return transaction
