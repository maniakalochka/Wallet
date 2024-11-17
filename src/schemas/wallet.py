from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Annotated
from models.wallet import CurrencyEnum


class WalletBase(BaseModel):
    currency: str = Field("RUB", example="RUB", title="Currency")

    class Config:
        from_attributes = True


class WalletCreate(BaseModel):
    currency: str = Field(CurrencyEnum.RUB, example="RUB", title="Currency")

    class Config:
        from_attributes = True


class WalletUpdate(WalletCreate):
    pass
