from src.backend.db import Base
from sqlalchemy import (
    Column, Integer, String, Float, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
import enum


class CurrencyEnum(enum.Enum):
    RUB = 'RUB'
    USD = 'USD'
    EUR = 'EUR'


class Wallet(Base):
    __tablename__ = 'wallet'

    id = Column(Integer, primary_key=True)
    currency = Column(Enum(CurrencyEnum), default=CurrencyEnum.RUB)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='wallet')
    balance = Column(Float, default=0.0)

    def __repr__(self):
        return f'<Wallet {self.id}>'