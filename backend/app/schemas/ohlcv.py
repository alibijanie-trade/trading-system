# -*- coding: utf-8 -*-
"""
Pydantic Schemas برای OHLCV
================================================================
دو گروه schema:

۱) Schema های DataSource Layer (فاز ۶):
   - OhlcvRowSchema    : یک ردیف داده خام
   - OhlcvImportResult : نتیجه import یک فایل

۲) Schema های API Response (فاز ۰ — endpoint GET /ohlcv):
   - OhlcvCandleOut : یک کندل برای پاسخ API (بدون id و row_index)
   - OhlcvListData  : بخش data پاسخ GET /ohlcv/{symbol_id}
================================================================
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# Schema های DataSource Layer (فاز ۶)
# ============================================================

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


# ============================================================
# Schema های API Response (فاز ۰ — endpoint GET /ohlcv)
# ============================================================

class OhlcvCandleOut(BaseModel):
    """
    یک کندل برای پاسخ API — بدون id، symbol_id، timeframe، row_index.

    این فیلدها در سطح parent (OhlcvListData) قرار دارند تا
    payload سبک‌تر باشد.
    """

    model_config = ConfigDict(from_attributes=True)

    timestamp: datetime = Field(..., description="زمان شروع کندل (UTC)")
    open: float
    high: float
    low: float
    close: float
    volume: float


class OhlcvListData(BaseModel):
    """
    بخش data پاسخ GET /ohlcv/{symbol_id}.

    ساختار نهایی پاسخ:
        {
            "success": true,
            "message": "...",
            "data": OhlcvListData,
            "errors": null
        }
    """

    symbol_id: int
    timeframe: str
    count: int = Field(..., description="تعداد کندل در این پاسخ")
    total: int = Field(..., description="کل کندل‌های مطابق فیلتر")
    limit: int
    offset: int
    candles: list[OhlcvCandleOut]
