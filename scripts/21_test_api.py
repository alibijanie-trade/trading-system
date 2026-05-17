# -*- coding: utf-8 -*-
"""
اسکریپت ۲۱ — تست API از ترمینال (به‌جای Swagger UI)
================================================================
این اسکریپت به Backend در حال اجرا متصل می‌شود و چند endpoint
را تست می‌کند، خروجی را خوانا چاپ می‌کند.

پیش‌نیاز:
  - Backend در tab «1 backend» در حال اجرا باشد (uvicorn روی پورت 8000)

نحوه اجرا (tab «2 scripts»):
    cd /d D:\\Projects\\trading-system
    backend\\venv\\Scripts\\activate
    python scripts\\21_test_api.py

تست‌های انجام‌شده:
  1) GET /                                  → ریشه
  2) GET /api/v1/health                     → health check
  3) GET /api/v1/ohlcv/1?timeframe=1d&limit=5
  4) GET /api/v1/ohlcv/1?timeframe=1d&limit=3&offset=1700  (آخر داده)
  5) GET /api/v1/ohlcv/999?timeframe=1d     → باید 404 بدهد
  6) GET /api/v1/ohlcv/1?timeframe=xx       → باید 200 با لیست خالی
================================================================
"""

import json
import sys

import httpx

BASE_URL = "http://127.0.0.1:8000"


# ============================================================
# توابع کمکی
# ============================================================
def hr(title: str) -> None:
    """خط جداکننده با عنوان"""
    print()
    print("=" * 72)
    print(f"  {title}")
    print("=" * 72)


def request(method: str, path: str, expected_status: int = 200) -> dict | None:
    """
    یک درخواست به API + چاپ نتیجه + بررسی status code.

    Returns:
        پاسخ JSON یا None در صورت خطا
    """
    url = f"{BASE_URL}{path}"
    print(f"\n[{method}] {url}")
    print(f"  انتظار: HTTP {expected_status}")

    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.request(method, url)
    except httpx.ConnectError:
        print("  ✗ خطا: اتصال برقرار نشد")
        print("    آیا Backend در tab «1 backend» روشن است؟")
        sys.exit(2)
    except httpx.RequestError as e:
        print(f"  ✗ خطای شبکه: {e}")
        return None

    status_ok = resp.status_code == expected_status
    icon = "✓" if status_ok else "✗"
    print(f"  {icon} HTTP {resp.status_code}")

    try:
        data = resp.json()
    except json.JSONDecodeError:
        print(f"  پاسخ غیر JSON: {resp.text[:200]}")
        return None

    # چاپ بخش‌های مهم
    if isinstance(data, dict):
        print(f"  success: {data.get('success')}")
        print(f"  message: {data.get('message')}")

        d = data.get("data")
        if isinstance(d, dict):
            # نمایش کلیدهای داده + شمارش candles
            keys_summary = []
            for k, v in d.items():
                if k == "candles" and isinstance(v, list):
                    keys_summary.append(f"candles=list[{len(v)}]")
                elif isinstance(v, (dict, list)):
                    keys_summary.append(f"{k}={type(v).__name__}")
                else:
                    keys_summary.append(f"{k}={v}")
            print(f"  data : {{ {', '.join(keys_summary)} }}")

            # نمونه ۲ کندل اول/آخر
            candles = d.get("candles")
            if isinstance(candles, list) and candles:
                print(f"  نمونه کندل اول:")
                print(f"    {json.dumps(candles[0], ensure_ascii=False)}")
                if len(candles) > 1:
                    print(f"  نمونه کندل آخر:")
                    print(f"    {json.dumps(candles[-1], ensure_ascii=False)}")
        elif d is not None:
            print(f"  data : {d}")

        errors = data.get("errors")
        if errors:
            print(f"  errors: {errors}")

    return data


# ============================================================
# اجرا
# ============================================================
def main() -> None:
    print("=" * 72)
    print("  اسکریپت ۲۱ — تست API از ترمینال")
    print("=" * 72)
    print(f"  Base URL: {BASE_URL}")

    # ============================================================
    # تست ۱ — ریشه
    # ============================================================
    hr("تست ۱: GET / (ریشه)")
    request("GET", "/")

    # ============================================================
    # تست ۲ — health
    # ============================================================
    hr("تست ۲: GET /api/v1/health")
    request("GET", "/api/v1/health")

    # ============================================================
    # تست ۳ — اولین ۵ کندل
    # ============================================================
    hr("تست ۳: GET /ohlcv/1?timeframe=1d&limit=5")
    request("GET", "/api/v1/ohlcv/1?timeframe=1d&limit=5")

    # ============================================================
    # تست ۴ — آخرین کندل‌ها (offset نزدیک پایان)
    # ============================================================
    hr("تست ۴: GET /ohlcv/1?timeframe=1d&limit=3&offset=1700")
    request("GET", "/api/v1/ohlcv/1?timeframe=1d&limit=3&offset=1700")

    # ============================================================
    # تست ۵ — symbol_id نامعتبر (انتظار 404)
    # ============================================================
    hr("تست ۵: GET /ohlcv/999  (symbol_id نامعتبر — انتظار 404)")
    request("GET", "/api/v1/ohlcv/999?timeframe=1d", expected_status=404)

    # ============================================================
    # تست ۶ — تایم‌فریم بدون داده
    # ============================================================
    hr("تست ۶: GET /ohlcv/1?timeframe=xx  (تایم‌فریم نامعلوم — انتظار 200 با لیست خالی)")
    request("GET", "/api/v1/ohlcv/1?timeframe=xx")

    print()
    print("=" * 72)
    print("  ✅ پایان تست‌ها")
    print("=" * 72)


if __name__ == "__main__":
    main()
