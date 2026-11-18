from datetime import datetime
from sqlalchemy import (
    Integer, String, DateTime, Numeric,
    ForeignKey, UniqueConstraint, Index
)
from sqlalchemy.orm import Mapped, mapped_column
from src.database.connection import Base

class BusinessOrder(Base):
    __tablename__ = "business_orders"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    tenant_id: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1
    )

    order_id: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    order_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False
    )

    customer: Mapped[str] = mapped_column(
        String(150), nullable=False
    )

    site: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    product: Mapped[str] = mapped_column(
        String(150), nullable=False
    )

    quantity: Mapped[float] = mapped_column(
        Numeric(14, 3), nullable=False
    )

    price_per_unit: Mapped[float] = mapped_column(
        Numeric(14, 2), nullable=False
    )

    cost_per_unit: Mapped[float] = mapped_column(
        Numeric(14, 2), nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "tenant_id", "order_id",
            name="uq_tenant_order"
        ),
        Index(
            "ix_tenant_order_date",
            "tenant_id", "order_date"
        ),
    )
