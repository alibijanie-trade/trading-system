# -*- coding: utf-8 -*-
"""
مدل Exchange — سند ۵.۳
================================================================
صرافی — مثلاً Binance، Kraken، Bybit.
ccxt_id برای پیوست با کتابخانه ccxt در فاز ۱.

ستون‌ها (سند ۵.۳):
  id, name (UNIQUE), ccxt_id, is_active, supports_futures,
  is_deleted, created_at, updated_at
================================================================
"""

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base, SoftDeleteMixin, TimestampMixin


class Exchange(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "Exchanges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(
        String, unique=True, nullable=False, index=True,
    )
    ccxt_id: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    supports_futures: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False,
    )

    # ===================================================
    # Relationships
    # ===================================================
    api_keys: Mapped[list["ExchangeAPIKey"]] = relationship(
        "ExchangeAPIKey",
        back_populates="exchange",
    )
    symbols: Mapped[list["Symbol"]] = relationship(
        "Symbol",
        back_populates="exchange",
    )
    # Part 2
    trades: Mapped[list["Trade"]] = relationship(
        "Trade",
        back_populates="exchange",
    )
    portfolio: Mapped[list["Portfolio"]] = relationship(
        "Portfolio",
        back_populates="exchange",
    )

    def __repr__(self) -> str:
        return f"<Exchange id={self.id} name={self.name!r} ccxt_id={self.ccxt_id!r}>"
