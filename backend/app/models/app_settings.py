# -*- coding: utf-8 -*-
"""
مدل AppSettings — سند ۵.۱۱
================================================================
تنظیمات شخصی UI و سیستم — رابطه یک‌به‌یک با User.

ستون‌ها (سند ۵.۱۱):
  user_id, theme, calendar_type, font_size, default_timeframe,
  active_exchanges (JSON), telegram_chat_id

پیش‌فرض‌ها (طبق Session 2 - تصمیم #12):
  - theme = "light"
  - calendar_type = "gregorian"  (تصمیم #12: تقویم پیش‌فرض میلادی)
  - font_size = 14
  - default_timeframe = "1h"
================================================================
"""

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base, TimestampMixin


class AppSettings(Base, TimestampMixin):
    __tablename__ = "AppSettings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # یک‌به‌یک
    )
    theme: Mapped[str] = mapped_column(String, default="light", nullable=False)
    calendar_type: Mapped[str] = mapped_column(
        String, default="gregorian", nullable=False,
    )
    font_size: Mapped[int] = mapped_column(Integer, default=14, nullable=False)
    default_timeframe: Mapped[str] = mapped_column(
        String, default="1h", nullable=False,
    )
    active_exchanges: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON list
    telegram_chat_id: Mapped[str | None] = mapped_column(String, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="app_settings")

    def __repr__(self) -> str:
        return f"<AppSettings user_id={self.user_id} theme={self.theme!r}>"
