# -*- coding: utf-8 -*-
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
