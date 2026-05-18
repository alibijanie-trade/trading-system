# -*- coding: utf-8 -*-
"""
اسکریپت ۲۷b — تست خودکار زیرگام ۸.۱ (Theme Engine Foundation)
================================================================
این اسکریپت idempotent است — فقط می‌خواند، نمی‌نویسد.

پوشش کامل ۷ چک قبلی به‌صورت خودکار:
  1) وجود ۸ فایل
  2) themes.js: ۵ تم با CSS variable های لازم
  3) themeStore: persist با کلید "theme-storage" + actions
  4) ThemeProvider: setProperty روی documentElement
  5) index.css: :root با fallback ها + body با var()
  6) main.jsx: wrap با ThemeProvider
  7) صفحات: استفاده از var(--color-) و بدون هگز هاردکد
  8) ChartPage: themeId در dep + readVar برای رنگ نمودار
  9) npm run build موفق (proof of compilation)
  10) Vite dev server روی :5173 (اختیاری — اگر بالا باشد)

خروج با کد 0 اگر همه سبز، 1 اگر حتی یک چک خراب.
================================================================
"""

import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
FRONTEND_SRC = FRONTEND_DIR / "src"

# جمع‌آوری نتایج: list of (description, ok, detail)
CHECKS = []


def check(desc, condition, detail=""):
    CHECKS.append((desc, bool(condition), detail))


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except (FileNotFoundError, UnicodeDecodeError):
        return ""


# ============================================================
# چک ۱: وجود ۸ فایل
# ============================================================
FILES = {
    "themes.js": FRONTEND_SRC / "themes" / "themes.js",
    "themeStore.js": FRONTEND_SRC / "stores" / "themeStore.js",
    "ThemeProvider.jsx": FRONTEND_SRC / "components" / "common" / "ThemeProvider.jsx",
    "index.css": FRONTEND_SRC / "index.css",
    "main.jsx": FRONTEND_SRC / "main.jsx",
    "LoginPage.jsx": FRONTEND_SRC / "pages" / "LoginPage.jsx",
    "HomePage.jsx": FRONTEND_SRC / "pages" / "HomePage.jsx",
    "ChartPage.jsx": FRONTEND_SRC / "pages" / "ChartPage.jsx",
}

for name, p in FILES.items():
    check(f"وجود {name}", p.exists(), str(p))


# ============================================================
# چک ۲: themes.js — ۵ تم با CSS variables
# ============================================================
themes_src = read_text(FILES["themes.js"])
EXPECTED_THEMES = ["binance-dark", "light-minimal", "dark-modern", "pastel", "sky-blue"]
for tid in EXPECTED_THEMES:
    check(f"themes.js شامل تم «{tid}»", f'"{tid}"' in themes_src)

REQUIRED_VARS = [
    "--color-primary",
    "--color-bg",
    "--color-card",
    "--color-border",
    "--color-text",
    "--color-text-muted",
    "--color-success",
    "--color-danger",
    "--color-danger-bg",
]
for v in REQUIRED_VARS:
    # هر متغیر باید حداقل ۵ بار (یک بار در هر تم) ظاهر شود
    count = themes_src.count(f'"{v}"')
    check(f"themes.js: «{v}» در همه ۵ تم", count >= 5, f"count={count}")

check(
    "themes.js: export DEFAULT_THEME_ID = binance-dark",
    'DEFAULT_THEME_ID = "binance-dark"' in themes_src,
)
check("themes.js: export listThemes()", "export function listThemes" in themes_src)


# ============================================================
# چک ۳: themeStore — Zustand + persist
# ============================================================
store_src = read_text(FILES["themeStore.js"])
check(
    "themeStore: import persist از zustand/middleware",
    'from "zustand/middleware"' in store_src and "persist" in store_src,
)
check(
    "themeStore: نام persist = «theme-storage»",
    '"theme-storage"' in store_src,
)
check("themeStore: action setTheme", "setTheme:" in store_src)
check("themeStore: action setFontSize", "setFontSize:" in store_src)
check("themeStore: state customColors", "customColors:" in store_src)
check(
    "themeStore: clamp font-size (Math.min/max)",
    "Math.max" in store_src and "Math.min" in store_src,
)


# ============================================================
# چک ۴: ThemeProvider — اعمال CSS vars روی :root
# ============================================================
tp_src = read_text(FILES["ThemeProvider.jsx"])
check("ThemeProvider: document.documentElement", "document.documentElement" in tp_src)
check("ThemeProvider: setProperty", "setProperty" in tp_src)
check("ThemeProvider: attribute data-theme", "data-theme" in tp_src)
check("ThemeProvider: useThemeStore subscribe", "useThemeStore" in tp_src)
check(
    "ThemeProvider: dep array شامل themeId/fontSize/customColors",
    "[themeId, fontSize, customColors]" in tp_src,
)


# ============================================================
# چک ۵: index.css — :root + body با var()
# ============================================================
css_src = read_text(FILES["index.css"])
check("index.css: بلوک :root", ":root {" in css_src)
check(
    "index.css: body با background var(--color-bg)",
    "background: var(--color-bg)" in css_src,
)
check(
    "index.css: body با color var(--color-text)",
    "color: var(--color-text)" in css_src,
)
check("index.css: متغیر --font-size-base", "--font-size-base" in css_src)
check(
    "index.css: scrollbar از CSS vars",
    "::-webkit-scrollbar" in css_src and "var(--color-border-strong)" in css_src,
)


# ============================================================
# چک ۶: main.jsx — wrap با ThemeProvider
# ============================================================
main_src = read_text(FILES["main.jsx"])
check(
    "main.jsx: import ThemeProvider",
    'from "./components/common/ThemeProvider.jsx"' in main_src,
)
check(
    "main.jsx: wrap با <ThemeProvider>",
    "<ThemeProvider>" in main_src and "</ThemeProvider>" in main_src,
)


