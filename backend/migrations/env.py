# -*- coding: utf-8 -*-
"""
Alembic env.py — async-aware برای SQLAlchemy 2.0 + aiosqlite
================================================================
این فایل نقطه ورود Alembic است.

کارهای کلیدی:
  1. افزودن backend/ به sys.path تا بتوان از app.* ایمپورت کرد
  2. خواندن DATABASE_URL از .env (نه از alembic.ini)
  3. ایمپورت همه ۱۵ مدل (تا metadata کشف شود)
  4. اجرای async migration با render_as_batch برای SQLite

نکته‌ها:
  - render_as_batch=True : برای پشتیبانی ALTER TABLE در SQLite
  - target_metadata = Base.metadata : به Alembic می‌گوید کدام مدل‌ها
    را برای autogenerate نگاه کند
================================================================
"""

import asyncio
import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# ============================================================
# افزودن backend/ به sys.path (یک سطح بالاتر از migrations/)
# ============================================================
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# اکنون می‌توانیم از app.* ایمپورت کنیم
from app.core.config import settings  # noqa: E402
from app.infrastructure.database import Base  # noqa: E402

# ایمپورت کردن همه مدل‌ها تا در Base.metadata ثبت شوند
# این خط کلیدی است — بدون آن، Alembic مدل‌ها را نمی‌بیند
import app.models  # noqa: F401, E402

# ============================================================
# Alembic Config
# ============================================================
config = context.config

# جایگزینی URL در runtime با مقدار واقعی از .env
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# لاگ کانفیگ
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata برای autogenerate
target_metadata = Base.metadata


# ============================================================
# Offline Migrations (تولید SQL بدون اتصال به DB)
# ============================================================
def run_migrations_offline() -> None:
    """اجرای migration در حالت offline (تولید SQL بدون اتصال)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,  # SQLite ALTER support
    )

    with context.begin_transaction():
        context.run_migrations()


# ============================================================
# Online Migrations (واقعی، با اتصال async)
# ============================================================
def do_run_migrations(connection: Connection) -> None:
    """اجرای migrations در حالت sync (داخل async wrapper)."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True,  # SQLite ALTER support — الزامی
        compare_type=True,     # تشخیص دقیق‌تر تغییرات نوع ستون
        compare_server_default=True,  # تشخیص تغییر مقدار پیش‌فرض
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """ساخت async engine و اجرای migrations."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """اجرای migration در حالت online (با اتصال)."""
    asyncio.run(run_async_migrations())


# ============================================================
# اجرا — انتخاب offline یا online
# ============================================================
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
