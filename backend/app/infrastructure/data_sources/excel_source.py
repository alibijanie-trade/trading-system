# -*- coding: utf-8 -*-
"""
ExcelDataSource — خواندن فایل اکسل بایننس
================================================================
فرمت ورودی (export بایننس):
  ستون‌های الزامی: stockID, IntervalID, OpenTime,
                  OpenPrice, HighPrice, LowPrice, ClosePrice, Volume
  ستون‌های اختیاری (فعلاً نادیده): QuoteAssetVolume, NumberOfTrades, ...

شناسایی نماد و تایم‌فریم:
  - stockID  → از STOCK_ID_TO_SYMBOL (مثلاً 294 → BTC/USDT)
  - IntervalID → از INTERVAL_ID_TO_TIMEFRAME (مثلاً 12 → 1d)
================================================================
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
from app.core.exceptions import BusinessLogicError, ValidationError
from app.core.logging import get_logger
from app.infrastructure.data_sources.base import DataSource
from app.infrastructure.data_sources.binance_mappings import get_symbol_info, get_timeframe
from app.schemas.ohlcv import OhlcvImportResult, OhlcvRowSchema

logger = get_logger(__name__)


# ستون‌های الزامی در فایل اکسل بایننس
REQUIRED_COLUMNS = [
    "stockID",
    "IntervalID",
    "OpenTime",
    "OpenPrice",
    "HighPrice",
    "LowPrice",
    "ClosePrice",
    "Volume",
]


class ExcelDataSource(DataSource):
    """منبع داده Excel (فرمت export بایننس)."""

    @property
    def name(self) -> str:
        return "excel"

    def read_ohlcv(self, source: Any, **kwargs: Any) -> OhlcvImportResult:
        """
        خواندن فایل اکسل بایننس و تبدیل به OhlcvRowSchema.

        Args:
            source: مسیر فایل (str یا Path)
            **kwargs:
                sheet_name (str|int): نام/ایندکس sheet (پیش‌فرض اول)

        Raises:
            ValidationError: فایل وجود ندارد یا فرمت اشتباه
            BusinessLogicError: stockID/IntervalID در mapping نباشد
        """
        path = Path(source)
        if not path.exists():
            raise ValidationError(
                message=f"فایل اکسل پیدا نشد: {path}",
                code="EXCEL_FILE_NOT_FOUND",
            )

        sheet_name = kwargs.get("sheet_name", 0)
        logger.info("خواندن فایل اکسل: %s (sheet=%s)", path.name, sheet_name)

        # خواندن فایل
        try:
            df = pd.read_excel(path, sheet_name=sheet_name)
        except Exception as e:
            raise ValidationError(
                message=f"خطا در خواندن فایل اکسل: {e}",
                code="EXCEL_READ_ERROR",
            ) from e

        # اعتبارسنجی ستون‌های الزامی
        missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            raise ValidationError(
                message=f"ستون‌های الزامی در فایل نیست: {missing}",
                code="EXCEL_MISSING_COLUMNS",
                details={"missing": missing, "found": list(df.columns)},
            )

        if df.empty:
            raise ValidationError(
                message="فایل اکسل خالی است",
                code="EXCEL_EMPTY",
            )

        # شناسایی نماد و تایم‌فریم (یک‌بار، از ردیف اول)
        stock_ids = df["stockID"].unique()
        interval_ids = df["IntervalID"].unique()

        if len(stock_ids) > 1:
            raise BusinessLogicError(
                message=f"فایل شامل چند stockID است: {list(stock_ids)}. هر فایل باید فقط یک نماد داشته باشد.",
                code="EXCEL_MULTIPLE_STOCKS",
            )
        if len(interval_ids) > 1:
            raise BusinessLogicError(
                message=f"فایل شامل چند IntervalID است: {list(interval_ids)}. هر فایل باید فقط یک تایم‌فریم داشته باشد.",
                code="EXCEL_MULTIPLE_INTERVALS",
            )

        stock_id = int(stock_ids[0])
        interval_id = int(interval_ids[0])

        try:
            symbol_info = get_symbol_info(stock_id)
        except KeyError as e:
            raise BusinessLogicError(
                message=str(e),
                code="UNKNOWN_STOCK_ID",
            ) from e

        try:
            timeframe = get_timeframe(interval_id)
        except KeyError as e:
            raise BusinessLogicError(
                message=str(e),
                code="UNKNOWN_INTERVAL_ID",
            ) from e

        logger.info(
            "نماد: %s | تایم‌فریم: %s | تعداد رکورد: %d",
            symbol_info["symbol"],
            timeframe,
            len(df),
        )

        # تبدیل ردیف‌ها به OhlcvRowSchema
        rows: list[OhlcvRowSchema] = []
        for idx, record in df.iterrows():
            # تبدیل OpenTime (Unix ms) → datetime UTC
            ts = datetime.fromtimestamp(
                int(record["OpenTime"]) / 1000,
                tz=timezone.utc,
            )
            rows.append(
                OhlcvRowSchema(
                    row_index=int(idx),  # از صفر — index pandas
                    timestamp=ts,
                    open=float(record["OpenPrice"]),
                    high=float(record["HighPrice"]),
                    low=float(record["LowPrice"]),
                    close=float(record["ClosePrice"]),
                    volume=float(record["Volume"]),
                )
            )

        return OhlcvImportResult(
            rows=rows,
            symbol_info=symbol_info,
            timeframe=timeframe,
            source_metadata={
                "file_name": path.name,
                "file_size_bytes": path.stat().st_size,
                "stock_id": stock_id,
                "interval_id": interval_id,
                "total_rows": len(rows),
                "first_timestamp": rows[0].timestamp.isoformat() if rows else None,
                "last_timestamp": rows[-1].timestamp.isoformat() if rows else None,
            },
        )
