# -*- coding: utf-8 -*-
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
