from datetime import datetime, timezone
from sqlalchemy import (
    Integer, String, DateTime, ForeignKey,
    Boolean, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column
from src.database.connection import Base


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(200), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"), nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(320), unique=True, nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(500), nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(20), default="viewer", nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
