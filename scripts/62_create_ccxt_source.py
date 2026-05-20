"""
62_create_ccxt_source.py — ساخت CCXTDataSource skeleton

طبق Decision معماری G2 چت ۱۰:
- async-first با ccxt.async_support
- sync wrapper برای CLI/tests
- lazy exchange initialization
- enableRateLimit=True
- error mapping به ValidationError/BusinessLogicError

Idempotent: اگر فایل قبلاً موجود است، skip.
Read-back verify: فایل ساخته شد + شامل کلاس CCXTDataSource است.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET_FILE = ROOT / "backend" / "app" / "infrastructure" / "data_sources" / "ccxt_source.py"


CCXT_SOURCE_CONTENT = '''# -*- coding: utf-8 -*-
"""
CCXTDataSource — منبع داده OHLCV مبتنی بر ccxt.async_support

پشتیبانی فعلی: binance (spot)
آینده: kraken, coinbase, kucoin, ...

طراحی (Decision معماری چت ۱۰):
1. async-first: read_ohlcv_async از ccxt.async_support استفاده می‌کند
2. sync wrapper: read_ohlcv فقط برای CLI/batch (نه FastAPI handler)
3. Lazy exchange initialization: instance ccxt در اولین استفاده ساخته می‌شود
4. enableRateLimit=True: rate limiting داخلی ccxt
5. Error mapping: BadSymbol → ValidationError، بقیه → BusinessLogicError

نحوه استفاده در FastAPI handler:
    async def fetch():
        source = CCXTDataSource(exchange_id="binance")
        try:
            result = await source.read_ohlcv_async(
                "BTC/USDT", timeframe="1d", limit=100
            )
            return result
        finally:
            await source.close()
