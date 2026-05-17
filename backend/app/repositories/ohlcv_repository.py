# -*- coding: utf-8 -*-
"""
OhlcvRepository — Query های اختصاصی OhlcvData
================================================================
این Repository از BaseRepository ارث می‌برد و Query های اختصاصی
برای جدول OhlcvData اضافه می‌کند.

استفاده در route ها:
    from app.repositories.ohlcv_repository import OhlcvRepository

    repo = OhlcvRepository(db)
    candles = await repo.list_by_symbol_and_timeframe(
        symbol_id=1,
        timeframe="1d",
        limit=100,
    )

قانون قفل‌شده (سند ۳.۳):
  - تمام Query های OhlcvData باید از این کلاس عبور کنند
  - هیچ select مستقیم از OhlcvData در api/ یا services/ نباشد
================================================================
"""

from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ohlcv_data import OhlcvData
from app.repositories.base import BaseRepository


class OhlcvRepository(BaseRepository[OhlcvData]):
    """Repository اختصاصی برای OhlcvData."""

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, OhlcvData)

    # ============================================================
    # Query های اختصاصی فاز ۰ — endpoint GET /ohlcv/{symbol_id}
    # ============================================================

    async def list_by_symbol_and_timeframe(
        self,
        symbol_id: int,
        timeframe: str,
        limit: int = 100,
        offset: int = 0,
        from_ts: datetime | None = None,
        to_ts: datetime | None = None,
    ) -> list[OhlcvData]:
        """
        لیست کندل‌ها برای یک نماد و تایم‌فریم خاص — مرتب صعودی
        بر اساس timestamp (قدیمی‌ترین اول).

        از ایندکس Critical (idx_ohlcv_symbol_tf_ts) برای کارایی
        استفاده می‌کند (سند ۵.۷).

        Args:
            symbol_id: شناسه نماد (FK→Symbols)
            timeframe: تایم‌فریم (مثلاً "1d", "1h", "15m")
            limit: حداکثر تعداد
            offset: شروع از کجا (برای pagination)
            from_ts: فقط کندل‌های با timestamp >= from_ts
            to_ts: فقط کندل‌های با timestamp <= to_ts

        Returns:
            list[OhlcvData] — می‌تواند خالی باشد
        """
        stmt = (
            select(OhlcvData)
            .where(
                OhlcvData.symbol_id == symbol_id,
                OhlcvData.timeframe == timeframe,
            )
            .order_by(OhlcvData.timestamp.asc())
        )
        if from_ts is not None:
            stmt = stmt.where(OhlcvData.timestamp >= from_ts)
        if to_ts is not None:
            stmt = stmt.where(OhlcvData.timestamp <= to_ts)

        stmt = stmt.offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count_by_symbol_and_timeframe(
        self,
        symbol_id: int,
        timeframe: str,
        from_ts: datetime | None = None,
        to_ts: datetime | None = None,
    ) -> int:
        """شمارش کل کندل‌های مطابق فیلتر — برای pagination metadata."""
        stmt = (
            select(func.count())
            .select_from(OhlcvData)
            .where(
                OhlcvData.symbol_id == symbol_id,
                OhlcvData.timeframe == timeframe,
            )
        )
        if from_ts is not None:
            stmt = stmt.where(OhlcvData.timestamp >= from_ts)
        if to_ts is not None:
            stmt = stmt.where(OhlcvData.timestamp <= to_ts)

        result = await self.db.execute(stmt)
        return int(result.scalar_one())
