# -*- coding: utf-8 -*-
"""
اسکریپت ۳۲b — تست خودکار اصلاحیه ۳۲
================================================================
طبق قانون #۲۲ سند v2.6.

پوشش تست:
  ۱) وجود فایل‌ها (regression check)
  ۲) index.css — html { font-size: var(--font-size-base) }
  ۳) Font px → rem در همه فایل‌های .jsx:
       - هیچ inline `fontSize: <number>` نباشد
       - استثنا: fontSize با template literal (مثل `${value}px`)
  ۴) dateFormat.js — افزودن GREGORIAN_FORMATS + isoMode + format logic
  ۵) preferencesStore.js — gregorianFormat + version 2 + migrate
  ۶) CalendarToggle.jsx — props format + onFormatChange + select
  ۷) SettingsPage.jsx — passing format به CalendarToggle
  ۸) HomePage.jsx — import formatNumber + استفاده
  ۹) ChartPage.jsx — timeFormatter (نه dateFormat function)
  ۱۰) Runtime test با Node.js:
       - formatDate با ۴ فرمت میلادی
       - gregorianFormat preset ها
  ۱۱) npm run build
================================================================
"""

from pathlib import Path
import re
import subprocess
import shutil
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
FRONTEND = PROJECT_ROOT / "frontend"
SRC = FRONTEND / "src"

INDEX_CSS = SRC / "index.css"
DATE_FORMAT = SRC / "utils" / "dateFormat.js"
PREFS_STORE = SRC / "stores" / "preferencesStore.js"
CALENDAR_TOGGLE = SRC / "components" / "settings" / "CalendarToggle.jsx"
SETTINGS_PAGE = SRC / "pages" / "SettingsPage.jsx"
HOME_JSX = SRC / "pages" / "HomePage.jsx"
CHART_JSX = SRC / "pages" / "ChartPage.jsx"

# فایل‌هایی که نباید fontSize عددی داشته باشند
JSX_FILES = [
    SRC / "pages" / "LoginPage.jsx",
    SRC / "pages" / "HomePage.jsx",
    SRC / "pages" / "ChartPage.jsx",
    SRC / "pages" / "SettingsPage.jsx",
    SRC / "components" / "common" / "Toast.jsx",
    SRC / "components" / "common" / "ConfirmDialog.jsx",
    SRC / "components" / "settings" / "ThemeCard.jsx",
    SRC / "components" / "settings" / "FontSizeControl.jsx",
    SRC / "components" / "settings" / "CalendarToggle.jsx",
]

# regex برای پیدا کردن fontSize: <integer> (بد) — هم با اعداد ۱ تا ۳ رقمی
# توجه: template literals با backtick شروع می‌شوند، آن‌ها مشکلی نیستند.
# `fontSize: 13,` بد است
# `fontSize: "0.93rem",` خوب است
# `fontSize: `${value}px`,` خوب است
BAD_FONT_SIZE = re.compile(r'fontSize:\s*\d+(?=\s*[,\}\)\s])')


class Checks:
    def __init__(self):
        self.results = []

    def add(self, name, ok, detail=""):
        self.results.append((name, ok, detail))

    @property
    def passed(self):
        return sum(1 for _, ok, _ in self.results if ok)

    @property
    def failed(self):
        return sum(1 for _, ok, _ in self.results if not ok)

    def print_section(self, t):
        print()
        print(f"--- {t} ---")

    def print_results(self):
        for name, ok, detail in self.results:
            mark = "✅" if ok else "❌"
            print(f"  {mark} {name}")
            if not ok and detail:
                print(f"      ↳ {detail}")


