import datetime

from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now()
    )
