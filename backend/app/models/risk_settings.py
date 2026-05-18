# -*- coding: utf-8 -*-
"""
مدل RiskSettings — سند ۵.۱۱
================================================================
تنظیمات ریسک شخصی کاربر — رابطه یک‌به‌یک با User.

ستون‌ها (سند ۵.۱۱):
  user_id, max_risk_per_trade, max_daily_drawdown,
  max_open_trades, default_rr_ratio, auto_stop_on_loss

مقادیر پیش‌فرض (بهترین‌رویه‌های ترید):
  - max_risk_per_trade = 0.02   (2% سرمایه در هر معامله)
  - max_daily_drawdown = 0.05   (5% افت روزانه ماکزیمم)
  - max_open_trades    = 5
  - default_rr_ratio   = 2.0    (Risk/Reward ratio)
  - auto_stop_on_loss  = True

یک‌به‌یک بودن: user_id با UNIQUE تضمین می‌شود.
================================================================
"""

from app.infrastructure.database import Base, TimestampMixin
from sqlalchemy import Boolean, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship


class RiskSettings(Base, TimestampMixin):
    __tablename__ = "RiskSettings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # یک‌به‌یک
    )
    max_risk_per_trade: Mapped[float] = mapped_column(
        Float,
        default=0.02,
        nullable=False,
    )
    max_daily_drawdown: Mapped[float] = mapped_column(
        Float,
        default=0.05,
        nullable=False,
    )
    max_open_trades: Mapped[int] = mapped_column(
        Integer,
        default=5,
        nullable=False,
    )
    default_rr_ratio: Mapped[float] = mapped_column(
        Float,
        default=2.0,
        nullable=False,
    )
    auto_stop_on_loss: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", back_populates="risk_settings")

    def __repr__(self) -> str:
        return f"<RiskSettings user_id={self.user_id} max_risk={self.max_risk_per_trade}>"
