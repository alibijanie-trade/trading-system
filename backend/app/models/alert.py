# -*- coding: utf-8 -*-
"""
مدل Alert — سند ۵.۱۱
================================================================
هشدار قابل تنظیم برای یک نماد (مثلاً قیمت بالاتر از X).

ستون‌ها (سند ۵.۱۱):
  user_id (FK), symbol_id (FK), alert_type, condition (JSON),
  is_triggered, triggered_at, is_active

نمونه condition (JSON):
  {"operator": ">", "value": 70000}              ← price_above
  {"indicator": "RSI", "operator": "<", "value": 30}  ← oversold
================================================================
"""

from datetime import datetime

from app.infrastructure.database import Base, TimestampMixin
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Alert(Base, TimestampMixin):
    __tablename__ = "Alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    symbol_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Symbols.id", ondelete="CASCADE"),
        nullable=False,
    )
    alert_type: Mapped[str] = mapped_column(
        String, nullable=False
    )  # price_above, indicator_cross, ...
    condition: Mapped[str] = mapped_column(Text, nullable=False)  # JSON
    is_triggered: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    triggered_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="alerts")
    symbol: Mapped["Symbol"] = relationship("Symbol", back_populates="alerts")

    def __repr__(self) -> str:
        return (
            f"<Alert id={self.id} type={self.alert_type!r} "
            f"triggered={self.is_triggered} active={self.is_active}>"
        )