def runtime_test(c):
    node = shutil.which("node") or shutil.which("node.exe")
    if not node:
        c.add("Runtime (Node.js)", False, "node یافت نشد")
        return

    script = """
        import { formatDate, GREGORIAN_FORMATS, GREGORIAN_FORMAT_LABELS, DEFAULT_GREGORIAN_FORMAT } from "%(df)s";

        const results = [];
        const c = (n, a, e) => results.push({name:n, ok:a===e, actual:a, expected:e});

        // تست ۴ فرمت میلادی
        const d = new Date("2024-01-15T12:00:00Z");

        const iso = formatDate(d, "gregorian", { format: "iso" });
        c("iso format = 2024-01-15", iso, "2024-01-15");

        const us = formatDate(d, "gregorian", { format: "us-short" });
        c("us-short شامل 01/15/2024", us.includes("01") && us.includes("15") && us.includes("2024"), true);

        const eu = formatDate(d, "gregorian", { format: "eu-short" });
        c("eu-short شامل 15/01/2024", eu.includes("15") && eu.includes("01") && eu.includes("2024"), true);

        const lng = formatDate(d, "gregorian", { format: "long" });
        c("long شامل January", lng.includes("January"), true);
        c("long شامل 2024", lng.includes("2024"), true);

        // ISO با ساعت
        const isoT = formatDate(d, "gregorian", { format: "iso", withTime: true });
        c("iso withTime شامل 2024-01-15", isoT.includes("2024-01-15"), true);

        // Jalali باید سال ۱۴۰۲ داشته باشد
        const jal = formatDate(d, "jalali", { format: "iso" });
        c("jalali ignore format param", jal.includes("1402") || jal.includes("۱۴۰۲"), true);

        // GREGORIAN_FORMATS array
        c("GREGORIAN_FORMATS موجود", Array.isArray(GREGORIAN_FORMATS), true);
        c("GREGORIAN_FORMATS طول ۴", GREGORIAN_FORMATS.length, 4);
        c("شامل 'iso'", GREGORIAN_FORMATS.includes("iso"), true);
        c("شامل 'us-short'", GREGORIAN_FORMATS.includes("us-short"), true);
        c("شامل 'eu-short'", GREGORIAN_FORMATS.includes("eu-short"), true);
        c("شامل 'long'", GREGORIAN_FORMATS.includes("long"), true);

        c("DEFAULT_GREGORIAN_FORMAT = us-short", DEFAULT_GREGORIAN_FORMAT, "us-short");

        console.log("RESULTS:" + JSON.stringify(results));
    """ % { "df": DATE_FORMAT.as_uri() }

    tmp = PROJECT_ROOT / "_runtime_test_32.mjs"
    tmp.write_text(script, encoding="utf-8")

    try:
        result = subprocess.run(
            [node, str(tmp)],
            capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=30,
        )
    except subprocess.TimeoutExpired:
        c.add("Runtime (Node.js)", False, "timeout")
        return
    finally:
        try:
            tmp.unlink()
        except OSError:
            pass

    if result.returncode != 0:
        c.add("Runtime (Node.js)", False, f"exit {result.returncode}: {result.stderr[:200]}")
        return

    import json
    line = None
    for ln in result.stdout.split("\n"):
        if ln.startswith("RESULTS:"):
            line = ln[len("RESULTS:"):]
            break
    if not line:
        c.add("Runtime (Node.js)", False, "RESULTS یافت نشد")
        return

    cases = json.loads(line)
    for case in cases:
        detail = "" if case["ok"] else f"actual={case['actual']!r}, expected={case['expected']!r}"
        c.add(f"Runtime: {case['name']}", case["ok"], detail)


