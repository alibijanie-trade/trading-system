# -*- coding: utf-8 -*-
"""
================================================================
اسکریپت ۰۸ — زیرساخت دیتابیس (Database Infrastructure)
================================================================
این اسکریپت چهار فایل را در `backend/app/infrastructure/database/`
می‌سازد یا به‌روز می‌کند:

  1. base.py     → DeclarativeBase + TimestampMixin + SoftDeleteMixin
  2. engine.py   → async engine + اعمال ۴ PRAGMA الزامی
  3. session.py  → AsyncSessionLocal + get_db() (Dependency Injection)
  4. __init__.py → export سطح بالا

نحوه اجرا (در CMD 3):
    cd D:\\Projects\\trading-system
    python scripts\\08_db_infrastructure.py

ویژگی‌ها:
  - idempotent: اجرای دوم بدون مشکل (فایل‌های بدون تغییر را دست نمی‌زند)
  - UTF-8 + colorama برای Windows CMD
  - چک پیش‌نیازها (وجود app/core/config.py)
================================================================
"""

import sys
from pathlib import Path

# ------------------------------------------------------------
# تلاش برای فعال‌سازی رنگ ANSI در Windows (colorama)
# ------------------------------------------------------------
try:
    from colorama import Fore, Style
    from colorama import init as _colorama_init

    _colorama_init(autoreset=True)
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    CYAN = Fore.CYAN
    BOLD = Style.BRIGHT
    RESET = Style.RESET_ALL
except ImportError:
    GREEN = RED = YELLOW = CYAN = BOLD = RESET = ""


# ============================================================
# مسیرها
# ============================================================
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent  # D:\Projects\trading-system
BACKEND_DIR = PROJECT_ROOT / "backend"
DB_DIR = BACKEND_DIR / "app" / "infrastructure" / "database"


# ============================================================
# محتوای فایل‌ها (به‌صورت ثابت در همین اسکریپت)
# ============================================================

BASE_PY = '''# -*- coding: utf-8 -*-
"""
Base Classes و Mixins برای مدل‌های SQLAlchemy
================================================================
این فایل پایه‌ای‌ترین کلاس‌های ORM را تعریف می‌کند که تمام مدل‌ها
از آن‌ها ارث می‌برند.

اجزا:
  - Base            → DeclarativeBase (SQLAlchemy 2.0 style)
  - TimestampMixin  → created_at + updated_at (UTC)
  - SoftDeleteMixin → is_deleted

تصمیمات معماری مرتبط:
  - سند ۵.۰  : تمام datetime ها timezone-aware و UTC ذخیره شوند
  - سند ۴.۵  : نام جداول PascalCase (Users, OhlcvData, AuditLog, ...)
  - استفاده از datetime.now(timezone.utc) — utcnow() در Python 3.12+ deprecated است
  - استفاده از Mapped[] annotation سبک SQLAlchemy 2.0
================================================================
"""

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def _utcnow() -> datetime:
    """تابع کمکی — زمان فعلی UTC به‌صورت timezone-aware."""
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    """
    کلاس پایه برای تمام مدل‌های SQLAlchemy.
    سبک SQLAlchemy 2.0 (DeclarativeBase) — جایگزین declarative_base() قدیمی.

    قرارداد نامگذاری جدول‌ها (سند ۴.۵):
      هر مدل __tablename__ خود را به‌صراحت تعریف می‌کند (مثلاً "Users").
    """
    pass


class TimestampMixin:
    """
    Mixin برای افزودن دو ستون زمان‌بندی به مدل.

    استفاده:
        class User(Base, TimestampMixin):
            __tablename__ = "Users"
            ...

    رفتار:
      - created_at : زمان درج رکورد (INSERT)
      - updated_at : زمان آخرین تغییر — در هر UPDATE خودکار به‌روز می‌شود
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        onupdate=_utcnow,
        nullable=False,
    )


class SoftDeleteMixin:
    """
    Mixin برای پشتیبانی از حذف نرم (Soft Delete).

    استفاده:
        class User(Base, TimestampMixin, SoftDeleteMixin):
            __tablename__ = "Users"
            ...

    قرارداد سند ۵.۰:
      - هرگز رکورد به‌صورت فیزیکی حذف نشود
      - فقط is_deleted = True تنظیم شود
      - Repository ها در query پیش‌فرض رکوردهای حذف‌شده را نمی‌آورند
    """

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
'''


