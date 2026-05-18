# -*- coding: utf-8 -*-
"""
tests/unit/test_response.py — تست توابع response wrapper

پوشش:
  - success_response : ساختار {success, message, data, errors}
  - error_response   : ساختار خطا + errors list
"""

import pytest
from app.core.response import error_response, success_response

pytestmark = pytest.mark.unit


class TestSuccessResponse:
    def test_default(self):
        r = success_response()
        assert r["success"] is True
        assert r["message"] == "عملیات با موفقیت انجام شد"
        assert r["data"] is None
        assert r["errors"] is None

    def test_with_data(self):
        r = success_response(data={"id": 5}, message="ساخته شد")
        assert r["success"] is True
        assert r["data"] == {"id": 5}
        assert r["message"] == "ساخته شد"
        assert r["errors"] is None

    def test_data_can_be_list(self):
        r = success_response(data=[1, 2, 3])
        assert r["data"] == [1, 2, 3]


class TestErrorResponse:
    def test_default(self):
        r = error_response(message="خطا رخ داد")
        assert r["success"] is False
        assert r["message"] == "خطا رخ داد"
        assert r["data"] is None

    def test_with_errors(self):
        r = error_response(
            message="نامعتبر",
            errors=[{"code": "X", "message": "Y"}],
        )
        assert r["errors"] == [{"code": "X", "message": "Y"}]
