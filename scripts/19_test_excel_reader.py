# -*- coding: utf-8 -*-
"""
اسکریپت ۱۹ — تست ExcelDataSource + درج کندل‌ها در DB
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
DATA_DIR = PROJECT_ROOT / "data" / "excel_imports"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


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


async def main_async(excel_file: Path) -> int:
    from app.infrastructure.data_sources import ExcelDataSource
    from app.infrastructure.database import AsyncSessionLocal, engine
    from app.models import Exchange, OhlcvData, Symbol
    from sqlalchemy import delete, select

    header(f"اسکریپت ۱۹ — Import فایل اکسل به DB")
    info(f"فایل: {excel_file}")
    print()

    # ===== مرحله 1: خواندن فایل اکسل =====
    info("[1/4] خواندن و parse فایل اکسل")
    source = ExcelDataSource()
    try:
        result = source.read_ohlcv(excel_file)
    except Exception as e:
        err(f"خطا در خواندن: {e}")
        return 1

    success(f"تعداد ردیف: {result.row_count}")
    info(f"نماد:        {result.symbol_info['symbol']}")
    info(f"تایم‌فریم:    {result.timeframe}")
    info(
        f"بازه زمانی:  {result.source_metadata['first_timestamp']}  →  {result.source_metadata['last_timestamp']}"
    )

    # نمایش 3 ردیف اول و 3 ردیف آخر
    print()
    info("سه ردیف اول:")
    for r in result.rows[:3]:
        print(
            f"  #{r.row_index:4d}  {r.timestamp.isoformat()}  O={r.open:>10.2f}  H={r.high:>10.2f}  L={r.low:>10.2f}  C={r.close:>10.2f}  V={r.volume:>12.4f}"
        )
    info("سه ردیف آخر:")
    for r in result.rows[-3:]:
        print(
            f"  #{r.row_index:4d}  {r.timestamp.isoformat()}  O={r.open:>10.2f}  H={r.high:>10.2f}  L={r.low:>10.2f}  C={r.close:>10.2f}  V={r.volume:>12.4f}"
        )
    print()

    # ===== مرحله 2: پیدا کردن symbol_id =====
    info("[2/4] پیدا کردن symbol_id در DB")
    async with AsyncSessionLocal() as session:
        stmt = (
            select(Symbol)
            .join(Exchange)
            .where(
                Symbol.symbol == result.symbol_info["symbol"],
                Exchange.name == "Excel",
            )
        )
        sym_result = await session.execute(stmt)
        symbol = sym_result.scalar_one_or_none()

        if symbol is None:
            err(f"نماد {result.symbol_info['symbol']} روی Exchange 'Excel' در DB نیست.")
            err("ابتدا اسکریپت ۱۷ را اجرا کنید.")
            await engine.dispose()
            return 1

        success(f"symbol_id = {symbol.id}")

        # ===== مرحله 3: پاک‌سازی داده‌های قبلی این نماد/تایم‌فریم =====
        info(
            f"[3/4] پاک‌سازی داده‌های قبلی {result.symbol_info['symbol']}/{result.timeframe} (در صورت وجود)"
        )
        del_stmt = delete(OhlcvData).where(
            OhlcvData.symbol_id == symbol.id,
            OhlcvData.timeframe == result.timeframe,
        )
        del_result = await session.execute(del_stmt)
        deleted = del_result.rowcount
        if deleted > 0:
            warn(f"حذف شد: {deleted} ردیف قبلی")
        else:
            info("هیچ ردیف قبلی نبود")

        # ===== مرحله 4: درج در DB =====
        info(f"[4/4] درج {result.row_count} ردیف کندل در DB...")

        ohlcv_objects = [
            OhlcvData(
                symbol_id=symbol.id,
                timeframe=result.timeframe,
                timestamp=r.timestamp,
                open=r.open,
                high=r.high,
                low=r.low,
                close=r.close,
                volume=r.volume,
                is_closed=True,
                row_index=r.row_index,
            )
            for r in result.rows
        ]
        session.add_all(ohlcv_objects)
        await session.commit()
        success(f"درج موفق: {len(ohlcv_objects)} ردیف")

    await engine.dispose()
    print()

    # ===== تأیید نهایی =====
    from app.core.config import settings
    from sqlalchemy import func
    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

    eng = create_async_engine(settings.DATABASE_URL)
    async with AsyncSession(eng) as session:
        count_stmt = select(func.count()).select_from(OhlcvData)
        result = await session.execute(count_stmt)
        total = result.scalar_one()

        # کمترین و بیشترین timestamp
        min_stmt = select(func.min(OhlcvData.timestamp), func.max(OhlcvData.timestamp))
        result = await session.execute(min_stmt)
        min_ts, max_ts = result.one()

        # یک نمونه (ردیف ۰)
        sample_stmt = select(OhlcvData).where(OhlcvData.row_index == 0).limit(1)
        result = await session.execute(sample_stmt)
        sample = result.scalar_one_or_none()

    await eng.dispose()

    header("خلاصه")
    info(f"تعداد کل کندل در DB:  {total}")
    info(f"اولین timestamp:      {min_ts}")
    info(f"آخرین timestamp:      {max_ts}")
    if sample:
        info(f"نمونه ردیف row_index=0:")
        print(f"    id={sample.id}  ts={sample.timestamp.isoformat()}")
        print(
            f"    O={sample.open}  H={sample.high}  L={sample.low}  C={sample.close}  V={sample.volume}"
        )

    print()
    success("🎉 تست عملی Excel Reader موفق! زیرگام ۶ کامل شد.")
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        err("استفاده: python scripts\\19_test_excel_reader.py <مسیر-فایل-اکسل>")
        err(
            "مثال:  python scripts\\19_test_excel_reader.py D:\\path\\to\\btcusdt-daily-20220426.xlsx"
        )
        return 1

    excel_file = Path(sys.argv[1])
    if not excel_file.exists():
        err(f"فایل وجود ندارد: {excel_file}")
        return 1

    try:
        return asyncio.run(main_async(excel_file))
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
