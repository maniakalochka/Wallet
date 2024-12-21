from typing import Optional

from pydantic import BaseModel, Field


class TransactionBase(BaseModel):
    amount: float = Field(0.0, example=100.0, title="Amount", gt=0.0)
    description: Optional[str] = Field(
        None, example="Transaction message", title="Description"
    )
    type: str = Field("INCOME", example="INCOME", title="Type")
    sender_wallet_id: int = Field(..., example=1, title="Sender Wallet ID")
    receiver_wallet_id: int = Field(..., example=2, title="Receiver Wallet ID")

    class Config:
        from_attributes = True


class TransactionCreate(TransactionBase):
    pass
