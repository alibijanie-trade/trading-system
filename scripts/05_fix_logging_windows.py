# -*- coding: utf-8 -*-
"""
اسکریپت گام ۳.۵ — Fix رنگ ANSI و emoji در Windows CMD
================================================================
این اسکریپت دو فایل را به‌روز می‌کند:

  • backend/app/core/logging.py    ← افزودن colorama + UTF-8 + detection
  • backend/requirements.txt       ← افزودن colorama==0.4.6

پس از اجرا باید colorama در محیط مجازی نصب شود.

نحوه اجرا (در CMD 3):
    cd /d D:\\Projects\\trading-system
    python scripts\\05_fix_logging_windows.py

نسخه: 1.0.0
================================================================
"""

import sys
from pathlib import Path

# ============================================================
# تنظیمات
# ============================================================
PROJECT_ROOT = Path(r"D:\Projects\trading-system")
BACKEND_DIR = PROJECT_ROOT / "backend"

# نسخه colorama
COLORAMA_VERSION = "colorama==0.4.6"


# ============================================================
# محتوای جدید logging.py
# ============================================================
LOGGING_PY = '''# -*- coding: utf-8 -*-
"""
سیستم لاگ حرفه‌ای — سامانه هوشمند ترید
================================================================
ویژگی‌ها:
  • Rotation روزانه — حفظ ۳۰ روز اخیر
  • دو خروجی: کنسول (با رنگ در dev) + فایل
  • فیلتر امنیتی خودکار — حذف اطلاعات حساس
  • سطوح: DEBUG / INFO / WARNING / ERROR / CRITICAL
  • Context-aware: قابلیت افزودن user_id، request_id
  • سازگاری کامل با Windows CMD (colorama + UTF-8)

نحوه استفاده در سایر فایل‌ها:
    from app.core.logging import get_logger
    logger = get_logger(__name__)
    logger.info("کاربر وارد شد")
================================================================
"""

import io
import logging
import os
import re
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from app.core.config import settings

# ============================================================
# فعال‌سازی پشتیبانی Windows از رنگ ANSI و UTF-8
# ============================================================
# (1) UTF-8 برای stdout — رفع نمایش emoji و فارسی
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    # fallback برای محیط‌هایی که reconfigure ندارند
    pass

# (2) ANSI Colors در Windows — colorama
_COLORS_ENABLED = True
try:
    import colorama

    # init رنگ‌ها (در Windows ANSI sequence ها را به Win32 API ترجمه می‌کند)
    # autoreset=False چون خودمان RESET می‌گذاریم
    colorama.just_fix_windows_console()
except ImportError:
    # اگر colorama نصب نباشد، در Windows رنگ‌ها را خاموش می‌کنیم
    if sys.platform == "win32" and not os.environ.get("ANSICON"):
        _COLORS_ENABLED = False
except Exception:
    _COLORS_ENABLED = False


# ============================================================
# مسیرها و ثابت‌ها
# ============================================================
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DIR = BACKEND_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"
ERROR_LOG_FILE = LOG_DIR / "error.log"

# کلمات حساس که باید از لاگ حذف شوند (طبق سند ۹ بند ۹.۶)
SENSITIVE_PATTERNS = [
    re.compile(r"(password\\s*[=:]\\s*)([^\\s,}]+)", re.IGNORECASE),
    re.compile(r"(token\\s*[=:]\\s*)([^\\s,}]+)", re.IGNORECASE),
    re.compile(r"(secret\\s*[=:]\\s*)([^\\s,}]+)", re.IGNORECASE),
    re.compile(r"(api[_-]?key\\s*[=:]\\s*)([^\\s,}]+)", re.IGNORECASE),
    re.compile(r"(authorization\\s*[=:]\\s*)([^\\s,}]+)", re.IGNORECASE),
    re.compile(r"(bearer\\s+)([\\w\\-\\.]+)", re.IGNORECASE),
]

# رنگ‌های ANSI (فقط در صورت پشتیبانی محیط)
if _COLORS_ENABLED:
    COLORS = {
        "DEBUG": "\\033[36m",       # cyan
        "INFO": "\\033[32m",        # green
        "WARNING": "\\033[33m",     # yellow
        "ERROR": "\\033[31m",       # red
        "CRITICAL": "\\033[1;31m",  # bold red
        "RESET": "\\033[0m",
    }
else:
    # رنگ‌های خالی — هیچ ANSI code خروجی داده نمی‌شود
    COLORS = {
        "DEBUG": "", "INFO": "", "WARNING": "",
        "ERROR": "", "CRITICAL": "", "RESET": "",
    }


# ============================================================
# فیلتر امنیتی
# ============================================================
class SensitiveDataFilter(logging.Filter):
    """حذف خودکار اطلاعات حساس از پیام‌های لاگ."""

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            msg = record.msg
            for pattern in SENSITIVE_PATTERNS:
                msg = pattern.sub(r"\\1***REDACTED***", msg)
            record.msg = msg

        if record.args:
            new_args = []
            for arg in record.args:
                if isinstance(arg, str):
                    for pattern in SENSITIVE_PATTERNS:
                        arg = pattern.sub(r"\\1***REDACTED***", arg)
                new_args.append(arg)
            record.args = tuple(new_args)

        return True


# ============================================================
# Formatter رنگی برای کنسول
# ============================================================
class ColoredFormatter(logging.Formatter):
    """فرمت‌کننده رنگی برای خروجی کنسول."""

    def format(self, record: logging.LogRecord) -> str:
        levelname = record.levelname
        color = COLORS.get(levelname, "")
        reset = COLORS["RESET"]

        user_info = ""
        if hasattr(record, "user_id"):
            user_info = f" [user={record.user_id}]"

        record.levelname = f"{color}{levelname:<8}{reset}"
        formatted = (
            f"{self.formatTime(record, '%Y-%m-%d %H:%M:%S')} "
            f"{record.levelname} "
            f"{record.name}{user_info} — {record.getMessage()}"
        )

        if record.exc_info:
            formatted += "\\n" + self.formatException(record.exc_info)

        record.levelname = levelname  # restore
        return formatted


# ============================================================
# Formatter ساده برای فایل
# ============================================================
class FileFormatter(logging.Formatter):
    """فرمت‌کننده برای فایل لاگ — بدون رنگ، با جزئیات کامل."""

    def format(self, record: logging.LogRecord) -> str:
        user_info = ""
        if hasattr(record, "user_id"):
            user_info = f" [user={record.user_id}]"

        formatted = (
            f"{self.formatTime(record, '%Y-%m-%d %H:%M:%S')} | "
            f"{record.levelname:<8} | "
            f"{record.name}:{record.funcName}:{record.lineno}{user_info} | "
            f"{record.getMessage()}"
        )

        if record.exc_info:
            formatted += "\\n" + self.formatException(record.exc_info)

        return formatted


# ============================================================
# تنظیم Root Logger
# ============================================================
def setup_logging() -> None:
    """تنظیم سیستم لاگ — در startup اپلیکیشن صدا زده می‌شود."""

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if settings.IS_DEVELOPMENT else logging.INFO)

    # حذف هندلرهای پیش‌فرض (جلوگیری از duplicate در reload)
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # ============= هندلر کنسول =============
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(
        logging.DEBUG if settings.IS_DEVELOPMENT else logging.INFO
    )
    console_handler.setFormatter(ColoredFormatter())
    console_handler.addFilter(SensitiveDataFilter())
    root_logger.addHandler(console_handler)

    # ============= هندلر فایل اصلی =============
    file_handler = TimedRotatingFileHandler(
        filename=str(LOG_FILE),
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(FileFormatter())
    file_handler.addFilter(SensitiveDataFilter())
    root_logger.addHandler(file_handler)

    # ============= هندلر فایل خطاها =============
    error_handler = TimedRotatingFileHandler(
        filename=str(ERROR_LOG_FILE),
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(FileFormatter())
    error_handler.addFilter(SensitiveDataFilter())
    root_logger.addHandler(error_handler)

    # ============= کاهش verbosity کتابخانه‌ها =============
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """دریافت logger برای یک ماژول مشخص."""
    return logging.getLogger(name)
'''


