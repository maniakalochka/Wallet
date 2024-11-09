from backend.db import Base
from sqlalchemy import (
    Column, Integer, String, Float, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum


class TransactionTypeEnum(enum.Enum):
    INCOME = 'INCOME'
    OUTCOME = 'OUTCOME'
    

class Transction(Base):
    __tablename__ = 'transaction'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wallet_id = Column(UUID(as_uuid=True), ForeignKey('wallet.id'))
    wallet = relationship('Wallet', back_populates='transaction')
    amount = Column(Float, default=0.0)
    description = Column(String, nullable=True)
    type = Column(Enum(TransactionTypeEnum), default=TransactionTypeEnum.INCOME)

    def __repr__(self):
        return f'<Transaction {self.id}>'