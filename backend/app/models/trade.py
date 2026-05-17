# -*- coding: utf-8 -*-
"""
مدل Trade — سند ۵.۱۰
================================================================
معامله واقعی یا paper trade کاربر.

ستون‌ها (سند ۵.۱۰):
  id, user_id (FK), strategy_id (FK, nullable), signal_id (FK, nullable),
  symbol_id (FK), exchange_id (FK), order_type, side, status,
  entry_price, exit_price, quantity, take_profit, stop_loss,
  pnl, pnl_percent, commission, is_paper, is_deleted,
  opened_at, closed_at

مقادیر مجاز:
  - order_type : market | limit | stop-limit
  - side       : buy | sell
  - status     : open | closed | cancelled

تصمیم پیاده‌سازی:
  - TimestampMixin اضافه شد (created_at/updated_at — audit trail رکورد)
  - opened_at/closed_at = زمان معاملاتی واقعی (متمایز از created_at)
  - SoftDeleteMixin برای is_deleted
================================================================
"""

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base, SoftDeleteMixin, TimestampMixin


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Trade(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "Trades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    strategy_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("Strategies.id", ondelete="SET NULL"),
        nullable=True,
    )
    signal_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("Signals.id", ondelete="SET NULL"),
        nullable=True,
    )
    symbol_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Symbols.id", ondelete="RESTRICT"),
        nullable=False,
    )
    exchange_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Exchanges.id", ondelete="RESTRICT"),
        nullable=False,
    )

    order_type: Mapped[str] = mapped_column(String, nullable=False)  # market/limit/stop-limit
    side: Mapped[str] = mapped_column(String, nullable=False)        # buy/sell
    status: Mapped[str] = mapped_column(
        String, default="open", nullable=False,
    )  # open/closed/cancelled

    entry_price: Mapped[float] = mapped_column(Float, nullable=False)
    exit_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    take_profit: Mapped[float | None] = mapped_column(Float, nullable=True)
    stop_loss: Mapped[float | None] = mapped_column(Float, nullable=True)
    pnl: Mapped[float | None] = mapped_column(Float, nullable=True)
    pnl_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    commission: Mapped[float | None] = mapped_column(Float, nullable=True)
    is_paper: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    opened_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        nullable=False,
    )
    closed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True,
    )

    # ===================================================
    # Relationships
    # ===================================================
    user: Mapped["User"] = relationship("User", back_populates="trades")
    strategy: Mapped["Strategy | None"] = relationship(
        "Strategy", back_populates="trades",
    )
    signal: Mapped["Signal | None"] = relationship(
        "Signal", back_populates="trades",
    )
    symbol: Mapped["Symbol"] = relationship("Symbol", back_populates="trades")
    exchange: Mapped["Exchange"] = relationship("Exchange", back_populates="trades")

    def __repr__(self) -> str:
        return (
            f"<Trade id={self.id} {self.side!r} {self.status!r} "
            f"qty={self.quantity} entry={self.entry_price} pnl={self.pnl}>"
        )