ENGINE_PY = '''# -*- coding: utf-8 -*-
"""
Async Engine برای SQLAlchemy + SQLite
================================================================
این فایل engine اصلی برنامه را تعریف می‌کند و چهار PRAGMA الزامی را
در هر اتصال تازه به دیتابیس اعمال می‌کند.

چهار PRAGMA الزامی (سند ۳.۲ — تصمیم #13):
  1. foreign_keys = ON      → اجبار رابطه‌های FK
  2. journal_mode = WAL     → concurrency بهتر
  3. synchronous = NORMAL   → تعادل سرعت/امنیت
  4. cache_size = -64000    → ۶۴ مگابایت حافظه کش

نکته مهم اعمال PRAGMA در async:
  Event ها در async engine فقط روی sync_engine قابل ثبت‌اند.
  بنابراین از engine.sync_engine به‌جای engine استفاده می‌شود.
================================================================
"""

from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


# ============================================================
# ساخت Async Engine
# ============================================================
engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.IS_DEVELOPMENT,  # log کوئری‌ها در محیط dev
    future=True,
    # نکته: aiosqlite در پشت صحنه از sqlite3 استفاده می‌کند
    # و connection pooling سنتی برای SQLite کاربرد چندانی ندارد
)


# ============================================================
# اعمال PRAGMA ها در هر اتصال جدید
# ============================================================
@event.listens_for(engine.sync_engine, "connect")
def _set_sqlite_pragmas(dbapi_connection, connection_record) -> None:
    """
    اعمال چهار PRAGMA الزامی در هر اتصال جدید SQLite.

    این تابع توسط SQLAlchemy فراخوانی می‌شود هر بار که یک
    اتصال جدید (به‌صورت lazy) برقرار می‌شود.
    """
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("PRAGMA journal_mode = WAL")
        cursor.execute("PRAGMA synchronous = NORMAL")
        cursor.execute("PRAGMA cache_size = -64000")
        logger.debug(
            "PRAGMA های SQLite اعمال شدند: FK=ON | WAL | NORMAL | cache=64MB"
        )
    finally:
        cursor.close()


async def dispose_engine() -> None:
    """بستن engine و آزاد کردن منابع — در shutdown اپ صدا زده می‌شود."""
    await engine.dispose()
    logger.info("Async engine بسته شد.")
'''


SESSION_PY = '''# -*- coding: utf-8 -*-
"""
Session Maker + Dependency Injection برای FastAPI
================================================================
این فایل دو چیز را تعریف می‌کند:
  1. AsyncSessionLocal → کارخانه ساخت AsyncSession
  2. get_db()          → Dependency برای injection در API routes

نحوه استفاده در API route ها:

    from fastapi import Depends
    from sqlalchemy.ext.asyncio import AsyncSession
    from app.infrastructure.database import get_db

    @router.get("/users/{user_id}")
    async def get_user(
        user_id: int,
        db: AsyncSession = Depends(get_db),
    ):
        ...

قانون قفل‌شده (سند ۳.۳):
  - هیچ Query مستقیمی در api/ یا services/ نباشد
  - Query فقط در repositories/ — با دریافت session از get_db
================================================================
"""

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.logging import get_logger
from app.infrastructure.database.engine import engine

logger = get_logger(__name__)


# ============================================================
# Session Factory
# ============================================================
AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # رکوردها پس از commit قابل خواندن می‌مانند
    autoflush=False,
    autocommit=False,
)


# ============================================================
# Dependency: get_db
# ============================================================
async def get_db() -> AsyncIterator[AsyncSession]:
    """
    Dependency Injection برای دریافت یک AsyncSession در route ها.

    رفتار:
      - یک session جدید ساخته می‌شود
      - در صورت بروز هر Exception، rollback خودکار انجام می‌شود
      - در پایان (چه موفق چه ناموفق)، session بسته می‌شود (async with)
      - commit مسئولیت لایه service است (نه این تابع)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            logger.exception("خطا در session — rollback انجام شد")
            raise
'''


