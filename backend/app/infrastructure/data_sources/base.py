# -*- coding: utf-8 -*-
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

from app.schemas.ohlcv import OhlcvImportResult, OhlcvRowSchema


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
