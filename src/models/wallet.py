from backend.db import Base
from sqlalchemy import (
    Column, Integer, String, Float, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum


class CurrencyEnum(enum.Enum):
    RUB = 'RUB'
    USD = 'USD'
    EUR = 'EUR'


class Wallet(Base):
    __tablename__ = 'wallet'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    currency = Column(Enum(CurrencyEnum), default=CurrencyEnum.RUB)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='wallet')
    balance = Column(Float, default=0.0)

    def __repr__(self):
        return f'<Wallet {self.id}>'