# ============================================================
# توابع کمکی
# ============================================================
def add_colorama_to_requirements(requirements_path: Path) -> str:
    """افزودن colorama به requirements.txt به‌صورت idempotent.

    خروجی: "added" / "already_present" / "missing_file"
    """
    if not requirements_path.exists():
        return "missing_file"

    content = requirements_path.read_text(encoding="utf-8")

    # چک idempotency — اگر colorama از قبل هست، رد می‌شود
    if "colorama" in content.lower():
        return "already_present"

    # افزودن بعد از بخش "Environment" (python-dotenv) — منطقی‌ترین جا
    marker = "# --- Environment ---"
    if marker in content:
        new_block = (
            "# --- Environment ---\n"
            "python-dotenv==1.0.1\n"
            f"{COLORAMA_VERSION}    # Windows ANSI colors support\n"
        )
        # دقیقاً ۲ خط بعد از marker را عوض می‌کنیم
        old_block = "# --- Environment ---\n" "python-dotenv==1.0.1\n"
        new_content = content.replace(old_block, new_block, 1)
        if new_content == content:
            # اگر pattern دقیق پیدا نشد، در انتها اضافه می‌کنیم
            new_content = content.rstrip() + f"\n\n# --- Console Colors ---\n{COLORAMA_VERSION}\n"
    else:
        # اگر marker نبود، در انتها اضافه می‌کنیم
        new_content = content.rstrip() + f"\n\n# --- Console Colors ---\n{COLORAMA_VERSION}\n"

    requirements_path.write_text(new_content, encoding="utf-8")
    return "added"


