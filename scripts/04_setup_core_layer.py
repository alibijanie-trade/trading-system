# -*- coding: utf-8 -*-
"""
اسکریپت گام ۳ — Core Layer (Logger + Exceptions + Response + Handlers)
================================================================
این اسکریپت لایه پایه Backend را می‌سازد:

  • backend/app/core/logging.py     ← سیستم لاگ حرفه‌ای
  • backend/app/core/exceptions.py  ← Custom Exception classes
  • backend/app/core/response.py    ← Helper پاسخ استاندارد
  • backend/app/core/handlers.py    ← Exception Handlers
  • backend/app/core/__init__.py    ← exportهای راحت
  • backend/main.py                 ← بازنویسی با handlers
  • backend/app/api/v1/routes/health.py ← استفاده از Response Wrapper
  • backend/logs/.gitkeep           ← حفظ پوشه در Git

نحوه اجرا (در CMD 3):
    cd /d D:\\Projects\\trading-system
    python scripts\\04_setup_core_layer.py

نسخه: 1.0.0
تاریخ: 2026-05-14
================================================================
"""

import sys
from pathlib import Path

# ============================================================
# تنظیمات
# ============================================================
PROJECT_ROOT = Path(r"D:\Projects\trading-system")
BACKEND_DIR = PROJECT_ROOT / "backend"


# ============================================================
# محتوای فایل‌ها
# ============================================================

# --- backend/app/core/logging.py ---
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
    re.compile(r"(password\\s*[=:]\\s*)([^\\s,}]+)", re.IGNORECASE),
    re.compile(r"(token\\s*[=:]\\s*)([^\\s,}]+)", re.IGNORECASE),
    re.compile(r"(secret\\s*[=:]\\s*)([^\\s,}]+)", re.IGNORECASE),
    re.compile(r"(api[_-]?key\\s*[=:]\\s*)([^\\s,}]+)", re.IGNORECASE),
    re.compile(r"(authorization\\s*[=:]\\s*)([^\\s,}]+)", re.IGNORECASE),
    re.compile(r"(bearer\\s+)([\\w\\-\\.]+)", re.IGNORECASE),
]

