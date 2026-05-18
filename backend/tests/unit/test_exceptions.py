# -*- coding: utf-8 -*-
"""
tests/unit/test_exceptions.py — تست سلسله مراتب AppException

پوشش:
  - AppException + subclasses (status_code، default_message، default_code)
  - override پیام و کد
"""

import pytest
from app.core.exceptions import (
    AppException,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ValidationError,
)

pytestmark = pytest.mark.unit


class TestAppException:
    def test_base_default(self):
        e = AppException()
        assert e.status_code == 500
        assert e.code == "INTERNAL_ERROR"
        assert e.message == "خطای داخلی سرور"

    def test_override_message_and_code(self):
        e = AppException(message="custom", code="CUSTOM_CODE")
        assert e.message == "custom"
        assert e.code == "CUSTOM_CODE"


class TestSubclasses:
    def test_validation_error(self):
        e = ValidationError()
        assert e.status_code == 400
        assert e.code == "VALIDATION_ERROR"

    def test_authentication_error(self):
        e = AuthenticationError()
        assert e.status_code == 401
        assert e.code == "AUTHENTICATION_FAILED"

    def test_authorization_error(self):
        e = AuthorizationError()
        assert e.status_code == 403
        assert e.code == "ACCESS_DENIED"

    def test_not_found_error(self):
        e = NotFoundError()
        assert e.status_code == 404

    def test_details_is_dict(self):
        e = NotFoundError(details={"resource_id": 5})
        assert e.details == {"resource_id": 5}