def write_file_full(path: Path, content: str) -> None:
    """نوشتن کامل فایل با ساخت پوشه‌های والد."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


# ============================================================
# تابع اصلی
# ============================================================
def main() -> None:
    print("=" * 60)
    print("🔧 گام ۳.۵ — Fix رنگ و emoji در Windows CMD")
    print("=" * 60)
    print(f"📁 ریشه پروژه: {PROJECT_ROOT}")
    print()

    if not PROJECT_ROOT.exists():
        print(f"❌ خطا: پوشه ریشه وجود ندارد: {PROJECT_ROOT}")
        sys.exit(1)

    # ============================================================
    # ۱) بازنویسی logging.py
    # ============================================================
    print("📝 [1/2] بازنویسی backend/app/core/logging.py ...")
    logging_path = BACKEND_DIR / "app" / "core" / "logging.py"
    if not logging_path.exists():
        print(f"   ❌ فایل logging.py وجود ندارد — ابتدا گام ۳ را اجرا کنید")
        sys.exit(1)

    write_file_full(logging_path, LOGGING_PY)
    print(f"   ✅ بازنویسی شد ({len(LOGGING_PY):,} کاراکتر)")
    print()

    # ============================================================
    # ۲) افزودن colorama به requirements.txt
    # ============================================================
    print("📦 [2/2] افزودن colorama به requirements.txt ...")
    req_path = BACKEND_DIR / "requirements.txt"
    result = add_colorama_to_requirements(req_path)
    if result == "added":
        print(f"   ✅ {COLORAMA_VERSION} اضافه شد")
    elif result == "already_present":
        print(f"   ℹ️  colorama از قبل در requirements.txt است — رد شد")
    else:
        print(f"   ❌ requirements.txt پیدا نشد")
        sys.exit(1)
    print()

    # ============================================================
    # پیام پایانی
    # ============================================================
    print("=" * 60)
    print("✅ گام ۳.۵ کامل شد!")
    print("=" * 60)
    print()
    print("📌 مراحل بعدی:")
    print()
    print("─" * 60)
    print("🔵 CMD 1 (Backend):  نصب colorama و restart")
    print("─" * 60)
    print()
    print("   ۱) متوقف کردن uvicorn:")
    print("      Ctrl+C")
    print()
    print("   ۲) نصب colorama (مهم: venv باید فعال باشد — (venv) در ابتدای خط)")
    print("      pip install colorama==0.4.6")
    print()
    print("   ۳) اجرای مجدد سرور:")
    print("      uvicorn main:app --reload")
    print()
    print("   ۴) باید این تفاوت‌ها را ببینید:")
    print("      • emoji 🚀 درست نمایش داده می‌شود (نه �)")
    print("      • رنگ‌های ANSI واقعاً سبز/زرد/قرمز هستند (نه ←[32m)")
    print()
    print("─" * 60)
    print("🟢 CMD 3 (Scripts/Git):  پس از تست موفق، commit")
    print("─" * 60)
    print()
    print(r"      cd /d D:\Projects\trading-system")
    print(
        r"      git add backend/app/core/logging.py backend/requirements.txt scripts/05_fix_logging_windows.py"
    )
    print(r'      git commit -m "fix(logging): add colorama and UTF-8 support for Windows CMD"')
    print()


if __name__ == "__main__":
    main()
