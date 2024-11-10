from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Annotated


class TransactionBase(BaseModel):
    amount: float = Field(0.0, example=100.0, title='Amount')
    description: Optional[str] = Field(None, example='Transaction message', title='Description')
    type: str = Field('INCOME', example='INCOME', title='Type')


class TransactionCreate(TransactionBase):
    pass

class TransctionUpdate(TransactionBase):
    pass