def main() -> int:
    print("=" * 64)
    print("اسکریپت ۳۲b — تست اصلاحیه ۳۲")
    print("=" * 64)

    c = Checks()

    # ============================================================
    # ۲) index.css — html font-size
    # ============================================================
    c.print_section("۲) index.css — html font-size scaling")
    src = INDEX_CSS.read_text(encoding="utf-8")
    c.add("html { font-size: var(--font-size-base) }",
          "html {" in src and "font-size: var(--font-size-base)" in src)
    c.add("body همچنان موجود",
          "body {" in src)
    c.add("regression: @keyframes toast-slide-in حفظ",
          "@keyframes toast-slide-in" in src)
    c.add("regression: @keyframes skeleton-shimmer حفظ",
          "@keyframes skeleton-shimmer" in src)
    c.add("regression: @keyframes dialog-fade-in حفظ",
          "@keyframes dialog-fade-in" in src)
    c.add("regression: button:focus-visible حفظ",
          "button:focus-visible" in src)

    # ============================================================
    # ۳) فایل‌های .jsx — بدون inline fontSize: <N>
    # ============================================================
    c.print_section("۳) Bug #47 — Font Size Scaling (px → rem)")
    for path in JSX_FILES:
        if not path.exists():
            c.add(f"موجود است: {path.name}", False)
            continue
        s = path.read_text(encoding="utf-8")
        matches = BAD_FONT_SIZE.findall(s)
        ok = len(matches) == 0
        detail = f"باقیمانده‌ها: {matches[:3]}" if matches else ""
        c.add(f"{path.name}: همه fontSize → rem", ok, detail)

    # ============================================================
    # ۴) dateFormat.js
    # ============================================================
    c.print_section("۴) dateFormat.js — فرمت‌های میلادی")
    s = DATE_FORMAT.read_text(encoding="utf-8")
    c.add("export GREGORIAN_FORMATS",
          "export const GREGORIAN_FORMATS" in s)
    c.add("export GREGORIAN_FORMAT_LABELS",
          "export const GREGORIAN_FORMAT_LABELS" in s)
    c.add("export DEFAULT_GREGORIAN_FORMAT",
          "export const DEFAULT_GREGORIAN_FORMAT" in s)
    c.add("export isValidGregorianFormat",
          "export function isValidGregorianFormat" in s)
    c.add("پشتیبانی format='iso'",
          '"iso"' in s)
    c.add("پشتیبانی format='us-short'",
          '"us-short"' in s)
    c.add("پشتیبانی format='eu-short'",
          '"eu-short"' in s)
    c.add("پشتیبانی format='long'",
          '"long"' in s and "dateStyle" in s)
    c.add("ISO با dateStyle:long استفاده نمی‌کند (custom)",
          "yyyy-${mm}" in s or "padStart(2" in s)
    c.add("eu-short → en-GB",
          '"en-GB"' in s)

    # ============================================================
    # ۵) preferencesStore.js
    # ============================================================
    c.print_section("۵) preferencesStore.js — gregorianFormat")
    s = PREFS_STORE.read_text(encoding="utf-8")
    c.add("state: gregorianFormat",
          "gregorianFormat:" in s)
    c.add("setGregorianFormat",
          "setGregorianFormat:" in s)
    c.add("isValidGregorianFormat در setter",
          "isValidGregorianFormat" in s)
    c.add("reset شامل gregorianFormat",
          "gregorianFormat: DEFAULT_GREGORIAN_FORMAT" in s)
    c.add("version: 2 (bump به‌خاطر افزودن field)",
          "version: 2" in s)
    c.add("migrate function برای v1 → v2",
          "migrate:" in s and "fromVersion" in s)
    c.add("regression: calendar حفظ شد",
          "calendar:" in s and "setCalendar:" in s)

    # ============================================================
    # ۶) CalendarToggle.jsx
    # ============================================================
    c.print_section("۶) CalendarToggle.jsx — select فرمت")
    s = CALENDAR_TOGGLE.read_text(encoding="utf-8")
    c.add("props: format, onFormatChange",
          "format" in s and "onFormatChange" in s)
    c.add("import GREGORIAN_FORMATS",
          "GREGORIAN_FORMATS" in s)
    c.add("import GREGORIAN_FORMAT_LABELS",
          "GREGORIAN_FORMAT_LABELS" in s)
    c.add("شرط isGregorian برای نمایش select",
          "isGregorian" in s and "&&" in s)
    c.add("<select> برای فرمت",
          "<select" in s and "onFormatChange" in s)
    c.add("label فرمت تاریخ میلادی",
          "فرمت تاریخ میلادی" in s)
    c.add("preview با format passed",
          "{ format }" in s or "{ format," in s)
    # regression
    c.add("regression: 2 دکمه radio (gregorian/jalali) حفظ",
          'role="radio"' in s and "isActive" in s)

    # ============================================================
    # ۷) SettingsPage.jsx
    # ============================================================
    c.print_section("۷) SettingsPage.jsx")
    s = SETTINGS_PAGE.read_text(encoding="utf-8")
    c.add("gregorianFormat از store",
          "gregorianFormat" in s and "usePreferencesStore" in s)
    c.add("setGregorianFormat از store",
          "setGregorianFormat" in s)
    c.add("passing format={gregorianFormat}",
          "format={gregorianFormat}" in s)
    c.add("passing onFormatChange={setGregorianFormat}",
          "onFormatChange={setGregorianFormat}" in s)
    # regression
    c.add("regression: <CalendarToggle حفظ",
          "<CalendarToggle" in s)
    c.add("regression: <ThemeCard حفظ",
          "<ThemeCard" in s)
    c.add("regression: <FontSizeControl حفظ",
          "<FontSizeControl" in s)
    c.add("regression: handleReset → resetTheme + resetPreferences",
          "resetTheme()" in s and "resetPreferences()" in s)

    # ============================================================
    # ۸) HomePage.jsx
    # ============================================================
    c.print_section("۸) HomePage.jsx — Bug #49 (formatNumber)")
    s = HOME_JSX.read_text(encoding="utf-8")
    c.add("import formatNumber",
          'from "../utils/numberFormat.js"' in s and "formatNumber" in s)
    c.add("استفاده formatNumber(1714)",
          "formatNumber(1714)" in s)
    c.add("متن 1714 hardcoded حذف شد",
          ">1714 کندل<" not in s and " 1714 کندل" not in s)
    # regression
    c.add("regression: Link /settings حفظ",
          'to="/settings"' in s)
    c.add("regression: askConfirm حفظ",
          "await askConfirm" in s)

    # ============================================================
    # ۹) ChartPage.jsx — Bug #48 (timeFormatter)
    # ============================================================
    c.print_section("۹) ChartPage.jsx — Bug #48 (timeFormatter)")
    s = CHART_JSX.read_text(encoding="utf-8")
    c.add("timeFormatter ست شده",
          "timeFormatter:" in s)
    c.add("dateFormat function حذف شد (به‌جای آن timeFormatter)",
          "dateFormat:" not in s or "dateFormat: '" in s,
          "هنوز localization.dateFormat (function) داریم")
    c.add("priceFormatter حفظ",
          "priceFormatter:" in s)
    c.add("locale: 'en-US' در localization",
          'locale: "en-US"' in s)
    c.add("formatDate در timeFormatter",
          "formatDate(d, calendar" in s)
    c.add("استفاده gregorianFormat در formatDate",
          "gregorianFormat" in s and "format: gregorianFormat" in s)
    c.add("gregorianFormat در useEffect deps",
          "gregorianFormat]" in s)
    # regression
    c.add("regression: SkeletonBlock حفظ",
          "<SkeletonBlock" in s)
    c.add("regression: formatNumber در متادیتا حفظ",
          "formatNumber(meta.count)" in s)

    # ============================================================
    # نتایج استاتیک
    # ============================================================
    if c.failed > 0:
        c.print_results()
        print()
        print("=" * 64)
        print(f"❌ {c.failed} چک ناموفق از {c.passed + c.failed}")
        print("=" * 64)
        return 1

    static_count = c.passed

    # ============================================================
    # ۱۰) Runtime
    # ============================================================
    c.print_section("۱۰) Runtime test (Node.js)")
    runtime_test(c)

    c.print_results()

    if c.failed > 0:
        print()
        print("=" * 64)
        print(f"❌ {c.failed} چک ناموفق")
        print("=" * 64)
        return 1

    print()
    print(f"✅ تمام {c.passed} چک سبز.")

    # ============================================================
    # ۱۱) npm build
    # ============================================================
    print()
    print("=" * 64)
    print("۱۱) npm run build (smoke test)")
    print("=" * 64)

    if not (FRONTEND / "node_modules").exists():
        print("⚠️  node_modules موجود نیست — build skipped.")
        return 0

    npm = shutil.which("npm") or shutil.which("npm.cmd")
    if not npm:
        print("⚠️  npm یافت نشد.")
        return 0

    try:
        result = subprocess.run(
            [npm, "run", "build"],
            cwd=str(FRONTEND),
            capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=180,
        )
    except subprocess.TimeoutExpired:
        print("❌ build timeout")
        return 1

    for line in (result.stdout or "").strip().split("\n")[-15:]:
        print(f"  {line}")

    if result.returncode == 0:
        print()
        print("=" * 64)
        print(f"✅ تمام تست‌ها سبز: {c.passed} چک + npm build")
        print("=" * 64)
        print()
        print("چک بصری در 🟧 tab «3 frontend»:")
        print("  ۱) refresh مرورگر")
        print("  ۲) /settings → اندازه فونت 'بزرگ‌تر' → همه‌جا بزرگ شود ✓")
        print("  ۳) /chart/1 → hover روی شمعی → تاریخ tooltip نمایش داده شود ✓")
        print("  ۴) برگشت / → '1,714 کندل' با کاما ✓")
        print("  ۵) /settings → بخش تقویم → select فرمت میلادی:")
        print("       - ISO: 2026-05-17")
        print("       - آمریکایی: 05/17/2026")
        print("       - اروپایی: 17/05/2026")
        print("       - کامل: May 17, 2026")
        print("  ۶) /chart/1 → tooltip تاریخ با فرمت انتخاب‌شده")
        print("  ۷) ریست → همه به پیش‌فرض (تقویم میلادی + فرمت us-short)")
        return 0
    else:
        for line in (result.stderr or "").strip().split("\n")[-15:]:
            print(f"  {line}")
        print(f"❌ build شکست (exit {result.returncode})")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
