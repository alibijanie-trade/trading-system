# -*- coding: utf-8 -*-
"""
53d_fix_test_security_keyerror.py — رفع KeyError در test_create_and_decode_access_token

payload واقعی: {'sub': '42', 'username': 'alice', 'role': 'admin', 'type': 'access', 'iat':..., 'exp':...}
- 'user_id' وجود ندارد ⇒ payload["user_id"] KeyError می‌دهد
- استفاده از .get() حل می‌کند
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEST_FILE = ROOT / "backend" / "tests" / "unit" / "test_security.py"

OLD = """    def test_create_and_decode_access_token(self):
        token = create_access_token(user_id=42, username="alice", role="admin")
        assert isinstance(token, str)
        payload = decode_token(token, expected_type="access")
        assert payload["user_id"] == 42 or payload.get("sub") == "42"
        assert payload.get("username") == "alice" or "alice" in str(payload)
"""

NEW = """    def test_create_and_decode_access_token(self):
        token = create_access_token(user_id=42, username="alice", role="admin")
        assert isinstance(token, str)
        payload = decode_token(token, expected_type="access")
        # توکن می‌تواند 'user_id' یا 'sub' (string) داشته باشد
        assert payload.get("user_id") == 42 or payload.get("sub") == "42"
        assert payload.get("username") == "alice"
        assert payload.get("role") == "admin"
"""


def main() -> int:
    if not TEST_FILE.exists():
        print(f"❌ فایل پیدا نشد: {TEST_FILE}")
        return 1

    text = TEST_FILE.read_text(encoding="utf-8")

    if 'payload.get("user_id") == 42 or payload.get("sub") == "42"' in text:
        print("  ✓  no-op: قبلاً اصلاح شده")
        return 0

    if OLD not in text:
        print("  ⚠️  ساختار با انتظار مطابقت ندارد — اصلاح دستی لازم")
        return 1

    TEST_FILE.write_text(text.replace(OLD, NEW, 1), encoding="utf-8")
    print(f"  ✏️  اصلاح: {TEST_FILE.relative_to(ROOT)}")
    print()
    print("📌 گام بعدی:")
    print("   🟦 tab «1 backend»")
    print("     pytest -v")
    return 0


if __name__ == "__main__":
    sys.exit(main())
