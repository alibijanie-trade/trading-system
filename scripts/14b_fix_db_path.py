# -*- coding: utf-8 -*-
"""
================================================================
اسکریپت ۱۴b — رفع Bug در DATABASE_URL
================================================================
هدف:
  اصلاح config.py تا DB_PATH نسبت به BACKEND_DIR resolve شود
  (نه نسبت به CWD). این تضمین می‌کند که هر اسکریپتی از هر
  پوشه‌ای اجرا شود، روی همان فایل DB واقعی کار کند.

علت Bug:
  DB_PATH = "./trading.db" → relative path
  وقتی اسکریپت ۱۴ از D:\\Projects\\trading-system اجرا شد،
  SQLite فایل D:\\Projects\\trading-system\\trading.db را ساخت
  (نه backend\\trading.db که جدول‌ها در آن هستند).

این اسکریپت چه می‌کند:
  1. فایل اشتباه trading.db در ریشه پروژه را پاک می‌کند (اگر خالی است)
     + فایل‌های مرتبط trading.db-shm و trading.db-wal
  2. تابع DATABASE_URL در config.py را اصلاح می‌کند
  3. تست می‌کند تا مطمئن شویم اصلاح درست انجام شده

نحوه اجرا (در tab 2 scripts):
    cd /d D:\\Projects\\trading-system
    python scripts\\14b_fix_db_path.py
================================================================
"""

import sqlite3
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
CONFIG_PY = BACKEND_DIR / "app" / "core" / "config.py"

# فایل اشتباه (در ریشه) و فایل صحیح (در backend/)
WRONG_DB = PROJECT_ROOT / "trading.db"
CORRECT_DB = BACKEND_DIR / "trading.db"


# ============================================================
# توابع کمکی نمایش
# ============================================================
def info(msg: str) -> None: print(f"{CYAN}ℹ {msg}{RESET}")
def success(msg: str) -> None: print(f"{GREEN}✅ {msg}{RESET}")
def warn(msg: str) -> None: print(f"{YELLOW}⚠ {msg}{RESET}")
def err(msg: str) -> None: print(f"{RED}❌ {msg}{RESET}")

def header(msg: str) -> None:
    line = "=" * 60
    print(f"\n{BOLD}{CYAN}{line}{RESET}")
    print(f"{BOLD}{CYAN}{msg}{RESET}")
    print(f"{BOLD}{CYAN}{line}{RESET}\n")


# ============================================================
# قسمت اصلاح config.py
# ============================================================

OLD_DATABASE_URL = '''    @property
    def DATABASE_URL(self) -> str:
        """آدرس اتصال SQLAlchemy برای SQLite + aiosqlite"""
        return f"sqlite+aiosqlite:///{self.DB_PATH}"'''

NEW_DATABASE_URL = '''    @property
    def DATABASE_URL(self) -> str:
        """آدرس اتصال SQLAlchemy برای SQLite + aiosqlite.

        اگر DB_PATH مسیر relative باشد (مثل './trading.db')،
        آن را نسبت به BACKEND_DIR resolve می‌کنیم تا مسیر DB
        ثابت بماند حتی اگر اپ از پوشه دیگری اجرا شود.
        مثال: اجرای اسکریپت‌ها از ریشه پروژه با /d و venv.
        """
        db_path = Path(self.DB_PATH)
        if not db_path.is_absolute():
            db_path = BACKEND_DIR / self.DB_PATH
        # as_posix() برای URL — جلوگیری از مشکل backslash در ویندوز
        return f"sqlite+aiosqlite:///{db_path.as_posix()}"'''


def check_db_is_empty_or_wrong(db_path: Path) -> tuple[bool, str]:
    """
    بررسی کن فایل DB در ریشه خالی است یا فاقد جدول‌های پروژه است.
    خروجی: (آیا قابل حذف است, دلیل)
    """
    if not db_path.exists():
        return (False, "فایل وجود ندارد")

    size = db_path.stat().st_size
    if size == 0:
        return (True, f"فایل خالی است ({size} byte)")

    # چک کن آیا جدول Exchanges در آن وجود دارد
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='Exchanges'"
        )
        has_exchanges = cursor.fetchone() is not None
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        all_tables = [r[0] for r in cursor.fetchall()]
        conn.close()
    except Exception as e:
        return (False, f"خطا در خواندن DB: {e}")

    if not has_exchanges:
        return (
            True,
            f"فاقد جدول Exchanges (تنها جدول‌های موجود: {all_tables})"
        )

    return (False, f"شامل جدول Exchanges + سایر جدول‌ها است ({len(all_tables)} جدول) - نباید پاک شود!")


