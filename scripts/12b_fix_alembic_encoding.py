# -*- coding: utf-8 -*-
"""
================================================================
اسکریپت ۱۲b — اصلاح UnicodeDecodeError در alembic.ini
================================================================
هدف: بازنویسی backend/alembic.ini با محتوای فقط-ASCII تا
خطای UnicodeDecodeError در ویندوز رفع شود.

علت:
  Alembic فایل alembic.ini را با encoding="locale" می‌خواند.
  در ویندوز locale = cp1252 (نه UTF-8) → بایت‌های فارسی شکست می‌خورند.

راه حل:
  - تمام کامنت‌های alembic.ini به انگلیسی
  - مقادیر و کلیدها بدون تغییر
  - رفتار Alembic ۱۰۰٪ یکسان

نکته: سایر فایل‌ها (env.py، script.py.mako) Python هستند و
       تحت تأثیر این محدودیت قرار ندارند.

نحوه اجرا (در CMD 3):
    cd D:\\Projects\\trading-system
    python scripts\\12b_fix_alembic_encoding.py
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
ALEMBIC_INI = BACKEND_DIR / "alembic.ini"


# ============================================================
# محتوای جدید alembic.ini — فقط ASCII
# ============================================================
ALEMBIC_INI_ASCII = """# ============================================================
# Alembic Configuration - Trading System
# ============================================================
# Note: The real database URL is read from .env at runtime via
# env.py (settings.DATABASE_URL). The 'sqlalchemy.url' below is
# only a placeholder.
#
# IMPORTANT: This file must remain ASCII-only on Windows because
# Alembic reads it with encoding='locale' (= cp1252 on Windows).
# UTF-8 / Persian characters cause UnicodeDecodeError here.
# (Persian comments are fine inside Python files such as env.py.)
# ============================================================

[alembic]
# Migration scripts location (we use 'migrations/' not default 'alembic/')
script_location = migrations

# Add backend/ to sys.path so env.py can `import app`
prepend_sys_path = .

# Version path separator (os = use os.pathsep)
version_path_separator = os

# Placeholder URL - env.py overrides this with settings.DATABASE_URL
sqlalchemy.url = sqlite+aiosqlite:///./trading.db

# Migration filename template: 2026_05_16_0900-abc123_initial_schema.py
file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s

# ============================================================
# Post-write hooks (disabled)
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


# ============================================================
# main
# ============================================================
def main() -> int:
    header("اسکریپت ۱۲b — اصلاح Encoding فایل alembic.ini")

    info(f"مسیر فایل: {ALEMBIC_INI}")
    print()

    # بررسی وجود فایل
    if not ALEMBIC_INI.exists():
        err(f"فایل alembic.ini یافت نشد در: {ALEMBIC_INI}")
        err("ابتدا اسکریپت ۱۲ را اجرا کنید.")
        return 1

    # بررسی محتوای فعلی (آیا حاوی کاراکتر non-ASCII است؟)
    try:
        current = ALEMBIC_INI.read_text(encoding="utf-8")
    except Exception as e:
        err(f"خطا در خواندن فایل: {e}")
        return 1

    # شناسایی کاراکترهای non-ASCII
    non_ascii_chars = set()
    for ch in current:
        if ord(ch) > 127:
            non_ascii_chars.add(ch)

    if non_ascii_chars:
        warn(f"تعداد کاراکترهای غیر-ASCII در فایل قبلی: {len(non_ascii_chars)}")
        info(f"نمونه: {sorted(non_ascii_chars)[:10]}")
        print()
    else:
        info("فایل قبلی از قبل ASCII است.")

    # تأیید اینکه محتوای جدید کاملاً ASCII است
    try:
        ALEMBIC_INI_ASCII.encode("ascii")
    except UnicodeEncodeError as e:
        err(f"محتوای جدید هنوز ASCII خالص نیست: {e}")
        return 1
    success("محتوای جدید: ASCII خالص ✓")

    # مقایسه با وضعیت فعلی (idempotent check)
    if current == ALEMBIC_INI_ASCII:
        info("فایل از قبل با محتوای صحیح آپدیت شده — تغییری لازم نیست.")
        print()
    else:
        # بک‌آپ سریع
        backup_path = ALEMBIC_INI.with_suffix(".ini.bak")
        backup_path.write_text(current, encoding="utf-8")
        info(f"بک‌آپ ساخته شد: {backup_path.relative_to(PROJECT_ROOT)}")

        # نوشتن محتوای جدید با encoding صریح ASCII
        ALEMBIC_INI.write_text(ALEMBIC_INI_ASCII, encoding="ascii")
        success(f"بازنویسی شد: {ALEMBIC_INI.relative_to(PROJECT_ROOT)}")
        print()

    # تست خواندن با cp1252 (مثل Alembic در ویندوز)
    info("تست خواندن فایل با cp1252 (شبیه‌سازی رفتار Alembic در ویندوز)...")
    try:
        ALEMBIC_INI.read_text(encoding="cp1252")
        success("تست cp1252 OK — Alembic قادر به خواندن فایل خواهد بود ✓")
    except UnicodeDecodeError as e:
        err(f"تست cp1252 شکست خورد: {e}")
        return 1

    print()

    # ===== راهنمای دستورات بعدی =====
    header("گام بعدی — دستورات Alembic (در CMD 1 با venv فعال)")

    print(f"  {BOLD}cd D:\\Projects\\trading-system\\backend{RESET}")
    print(f"  {BOLD}venv\\Scripts\\activate{RESET}")
    print()

    print(f"{BOLD}{GREEN}# دستور ۱ — تست پیکربندی (باید الان بدون خطا کار کند):{RESET}")
    print(f"  {BOLD}alembic current{RESET}")
    info("    خروجی: 'INFO ...' (هنوز migration نداریم، پس revision خاص نشان نمی‌دهد)")
    print()

    print(f"{BOLD}{GREEN}# دستور ۲ — تولید Migration اولیه برای ۱۵ جدول:{RESET}")
    print(f"  {BOLD}alembic revision --autogenerate -m \"initial_schema\"{RESET}")
    info("    این یک فایل جدید در backend/migrations/versions/ می‌سازد")
    print()

    warn("⚠ فایل تولیدشده در backend/migrations/versions/ را")
    warn("  بدون اجرای 'alembic upgrade head' برای بازبینی به من بفرستید")
    warn("  (یا محتوای آن را در چت paste کنید).")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
