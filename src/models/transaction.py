from database.db import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum


class TransactionTypeEnum(enum.Enum):
    INCOME = "INCOME"
    OUTCOME = "OUTCOME"


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True)
    sender_wallet_id = Column(Integer, ForeignKey("wallet.id"), nullable=False)
    receiver_wallet_id = Column(Integer, ForeignKey("wallet.id"), nullable=False)
    sender_wallet = relationship(
        "Wallet", foreign_keys=[sender_wallet_id], back_populates="sent_transactions"
    )
    receiver_wallet = relationship(
        "Wallet",
        foreign_keys=[receiver_wallet_id],
        back_populates="received_transactions",
    )
    amount = Column(Float, default=0.0)
    description = Column(String, nullable=True)
    type = Column(Enum(TransactionTypeEnum), default=TransactionTypeEnum.INCOME)

    def __repr__(self):
        return f"<Transaction {self.id}>"
