# -*- coding: utf-8 -*-
"""
مدل OhlcvData — سند ۵.۷ ⭐
================================================================
داده‌های کندل (Open/High/Low/Close/Volume) برای یک نماد در یک
تایم‌فریم خاص. این بزرگ‌ترین جدول دیتابیس خواهد بود.

ستون‌ها (سند ۵.۷ + توسعه فاز ۶):
  id, symbol_id (FK→Symbols), timeframe, timestamp (UTC),
  open, high, low, close, volume, is_closed, created_at,
  row_index (🆕 ترتیب ردیف در فایل ورودی — از صفر)

ایندکس Critical (سند ۵.۷ — قطعی):
  idx_ohlcv_symbol_tf_ts روی (symbol_id, timeframe, timestamp)
================================================================
"""

from datetime import datetime, timezone

from app.infrastructure.database import Base
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class OhlcvData(Base):
    __tablename__ = "OhlcvData"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Symbols.id", ondelete="CASCADE"),
        nullable=False,
    )
    timeframe: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    open: Mapped[float] = mapped_column(Float, nullable=False)
    high: Mapped[float] = mapped_column(Float, nullable=False)
    low: Mapped[float] = mapped_column(Float, nullable=False)
    close: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[float] = mapped_column(Float, nullable=False)
    is_closed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    row_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        nullable=False,
    )

    symbol: Mapped["Symbol"] = relationship("Symbol", back_populates="ohlcv_data")

    __table_args__ = (Index("idx_ohlcv_symbol_tf_ts", "symbol_id", "timeframe", "timestamp"),)

    def __repr__(self) -> str:
        return (
            f"<OhlcvData #{self.row_index} symbol_id={self.symbol_id} "
            f"tf={self.timeframe!r} ts={self.timestamp.isoformat()} close={self.close}>"
        )
