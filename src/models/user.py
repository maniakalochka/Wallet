from database.db import Base, async_session
import models
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean, event
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from models.wallet import Wallet


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    wallet: Mapped[Wallet] = relationship(back_populates="user")

    def __repr__(self):
        return f"<User {self.last_name}>"