# ============================================================
# main
# ============================================================
def main() -> int:
    header("اسکریپت ۱۴b — رفع Bug در DATABASE_URL")

    info(f"ریشه پروژه : {PROJECT_ROOT}")
    info(f"Backend    : {BACKEND_DIR}")
    info(f"Config.py  : {CONFIG_PY.relative_to(PROJECT_ROOT)}")
    print()

    # ===== مرحله 1: تأیید فایل DB صحیح =====
    header("مرحله ۱ — تأیید فایل DB صحیح در backend/")

    if not CORRECT_DB.exists():
        err(f"فایل صحیح backend/trading.db پیدا نشد!")
        err("ابتدا 'alembic upgrade head' را اجرا کنید.")
        return 1

    try:
        conn = sqlite3.connect(str(CORRECT_DB))
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = [r[0] for r in cursor.fetchall()]
        conn.close()
        success(f"فایل backend/trading.db سالم است — شامل {len(tables)} جدول:")
        for t in tables:
            print(f"    {GREEN}•{RESET} {t}")
    except Exception as e:
        err(f"خطا در خواندن backend/trading.db: {e}")
        return 1

    print()

    # ===== مرحله 2: پاک‌سازی فایل اشتباه =====
    header("مرحله ۲ — پاک‌سازی فایل trading.db اشتباه در ریشه")

    if WRONG_DB.exists():
        can_delete, reason = check_db_is_empty_or_wrong(WRONG_DB)
        info(f"وضعیت {WRONG_DB.relative_to(PROJECT_ROOT)}: {reason}")

        if not can_delete:
            err("این فایل DB نباید حذف شود — به‌نظر شامل داده است!")
            err("لطفاً به من اطلاع دهید برای بررسی دستی.")
            return 1

        # حذف فایل و فایل‌های مرتبط WAL/SHM
        deleted = []
        for suffix in ["", "-shm", "-wal", "-journal"]:
            target = WRONG_DB.with_suffix(WRONG_DB.suffix + suffix) if suffix else WRONG_DB
            if target.exists():
                target.unlink()
                deleted.append(target.name)

        for name in deleted:
            success(f"پاک شد: {name}")
    else:
        info("فایل اشتباهی وجود ندارد (احتمالاً قبلاً پاک شده)")

    print()

    # ===== مرحله 3: اصلاح config.py =====
    header("مرحله ۳ — اصلاح DATABASE_URL در config.py")

    if not CONFIG_PY.exists():
        err(f"فایل config.py پیدا نشد: {CONFIG_PY}")
        return 1

    content = CONFIG_PY.read_text(encoding="utf-8")

    # ===== چک idempotent =====
    if NEW_DATABASE_URL in content:
        success("config.py از قبل اصلاح شده — تغییری لازم نیست.")
        print()
    elif OLD_DATABASE_URL not in content:
        err("الگوی قدیمی DATABASE_URL در config.py پیدا نشد.")
        err("شاید قبلاً تغییر دستی داده شده. فایل را به من نشان دهید.")
        return 1
    else:
        # backup
        backup = CONFIG_PY.with_suffix(".py.bak")
        backup.write_text(content, encoding="utf-8")
        info(f"بک‌آپ ساخته شد: {backup.name}")

        # جایگزینی
        new_content = content.replace(OLD_DATABASE_URL, NEW_DATABASE_URL, 1)
        if new_content == content:
            err("جایگزینی ناموفق بود.")
            return 1

        CONFIG_PY.write_text(new_content, encoding="utf-8")
        success(f"config.py به‌روز شد")
        print()

    # ===== مرحله 4: تست =====
    header("مرحله ۴ — تست: DATABASE_URL باید absolute باشد")

    # اضافه کردن backend/ به sys.path
    if str(BACKEND_DIR) not in sys.path:
        sys.path.insert(0, str(BACKEND_DIR))

    # ایمپورت مجدد در صورت لزوم (ممکن است cache شده باشد)
    # اما این اسکریپت اولین بار اجرا می‌شود پس cache مشکلی ندارد
    try:
        from app.core.config import settings
        url = settings.DATABASE_URL
        info(f"DATABASE_URL فعلی: {url}")

        if "backend" in url.replace("\\", "/"):
            success("URL به backend/trading.db اشاره می‌کند (مسیر absolute) ✓")
        else:
            warn(f"URL absolute نیست — اشکال ممکن است باقی باشد")
            return 1
    except Exception as e:
        err(f"خطا در ایمپورت config: {e}")
        return 1

    print()

    # ===== خلاصه و گام بعدی =====
    header("گام بعدی — اجرای مجدد اسکریپت ۱۴")

    print(f"{BOLD}📍 Tab: 2 scripts{RESET}")
    print()
    print(f"  {BOLD}python scripts\\14_seed_data.py{RESET}")
    print()
    info("این بار باید بدون خطا اجرا شود و چهار رکورد در DB درج کند.")
    print()

    warn("⚠ نکته: uvicorn در tab 1 backend شاید لازم باشد restart شود")
    warn("  چون config.py تغییر کرده — ولی --reload خودش این کار را می‌کند.")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