# رنگ‌های ANSI برای کنسول (فقط در development)
COLORS = {
    "DEBUG": "\\033[36m",     # cyan
    "INFO": "\\033[32m",      # green
    "WARNING": "\\033[33m",   # yellow
    "ERROR": "\\033[31m",     # red
    "CRITICAL": "\\033[1;31m",  # bold red
    "RESET": "\\033[0m",
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

        # اگر args هم رشته دارد، آنها را هم پاک کن
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
'''


# --- backend/app/core/exceptions.py ---
EXCEPTIONS_PY = '''# -*- coding: utf-8 -*-
"""
Custom Exception Classes — سامانه هوشمند ترید
================================================================
تمام Exception های دامنه پروژه که در ساختار استاندارد پاسخ
(سند ۶) ترجمه می‌شوند.

سلسله مراتب:
    AppException (پایه)
    ├── ValidationError      (400)
    ├── AuthenticationError  (401)
    ├── AuthorizationError   (403)
    ├── NotFoundError        (404)
    ├── ConflictError        (409)
    ├── RateLimitError       (429)
    ├── BusinessLogicError   (422)
    ├── ExternalServiceError (502)
    └── DatabaseError        (500)

نحوه استفاده در services/:
    from app.core.exceptions import NotFoundError
    if user is None:
        raise NotFoundError(message="کاربر یافت نشد", code="USER_NOT_FOUND")
================================================================
"""

from typing import Any


class AppException(Exception):
    """کلاس پایه برای تمام Exception های دامنه پروژه."""

    status_code: int = 500
    default_message: str = "خطای داخلی سرور"
    default_code: str = "INTERNAL_ERROR"

    def __init__(
        self,
        message: str | None = None,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message or self.default_message
        self.code = code or self.default_code
        self.details = details or {}
        super().__init__(self.message)


# ============================================================
# 4xx — Client Errors
# ============================================================
class ValidationError(AppException):
    """خطای اعتبارسنجی ورودی."""

    status_code = 400
    default_message = "داده‌های ورودی نامعتبر است"
    default_code = "VALIDATION_ERROR"


class AuthenticationError(AppException):
    """خطای احراز هویت — کاربر ناشناس یا توکن نامعتبر."""

    status_code = 401
    default_message = "احراز هویت ناموفق"
    default_code = "AUTHENTICATION_FAILED"


class AuthorizationError(AppException):
    """خطای دسترسی — کاربر شناخته‌شده اما مجوز ندارد."""

    status_code = 403
    default_message = "دسترسی به این منبع مجاز نیست"
    default_code = "ACCESS_DENIED"


class NotFoundError(AppException):
    """منبع درخواست‌شده یافت نشد."""

    status_code = 404
    default_message = "منبع درخواست‌شده یافت نشد"
    default_code = "NOT_FOUND"


class ConflictError(AppException):
    """تعارض — مثلاً ایجاد رکورد تکراری."""

    status_code = 409
    default_message = "منبع تکراری است"
    default_code = "CONFLICT"


class BusinessLogicError(AppException):
    """نقض قاعده دامنه — مثلاً اردر بدون سرمایه کافی."""

    status_code = 422
    default_message = "عملیات قابل انجام نیست"
    default_code = "BUSINESS_LOGIC_ERROR"


class RateLimitError(AppException):
    """تعداد درخواست از حد مجاز فراتر رفته."""

    status_code = 429
    default_message = "تعداد درخواست‌ها از حد مجاز گذشته — لطفاً کمی صبر کنید"
    default_code = "RATE_LIMIT_EXCEEDED"


# ============================================================
# 5xx — Server Errors
# ============================================================
class DatabaseError(AppException):
    """خطای داخلی دیتابیس."""

    status_code = 500
    default_message = "خطای داخلی در دسترسی به داده"
    default_code = "DATABASE_ERROR"


class ExternalServiceError(AppException):
    """خطا در سرویس خارجی — مثلاً API صرافی."""

    status_code = 502
    default_message = "خطا در ارتباط با سرویس خارجی"
    default_code = "EXTERNAL_SERVICE_ERROR"


class ConfigurationError(AppException):
    """خطای پیکربندی سیستم — مقدار ناصحیح در .env یا config."""

    status_code = 500
    default_message = "خطا در پیکربندی سیستم"
    default_code = "CONFIGURATION_ERROR"


# ============================================================
# دامنه‌ای — خطاهای تخصصی پروژه
# ============================================================
class EncryptionError(AppException):
    """خطای رمزنگاری/رمزگشایی API Key صرافی."""

    status_code = 500
    default_message = "خطا در رمزنگاری اطلاعات"
    default_code = "ENCRYPTION_ERROR"


class ExchangeError(ExternalServiceError):
    """خطای ارتباط با صرافی — زیرکلاس ExternalServiceError."""

    default_message = "خطا در ارتباط با صرافی"
    default_code = "EXCHANGE_ERROR"
'''


# --- backend/app/core/response.py ---
RESPONSE_PY = '''# -*- coding: utf-8 -*-
"""
Response Wrapper — ساختار استاندارد پاسخ
================================================================
طبق سند ۶ بند ۶.۲، هر پاسخ API باید این ساختار را داشته باشد:
    {
        "success": bool,
        "message": "پیام فارسی",
        "data": {...} | null,
        "errors": null | [...]
    }

این فایل توابع کمکی برای ساخت آسان این ساختار را فراهم می‌کند.

نحوه استفاده در روت‌ها:
    from app.core.response import success_response
    return success_response(data={"id": 5}, message="کاربر ساخته شد")
================================================================
"""

from typing import Any


def success_response(
    data: Any = None,
    message: str = "عملیات با موفقیت انجام شد",
) -> dict[str, Any]:
    """ساخت پاسخ موفق استاندارد.

    Args:
        data: داده پاسخ (هر نوع JSON-serializable)
        message: پیام فارسی برای نمایش به کاربر

    Returns:
        دیکشنری با ساختار استاندارد سند ۶
    """
    return {
        "success": True,
        "message": message,
        "data": data,
        "errors": None,
    }


def error_response(
    message: str,
    code: str = "ERROR",
    errors: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """ساخت پاسخ خطا استاندارد.

    Args:
        message: پیام خطای فارسی
        code: کد خطای داخلی (برای ترجمه/مستندسازی)
        errors: لیست جزئیات خطاها (مثلاً validation errors فیلد به فیلد)

    Returns:
        دیکشنری با ساختار استاندارد سند ۶
    """
    return {
        "success": False,
        "message": message,
        "data": None,
        "errors": errors if errors is not None else [{"code": code, "message": message}],
    }
'''


# --- backend/app/core/handlers.py ---
HANDLERS_PY = '''# -*- coding: utf-8 -*-
"""
Exception Handlers — تبدیل خطاها به ساختار استاندارد پاسخ
================================================================
این فایل تمام handlerهای لازم برای FastAPI را تعریف می‌کند.
هر خطا (چه AppException، چه HTTPException، چه Exception ناشناخته)
به ساختار {success, message, data, errors} تبدیل می‌شود.

نحوه register در main.py:
    from app.core.handlers import register_exception_handlers
    register_exception_handlers(app)

قانون امنیتی (سند ۱۰ بند ۱۰.۴):
  - پیام به کاربر: فارسی، کوتاه، بدون جزئیات فنی
  - جزئیات فنی: فقط در لاگ
  - هرگز stack trace به Frontend نرود
================================================================
"""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import AppException
from app.core.logging import get_logger
from app.core.response import error_response

logger = get_logger(__name__)


# ============================================================
# Handler: AppException (و تمام زیرکلاس‌ها)
# ============================================================
async def app_exception_handler(
    request: Request, exc: AppException
) -> JSONResponse:
    """رسیدگی به Exception های دامنه پروژه."""
    logger.warning(
        "AppException: %s — code=%s — path=%s",
        exc.message, exc.code, request.url.path,
        extra={"details": exc.details},
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            message=exc.message,
            code=exc.code,
            errors=[{"code": exc.code, "message": exc.message, **exc.details}],
        ),
    )


# ============================================================
# Handler: RequestValidationError (Pydantic validation از FastAPI)
# ============================================================
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """رسیدگی به خطاهای validation پارامترها و body."""
    errors = []
    for err in exc.errors():
        field = ".".join(str(loc) for loc in err.get("loc", []))
        errors.append({
            "code": "VALIDATION_ERROR",
            "field": field,
            "message": err.get("msg", "مقدار نامعتبر"),
            "type": err.get("type", "value_error"),
        })

    logger.info(
        "Validation error — path=%s — fields=%s",
        request.url.path, [e["field"] for e in errors],
    )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=error_response(
            message="داده‌های ورودی نامعتبر است",
            code="VALIDATION_ERROR",
            errors=errors,
        ),
    )


# ============================================================
# Handler: HTTPException (خطاهای استاندارد HTTP از Starlette/FastAPI)
# ============================================================
async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """رسیدگی به HTTPException های استاندارد."""
    # تبدیل پیام انگلیسی پیش‌فرض به فارسی برای کدهای متداول
    persian_messages = {
        401: "احراز هویت لازم است",
        403: "دسترسی مجاز نیست",
        404: "آدرس درخواستی یافت نشد",
        405: "متد درخواستی پشتیبانی نمی‌شود",
        429: "تعداد درخواست‌ها از حد مجاز گذشته",
    }

    message = persian_messages.get(exc.status_code, str(exc.detail))
    code = f"HTTP_{exc.status_code}"

    if exc.status_code >= 500:
        logger.error("HTTPException %s — path=%s — %s",
                     exc.status_code, request.url.path, exc.detail)
    else:
        logger.info("HTTPException %s — path=%s",
                    exc.status_code, request.url.path)

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(message=message, code=code),
    )


