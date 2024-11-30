from database.db import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
import enum
from models.transaction import Transaction
from models.user import User


class CurrencyEnum(enum.Enum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"


class Wallet(Base):
    __tablename__ = "wallet"

    id: Mapped[int] = mapped_column(primary_key=True)
    currency: Mapped[CurrencyEnum] = mapped_column(default=CurrencyEnum.RUB)
    user_id: Mapped[int] = mapped_column(foreign_key="user.id", nullable=False)
    user: Mapped["User"] = relationship(back_populates="wallet")
    balance: Mapped[float] = mapped_column(default=0.0)
    sent_transactions: Mapped["Transaction"] = relationship(
        foreign_keys="[Transaction.sender_wallet_id]", back_populates="sender_wallet"
    )
    received_transactions: Mapped["Transaction"] = relationship(
        foreign_keys="[Transaction.receiver_wallet_id]",
        back_populates="receiver_wallet",
    )

    def __repr__(self):
        return f"<Wallet {self.id}>"
