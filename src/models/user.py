from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from models.transaction import Transaction
    from models.wallet import Wallet


class User(Base):
    __tablename__ = "user"

    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    wallet: Mapped["Wallet"] = relationship("Wallet", back_populates="user")
    transactions: Mapped["Transaction"] = relationship(
        "Transaction", back_populates="user"
    )

    def __repr__(self):
        return f"<User {self.last_name}>"
