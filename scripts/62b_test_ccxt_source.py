"""
62b_test_ccxt_source.py — تست CCXTDataSource با AsyncMock

۵ تست:
1. name property = 'ccxt_binance'
2. exchange_id نامعتبر → ValueError
3. basic fetch — AsyncMock mocked، result rows/symbol_info صحیح، fetch_ohlcv با kwargs درست
4. BadSymbol → ValidationError با code CCXT_BAD_SYMBOL
5. metadata در source_metadata صحیح (exchange، fetch_params، total_rows)

هیچ network call واقعی انجام نمی‌شود — همه با AsyncMock شبیه‌سازی.
"""

import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))


# Sample OHLCV data — معادل خروجی binance fetch_ohlcv
# format: [timestamp_ms, open, high, low, close, volume]
SAMPLE_OHLCV = [
    [1700000000000, 35000.0, 36000.0, 34500.0, 35800.0, 1234.5],
    [1700086400000, 35800.0, 36500.0, 35500.0, 36200.0, 987.3],
    [1700172800000, 36200.0, 37000.0, 36000.0, 36800.0, 1500.0],
]


def t_name_property() -> bool:
    """name property = 'ccxt_binance'."""
    from app.infrastructure.data_sources.ccxt_source import CCXTDataSource

    source = CCXTDataSource(exchange_id="binance")
    if source.name != "ccxt_binance":
        print(f"[FAIL] t_name_property: name={source.name!r} (expected 'ccxt_binance')")
        return False
    print("[OK] t_name_property: name='ccxt_binance'")
    return True


def t_unsupported_exchange() -> bool:
    """exchange_id نامعتبر → ValueError."""
    from app.infrastructure.data_sources.ccxt_source import CCXTDataSource

    try:
        CCXTDataSource(exchange_id="bogus_exchange")
        print("[FAIL] t_unsupported_exchange: ValueError not raised")
        return False
    except ValueError:
        print("[OK] t_unsupported_exchange: ValueError raised correctly")
        return True


async def _basic_fetch() -> bool:
    from app.infrastructure.data_sources.ccxt_source import CCXTDataSource

    source = CCXTDataSource(exchange_id="binance")

    # Inject mocked exchange BEFORE first call (bypasses _get_exchange creation)
    mock_exchange = AsyncMock()
    mock_exchange.fetch_ohlcv = AsyncMock(return_value=SAMPLE_OHLCV)
    mock_exchange.close = AsyncMock()
    source._exchange = mock_exchange

    result = await source.read_ohlcv_async("BTC/USDT", timeframe="1d", limit=3)

    # تأیید rows
    if len(result.rows) != 3:
        print(f"[FAIL] t_basic_fetch: expected 3 rows, got {len(result.rows)}")
        return False
    if result.rows[0].open != 35000.0 or result.rows[0].close != 35800.0:
        print(f"[FAIL] t_basic_fetch: row[0] OHLC mismatch")
        return False

    # تأیید symbol_info
    si = result.symbol_info
    if si["symbol"] != "BTC/USDT" or si["base_asset"] != "BTC" or si["quote_asset"] != "USDT":
        print(f"[FAIL] t_basic_fetch: symbol_info mismatch: {si}")
        return False

    if result.timeframe != "1d":
        print(f"[FAIL] t_basic_fetch: timeframe={result.timeframe} (expected '1d')")
        return False

    # تأیید fetch_ohlcv با kwargs درست call شد
    mock_exchange.fetch_ohlcv.assert_called_once_with(
        symbol="BTC/USDT",
        timeframe="1d",
        since=None,
        limit=3,
    )

    await source.close()
    print("[OK] t_basic_fetch: 3 rows, OHLC values, symbol_info, fetch_ohlcv args")
    return True


def t_basic_fetch() -> bool:
    return asyncio.run(_basic_fetch())


async def _bad_symbol() -> bool:
    import ccxt.async_support as ccxt_async
    from app.core.exceptions import ValidationError
    from app.infrastructure.data_sources.ccxt_source import CCXTDataSource

    source = CCXTDataSource(exchange_id="binance")
    mock_exchange = AsyncMock()
    mock_exchange.fetch_ohlcv = AsyncMock(side_effect=ccxt_async.BadSymbol("FAKE/USDT not listed"))
    mock_exchange.close = AsyncMock()
    source._exchange = mock_exchange

    try:
        await source.read_ohlcv_async("FAKE/USDT")
        print("[FAIL] t_bad_symbol: ValidationError not raised")
        return False
    except ValidationError as e:
        if getattr(e, "code", None) != "CCXT_BAD_SYMBOL":
            print(f"[FAIL] t_bad_symbol: wrong code: {getattr(e, 'code', None)}")
            return False
        await source.close()
        print("[OK] t_bad_symbol: ValidationError with code CCXT_BAD_SYMBOL")
        return True


def t_bad_symbol() -> bool:
    return asyncio.run(_bad_symbol())


async def _metadata() -> bool:
    from app.infrastructure.data_sources.ccxt_source import CCXTDataSource

    source = CCXTDataSource(exchange_id="binance")
    mock_exchange = AsyncMock()
    mock_exchange.fetch_ohlcv = AsyncMock(return_value=SAMPLE_OHLCV)
    mock_exchange.close = AsyncMock()
    source._exchange = mock_exchange

    result = await source.read_ohlcv_async("ETH/USDT", timeframe="1h", since=1700000000000, limit=3)

    md = result.source_metadata
    if md.get("exchange") != "binance":
        print(f"[FAIL] t_metadata: exchange={md.get('exchange')}")
        return False
    fp = md.get("fetch_params") or {}
    if fp.get("since") != 1700000000000 or fp.get("limit") != 3:
        print(f"[FAIL] t_metadata: fetch_params={fp}")
        return False
    if md.get("total_rows") != 3:
        print(f"[FAIL] t_metadata: total_rows={md.get('total_rows')}")
        return False
    if not md.get("first_timestamp") or not md.get("last_timestamp"):
        print("[FAIL] t_metadata: timestamps missing")
        return False

    await source.close()
    print(f"[OK] t_metadata: exchange={md['exchange']}, total_rows={md['total_rows']}")
    return True


def t_metadata() -> bool:
    return asyncio.run(_metadata())


def main() -> int:
    tests = [
        t_name_property,
        t_unsupported_exchange,
        t_basic_fetch,
        t_bad_symbol,
        t_metadata,
    ]
    print(f"=== Running {len(tests)} tests ===")
    print()
    results = []
    for t in tests:
        try:
            results.append(t())
        except Exception as e:
            print(f"[ERROR] {t.__name__}: {type(e).__name__}: {e}")
            results.append(False)
    print()
    passed = sum(results)
    total = len(results)
    print(f"=== {passed}/{total} pass ===")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
