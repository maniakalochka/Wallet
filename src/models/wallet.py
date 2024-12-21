from database.db import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
import enum
from models.transaction import Transaction


from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from models.transaction import Transaction
    from models.user import User


class Wallet(Base):
    __tablename__ = "wallet"

    currency: Mapped[str] = mapped_column(default="RUB", nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="wallet")
    balance: Mapped[float] = mapped_column(default=0.0)
    sent_transactions: Mapped["Transaction"] = relationship(
        foreign_keys="[Transaction.sender_wallet_id]", back_populates="sender_wallet"
    )
    received_transactions: Mapped["Transaction"] = relationship(
        foreign_keys="[Transaction.receiver_wallet_id]",
        back_populates="receiver_wallet",
    )

    def __repr__(self) -> str:
        return f"<Wallet {self.id}>"
