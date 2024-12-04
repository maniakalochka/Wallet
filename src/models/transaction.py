from models.base import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
import enum
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from models.wallet import Wallet
    from models.user import User


class TransactionTypeEnum(enum.Enum):
    INCOME = "INCOME"
    OUTCOME = "OUTCOME"


class Transaction(Base):
    __tablename__ = "transaction"

    sender_wallet_id: Mapped[int] = mapped_column(
        ForeignKey("wallet.id"), nullable=False
    )
    receiver_wallet_id: Mapped[int] = mapped_column(
        ForeignKey("wallet.id"), nullable=False
    )
    sender_wallet: Mapped["Wallet"] = relationship(
        foreign_keys=[sender_wallet_id], back_populates="sent_transactions"
    )
    receiver_wallet: Mapped["Wallet"] = relationship(
        foreign_keys=[receiver_wallet_id], back_populates="received_transactions"
    )
    amount: Mapped[float] = mapped_column(default=0.0)
    description: Mapped[str] = mapped_column()
    type: Mapped[TransactionTypeEnum] = mapped_column(default=TransactionTypeEnum)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction {self.id}>"
