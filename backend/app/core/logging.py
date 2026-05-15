# -*- coding: utf-8 -*-
"""
سیستم لاگ حرفه‌ای — سامانه هوشمند ترید
================================================================
ویژگی‌ها:
  • Rotation روزانه — حفظ ۳۰ روز اخیر
  • دو خروجی: کنسول (با رنگ در dev) + فایل
  • فیلتر امنیتی خودکار — حذف اطلاعات حساس
  • سطوح: DEBUG / INFO / WARNING / ERROR / CRITICAL
  • Context-aware: قابلیت افزودن user_id، request_id

نحوه استفاده در سایر فایل‌ها:
    from app.core.logging import get_logger
    logger = get_logger(__name__)
    logger.info("کاربر وارد شد")
    logger.error("خطا در پردازش", extra={"user_id": 5})
================================================================
"""

import logging
import re
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from app.core.config import settings

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
    re.compile(r"(password\s*[=:]\s*)([^\s,}]+)", re.IGNORECASE),
    re.compile(r"(token\s*[=:]\s*)([^\s,}]+)", re.IGNORECASE),
    re.compile(r"(secret\s*[=:]\s*)([^\s,}]+)", re.IGNORECASE),
    re.compile(r"(api[_-]?key\s*[=:]\s*)([^\s,}]+)", re.IGNORECASE),
    re.compile(r"(authorization\s*[=:]\s*)([^\s,}]+)", re.IGNORECASE),
    re.compile(r"(bearer\s+)([\w\-\.]+)", re.IGNORECASE),
]

# رنگ‌های ANSI برای کنسول (فقط در development)
COLORS = {
    "DEBUG": "\033[36m",     # cyan
    "INFO": "\033[32m",      # green
    "WARNING": "\033[33m",   # yellow
    "ERROR": "\033[31m",     # red
    "CRITICAL": "\033[1;31m",  # bold red
    "RESET": "\033[0m",
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
                msg = pattern.sub(r"\1***REDACTED***", msg)
            record.msg = msg

        # اگر args هم رشته دارد، آنها را هم پاک کن
        if record.args:
            new_args = []
            for arg in record.args:
                if isinstance(arg, str):
                    for pattern in SENSITIVE_PATTERNS:
                        arg = pattern.sub(r"\1***REDACTED***", arg)
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

        # افزودن user_id اگر موجود است
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
            formatted += "\n" + self.formatException(record.exc_info)

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
            formatted += "\n" + self.formatException(record.exc_info)

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

    # ============= هندلر فایل اصلی (همه سطوح) =============
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

    # ============= هندلر فایل خطاها (فقط ERROR و بالاتر) =============
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

    # ============= تنظیم سطح کتابخانه‌های پر سر و صدا =============
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """دریافت logger برای یک ماژول مشخص.

    نحوه استفاده:
        logger = get_logger(__name__)
    """
    return logging.getLogger(name)
