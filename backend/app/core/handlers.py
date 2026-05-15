# -*- coding: utf-8 -*-
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