# ============================================================
# Handler: Exception ناشناخته (حالت آخر)
# ============================================================
async def unhandled_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """رسیدگی به Exceptionهای پیش‌بینی‌نشده.

    این handler هرگز نباید جزئیات فنی را به کاربر نشان دهد.
    """
    logger.exception(
        "Unhandled exception — path=%s — type=%s",
        request.url.path, type(exc).__name__,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response(
            message="خطای داخلی سرور — لطفاً دوباره تلاش کنید",
            code="INTERNAL_SERVER_ERROR",
        ),
    )


# ============================================================
# تابع register
# ============================================================
def register_exception_handlers(app: FastAPI) -> None:
    """ثبت تمام handlerها در FastAPI app.

    باید پس از ساخت app صدا زده شود.
    """
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
'''


# --- backend/app/core/__init__.py ---
CORE_INIT_PY = '''# -*- coding: utf-8 -*-
"""
Core Layer — تنظیمات و ابزارهای پایه

این پکیج شامل:
  • config        : تنظیمات از .env
  • logging       : سیستم لاگ
  • exceptions    : Custom Exception classes
  • response      : Helper پاسخ استاندارد
  • handlers      : Exception Handlers
"""

from app.core.config import settings
from app.core.logging import get_logger, setup_logging
from app.core.response import error_response, success_response