INIT_PY = '''# -*- coding: utf-8 -*-
"""
Database Infrastructure — export سطح بالا
================================================================
این پکیج زیرساخت دیتابیس را در اختیار سایر لایه‌ها می‌گذارد.

استفاده:
    from app.infrastructure.database import Base, engine, get_db
    from app.infrastructure.database import TimestampMixin, SoftDeleteMixin
================================================================
"""

from app.infrastructure.database.base import (
    Base,
    SoftDeleteMixin,
    TimestampMixin,
)
from app.infrastructure.database.engine import dispose_engine, engine
from app.infrastructure.database.session import AsyncSessionLocal, get_db

__all__ = [
    # Base + Mixins
    "Base",
    "TimestampMixin",
    "SoftDeleteMixin",
    # Engine
    "engine",
    "dispose_engine",
    # Session
    "AsyncSessionLocal",
    "get_db",
]
'''


# ============================================================
# توابع کمکی نمایش
# ============================================================


def info(msg: str) -> None:
    print(f"{CYAN}ℹ {msg}{RESET}")


def success(msg: str) -> None:
    print(f"{GREEN}✅ {msg}{RESET}")


def warn(msg: str) -> None:
    print(f"{YELLOW}⚠ {msg}{RESET}")


def err(msg: str) -> None:
    print(f"{RED}❌ {msg}{RESET}")


def header(msg: str) -> None:
    line = "=" * 60
    print(f"\n{BOLD}{CYAN}{line}{RESET}")
    print(f"{BOLD}{CYAN}{msg}{RESET}")
    print(f"{BOLD}{CYAN}{line}{RESET}\n")


# ============================================================
# نوشتن فایل (idempotent)
# ============================================================
def write_file(path: Path, content: str) -> str:
    """
    نوشتن یا به‌روزرسانی یک فایل.
    خروجی: 'created' | 'updated' | 'unchanged'
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    rel = path.relative_to(PROJECT_ROOT)

    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if existing == content:
            info(f"بدون تغییر:  {rel}")
            return "unchanged"
        path.write_text(content, encoding="utf-8")
        warn(f"بازنویسی:    {rel}")
        return "updated"

    path.write_text(content, encoding="utf-8")
    success(f"ساخت جدید:   {rel}")
    return "created"


# ============================================================
# main
# ============================================================
def main() -> int:
    header("اسکریپت ۰۸ — زیرساخت دیتابیس (DB Infrastructure)")

    # نمایش مسیرها
    info(f"ریشه پروژه : {PROJECT_ROOT}")
    info(f"پوشه DB    : {DB_DIR}")

    # بررسی پیش‌نیازها
    if not BACKEND_DIR.exists():
        err(f"پوشه backend پیدا نشد: {BACKEND_DIR}")
        err("لطفاً اسکریپت را از ریشه پروژه اجرا کنید.")
        return 1

    config_path = BACKEND_DIR / "app" / "core" / "config.py"
    if not config_path.exists():
        err("فایل app/core/config.py وجود ندارد.")
        err("ابتدا اسکریپت‌های ۰۳ و ۰۴ را اجرا کنید.")
        return 1

    success("پیش‌نیازها OK")
    print()
    info("شروع ساخت فایل‌ها...\n")

    # ساخت فایل‌ها
    results = {
        "base.py": write_file(DB_DIR / "base.py", BASE_PY),
        "engine.py": write_file(DB_DIR / "engine.py", ENGINE_PY),
        "session.py": write_file(DB_DIR / "session.py", SESSION_PY),
        "__init__.py": write_file(DB_DIR / "__init__.py", INIT_PY),
    }

    # خلاصه
    header("خلاصه")
    created = sum(1 for v in results.values() if v == "created")
    updated = sum(1 for v in results.values() if v == "updated")
    unchanged = sum(1 for v in results.values() if v == "unchanged")

    print(f"  {GREEN}ساخت جدید :{RESET} {created}")
    print(f"  {YELLOW}بازنویسی  :{RESET} {updated}")
    print(f"  {CYAN}بدون تغییر:{RESET} {unchanged}")
    print()

    # دستور تست
    info("گام بعدی — تست ایمپورت در CMD 1 (یا CMD 3):")
    print()
    print(f"  {BOLD}cd D:\\Projects\\trading-system\\backend{RESET}")
    print(f"  {BOLD}venv\\Scripts\\activate{RESET}")
    print(
        f"  {BOLD}python -c \"from app.infrastructure.database import Base, engine, get_db, TimestampMixin, SoftDeleteMixin; print('OK - DB infrastructure imported')\"{RESET}"
    )
    print()
    info("اگر پیام «OK - DB infrastructure imported» دیدید، گام ۴.۱-۲ (مدل‌ها) شروع می‌شود.")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
