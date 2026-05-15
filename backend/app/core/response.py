# -*- coding: utf-8 -*-
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