__all__ = [
    "settings",
    "get_logger",
    "setup_logging",
    "success_response",
    "error_response",
]
'''


# --- backend/main.py (بازنویسی شده) ---
MAIN_PY = '''# -*- coding: utf-8 -*-
"""
نقطه ورود FastAPI — سامانه هوشمند ترید
================================================================
این فایل فقط شامل: app instance + middleware + handlers + router include.

قواعد قفل‌شده:
  - Business Logic در services/ — هرگز اینجا
  - Query در repositories/ — هرگز اینجا
  - Validation در schemas/ — هرگز اینجا

نحوه اجرا (در CMD 1):
    cd backend
    venv\\\\Scripts\\\\activate
    uvicorn main:app --reload
================================================================
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import health
from app.core.config import settings
from app.core.handlers import register_exception_handlers
from app.core.logging import get_logger, setup_logging

# تنظیم لاگ پیش از هر چیز
setup_logging()
logger = get_logger(__name__)


# ============================================================
# Lifecycle Events (Startup / Shutdown)
# ============================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """مدیریت چرخه عمر اپلیکیشن"""
    # ===== Startup =====
    logger.info("=" * 60)
    logger.info(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"   Environment: {settings.APP_ENV}")
    logger.info(f"   API: http://{settings.API_HOST}:{settings.API_PORT}{settings.API_PREFIX}")
    logger.info(f"   Docs: http://{settings.API_HOST}:{settings.API_PORT}/docs")
    logger.info("=" * 60)

    yield

    # ===== Shutdown =====
    logger.info(f"👋 {settings.APP_NAME} shutting down...")


# ============================================================
# ساخت FastAPI app
# ============================================================
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="سامانه هوشمند ترید — کریپتو و فارکس",
    lifespan=lifespan,
)


# ============================================================
# Middleware
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Exception Handlers
# ============================================================
register_exception_handlers(app)


# ============================================================
# Router Registration
# ============================================================
app.include_router(health.router, prefix=settings.API_PREFIX)


# ============================================================
# Root Endpoint
# ============================================================
from app.core.response import success_response


@app.get("/")
async def root() -> dict:
    """صفحه ریشه — اطلاعات کلی"""
    return success_response(
        message="سامانه هوشمند ترید فعال است",
        data={
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "health": f"{settings.API_PREFIX}/health",
        },
    )
'''


# --- backend/app/api/v1/routes/health.py (بازنویسی شده) ---
HEALTH_PY = '''# -*- coding: utf-8 -*-
"""
Endpoint بررسی سلامت سیستم
================================================================
این endpoint برای:
  - تأیید فعال بودن API
  - بررسی نسخه و محیط در حال اجرا
  - Health check در Production Monitoring
================================================================
"""

from datetime import datetime, timezone

from fastapi import APIRouter

from app.core.config import settings
from app.core.response import success_response

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check() -> dict:
    """
    بررسی سلامت API.

    خروجی: ساختار استاندارد پاسخ طبق سند ۶
        {success, message, data, errors}
    """
    return success_response(
        message="API سالم است",
        data={
            "status": "ok",
            "version": settings.APP_VERSION,
            "environment": settings.APP_ENV,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )
'''


# --- backend/logs/.gitkeep ---
GITKEEP_CONTENT = """# این فایل فقط برای نگه داشتن پوشه logs/ در Git است.
# محتوای log file ها توسط .gitignore ignore می‌شود.
"""


# ============================================================
# توابع کمکی
# ============================================================
def write_file_full(path: Path, content: str) -> None:
    """نوشتن کامل فایل با ساخت پوشه‌های والد."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def ensure_gitignore_has_log_pattern(gitignore_path: Path) -> str:
    """اطمینان از وجود الگوی exclude لاگ‌ها در .gitignore.

    خروجی: یکی از "added", "already_present", "missing_file"
    """
    if not gitignore_path.exists():
        return "missing_file"

    content = gitignore_path.read_text(encoding="utf-8")

    log_patterns = ["logs/*.log", "logs/*.log.*"]
    new_patterns = [p for p in log_patterns if p not in content]

    if not new_patterns:
        return "already_present"

    addition = "\n# Log files (بدون .gitkeep)\n" + "\n".join(new_patterns) + "\n"
    gitignore_path.write_text(content.rstrip() + "\n" + addition, encoding="utf-8")
    return "added"


