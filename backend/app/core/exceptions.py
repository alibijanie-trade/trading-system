# -*- coding: utf-8 -*-
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
