# -*- coding: utf-8 -*-
"""
مدل Signal — سند ۵.۹
================================================================
سیگنال تولیدشده از یک استراتژی برای یک نماد.

ستون‌ها (سند ۵.۹):
  id, strategy_id (FK), symbol_id (FK), signal_type (buy/sell),
  strength (strong/medium/weak), timeframe, price_at_signal,
  suggested_entry, suggested_tp, suggested_sl, notes,
  is_executed, created_at

نکته: signals immutable هستند — بدون updated_at و is_deleted.
       اگر باطل شد، فقط is_executed=False باقی می‌ماند و سیگنال
       جدید ایجاد می‌شود.
================================================================
"""

from datetime import datetime, timezone

from app.infrastructure.database import Base
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Signal(Base):
    __tablename__ = "Signals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    strategy_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Strategies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    symbol_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Symbols.id", ondelete="CASCADE"),
        nullable=False,
    )
    signal_type: Mapped[str] = mapped_column(String, nullable=False)  # buy/sell
    strength: Mapped[str] = mapped_column(String, nullable=False)  # strong/medium/weak
    timeframe: Mapped[str] = mapped_column(String, nullable=False)
    price_at_signal: Mapped[float] = mapped_column(Float, nullable=False)
    suggested_entry: Mapped[float | None] = mapped_column(Float, nullable=True)
    suggested_tp: Mapped[float | None] = mapped_column(Float, nullable=True)  # Take Profit
    suggested_sl: Mapped[float | None] = mapped_column(Float, nullable=True)  # Stop Loss
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_executed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        nullable=False,
    )

    # ===================================================
    # Relationships
    # ===================================================
    strategy: Mapped["Strategy"] = relationship("Strategy", back_populates="signals")
    symbol: Mapped["Symbol"] = relationship("Symbol", back_populates="signals")
    trades: Mapped[list["Trade"]] = relationship("Trade", back_populates="signal")

    def __repr__(self) -> str:
        return (
            f"<Signal id={self.id} {self.signal_type!r}/{self.strength!r} "
            f"strategy_id={self.strategy_id} symbol_id={self.symbol_id}>"
        )
