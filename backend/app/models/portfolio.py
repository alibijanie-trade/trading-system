# -*- coding: utf-8 -*-
"""
مدل Portfolio — سند ۵.۱۱
================================================================
Snapshot موجودی کاربر در یک صرافی برای یک دارایی، در زمان معین.
هر رکورد یک snapshot تاریخی است (نه وضعیت زنده).

ستون‌ها (سند ۵.۱۱):
  user_id (FK), exchange_id (FK), asset, balance_total,
  balance_free, balance_locked, snapshot_at

نکته: Portfolio به‌صورت time-series است:
  - یک snapshot روزانه/ساعتی برای هر (user, exchange, asset)
  - تاریخچه نگه‌داشته می‌شود برای نمودار equity
================================================================
"""

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Portfolio(Base):
    __tablename__ = "Portfolio"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    exchange_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Exchanges.id", ondelete="CASCADE"),
        nullable=False,
    )
    asset: Mapped[str] = mapped_column(String, nullable=False)  # BTC, USDT, ...
    balance_total: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    balance_free: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    balance_locked: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    snapshot_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", back_populates="portfolio")
    exchange: Mapped["Exchange"] = relationship("Exchange", back_populates="portfolio")

    def __repr__(self) -> str:
        return (
            f"<Portfolio user_id={self.user_id} {self.asset!r} "
            f"total={self.balance_total} at={self.snapshot_at.isoformat()}>"
        )
