from pydantic import BaseModel, Field


class WalletBase(BaseModel):
    currency: str = Field("RUB", example="RUB", title="Currency")

    class Config:
        from_attributes = True


class WalletCreate(BaseModel):
    currency: str = Field(..., example="RUB", title="Currency")


class WalletUpdate(WalletCreate):
    pass