# ============================================================
# تابع اصلی
# ============================================================
def main() -> None:
    print("=" * 60)
    print("🛠️  گام ۳ — Core Layer")
    print("=" * 60)
    print(f"📁 ریشه پروژه: {PROJECT_ROOT}")
    print(f"📁 ریشه Backend: {BACKEND_DIR}")
    print()

    if not PROJECT_ROOT.exists():
        print(f"❌ خطا: پوشه ریشه وجود ندارد: {PROJECT_ROOT}")
        sys.exit(1)
    if not BACKEND_DIR.exists():
        print(f"❌ خطا: پوشه backend وجود ندارد: {BACKEND_DIR}")
        sys.exit(1)

    # ============================================================
    # ساخت/بازنویسی فایل‌ها
    # ============================================================
    files = [
        ("backend/app/core/logging.py",            LOGGING_PY,     "📝"),
        ("backend/app/core/exceptions.py",         EXCEPTIONS_PY,  "⚠️ "),
        ("backend/app/core/response.py",           RESPONSE_PY,    "📦"),
        ("backend/app/core/handlers.py",           HANDLERS_PY,    "🎯"),
        ("backend/app/core/__init__.py",           CORE_INIT_PY,   "📂"),
        ("backend/main.py",                        MAIN_PY,        "🐍"),
        ("backend/app/api/v1/routes/health.py",    HEALTH_PY,      "🩺"),
        ("backend/logs/.gitkeep",                  GITKEEP_CONTENT, "📁"),
    ]

    print("📝 ساخت/بازنویسی فایل‌ها:")
    print("-" * 60)
    for rel_path, content, icon in files:
        full = PROJECT_ROOT / rel_path
        existed = full.exists()
        write_file_full(full, content)
        status = "بازنویسی شد" if existed else "ساخته شد   "
        print(f"   {icon} {rel_path:<46} {status}")
    print()

    # ============================================================
    # به‌روزرسانی .gitignore برای فایل‌های log
    # ============================================================
    print("📄 به‌روزرسانی .gitignore:")
    print("-" * 60)
    gitignore_path = PROJECT_ROOT / ".gitignore"
    result = ensure_gitignore_has_log_pattern(gitignore_path)
    if result == "added":
        print("   ✅ الگوی logs/*.log به .gitignore اضافه شد")
    elif result == "already_present":
        print("   ℹ️  الگوی logs/*.log از قبل در .gitignore موجود است")
    else:
        print("   ⚠️  فایل .gitignore وجود ندارد — رد شد")
    print()

    # ============================================================
    # پیام پایانی
    # ============================================================
    print("=" * 60)
    print("✅ گام ۳ — Core Layer کامل شد!")
    print("=" * 60)
    print()
    print("📌 تست در CMD 1 (Backend):")
    print()
    print("   ۱) اگر uvicorn در حال اجراست، آن را با Ctrl+C متوقف کنید")
    print("      (یا اگر --reload دارد، خودش restart می‌شود)")
    print()
    print("   ۲) دوباره اجرا کنید:")
    print("      uvicorn main:app --reload")
    print()
    print("   ۳) باید پیام رنگی استارت‌آپ ببینید:")
    print(r"      2026-05-14 ... INFO     __main__ — 🚀 Trading System v0.1.1")
    print()
    print("   ۴) در مرورگر چک کنید (همانند گام ۲):")
    print("      http://127.0.0.1:8000/")
    print("      http://127.0.0.1:8000/api/v1/health")
    print("      http://127.0.0.1:8000/docs")
    print()
    print("   ۵) تست خطا — این URL باید JSON خطای فارسی استاندارد بدهد:")
    print("      http://127.0.0.1:8000/api/v1/no-such-route")
    print('      → {"success": false, "message": "آدرس درخواستی یافت نشد", ...}')
    print()
    print("   ۶) چک کنید فایل log ساخته شده:")
    print(r"      D:\\Projects\\trading-system\\backend\\logs\\app.log")
    print()
    print("📌 پس از تست موفق، commit کنید (CMD 3):")
    print()
    print(r'   cd /d D:\Projects\trading-system')
    print(r'   git add backend/ scripts/04_setup_core_layer.py .gitignore')
    print(r'   git commit -m "feat(core): add logger, exceptions, handlers, response wrapper"')
    print()


if __name__ == "__main__":
    main()
