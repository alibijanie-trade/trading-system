# -*- coding: utf-8 -*-
"""
اسکریپت ۲۷d — تست خودکار رنگ‌های بایننس در تم binance-dark
================================================================
این اسکریپت idempotent است — فقط می‌خواند.

چک می‌کند رنگ‌های رسمی بایننس دقیقاً ست شده‌اند:
  - --color-primary       #F0B90B  (طلایی برند)
  - --color-bg            #181A20
  - --color-card          #1E2329
  - --color-border        #2B3139
  - --color-text          #EAECEF
  - --color-text-muted    #848E9C
  - --color-success       #0ECB81  (سبز بایننس)
  - --color-danger        #F6465D  (قرمز بایننس)
  - --color-link          #F0B90B  ⭐ بحرانی: طلایی نه آبی

همچنین چک می‌کند:
  - npm run build بدون خطا (proof of valid CSS/JS)
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
THEMES_JS = FRONTEND_SRC / "themes" / "themes.js"
INDEX_CSS = FRONTEND_SRC / "index.css"

CHECKS = []


def check(desc, condition, detail=""):
    CHECKS.append((desc, bool(condition), detail))


# ============================================================
# رنگ‌های رسمی بایننس
# ============================================================
BINANCE_COLORS = {
    "--color-primary": "#F0B90B",
    "--color-primary-hover": "#FCD535",
    "--color-bg": "#181A20",
    "--color-bg-elevated": "#1E2329",
    "--color-card": "#1E2329",
    "--color-card-hover": "#2B2F36",
    "--color-border": "#2B3139",
    "--color-border-strong": "#474D57",
    "--color-text": "#EAECEF",
    "--color-text-muted": "#848E9C",
    "--color-success": "#0ECB81",
    "--color-danger": "#F6465D",
    "--color-link": "#F0B90B",
}

# رنگ‌های قدیمی TradingView — اگر هنوز باشند، خطا
TRADINGVIEW_REMNANTS = {
    "--color-link": "#2962ff",     # آبی به جای طلایی
    "--color-bg": "#1e222d",       # خاکستری TradingView
    "--color-text": "#d1d4dc",     # متن TradingView
    "--color-success": "#26a69a",  # فیروزه‌ای TradingView
    "--color-danger": "#ef5350",   # نارنجی-قرمز TradingView
}


# ============================================================
# استخراج بلوک binance-dark از themes.js
# ============================================================
def extract_binance_block(src: str) -> str:
    """بلوک binance-dark را استخراج می‌کند."""
    pattern = re.compile(
        r'"binance-dark":\s*\{.*?^  \},',
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(src)
    return match.group(0) if match else ""


# ============================================================
# چک‌ها
# ============================================================

# 1) وجود فایل‌ها
check("themes.js موجود است", THEMES_JS.exists())
check("index.css موجود است", INDEX_CSS.exists())

if not (THEMES_JS.exists() and INDEX_CSS.exists()):
    print("❌ فایل‌ها موجود نیستند. ابتدا اسکریپت ۲۷ + ۲۷c را اجرا کنید.")
    sys.exit(1)

themes_src = THEMES_JS.read_text(encoding="utf-8")
css_src = INDEX_CSS.read_text(encoding="utf-8")
binance_block = extract_binance_block(themes_src)

check("بلوک binance-dark در themes.js پیدا شد", bool(binance_block))

# 2) هر رنگ بایننس باید در بلوک باشد
print()
for var, color in BINANCE_COLORS.items():
    expected = f'"{var}": "{color}"'
    check(f"binance-dark: {var} = {color}", expected in binance_block)

# 3) رنگ‌های TradingView نباید در بلوک binance-dark باشند
print()
for var, old_color in TRADINGVIEW_REMNANTS.items():
    bad = f'"{var}": "{old_color}"'
    check(
        f"بدون رنگ TradingView: {var} ≠ {old_color}",
        bad not in binance_block,
        f"found: {bad}",
    )

# 4) index.css :root شامل رنگ‌های بایننس
print()
for var, color in BINANCE_COLORS.items():
    expected_css = f"{var}: {color};"
    # case-insensitive چون hex می‌تواند uppercase/lowercase باشد
    check(
        f"index.css :root شامل {var}: {color}",
        expected_css.lower() in css_src.lower(),
    )

# 5) سایر تم‌ها دست‌نخورده‌اند (بقیه تم‌ها باید هنوز موجود باشند)
print()
for tid in ["light-minimal", "dark-modern", "pastel", "sky-blue"]:
    check(f"تم «{tid}» همچنان موجود است", f'"{tid}"' in themes_src)

# 6) npm run build (proof of compilation)
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
print("📋 نتایج تست رنگ‌های بایننس:")
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
    print(f"✅ همه {passed} چک سبز — تم binance-dark دقیقاً مطابق بایننس است.")
    print("=" * 64)
    print()
    print("چک بصری نهایی در مرورگر:")
    print("  http://localhost:5173/  →  refresh  →  لینک «BTC/USDT» باید طلایی")
    print("                                        پس‌زمینه باید مشکی‌تر")
    sys.exit(0)
else:
    print(f"❌ {failed} چک ناموفق از {passed + failed}")
    print("=" * 64)
    sys.exit(1)
