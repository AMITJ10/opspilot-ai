from datetime import datetime, timezone

from sqlalchemy import (
    Integer, String, DateTime, ForeignKey,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        unique=True
    )

    plan: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="starter"
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="trial"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
