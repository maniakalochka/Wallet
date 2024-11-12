from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Annotated


class WalletBase(BaseModel):
    user_id: int = Field(...)
    balance: float = Field(0.0, example=100.0, title="Balance")
    # currency: str = Field('RUB', example='RUB', title='Currency')

    class Config:
        from_attributes = True

class WalletCreate(WalletBase):
    pass


class WalletUpdate(WalletBase):
    pass
