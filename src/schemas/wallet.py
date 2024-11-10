from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Annotated


class WalletBase(BaseModel):
    balance: float = Field(0.0, example=100.0, title="Balance")
    # currency: str = Field('RUB', example='RUB', title='Currency')


class WalletCreate(WalletBase):
    pass


class WalletUpdate(WalletBase):
    pass
