# -*- coding: utf-8 -*-
"""
tests/unit/test_security.py — تست bcrypt + JWT helpers

پوشش:
  - hash_password / verify_password
  - create_access_token / decode_token
  - رفتار رمز عبور > 72 بایت (truncate)
"""

import os

# قبل از import مطمئن باشیم env var ها هست
os.environ.setdefault("SECRET_KEY", "test-secret-key-not-for-production-only-pytest")
os.environ.setdefault(
    "ENCRYPTION_KEY",
    "dGVzdC1lbmNyeXB0aW9uLWtleS0zMi1ieXRlcy1mb3ItcHl0ZXN0ISE=",
)

import pytest
from app.core.security import create_access_token, decode_token, hash_password, verify_password

pytestmark = pytest.mark.unit


class TestPassword:
    def test_hash_returns_string(self):
        h = hash_password("password123")
        assert isinstance(h, str)
        assert h.startswith("$2b$") or h.startswith("$2a$")

    def test_hash_is_different_each_call(self):
        h1 = hash_password("password123")
        h2 = hash_password("password123")
        assert h1 != h2  # bcrypt salt تصادفی

    def test_verify_correct_password(self):
        h = hash_password("mypassword")
        assert verify_password("mypassword", h) is True

    def test_verify_wrong_password(self):
        h = hash_password("mypassword")
        assert verify_password("wrongpassword", h) is False

    def test_long_password_truncated_to_72_bytes(self):
        """bcrypt 4.x طولانی‌تر از 72 بایت را silently truncate نمی‌کند.
        پروژه باید خودش این کار را انجام دهد."""
        long_pwd = "a" * 100
        h = hash_password(long_pwd)
        # اگر truncation کار کند: همان رمز با همان اول 72 بایت verify می‌شود
        assert verify_password("a" * 72, h) is True


class TestJWT:
    def test_create_and_decode_access_token(self):
        token = create_access_token(user_id=42, username="alice", role="admin")
        assert isinstance(token, str)
        payload = decode_token(token, expected_type="access")
        # توکن می‌تواند 'user_id' یا 'sub' (string) داشته باشد
        assert payload.get("user_id") == 42 or payload.get("sub") == "42"
        assert payload.get("username") == "alice"
        assert payload.get("role") == "admin"

    def test_decoded_has_exp(self):
        token = create_access_token(user_id=1, username="u", role="user")
        payload = decode_token(token, expected_type="access")
        assert "exp" in payload

    def test_decoded_type_is_access(self):
        token = create_access_token(user_id=1, username="u", role="user")
        payload = decode_token(token, expected_type="access")
        # type field یا 'access' در payload باشد
        assert payload.get("type") == "access" or "access" in str(payload)
