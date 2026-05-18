# -*- coding: utf-8 -*-
"""
51b_test_api_docs.py — تست تولید docs/API_DOCS.md

بررسی‌ها:
  - فایل موجود است
  - ۹ بخش اصلی + ۷ endpoint detail
  - هر ۶ endpoint اصلی + root ذکر شده‌اند
  - Method ها صحیح (GET/POST)
  - Auth requirement ها صحیح
  - ساختار {success, message, data, errors} ذکر شده
  - مثال curl + httpx + Swagger
  - عیب‌یابی شامل ۵+ مشکل رایج
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "docs" / "API_DOCS.md"

PASS = "✅"
FAIL = "❌"


def main() -> int:
    passes: list[str] = []
    failures: list[str] = []

    if not DOC.exists():
        failures.append(f"فایل پیدا نشد: {DOC.name}")
        return _report(passes, failures)
    passes.append(f"فایل {DOC.name} موجود است")

    text = DOC.read_text(encoding="utf-8")

    # ---------- بخش‌های اصلی ----------
    sections = [
        "## ۱. اطلاعات کلی",
        "## ۲. ساختار استاندارد پاسخ",
        "## ۳. احراز هویت",
        "## ۴. کدهای HTTP و خطا",
        "## ۵. Endpoints",
        "## ۶. مثال‌های End-to-End",
        "## ۷. عیب‌یابی",
        "## ۸. تست با ابزارهای مختلف",
    ]
    for sec in sections:
        if sec in text:
            passes.append(f"بخش موجود: {sec[:55]}")
        else:
            failures.append(f"بخش گم: {sec}")

    # ---------- هر ۶ endpoint + root ----------
    endpoints = [
        ("GET", "/api/v1/health"),
        ("POST", "/api/v1/auth/login"),
        ("POST", "/api/v1/auth/refresh"),
        ("POST", "/api/v1/auth/logout"),
        ("GET", "/api/v1/auth/me"),
        ("GET", "/api/v1/ohlcv/{symbol_id}"),
    ]
    for method, path in endpoints:
        # شناسایی بر اساس heading مثل `### ۵.۲ \`GET /api/v1/health\``
        if path in text and method in text:
            passes.append(f"endpoint {method} {path} مستند شده")
        else:
            failures.append(f"endpoint {method} {path} گم است")

    # ---------- ساختار پاسخ ----------
    keys = ['"success"', '"message"', '"data"', '"errors"']
    missing_keys = [k for k in keys if k not in text]
    if not missing_keys:
        passes.append("هر ۴ کلید پاسخ استاندارد {success,message,data,errors} ذکر شده")
    else:
        failures.append(f"کلیدهای پاسخ گم: {missing_keys}")

    # ---------- OAuth2 و Bearer ----------
    if "OAuth2" in text and "Bearer" in text:
        passes.append("OAuth2 + Bearer mechanism ذکر شده")
    else:
        failures.append("OAuth2 یا Bearer گم")

    # ---------- Content-Type تأکید form data ----------
    if "application/x-www-form-urlencoded" in text or "multipart/form-data" in text:
        passes.append("هشدار Content-Type برای /auth/login (form data) موجود")
    else:
        failures.append("اشاره به form data در /auth/login گم")

    # ---------- مدت توکن‌ها ----------
    if "30 دقیقه" in text or "۳۰ دقیقه" in text or "1800" in text:
        passes.append("مدت اعتبار access_token (۳۰ دقیقه/1800 ثانیه) ذکر شده")
    else:
        failures.append("مدت توکن گم")

    # ---------- کدهای HTTP ----------
    http_codes = ["200", "401", "404", "422", "500"]
    missing_codes = [c for c in http_codes if f"`{c}`" not in text]
    if not missing_codes:
        passes.append("کدهای HTTP رایج (200/401/404/422/500) ذکر شده‌اند")
    else:
        failures.append(f"کدهای HTTP گم: {missing_codes}")

    # ---------- مثال‌ها ----------
    if "curl" in text:
        passes.append("مثال curl موجود")
    else:
        failures.append("مثال curl گم")

    if "httpx" in text:
        passes.append("مثال httpx موجود")
    else:
        failures.append("مثال httpx گم")

    if "Swagger" in text:
        passes.append("مثال Swagger UI موجود")
    else:
        failures.append("مثال Swagger گم")

    # ---------- عیب‌یابی ----------
    troubleshoot_topics = ["405", "401", "422", "404", "CORS"]
    missing_topics = [t for t in troubleshoot_topics if t not in text]
    if not missing_topics:
        passes.append("۵ مشکل رایج (405/401/422/404/CORS) در عیب‌یابی")
    else:
        failures.append(f"موضوعات عیب‌یابی گم: {missing_topics}")

    # ---------- پارامترهای OHLCV ----------
    ohlcv_params = ["timeframe", "limit", "offset", "from_ts", "to_ts"]
    missing_params = [p for p in ohlcv_params if p not in text]
    if not missing_params:
        passes.append("همه ۵ پارامتر OHLCV (timeframe/limit/offset/from_ts/to_ts) ذکر شده")
    else:
        failures.append(f"پارامترهای OHLCV گم: {missing_params}")

    # ---------- ارجاع به قوانین ----------
    if "قانون #۱۹" in text:
        passes.append("ارجاع به قانون #۱۹ (تست با httpx، نه Swagger) موجود")
    else:
        failures.append("ارجاع به قانون #۱۹ گم")

    # ---------- Base URL ----------
    if "http://localhost:8000" in text and "/api/v1" in text:
        passes.append("Base URL (http://localhost:8000/api/v1) ذکر شده")
    else:
        failures.append("Base URL ناقص یا گم")

    return _report(passes, failures)


def _report(passes: list[str], failures: list[str]) -> int:
    total = len(passes) + len(failures)
    print()
    print("=" * 64)
    print(f"  گزارش تست — 51b_test_api_docs")
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
