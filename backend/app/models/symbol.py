# -*- coding: utf-8 -*-
"""
مدل Symbol — سند ۵.۵
================================================================
نماد معاملاتی — مثلاً BTC/USDT در Binance spot.

ستون‌ها (سند ۵.۵):
  id, exchange_id (FK→Exchanges), symbol, base_asset, quote_asset,
  market_type (spot/futures), is_active, is_deleted

ایندکس Composite (سند ۵.۵):
  idx_symbols_exchange_symbol روی (exchange_id, symbol)

نکته: TimestampMixin اضافه شد طبق سند ۵.۰ (created_at/updated_at
       در همه جداول اصلی).
================================================================
"""

from app.infrastructure.database import Base, SoftDeleteMixin, TimestampMixin
from sqlalchemy import Boolean, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Symbol(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "Symbols"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exchange_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Exchanges.id", ondelete="CASCADE"),
        nullable=False,
    )
    symbol: Mapped[str] = mapped_column(String, nullable=False)  # BTC/USDT
    base_asset: Mapped[str] = mapped_column(String, nullable=False)  # BTC
    quote_asset: Mapped[str] = mapped_column(String, nullable=False)  # USDT
    market_type: Mapped[str] = mapped_column(String, nullable=False)  # spot/futures
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # ===================================================
    # Relationships
    # ===================================================
    exchange: Mapped["Exchange"] = relationship("Exchange", back_populates="symbols")
    watchlist_entries: Mapped[list["Watchlist"]] = relationship(
        "Watchlist",
        back_populates="symbol",
    )
    # Part 2
    ohlcv_data: Mapped[list["OhlcvData"]] = relationship(
        "OhlcvData",
        back_populates="symbol",
    )
    signals: Mapped[list["Signal"]] = relationship(
        "Signal",
        back_populates="symbol",
    )
    trades: Mapped[list["Trade"]] = relationship(
        "Trade",
        back_populates="symbol",
    )
    alerts: Mapped[list["Alert"]] = relationship(
        "Alert",
        back_populates="symbol",
    )

    # ===================================================
    # Indexes
    # ===================================================
    __table_args__ = (Index("idx_symbols_exchange_symbol", "exchange_id", "symbol"),)

    def __repr__(self) -> str:
        return (
            f"<Symbol id={self.id} symbol={self.symbol!r} "
            f"exchange_id={self.exchange_id} market={self.market_type!r}>"
        )
