# -*- coding: utf-8 -*-
"""
اسکریپت ۲۷f — تست خودکار Binance UI Polish
================================================================
این اسکریپت idempotent است — فقط می‌خواند.

چک می‌کند state های تعاملی به‌درستی پیاده شده‌اند:
  - index.css: rules برای button:hover/:active/:focus-visible
  - index.css: rules برای select:hover/:focus
  - index.css: rules برای input:focus
  - index.css: rules برای [data-card-link]:hover
  - HomePage: Link با data-card-link="true"
  - npm run build بدون خطا
================================================================
"""

import os
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
FRONTEND_SRC = FRONTEND_DIR / "src"
INDEX_CSS = FRONTEND_SRC / "index.css"
HOME_PAGE = FRONTEND_SRC / "pages" / "HomePage.jsx"

CHECKS = []


def check(desc, condition, detail=""):
    CHECKS.append((desc, bool(condition), detail))


# ============================================================
# خواندن فایل‌ها
# ============================================================
check("index.css موجود است", INDEX_CSS.exists())
check("HomePage.jsx موجود است", HOME_PAGE.exists())

if not (INDEX_CSS.exists() and HOME_PAGE.exists()):
    print("❌ فایل‌ها موجود نیستند.")
    sys.exit(1)

css = INDEX_CSS.read_text(encoding="utf-8")
home = HOME_PAGE.read_text(encoding="utf-8")


# ============================================================
# چک‌های index.css — interactive states
# ============================================================
print()

# button states
check(
    "button:hover با filter brightness",
    re.search(r"button:hover:not\(:disabled\)\s*\{[^}]*filter:\s*brightness", css) is not None,
)
check(
    "button:active با translateY",
    re.search(r"button:active:not\(:disabled\)\s*\{[^}]*translateY", css) is not None,
)
check(
    "button:focus-visible با outline طلایی",
    re.search(
        r"button:focus-visible\s*\{[^}]*outline:\s*2px solid var\(--color-primary\)",
        css,
    )
    is not None,
)
check(
    "button:disabled با cursor not-allowed",
    "button:disabled" in css and "not-allowed" in css,
)

# select states
check(
    "select:hover با border-color تغییر",
    re.search(r"select:hover\s*\{[^}]*border-color:\s*var\(--color-border-strong\)", css)
    is not None,
)
check(
    "select:focus با border-color طلایی",
    re.search(r"select:focus\s*\{[^}]*border-color:\s*var\(--color-primary\)", css) is not None,
)

# input focus
check(
    "input:focus با border-color طلایی",
    re.search(r"input:focus[^{]*\{[^}]*border-color:\s*var\(--color-primary\)", css) is not None,
)

# data-card-link
check(
    'rule [data-card-link="true"] تعریف شده',
    '[data-card-link="true"]' in css,
)
check(
    "[data-card-link]:hover با background تغییر",
    re.search(
        r'\[data-card-link="true"\]:hover\s*\{[^}]*background:\s*var\(--color-card-hover\)',
        css,
    )
    is not None,
)

# transition properties (smooth feel)
check("button با transition", "transition:" in css and "filter" in css)
check("select با transition", re.search(r"input,?\s*select", css) is not None)

# scrollbar still works
check(
    "scrollbar با transition",
    "::-webkit-scrollbar-thumb" in css and "transition" in css,
)


# ============================================================
# چک‌های HomePage.jsx
# ============================================================
print()
check('HomePage: Link با data-card-link="true"', 'data-card-link="true"' in home)
check(
    "HomePage: h1 با fontWeight 600",
    re.search(r"fontWeight:\s*600", home) is not None,
)
check(
    "HomePage: header «نمودارها» با uppercase",
    "textTransform" in home and "uppercase" in home,
)
check(
    "HomePage: کارت Link با border var",
    re.search(r'border:\s*"1px solid var\(--color-border\)"', home) is not None,
)


# ============================================================
# چک ۱۲: npm run build
# ============================================================
print()
print("⏳ npm run build در حال اجرا...")
build_ok = False
build_detail = ""

node_modules = FRONTEND_DIR / "node_modules"
node_bin = node_modules / ".bin"

if not node_bin.exists():
    build_detail = "node_modules\\.bin پیدا نشد"
else:
    env = os.environ.copy()
    env["PATH"] = str(node_bin) + os.pathsep + env.get("PATH", "")

    try:
        result = subprocess.run(
            "npm run build",
            cwd=str(FRONTEND_DIR),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=True,
            timeout=120,
        )
        build_ok = result.returncode == 0
        build_detail = f"exit={result.returncode}"
        if not build_ok:
            print("--- stderr ---")
            print((result.stderr or "")[-1500:])
    except Exception as e:
        build_detail = f"exception: {e}"

check("npm run build بدون خطا", build_ok, build_detail)


# ============================================================
# گزارش
# ============================================================
print()
print("=" * 64)
print("📋 نتایج تست Binance Polish:")
print("=" * 64)
passed = sum(1 for _, ok, _ in CHECKS if ok)
failed = sum(1 for _, ok, _ in CHECKS if not ok)

for desc, ok, detail in CHECKS:
    mark = "✅" if ok else "❌"
    extra = f"  ← {detail}" if detail and not ok else ""
    print(f"  {mark} {desc}{extra}")

print()
print("=" * 64)
if failed == 0:
    print(f"✅ همه {passed} چک سبز — UI Polish بایننس کامل است.")
    print("=" * 64)
    print()
    print("چک بصری در مرورگر:")
    print("  ۱) موس روی «خروج» → روشن‌تر")
    print("  ۲) موس روی کارت BTC/USDT → پس‌زمینه روشن")
    print("  ۳) Tab روی dropdown → border طلایی")
    print("  ۴) کلیک روی هر دکمه → فرورفتن لحظه‌ای")
    sys.exit(0)
else:
    print(f"❌ {failed} چک ناموفق از {passed + failed}")
    print("=" * 64)
    sys.exit(1)
