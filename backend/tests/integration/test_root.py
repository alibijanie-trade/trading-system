# -*- coding: utf-8 -*-
"""
tests/integration/test_root.py — تست GET /

پوشش:
  - status 200
  - ساختار پاسخ استاندارد
"""

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_root_returns_200(client):
    r = await client.get("/")
    assert r.status_code == 200


async def test_root_returns_app_info(client):
    r = await client.get("/")
    data = r.json()["data"]
    assert "name" in data
    assert "version" in data
    assert data["docs"] == "/docs"
