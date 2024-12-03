from models.base import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
import enum
from models.wallet import Wallet


class TransactionTypeEnum(enum.Enum):
    INCOME = "INCOME"
    OUTCOME = "OUTCOME"


class Transaction(Base):
    __tablename__ = "transaction"

    sender_wallet_id: Mapped[int] = mapped_column(
        foreign_key="wallet.id", nullable=False
    )
    receiver_wallet_id: Mapped[int] = mapped_column(
        foreign_key="wallet.id", nullable=False
    )
    sender_wallet: Mapped["Wallet"] = relationship(back_populates="sent_transactions")
    receiver_wallet: Mapped["Wallet"] = relationship(
        back_populates="received_transactions"
    )
    amount: Mapped[float] = mapped_column(default=0.0)
    description: Mapped[str] = mapped_column()
    type: Mapped[TransactionTypeEnum] = mapped_column(default=TransactionTypeEnum)

    def __repr__(self):
        return f"<Transaction {self.id}>"