"""

import asyncio
from datetime import datetime, timezone
from typing import Any

import ccxt.async_support as ccxt_async

from app.core.exceptions import BusinessLogicError, ValidationError
from app.core.logging import get_logger
from app.infrastructure.data_sources.base import DataSource
from app.schemas.ohlcv import OhlcvImportResult, OhlcvRowSchema

logger = get_logger(__name__)


# Exchange هایی که فعلاً پشتیبانی می‌شوند.
# افزودن جدید: نام آن را در ccxt.async_support بررسی کنید و در این tuple اضافه کنید.
SUPPORTED_EXCHANGES: tuple[str, ...] = ("binance",)


class CCXTDataSource(DataSource):
    """منبع داده OHLCV مبتنی بر ccxt.async_support."""

    def __init__(
        self,
        exchange_id: str = "binance",
        **exchange_kwargs: Any,
    ) -> None:
        """
        Args:
            exchange_id: نام exchange در ccxt (مثلاً 'binance')
            **exchange_kwargs: تنظیمات اضافی برای ccxt (مثلاً apiKey, secret).
                enableRateLimit به‌صورت پیش‌فرض True تنظیم می‌شود.

        Raises:
            ValueError: exchange_id پشتیبانی نمی‌شود
        """
        if exchange_id not in SUPPORTED_EXCHANGES:
            raise ValueError(
                f"exchange_id='{exchange_id}' is not supported. "
                f"Supported: {SUPPORTED_EXCHANGES}"
            )

        self.exchange_id = exchange_id
        self._exchange_class = getattr(ccxt_async, exchange_id)
        self._exchange_config: dict[str, Any] = {
            "enableRateLimit": True,
            **exchange_kwargs,
        }
        # lazy: در اولین فراخوانی async ساخته می‌شود
        self._exchange: Any = None

    @property
    def name(self) -> str:
        return f"ccxt_{self.exchange_id}"

    async def _get_exchange(self) -> Any:
        """ساخت lazy exchange instance (نیاز به event loop)."""
        if self._exchange is None:
            self._exchange = self._exchange_class(self._exchange_config)
        return self._exchange

    async def close(self) -> None:
        """بستن aiohttp session داخلی ccxt — مهم برای cleanup."""
        if self._exchange is not None:
            await self._exchange.close()
            self._exchange = None

    async def read_ohlcv_async(
        self,
        source: Any,
        **kwargs: Any,
    ) -> OhlcvImportResult:
        """
        خواندن کندل OHLCV از exchange با ccxt.async_support.

        Args:
            source: symbol به فرمت ccxt (مثلاً 'BTC/USDT')
            **kwargs:
                timeframe (str): پیش‌فرض '1d'
                    binance: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
                since (int | None): timestamp شروع به Unix ms.
                    None یعنی آخرین کندل‌ها.
                limit (int): تعداد کندل (پیش‌فرض 500، سقف binance: 1000)

        Returns:
            OhlcvImportResult با rows + symbol_info + timeframe + source_metadata

        Raises:
            ValidationError(CCXT_BAD_SYMBOL): symbol در exchange نیست
            BusinessLogicError(CCXT_FETCH_ERROR): سایر خطاهای exchange/network
        """
        symbol = str(source)
        timeframe = kwargs.get("timeframe", "1d")
        since = kwargs.get("since", None)
        limit = kwargs.get("limit", 500)

        logger.info(
            "fetch_ohlcv: exchange=%s symbol=%s tf=%s since=%s limit=%s",
            self.exchange_id, symbol, timeframe, since, limit,
        )

        exchange = await self._get_exchange()

        try:
            ohlcv_data = await exchange.fetch_ohlcv(
                symbol=symbol,
                timeframe=timeframe,
                since=since,
                limit=limit,
            )
        except ccxt_async.BadSymbol as e:
            raise ValidationError(
                message=f"symbol نامعتبر در {self.exchange_id}: {symbol}",
                code="CCXT_BAD_SYMBOL",
            ) from e
        except Exception as e:
            raise BusinessLogicError(
                message=f"خطا در fetch_ohlcv از {self.exchange_id}: {e}",
                code="CCXT_FETCH_ERROR",
            ) from e

        # تبدیل [ts_ms, o, h, l, c, v] به OhlcvRowSchema
        rows: list[OhlcvRowSchema] = []
        for idx, candle in enumerate(ohlcv_data):
            ts = datetime.fromtimestamp(candle[0] / 1000, tz=timezone.utc)
            rows.append(
                OhlcvRowSchema(
                    row_index=idx,
                    timestamp=ts,
                    open=float(candle[1]),
                    high=float(candle[2]),
                    low=float(candle[3]),
                    close=float(candle[4]),
                    volume=float(candle[5]),
                )
            )

        # symbol_info — ccxt symbols معمولاً 'BASE/QUOTE'
        if "/" in symbol:
            base, quote = symbol.split("/", 1)
        else:
            base, quote = symbol, ""

        return OhlcvImportResult(
            rows=rows,
            symbol_info={
                "symbol": symbol,
                "base_asset": base,
                "quote_asset": quote,
                "market_type": "spot",
            },
            timeframe=timeframe,
            source_metadata={
                "exchange": self.exchange_id,
                "fetch_params": {
                    "since": since,
                    "limit": limit,
                },
                "total_rows": len(rows),
                "first_timestamp": rows[0].timestamp.isoformat() if rows else None,
                "last_timestamp": rows[-1].timestamp.isoformat() if rows else None,
            },
        )

    def read_ohlcv(
        self,
        source: Any,
        **kwargs: Any,
    ) -> OhlcvImportResult:
        """
        Sync wrapper برای read_ohlcv_async.

        ⚠️ توجه (M69 احتمالی): این متد از asyncio.run() استفاده می‌کند.
        در محیط async (FastAPI handler) با خطای
        'asyncio.run() cannot be called from a running event loop' crash می‌کند.

        فقط در: CLI scripts، batch jobs، unit tests استفاده شود.
        در FastAPI handler از read_ohlcv_async استفاده کنید.
        """
        try:
            return asyncio.run(self.read_ohlcv_async(source, **kwargs))
        finally:
            # asyncio.run() loop جدید می‌سازد و در پایان آن را می‌بندد،
            # بنابراین exchange instance قبلی dead است.
            self._exchange = None
'''


def main() -> int:
    if TARGET_FILE.exists():
        size = TARGET_FILE.stat().st_size
        print(f"[SKIP] {TARGET_FILE.name} already exists ({size} bytes)")
        print("       حذف دستی برای re-generate")
        return 0

    # ساخت directory اگر نباشد (احتمال صفر — موجود است)
    TARGET_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Write
    TARGET_FILE.write_text(CCXT_SOURCE_CONTENT, encoding="utf-8")

    # Read-back verify
    if not TARGET_FILE.exists():
        print(f"[FAIL] file not created: {TARGET_FILE}")
        return 1

    verify = TARGET_FILE.read_text(encoding="utf-8")
    if "class CCXTDataSource" not in verify:
        print("[FAIL] class CCXTDataSource missing in created file")
        return 2

    if "async def read_ohlcv_async" not in verify:
        print("[FAIL] read_ohlcv_async missing")
        return 3

    size = TARGET_FILE.stat().st_size
    print(f"[OK] created {TARGET_FILE.name} ({size} bytes)")
    print()
    print("Next: python scripts/62b_test_ccxt_source.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
