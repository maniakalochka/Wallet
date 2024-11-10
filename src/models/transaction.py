from backend.db import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum


class TransactionTypeEnum(enum.Enum):
    INCOME = "INCOME"
    OUTCOME = "OUTCOME"


class Transction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True)
    wallet_id = Column(Integer, ForeignKey("wallet.id"))
    wallet = relationship("Wallet", back_populates="transaction")
    amount = Column(Float, default=0.0)
    description = Column(String, nullable=True)
    type = Column(Enum(TransactionTypeEnum), default=TransactionTypeEnum.INCOME)

    def __repr__(self):
        return f"<Transaction {self.id}>"
