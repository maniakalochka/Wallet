from database.db import Base, async_session
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean, event
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from models.wallet import Wallet


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    wallet = relationship("Wallet", back_populates="user")

    def __repr__(self):
        return f"<User {self.last_name}>"

@event.listens_for(User, 'after_insert')
async def create_wallet_after_user_insert(mapper, connection, target):
    async with async_session() as session:
        async with session.begin():
            new_wallet = Wallet(user_id=target.id)
            session.add(new_wallet)
