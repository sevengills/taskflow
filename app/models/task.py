from datetime import date

from sqlalchemy import Boolean, Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(String(255))

    description: Mapped[str] = mapped_column(
        String,
        default="",
    )

    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    due_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )