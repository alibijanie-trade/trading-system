# -*- coding: utf-8 -*-
"""
مدل Watchlist — سند ۵.۶
================================================================
لیست نمادهای مورد علاقه کاربر با ترتیب نمایش.

ستون‌ها (سند ۵.۶):
  id, user_id (FK→Users), symbol_id (FK→Symbols),
  sort_order, created_at

نکته: Watchlist مشمول soft delete نیست — حذف می‌شود به‌صورت
       فیزیکی (cascade از User).
================================================================
"""

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Watchlist(Base):
    __tablename__ = "Watchlist"

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
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", back_populates="watchlist")
    symbol: Mapped["Symbol"] = relationship("Symbol", back_populates="watchlist_entries")

    def __repr__(self) -> str:
        return f"<Watchlist id={self.id} user_id={self.user_id} symbol_id={self.symbol_id}>"
