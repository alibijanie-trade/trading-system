# -*- coding: utf-8 -*-
"""
tests/integration/test_health.py — تست GET /api/v1/health

پوشش:
  - status 200
  - ساختار پاسخ {success, message, data, errors}
  - data شامل status, version, environment, timestamp
"""

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_health_endpoint_returns_200(client):
    r = await client.get("/api/v1/health")
    assert r.status_code == 200


async def test_health_response_structure(client):
    r = await client.get("/api/v1/health")
    body = r.json()
    assert "success" in body
    assert "message" in body
    assert "data" in body
    assert "errors" in body
    assert body["success"] is True
    assert body["errors"] is None


async def test_health_data_fields(client):
    r = await client.get("/api/v1/health")
    data = r.json()["data"]
    assert data["status"] == "ok"
    assert "version" in data
    assert "environment" in data
    assert "timestamp" in data
