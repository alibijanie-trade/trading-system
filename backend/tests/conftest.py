# -*- coding: utf-8 -*-
"""
conftest.py — Fixtures مشترک pytest برای کل tests/

این فایل به‌صورت خودکار توسط pytest پیدا می‌شود.

Fixtures:
  - anyio_backend     : asyncio backend برای anyio
  - test_app          : FastAPI app برای تست (بدون DB)
  - test_client       : httpx.AsyncClient متصل به test_app
"""

from __future__ import annotations

import os

# قبل از import کردن app، متغیرهای محیطی الزامی را تنظیم کنیم
# تا config.py با خطا مواجه نشود.
os.environ.setdefault("SECRET_KEY", "test-secret-key-not-for-production-only-pytest")
os.environ.setdefault(
    "ENCRYPTION_KEY",
    "dGVzdC1lbmNyeXB0aW9uLWtleS0zMi1ieXRlcy1mb3ItcHl0ZXN0ISE=",
)
os.environ.setdefault("APP_ENV", "development")

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient


@pytest.fixture
def anyio_backend() -> str:
    """anyio backend — همیشه asyncio."""
    return "asyncio"


@pytest.fixture(scope="session")
def app_module():
    """Import lazy از app برای جلوگیری از side effects."""
    from main import app

    return app


@pytest_asyncio.fixture
async def client(app_module):
    """httpx AsyncClient متصل به ASGI app — برای تست endpoints."""
    transport = ASGITransport(app=app_module)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
