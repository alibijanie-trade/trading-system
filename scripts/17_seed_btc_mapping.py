# -*- coding: utf-8 -*-
"""
اسکریپت ۱۷ — Seed نماد BTCUSDT + Mapping Constants
"""

import asyncio
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

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


# ============================================================
# محتوای فایل mapping
# ============================================================
DATA_SOURCES_DIR = BACKEND_DIR / "app" / "infrastructure" / "data_sources"
MAPPINGS_PY = DATA_SOURCES_DIR / "binance_mappings.py"

MAPPINGS_CONTENT = '''# -*- coding: utf-8 -*-
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
'''


# ============================================================
# توابع کمکی نمایش
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


async def seed_symbol() -> None:
    """درج نماد BTC/USDT روی Exchange 'Excel'."""
    from app.infrastructure.database import AsyncSessionLocal, engine
    from app.models import Exchange, Symbol
    from sqlalchemy import select

    async with AsyncSessionLocal() as session:
        # پیدا کردن Exchange Excel
        result = await session.execute(select(Exchange).where(Exchange.name == "Excel"))
        excel_exchange = result.scalar_one_or_none()

        if excel_exchange is None:
            err("Exchange 'Excel' پیدا نشد. ابتدا اسکریپت ۱۴ را اجرا کنید.")
            await engine.dispose()
            return

        info(f"Exchange 'Excel' یافت شد (id={excel_exchange.id})")

        # چک کن نماد از قبل وجود ندارد
        result = await session.execute(
            select(Symbol).where(
                Symbol.exchange_id == excel_exchange.id,
                Symbol.symbol == "BTC/USDT",
            )
        )
        existing = result.scalar_one_or_none()

        if existing is not None:
            info(f"نماد BTC/USDT از قبل موجود است (id={existing.id})")
        else:
            sym = Symbol(
                exchange_id=excel_exchange.id,
                symbol="BTC/USDT",
                base_asset="BTC",
                quote_asset="USDT",
                market_type="spot",
                is_active=True,
            )
            session.add(sym)
            await session.flush()
            await session.refresh(sym)
            success(f"نماد BTC/USDT درج شد (id={sym.id})")

        await session.commit()

    await engine.dispose()


async def main_async() -> int:
    header("اسکریپت ۱۷ — Seed BTCUSDT + Mapping")

    # مرحله 1: ساخت binance_mappings.py
    info("[1/2] ساخت binance_mappings.py")
    write_file(MAPPINGS_PY, MAPPINGS_CONTENT)
    print()

    # مرحله 2: seed نماد در DB
    info("[2/2] درج نماد BTC/USDT در DB")
    await seed_symbol()
    print()

    # تأیید
    from app.core.config import settings
    from app.models import Exchange, Symbol
    from sqlalchemy import select
    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

    eng = create_async_engine(settings.DATABASE_URL)
    async with AsyncSession(eng) as session:
        result = await session.execute(select(Symbol, Exchange).join(Exchange))
        rows = result.all()
        info(f"Symbols در DB: {len(rows)}")
        for sym, ex in rows:
            print(f"    {GREEN}•{RESET} id={sym.id}  {ex.name}/{sym.symbol}  ({sym.market_type})")
    await eng.dispose()

    print()
    header("گام بعدی — اسکریپت ۱۸ (DataSource Layer)")
    return 0


def main() -> int:
    try:
        return asyncio.run(main_async())
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
