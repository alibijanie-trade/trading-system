# -*- coding: utf-8 -*-
"""
================================================================
اسکریپت ۱۲ — پیکربندی Alembic (شروع زیرگام ۴.۲)
================================================================
این اسکریپت سه فایل پیکربندی Alembic را در backend/ می‌سازد:

  1. backend/alembic.ini             → تنظیمات Alembic
  2. backend/migrations/env.py       → نقطه ورود (async-aware)
  3. backend/migrations/script.py.mako → قالب فایل‌های migration

پیکربندی کلیدی:
  - script_location = migrations  (نه پیش‌فرض alembic/)
  - استفاده از settings.DATABASE_URL از .env (نه hardcode)
  - استفاده از async engine
  - render_as_batch=True برای پشتیبانی ALTER TABLE در SQLite

نحوه اجرا (در CMD 3):
    cd D:\\Projects\\trading-system
    python scripts\\12_alembic_setup.py

پس از این اسکریپت، دستورات Alembic دستی در CMD 1 (venv) اجرا می‌شوند.
================================================================
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


# ============================================================
# مسیرها
# ============================================================
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
MIGRATIONS_DIR = BACKEND_DIR / "migrations"
VERSIONS_DIR = MIGRATIONS_DIR / "versions"


# ============================================================
# محتوای فایل‌ها
# ============================================================

ALEMBIC_INI = """# ============================================================
# Alembic Configuration — سامانه هوشمند ترید
# ============================================================
# نکته: sqlalchemy.url در env.py از settings.DATABASE_URL خوانده
# می‌شود؛ مقدار اینجا فقط placeholder است.
# ============================================================

[alembic]
# مسیر اسکریپت‌های migration (نه alembic/ پیش‌فرض)
script_location = migrations

# اضافه‌کردن مسیر backend/ به sys.path تا env.py بتواند `app` را import کند
prepend_sys_path = .

# جداکننده مسیر version paths
version_path_separator = os

# placeholder — env.py مقدار واقعی را از .env می‌گیرد
sqlalchemy.url = sqlite+aiosqlite:///./trading.db

# قالب نام فایل migration: <timestamp>_<slug>.py
# مثال: 2026_05_16_0900-abc123_initial_schema.py
file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s

# ============================================================
# Post-write hooks (خاموش)
# ============================================================
[post_write_hooks]

# ============================================================
# Logging
# ============================================================
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARNING
handlers = console
qualname =

[logger_sqlalchemy]
level = WARNING
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
"""


ENV_PY = '''# -*- coding: utf-8 -*-
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
'''


SCRIPT_PY_MAKO = '''"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    """Upgrade schema."""
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """Downgrade schema."""
    ${downgrades if downgrades else "pass"}
'''


VERSIONS_GITKEEP = """# این پوشه برای فایل‌های migration توسط Alembic استفاده می‌شود.
# فایل‌ها به‌صورت خودکار با `alembic revision --autogenerate` ساخته می‌شوند.
"""


# ============================================================
# توابع کمکی
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


def write_file(path: Path, content: str) -> str:
    """نوشتن idempotent. خروجی: 'created' | 'updated' | 'unchanged'"""
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
    header("اسکریپت ۱۲ — پیکربندی Alembic")

    info(f"ریشه پروژه : {PROJECT_ROOT}")
    info(f"پوشه backend: {BACKEND_DIR}")

    # بررسی پیش‌نیازها
    if not (BACKEND_DIR / "main.py").exists():
        err("Backend راه‌اندازی نشده.")
        err("ابتدا اسکریپت‌های قبلی را اجرا کنید.")
        return 1

    if not (BACKEND_DIR / "app" / "models" / "__init__.py").exists():
        err("مدل‌ها هنوز ساخته نشده‌اند.")
        err("ابتدا اسکریپت‌های ۰۸، ۰۹، ۱۰ را اجرا کنید.")
        return 1

    success("پیش‌نیازها OK")
    print()
    info("شروع ساخت فایل‌های Alembic...\n")

    # ساخت پوشه versions اگر وجود ندارد
    VERSIONS_DIR.mkdir(parents=True, exist_ok=True)
    info(f"پوشه versions/ آماده: {VERSIONS_DIR.relative_to(PROJECT_ROOT)}")
    print()

    # ساخت فایل‌ها
    results = {
        "alembic.ini":              write_file(BACKEND_DIR / "alembic.ini", ALEMBIC_INI),
        "migrations/env.py":        write_file(MIGRATIONS_DIR / "env.py", ENV_PY),
        "migrations/script.py.mako": write_file(MIGRATIONS_DIR / "script.py.mako", SCRIPT_PY_MAKO),
        "migrations/versions/README.md": write_file(VERSIONS_DIR / "README.md", VERSIONS_GITKEEP),
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

    # ===== راهنمای دستورات بعدی =====
    header("گام بعدی — دو دستور Alembic (در CMD 1 با venv فعال)")

    info("⚠ uvicorn را با Ctrl+C متوقف کنید.\n")

    print(f"  {BOLD}cd D:\\Projects\\trading-system\\backend{RESET}")
    print(f"  {BOLD}venv\\Scripts\\activate{RESET}")
    print()

    print(f"{BOLD}{GREEN}# دستور ۱ — تست پیکربندی Alembic (نباید خطا بدهد):{RESET}")
    print(f"  {BOLD}alembic current{RESET}")
    info("    خروجی مورد انتظار: خالی یا 'INFO ... No revision'  (هنوز migration نداریم)")
    print()

    print(f"{BOLD}{GREEN}# دستور ۲ — تولید Migration اولیه برای ۱۵ جدول:{RESET}")
    print(f"  {BOLD}alembic revision --autogenerate -m \"initial_schema\"{RESET}")
    info("    این یک فایل جدید در backend/migrations/versions/ می‌سازد")
    info("    فایل به‌طور خودکار شامل CREATE TABLE برای همه ۱۵ جدول می‌شود")
    print()

    info("توجه: در این مرحله هنوز جدول‌ها در DB ساخته نمی‌شوند — فقط فایل migration تولید می‌شود.")
    print()

    warn("⚠ پس از دستور ۲، فایل تولیدشده در backend/migrations/versions/ را")
    warn("  بدون اجرای 'alembic upgrade head' برای من بفرستید تا بازبینی کنم")
    warn("  (مخصوصاً ایندکس‌های critical: idx_ohlcv_symbol_tf_ts و idx_audit_*).")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
