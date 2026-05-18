# -*- coding: utf-8 -*-
"""
53b_test_backend_pytest.py — تست راه‌اندازی pytest backend

این اسکریپت اجرای واقعی pytest را انجام نمی‌دهد (آن کار دستی است).
فقط بررسی می‌کند:
  ۱. همه فایل‌های pytest infrastructure ساخته شده‌اند
  ۲. requirements.txt شامل dev deps است
  ۳. pytest.ini شامل markers و asyncio_mode است
  ۴. conftest.py شامل client fixture است
  ۵. ۵ فایل تست با ساختار صحیح هستند
  ۶. docs/BACKEND_TESTING.md شامل ۱۰ بخش است
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "backend"
TESTS = BACKEND / "tests"
DOCS = ROOT / "docs"

PASS = "✅"
FAIL = "❌"


def main() -> int:
    passes: list[str] = []
    failures: list[str] = []

    # ---------- فایل‌ها موجود ----------
    expected_files = [
        BACKEND / "pytest.ini",
        BACKEND / ".coveragerc",
        TESTS / "conftest.py",
        TESTS / "unit" / "test_response.py",
        TESTS / "unit" / "test_security.py",
        TESTS / "unit" / "test_exceptions.py",
        TESTS / "integration" / "test_health.py",
        TESTS / "integration" / "test_root.py",
        DOCS / "BACKEND_TESTING.md",
    ]
    for f in expected_files:
        if f.exists():
            passes.append(f"فایل موجود: {f.relative_to(ROOT)}")
        else:
            failures.append(f"فایل گم: {f.relative_to(ROOT)}")

    # ---------- requirements.txt ----------
    req = (BACKEND / "requirements.txt").read_text(encoding="utf-8")
    for pkg in ["pytest==", "pytest-asyncio==", "pytest-cov=="]:
        if pkg in req:
            passes.append(f"requirements.txt شامل {pkg.rstrip('=')}")
        else:
            failures.append(f"requirements.txt گم: {pkg}")

    # ---------- pytest.ini ----------
    if (BACKEND / "pytest.ini").exists():
        pi = (BACKEND / "pytest.ini").read_text(encoding="utf-8")
        for key in ["asyncio_mode = auto", "unit:", "integration:", "testpaths = tests"]:
            if key in pi:
                passes.append(f"pytest.ini دارد: {key}")
            else:
                failures.append(f"pytest.ini گم: {key}")

    # ---------- conftest.py ----------
    if (TESTS / "conftest.py").exists():
        cf = (TESTS / "conftest.py").read_text(encoding="utf-8")
        for key in ["SECRET_KEY", "AsyncClient", "ASGITransport", "@pytest_asyncio.fixture"]:
            if key in cf:
                passes.append(f"conftest.py دارد: {key}")
            else:
                failures.append(f"conftest.py گم: {key}")

    # ---------- test files ----------
    test_checks = [
        ("test_response.py", ["success_response", "error_response", "pytestmark"]),
        ("test_security.py", ["hash_password", "verify_password", "create_access_token"]),
        ("test_exceptions.py", ["AppException", "NotFoundError", "ValidationError"]),
        ("test_health.py", ["GET", "/api/v1/health", "async def test_"]),
        ("test_root.py", ["async def test_", "/"]),
    ]
    for fname, keywords in test_checks:
        # Find the file
        found = None
        for f in (TESTS / "unit", TESTS / "integration"):
            if (f / fname).exists():
                found = f / fname
                break
        if not found:
            failures.append(f"{fname}: فایل پیدا نشد")
            continue
        text = found.read_text(encoding="utf-8")
        for kw in keywords:
            if kw in text:
                passes.append(f"{fname} دارد: {kw}")
            else:
                failures.append(f"{fname} گم: {kw}")

    # ---------- BACKEND_TESTING.md ----------
    if (DOCS / "BACKEND_TESTING.md").exists():
        doc = (DOCS / "BACKEND_TESTING.md").read_text(encoding="utf-8")
        sections = [
            "## ۱. نصب وابستگی‌ها",
            "## ۲. ساختار پوشه‌ها",
            "## ۳. اجرای تست‌ها",
            "## ۴. Coverage Report",
            "## ۵. نوشتن تست جدید",
            "## ۶. Fixtures موجود",
            "## ۷. Markers",
            "## ۸. تست async functions",
            "## ۹. CI/CD آینده",
            "## ۱۰. عیب‌یابی",
        ]
        for sec in sections:
            if sec in doc:
                passes.append(f"BACKEND_TESTING.md دارد: {sec[:45]}")
            else:
                failures.append(f"BACKEND_TESTING.md گم: {sec}")

        # محتوای کلیدی
        for key in ["pytest -m unit", "pytest -m integration", "--cov=app", "AsyncClient"]:
            if key in doc:
                passes.append(f"BACKEND_TESTING.md مثال: {key}")
            else:
                failures.append(f"BACKEND_TESTING.md گم: {key}")

    return _report(passes, failures)


def _report(passes: list[str], failures: list[str]) -> int:
    total = len(passes) + len(failures)
    print()
    print("=" * 64)
    print(f"  گزارش تست — 53b_test_backend_pytest")
    print(f"  {len(passes)} pass / {len(failures)} fail / {total} total")
    print("=" * 64)
    print()
    for p in passes:
        print(f"  {PASS} {p}")
    for f in failures:
        print(f"  {FAIL} {f}")
    print()
    print("=" * 64)
    if failures:
        print(f"  ❌ FAILED — {len(failures)} مورد نیاز به اصلاح")
        print("=" * 64)
        return 1
    print(f"  ✅ همه {len(passes)} تست pass شدند")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    sys.exit(main())
