# -*- coding: utf-8 -*-
"""
اسکریپت ۱۶ — افزودن row_index به مدل OhlcvData + تولید Migration
"""

import sys
from pathlib import Path

try:
    from colorama import init as _colorama_init
    from colorama import Fore, Style
    _colorama_init(autoreset=True)
    GREEN, RED, YELLOW, CYAN, BOLD, RESET = (
        Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.CYAN, Style.BRIGHT, Style.RESET_ALL,
    )
except ImportError:
    GREEN = RED = YELLOW = CYAN = BOLD = RESET = ""


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
OHLCV_MODEL = BACKEND_DIR / "app" / "models" / "ohlcv_data.py"


NEW_OHLCV_DATA_PY = '''# -*- coding: utf-8 -*-
"""
مدل OhlcvData — سند ۵.۷ ⭐
================================================================
داده‌های کندل (Open/High/Low/Close/Volume) برای یک نماد در یک
تایم‌فریم خاص. این بزرگ‌ترین جدول دیتابیس خواهد بود.

ستون‌ها (سند ۵.۷ + توسعه فاز ۶):
  id, symbol_id (FK→Symbols), timeframe, timestamp (UTC),
  open, high, low, close, volume, is_closed, created_at,
  row_index (🆕 ترتیب ردیف در فایل ورودی — از صفر)

ایندکس Critical (سند ۵.۷ — قطعی):
  idx_ohlcv_symbol_tf_ts روی (symbol_id, timeframe, timestamp)
================================================================
"""

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class OhlcvData(Base):
    __tablename__ = "OhlcvData"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Symbols.id", ondelete="CASCADE"),
        nullable=False,
    )
    timeframe: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
    )
    open: Mapped[float] = mapped_column(Float, nullable=False)
    high: Mapped[float] = mapped_column(Float, nullable=False)
    low: Mapped[float] = mapped_column(Float, nullable=False)
    close: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[float] = mapped_column(Float, nullable=False)
    is_closed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    row_index: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        nullable=False,
    )

    symbol: Mapped["Symbol"] = relationship("Symbol", back_populates="ohlcv_data")

    __table_args__ = (
        Index("idx_ohlcv_symbol_tf_ts", "symbol_id", "timeframe", "timestamp"),
    )

    def __repr__(self) -> str:
        return (
            f"<OhlcvData #{self.row_index} symbol_id={self.symbol_id} "
            f"tf={self.timeframe!r} ts={self.timestamp.isoformat()} close={self.close}>"
        )
'''


def info(msg): print(f"{CYAN}ℹ {msg}{RESET}")
def success(msg): print(f"{GREEN}✅ {msg}{RESET}")
def warn(msg): print(f"{YELLOW}⚠ {msg}{RESET}")
def err(msg): print(f"{RED}❌ {msg}{RESET}")

def header(msg):
    line = "=" * 60
    print(f"\n{BOLD}{CYAN}{line}{RESET}")
    print(f"{BOLD}{CYAN}{msg}{RESET}")
    print(f"{BOLD}{CYAN}{line}{RESET}\n")


def main() -> int:
    header("اسکریپت ۱۶ — افزودن row_index به OhlcvData")

    if not OHLCV_MODEL.exists():
        err(f"مدل OhlcvData پیدا نشد: {OHLCV_MODEL}")
        return 1

    current = OHLCV_MODEL.read_text(encoding="utf-8")

    if current == NEW_OHLCV_DATA_PY:
        info("مدل OhlcvData از قبل به‌روز است.")
    else:
        backup = OHLCV_MODEL.with_suffix(".py.bak")
        backup.write_text(current, encoding="utf-8")
        OHLCV_MODEL.write_text(NEW_OHLCV_DATA_PY, encoding="utf-8")
        success("مدل OhlcvData به‌روز شد")
        info(f"بک‌آپ: {backup.name}")

    print()
    header("گام بعدی — تولید Migration و اعمال")

    print(f"{BOLD}📍 Tab: 1 backend{RESET} — uvicorn را Ctrl+C کنید\n")

    print(f"{BOLD}📍 Tab: 2 scripts{RESET}\n")
    print(f"  {BOLD}cd /d D:\\Projects\\trading-system\\backend{RESET}")
    print(f"  {BOLD}alembic revision --autogenerate -m \"add_row_index_to_ohlcv\"{RESET}\n")
    info("یک فایل migration جدید در backend/migrations/versions/ ساخته می‌شود")
    print()

    print(f"{BOLD}📍 Tab: 2 scripts{RESET} — اعمال migration\n")
    print(f"  {BOLD}alembic upgrade head{RESET}\n")
    info("خروجی: 'Running upgrade XXXX -> YYYY, add_row_index_to_ohlcv'")
    print()

    print(f"{BOLD}📍 Tab: 2 scripts{RESET} — تأیید ستون جدید\n")
    print(f"  {BOLD}python -c \"import sqlite3; c=sqlite3.connect('trading.db'); [print(r) for r in c.execute('PRAGMA table_info(OhlcvData)')]\"{RESET}\n")
    info("باید ستون row_index در لیست دیده شود")
    print()

    print(f"{BOLD}📍 Tab: 1 backend{RESET} — راه‌اندازی مجدد uvicorn\n")
    print(f"  {BOLD}uvicorn main:app --reload{RESET}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