# ============================================================
# چک ۷: صفحات از var(--color-) استفاده می‌کنند و بدون هگز هاردکد
# ============================================================
# الگوی هگز در inline style (به‌جز کامنت‌ها): background/color/border followed by a hex literal
HEX_IN_STYLE_PATTERN = re.compile(
    r'(?:background|backgroundColor|color|border|borderColor|boxShadow)\s*:\s*"[^"]*#[0-9a-fA-F]{3,8}'
)

for page_name in ["LoginPage.jsx", "HomePage.jsx", "ChartPage.jsx"]:
    src = read_text(FILES[page_name])

    # تعداد استفاده از var(--color-)
    var_uses = len(re.findall(r"var\(--color-", src))
    check(f"{page_name}: حداقل ۸ بار var(--color-)", var_uses >= 8, f"count={var_uses}")

    # بدون هگز هاردکد در inline style ها
    suspicious = HEX_IN_STYLE_PATTERN.findall(src)
    check(
        f"{page_name}: بدون هگز هاردکد در style",
        len(suspicious) == 0,
        f"found: {suspicious[:2]}",
    )


# ============================================================
# چک ۸: ChartPage — themeId در deps + readVar
# ============================================================
chart_src = read_text(FILES["ChartPage.jsx"])
check("ChartPage: import useThemeStore", "useThemeStore" in chart_src)
check(
    "ChartPage: themeId در useEffect dep array",
    re.search(r"\[symbolId,\s*timeframe,\s*themeId\]", chart_src) is not None,
)
check("ChartPage: تابع readVar", "function readVar" in chart_src)
check(
    "ChartPage: رنگ candle از readVar",
    'readVar("--color-success"' in chart_src and 'readVar("--color-danger"' in chart_src,
)
check(
    "ChartPage: layout chart از readVar",
    'readVar("--color-card"' in chart_src and 'readVar("--color-text"' in chart_src,
)


# ============================================================
# چک ۹: HomePage — theme switcher (Select با listThemes)
# ============================================================
home_src = read_text(FILES["HomePage.jsx"])
check("HomePage: import useThemeStore", "useThemeStore" in home_src)
check("HomePage: import listThemes", "listThemes" in home_src)
check("HomePage: <select> با value={themeId}", "value={themeId}" in home_src)
check("HomePage: setTheme در onChange", "setTheme" in home_src)


# ============================================================
# چک ۱۰: npm run build — proof of compilation
# ============================================================
print()
print("⏳ npm run build در حال اجرا (~۱۵-۳۰ ثانیه)...")

build_ok = False
build_detail = ""

# بررسی اولیه: node_modules وجود دارد؟
node_modules = FRONTEND_DIR / "node_modules"
node_bin = node_modules / ".bin"

if not node_modules.exists():
    build_detail = f"node_modules وجود ندارد — ابتدا 'npm install' در {FRONTEND_DIR}"
elif not node_bin.exists():
    build_detail = f"node_modules\\.bin پیدا نشد — احتمالاً npm install ناتمام"
else:
    # تنظیم explicit PATH تا shell child بتواند vite را پیدا کند
    env = os.environ.copy()
    env["PATH"] = str(node_bin) + os.pathsep + env.get("PATH", "")

    try:
        # روی ویندوز npm یک .cmd است — رشته + shell=True استانداردترین راه
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
            print("--- npm build stderr (تاب آخر) ---")
            print((result.stderr or "")[-2000:])
            print("--- npm build stdout (تاب آخر) ---")
            print((result.stdout or "")[-1500:])
    except subprocess.TimeoutExpired:
        build_detail = "timeout >120s"
    except Exception as e:
        build_detail = f"exception: {e}"

check("npm run build بدون خطا", build_ok, build_detail)


# ============================================================
# چک ۱۱: Vite dev server روی :5173 (اختیاری — informational)
# ============================================================
dev_server_up = False
try:
    req = urllib.request.Request("http://localhost:5173/")
    with urllib.request.urlopen(req, timeout=3) as resp:
        dev_server_up = resp.status == 200
except (urllib.error.URLError, OSError):
    dev_server_up = False


# ============================================================
# گزارش نهایی
# ============================================================
print()
print("=" * 64)
print("📋 نتایج تست خودکار:")
print("=" * 64)

passed = sum(1 for _, ok, _ in CHECKS if ok)
failed = sum(1 for _, ok, _ in CHECKS if not ok)

for desc, ok, detail in CHECKS:
    mark = "✅" if ok else "❌"
    extra = f"  ← {detail}" if detail and not ok else ""
    print(f"  {mark} {desc}{extra}")

print()
print(
    "ℹ️  Vite dev server روی :5173:",
    "✅ بالاست" if dev_server_up else "⚠️ پاسخ نمی‌دهد (اشکالی نیست — اختیاری)",
)

print()
print("=" * 64)
if failed == 0:
    print(f"✅ همه {passed} چک خودکار موفق — زیرگام ۸.۱ کامل است.")
    print("=" * 64)
    print()
    print("ℹ️  تنها چک واقعاً غیرقابل خودکارسازی:")
    print("    رنگ‌بندی بصری تم‌های مختلف در مرورگر")
    print("    (با ست شدن CSS vars + npm build سالم، نتیجه قطعی است)")
    print()
    print("گام بعدی: اسکریپت ۲۸ — Toast Notifications")
    sys.exit(0)
else:
    print(f"❌ {failed} چک ناموفق از {passed + failed} — اصلاح لازم است.")
    print("=" * 64)
    sys.exit(1)
