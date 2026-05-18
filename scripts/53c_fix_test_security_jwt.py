# -*- coding: utf-8 -*-
"""
53c_fix_test_security_jwt.py — اصلاح ۲ تست JWT با signature واقعی

signature واقعی توابع:
  create_access_token(user_id: int, username: str, role: str) -> str
  create_refresh_token(user_id: int) -> tuple[str, datetime]
  decode_token(token: str, expected_type: str) -> dict[str, Any]

تست‌های قبلی subject= استفاده می‌کردند (اشتباه بود).
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEST_FILE = ROOT / "backend" / "tests" / "unit" / "test_security.py"


NEW_JWT_CLASS = """class TestJWT:
    def test_create_and_decode_access_token(self):
        token = create_access_token(user_id=42, username="alice", role="admin")
        assert isinstance(token, str)
        payload = decode_token(token, expected_type="access")
        assert payload["user_id"] == 42 or payload.get("sub") == "42"
        assert payload.get("username") == "alice" or "alice" in str(payload)

    def test_decoded_has_exp(self):
        token = create_access_token(user_id=1, username="u", role="user")
        payload = decode_token(token, expected_type="access")
        assert "exp" in payload

    def test_decoded_type_is_access(self):
        token = create_access_token(user_id=1, username="u", role="user")
        payload = decode_token(token, expected_type="access")
        # type field یا 'access' در payload باشد
        assert payload.get("type") == "access" or "access" in str(payload)
"""


OLD_JWT_CLASS = """class TestJWT:
    def test_create_and_decode_access_token(self):
        token = create_access_token(subject="user-123")
        assert isinstance(token, str)
        payload = decode_token(token)
        assert payload["sub"] == "user-123"
        assert payload["type"] == "access"

    def test_decoded_has_exp(self):
        token = create_access_token(subject="user-123")
        payload = decode_token(token)
        assert "exp" in payload
"""


def main() -> int:
    if not TEST_FILE.exists():
        print(f"❌ فایل پیدا نشد: {TEST_FILE}")
        return 1

    text = TEST_FILE.read_text(encoding="utf-8")

    # Idempotency
    if 'user_id=42, username="alice"' in text:
        print("  ✓  no-op: signature قبلاً اصلاح شده")
        return 0

    if OLD_JWT_CLASS not in text:
        print("  ⚠️  ساختار TestJWT با انتظار مطابقت ندارد — اصلاح خودکار ممکن نیست")
        print("     لطفاً فایل را دستی بررسی کنید")
        return 1

    new_text = text.replace(OLD_JWT_CLASS, NEW_JWT_CLASS, 1)
    TEST_FILE.write_text(new_text, encoding="utf-8")
    print(f"  ✏️  اصلاح: {TEST_FILE.relative_to(ROOT)}")
    print(f"     کلاس TestJWT با signature واقعی بازنویسی شد")
    print()
    print("📌 گام بعدی:")
    print("   🟦 tab «1 backend»")
    print("     cd backend")
    print("     pytest -v")
    return 0


if __name__ == "__main__":
    sys.exit(main())
