# -*- coding: utf-8 -*-
"""
اسکریپت ۱۸ — DataSource Layer
ساخت base.py + excel_source.py + schemas/ohlcv.py
"""

import sys
from pathlib import Path

try:
    from colorama import Fore, Style
    from colorama import init as _colorama_init

    _colorama_init(autoreset=True)
    GREEN, RED, YELLOW, CYAN, BOLD, RESET = (
        Fore.GREEN,
        Fore.RED,
        Fore.YELLOW,
        Fore.CYAN,
        Style.BRIGHT,
        Style.RESET_ALL,
    )
except ImportError:
    GREEN = RED = YELLOW = CYAN = BOLD = RESET = ""


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
DATA_SOURCES_DIR = BACKEND_DIR / "app" / "infrastructure" / "data_sources"
SCHEMAS_DIR = BACKEND_DIR / "app" / "schemas"


# ============================================================
# محتوای فایل‌ها
# ============================================================

BASE_PY = '''# -*- coding: utf-8 -*-
"""
DataSource — کلاس انتزاعی پایه برای منابع داده OHLCV

این لایه به ما اجازه می‌دهد منابع داده مختلف (Excel، ccxt API،
WebSocket، فایل CSV، ...) را پشت یک interface واحد قرار دهیم.

نحوه افزودن منبع داده جدید:
    1. کلاس جدیدی بساز که از DataSource ارث ببرد
    2. متد read_ohlcv را پیاده‌سازی کن
    3. تست بنویس
"""

from abc import ABC, abstractmethod
from typing import Any

from app.schemas.ohlcv import OhlcvRowSchema, OhlcvImportResult


class DataSource(ABC):
    """کلاس انتزاعی پایه برای منابع داده OHLCV."""

    @abstractmethod
    def read_ohlcv(self, source: Any, **kwargs: Any) -> OhlcvImportResult:
        """
        خواندن داده‌های OHLCV از منبع و تبدیل به ساختار استاندارد.

        Args:
            source: منبع داده (مسیر فایل، URL، object، ...)
            **kwargs: پارامترهای اختیاری مخصوص هر منبع

        Returns:
            OhlcvImportResult حاوی:
              - rows: لیست OhlcvRowSchema
              - symbol_info: اطلاعات نماد (symbol, base_asset, quote_asset)
              - timeframe: تایم‌فریم
              - source_metadata: متادیتای خام منبع (برای debug)
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def name(self) -> str:
        """نام منبع داده (مثلاً 'excel', 'binance_api')."""
        raise NotImplementedError
'''


EXCEL_SOURCE_PY = '''# -*- coding: utf-8 -*-
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
from app.infrastructure.data_sources.binance_mappings import (
    get_symbol_info,
    get_timeframe,
)
from app.schemas.ohlcv import OhlcvRowSchema, OhlcvImportResult

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
            symbol_info["symbol"], timeframe, len(df),
        )

        # تبدیل ردیف‌ها به OhlcvRowSchema
        rows: list[OhlcvRowSchema] = []
        for idx, record in df.iterrows():
            # تبدیل OpenTime (Unix ms) → datetime UTC
            ts = datetime.fromtimestamp(
                int(record["OpenTime"]) / 1000,
                tz=timezone.utc,
            )
            rows.append(OhlcvRowSchema(
                row_index=int(idx),  # از صفر — index pandas
                timestamp=ts,
                open=float(record["OpenPrice"]),
                high=float(record["HighPrice"]),
                low=float(record["LowPrice"]),
                close=float(record["ClosePrice"]),
                volume=float(record["Volume"]),
            ))

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
'''


DATA_SOURCES_INIT = '''# -*- coding: utf-8 -*-
"""
DataSource Layer — منابع داده OHLCV
"""

from app.infrastructure.data_sources.base import DataSource
from app.infrastructure.data_sources.excel_source import ExcelDataSource

__all__ = ["DataSource", "ExcelDataSource"]
'''


OHLCV_SCHEMA_PY = '''# -*- coding: utf-8 -*-
"""
Pydantic schemas برای OHLCV
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class OhlcvRowSchema(BaseModel):
    """یک ردیف داده OHLCV — مستقل از منبع."""

    model_config = ConfigDict(from_attributes=True)

    row_index: int = Field(..., ge=0, description="شماره ردیف از صفر")
    timestamp: datetime = Field(..., description="زمان شروع کندل (UTC)")
    open: float = Field(..., gt=0)
    high: float = Field(..., gt=0)
    low: float = Field(..., gt=0)
    close: float = Field(..., gt=0)
    volume: float = Field(..., ge=0)


class OhlcvImportResult(BaseModel):
    """نتیجه import یک فایل/منبع OHLCV."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    rows: list[OhlcvRowSchema]
    symbol_info: dict[str, str] = Field(
        ..., description="symbol, base_asset, quote_asset, market_type",
    )
    timeframe: str
    source_metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def row_count(self) -> int:
        return len(self.rows)
'''


SCHEMAS_INIT = '''# -*- coding: utf-8 -*-
"""Pydantic schemas — DTO های پروژه."""

from app.schemas.ohlcv import OhlcvRowSchema, OhlcvImportResult

__all__ = ["OhlcvRowSchema", "OhlcvImportResult"]
'''


# ============================================================
# توابع کمکی
# ============================================================
def info(msg):
    print(f"{CYAN}ℹ {msg}{RESET}")


def success(msg):
    print(f"{GREEN}✅ {msg}{RESET}")


def warn(msg):
    print(f"{YELLOW}⚠ {msg}{RESET}")


def err(msg):
    print(f"{RED}❌ {msg}{RESET}")


def header(msg):
    line = "=" * 60
    print(f"\n{BOLD}{CYAN}{line}{RESET}")
    print(f"{BOLD}{CYAN}{msg}{RESET}")
    print(f"{BOLD}{CYAN}{line}{RESET}\n")


def write_file(path: Path, content: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_text(encoding="utf-8") == content:
            info(f"بدون تغییر:  {path.relative_to(PROJECT_ROOT)}")
            return "unchanged"
        path.write_text(content, encoding="utf-8")
        warn(f"بازنویسی:    {path.relative_to(PROJECT_ROOT)}")
        return "updated"
    path.write_text(content, encoding="utf-8")
    success(f"ساخت جدید:   {path.relative_to(PROJECT_ROOT)}")
    return "created"


def main() -> int:
    header("اسکریپت ۱۸ — DataSource Layer")

    files = [
        (SCHEMAS_DIR / "ohlcv.py", OHLCV_SCHEMA_PY),
        (SCHEMAS_DIR / "__init__.py", SCHEMAS_INIT),
        (DATA_SOURCES_DIR / "base.py", BASE_PY),
        (DATA_SOURCES_DIR / "excel_source.py", EXCEL_SOURCE_PY),
        (DATA_SOURCES_DIR / "__init__.py", DATA_SOURCES_INIT),
    ]

    for path, content in files:
        write_file(path, content)

    print()
    header("گام بعدی — تست ایمپورت")

    print(f"{BOLD}📍 Tab: 2 scripts{RESET}\n")
    print(
        f"  {BOLD}python -c \"from app.schemas import OhlcvRowSchema, OhlcvImportResult; from app.infrastructure.data_sources import DataSource, ExcelDataSource; print('OK')\"{RESET}\n"
    )
    info("خروجی: 'OK'")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
