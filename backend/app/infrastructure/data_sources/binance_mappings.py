# -*- coding: utf-8 -*-
"""
نگاشت stockID و IntervalID بایننس به نماد و تایم‌فریم پروژه.

این نگاشت‌ها برای import فایل‌های اکسل بایننس استفاده می‌شوند.
در آینده می‌توان آنها را به جدول DB منتقل کرد.

ساختار قابل توسعه:
  - افزودن نماد جدید: یک ردیف به STOCK_ID_TO_SYMBOL اضافه کنید
  - افزودن timeframe جدید: یک ردیف به INTERVAL_ID_TO_TIMEFRAME اضافه کنید
"""

from typing import Final


# stockID → (symbol, base_asset, quote_asset, market_type)
STOCK_ID_TO_SYMBOL: Final[dict[int, dict[str, str]]] = {
    294: {
        "symbol": "BTC/USDT",
        "base_asset": "BTC",
        "quote_asset": "USDT",
        "market_type": "spot",
    },
    # نمونه‌های آینده:
    # 295: {"symbol": "ETH/USDT", "base_asset": "ETH", "quote_asset": "USDT", "market_type": "spot"},
    # 296: {"symbol": "BNB/USDT", "base_asset": "BNB", "quote_asset": "USDT", "market_type": "spot"},
}


# IntervalID → timeframe string
INTERVAL_ID_TO_TIMEFRAME: Final[dict[int, str]] = {
    1: "1m",
    2: "3m",
    3: "5m",
    4: "15m",
    5: "30m",
    6: "1h",
    7: "2h",
    8: "4h",
    9: "6h",
    10: "8h",
    11: "12h",
    12: "1d",
    13: "3d",
    14: "1w",
    15: "1M",
}


def get_symbol_info(stock_id: int) -> dict[str, str]:
    """دریافت اطلاعات نماد از stockID. KeyError اگر نباشد."""
    if stock_id not in STOCK_ID_TO_SYMBOL:
        raise KeyError(
            f"stockID={stock_id} در mapping تعریف نشده. "
            f"موارد تعریف‌شده: {sorted(STOCK_ID_TO_SYMBOL.keys())}"
        )
    return STOCK_ID_TO_SYMBOL[stock_id]


def get_timeframe(interval_id: int) -> str:
    """دریافت timeframe از IntervalID. KeyError اگر نباشد."""
    if interval_id not in INTERVAL_ID_TO_TIMEFRAME:
        raise KeyError(
            f"IntervalID={interval_id} در mapping تعریف نشده. "
            f"موارد تعریف‌شده: {sorted(INTERVAL_ID_TO_TIMEFRAME.keys())}"
        )
    return INTERVAL_ID_TO_TIMEFRAME[interval_id]
