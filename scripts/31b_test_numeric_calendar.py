# -*- coding: utf-8 -*-
"""
اسکریپت ۳۱b — تست خودکار زیرگام ۸.۵
================================================================
طبق قانون #۲۲ سند v2.6.

پوشش تست:
  ۱) وجود فایل‌ها
  ۲) numberFormat.js
       - export formatNumber
       - export parseFormattedNumber
       - استفاده از Intl.NumberFormat
       - تابع formatNumber در runtime با Node.js — تست واقعی I/O
  ۳) dateFormat.js
       - export formatDate + CALENDARS + CALENDAR_LABELS
       - استفاده از Intl.DateTimeFormat
       - locale "fa-IR-u-ca-persian"
       - try/catch fallback
       - تست runtime با Node.js
  ۴) preferencesStore.js
       - Zustand + persist
       - state: calendar
       - متد setCalendar + reset
       - import از dateFormat.js (CALENDARS)
  ۵) CalendarToggle.jsx
       - props: value, onChange
       - role=radiogroup, radio, aria-checked
       - import formatDate + CALENDARS
       - preview تاریخ امروز (هم بدون ساعت هم با ساعت)
       - بدون hex hardcoded
  ۶) SettingsPage.jsx
       - import preferencesStore + CalendarToggle
       - بخش "زبان و تقویم"
       - calendar از store
       - setCalendar
       - handleReset: ریست هر دو store (resetTheme + resetPreferences)
  ۷) ChartPage.jsx
       - import preferencesStore + formatNumber + formatDate
       - calendar در useEffect deps
       - localization.dateFormat
       - localization.priceFormatter
       - متن "1714 کندل" حذف شده و formatNumber استفاده شده
       - regression checks

سپس smoke test:
  ۸) Runtime test با Node.js (formatNumber + formatDate)
  ۹) npm run build
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

NUMBER_FORMAT = SRC / "utils" / "numberFormat.js"
DATE_FORMAT = SRC / "utils" / "dateFormat.js"
PREFS_STORE = SRC / "stores" / "preferencesStore.js"
CALENDAR_TOGGLE = SRC / "components" / "settings" / "CalendarToggle.jsx"
SETTINGS_PAGE = SRC / "pages" / "SettingsPage.jsx"
CHART_PAGE = SRC / "pages" / "ChartPage.jsx"

HEX_PATTERN = re.compile(r'#[0-9a-fA-F]{3,8}\b')


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

    def print_section(self, title):
        print()
        print(f"--- {title} ---")

    def print_results(self):
        for name, ok, detail in self.results:
            mark = "✅" if ok else "❌"
            print(f"  {mark} {name}")
            if not ok and detail:
                print(f"      ↳ {detail}")


def check_no_hex(src):
    cleaned = re.sub(r'/\*.*?\*/', '', src, flags=re.DOTALL)
    cleaned = re.sub(r'//.*$', '', cleaned, flags=re.MULTILINE)
    matches = HEX_PATTERN.findall(cleaned)
    return (len(matches) == 0, ", ".join(sorted(set(matches))[:5]) if matches else "")


def runtime_test_node(c: Checks):
    """تست واقعی formatNumber و formatDate با Node.js"""
    node = shutil.which("node") or shutil.which("node.exe")
    if not node:
        c.add("Runtime test (Node.js)", False, "node در PATH یافت نشد — skipped")
        return

    test_script = """
        import { formatNumber, parseFormattedNumber } from "%(numfmt)s";
        import { formatDate, CALENDARS } from "%(datefmt)s";

        const results = [];

        function check(name, actual, expected) {
            const ok = actual === expected;
            results.push({ name, ok, actual, expected });
        }

        // formatNumber
        check("formatNumber(1714)", formatNumber(1714), "1,714");
        check("formatNumber(102345.67)", formatNumber(102345.67), "102,345.67");
        check("formatNumber(0)", formatNumber(0), "0");
        check("formatNumber(null)", formatNumber(null), "");
        check("formatNumber('abc')", formatNumber("abc"), "");
        check("formatNumber(1000, decimals=2)", formatNumber(1000, { decimals: 2 }), "1,000.00");

        // parseFormattedNumber
        check("parse('1,714')", parseFormattedNumber("1,714"), 1714);
        check("parse('102,345.67')", parseFormattedNumber("102,345.67"), 102345.67);
        check("parse('')", parseFormattedNumber(""), null);
        check("parse('abc')", parseFormattedNumber("abc"), null);

        // formatDate — gregorian
        const d = new Date("2024-01-15T12:00:00Z");
        const gOut = formatDate(d, "gregorian");
        check("formatDate gregorian contains 2024", gOut.includes("2024"), true);
        check("formatDate gregorian contains 01", gOut.includes("01"), true);

        // formatDate — jalali (سال شمسی متناظر با 2024-01-15 برابر ۱۴۰۲ است)
        const jOut = formatDate(d, "jalali");
        const jHas1402 = jOut.includes("1402") || jOut.includes("۱۴۰۲");
        check("formatDate jalali → سال ۱۴۰۲", jHas1402, true);

        // formatDate invalid
        check("formatDate(null)", formatDate(null, "gregorian"), "");
        check("formatDate('invalid')", formatDate("invalid", "gregorian"), "");

        // خروجی JSON برای parse در Python
        console.log("RESULTS:" + JSON.stringify(results));
    """ % {
        # as_uri() = portable file:///... URL (در ویندوز file:///D:/... — معتبر برای ESM)
        # as_posix() در ویندوز D:/... برمی‌گرداند که Node ESM آن را scheme نامعتبر می‌داند (Bug #46)
        "numfmt": NUMBER_FORMAT.as_uri(),
        "datefmt": DATE_FORMAT.as_uri(),
    }

    # write to temp file then run
    tmp = PROJECT_ROOT / "_runtime_test.mjs"
    tmp.write_text(test_script, encoding="utf-8")

    try:
        result = subprocess.run(
            [node, str(tmp)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        c.add("Runtime test (Node.js)", False, "timeout")
        return
    finally:
        try:
            tmp.unlink()
        except OSError:
            pass

    if result.returncode != 0:
        c.add("Runtime test (Node.js)", False, f"exit {result.returncode}: {result.stderr[:200]}")
        return

    # parse output
    import json
    line = None
    for ln in result.stdout.split("\n"):
        if ln.startswith("RESULTS:"):
            line = ln[len("RESULTS:"):]
            break
    if not line:
        c.add("Runtime test (Node.js)", False, "خروجی RESULTS یافت نشد")
        return

    try:
        cases = json.loads(line)
    except json.JSONDecodeError:
        c.add("Runtime test (Node.js)", False, "JSON parse failed")
        return

    for case in cases:
        detail = ""
        if not case["ok"]:
            detail = f"actual={case['actual']!r}, expected={case['expected']!r}"
        c.add(f"Runtime: {case['name']}", case["ok"], detail)


def main() -> int:
    print("=" * 64)
    print("اسکریپت ۳۱b — تست خودکار زیرگام ۸.۵")
    print("=" * 64)

    c = Checks()

    # ============================================================
    # ۱) وجود فایل‌ها
    # ============================================================
    c.print_section("۱) وجود فایل‌ها")
    files = {
        "numberFormat.js":       NUMBER_FORMAT,
        "dateFormat.js":         DATE_FORMAT,
        "preferencesStore.js":   PREFS_STORE,
        "CalendarToggle.jsx":    CALENDAR_TOGGLE,
        "SettingsPage.jsx":      SETTINGS_PAGE,
        "ChartPage.jsx":         CHART_PAGE,
    }
    for label, path in files.items():
        c.add(f"موجود است: {label}", path.exists())

    if any(not p.exists() for p in files.values()):
        c.print_results()
        print()
        print("=" * 64)
        print(f"❌ {c.failed} چک ناموفق")
        print("=" * 64)
        return 1

    # ============================================================
    # ۲) numberFormat.js
    # ============================================================
    c.print_section("۲) numberFormat.js")
    src = NUMBER_FORMAT.read_text(encoding="utf-8")

    c.add("export formatNumber",        "export function formatNumber" in src)
    c.add("export parseFormattedNumber", "export function parseFormattedNumber" in src)
    c.add("استفاده از Intl.NumberFormat", "Intl.NumberFormat" in src)
    c.add("پشتیبانی decimals option",    "decimals" in src)
    c.add("handle null/undefined",       "null" in src and "undefined" in src)
    c.add("Number.isFinite چک",          "Number.isFinite" in src)

    # ============================================================
    # ۳) dateFormat.js
    # ============================================================
    c.print_section("۳) dateFormat.js")
    src = DATE_FORMAT.read_text(encoding="utf-8")

    c.add("export formatDate",          "export function formatDate" in src)
    c.add("export CALENDARS",           "export const CALENDARS" in src)
    c.add("export CALENDAR_LABELS",     "export const CALENDAR_LABELS" in src)
    c.add("CALENDARS.GREGORIAN",        "GREGORIAN:" in src)
    c.add("CALENDARS.JALALI",           "JALALI:" in src)
    c.add('locale "fa-IR-u-ca-persian"', '"fa-IR-u-ca-persian"' in src)
    c.add("Intl.DateTimeFormat",        "Intl.DateTimeFormat" in src)
    c.add("try/catch fallback",         "try {" in src and "catch" in src)
    c.add("پشتیبانی withTime option",   "withTime" in src)

    # ============================================================
    # ۴) preferencesStore.js
    # ============================================================
    c.print_section("۴) preferencesStore.js")
    src = PREFS_STORE.read_text(encoding="utf-8")

    c.add("Zustand: create",             'from "zustand"' in src and "create(" in src)
    c.add("persist middleware",          "persist" in src and 'from "zustand/middleware"' in src)
    c.add("import CALENDARS از dateFormat", 'from "../utils/dateFormat.js"' in src and "CALENDARS" in src)
    c.add("state: calendar",             "calendar:" in src)
    c.add("DEFAULT_CALENDAR = GREGORIAN",
          "DEFAULT_CALENDAR" in src and "GREGORIAN" in src)
    c.add("setCalendar",                 "setCalendar:" in src)
    c.add("reset",                       "reset:" in src)
    c.add('name: "preferences-storage"', '"preferences-storage"' in src)

    # ============================================================
    # ۵) CalendarToggle.jsx
    # ============================================================
    c.print_section("۵) CalendarToggle.jsx")
    src = CALENDAR_TOGGLE.read_text(encoding="utf-8")

    c.add("props: value, onChange",
          "value" in src and "onChange" in src)
    c.add("import formatDate + CALENDARS",
          "formatDate" in src and "CALENDARS" in src and
          'from "../../utils/dateFormat.js"' in src)
    c.add("import CALENDAR_LABELS",
          "CALENDAR_LABELS" in src)
    c.add('role="radiogroup"',  'role="radiogroup"' in src)
    c.add('role="radio"',       'role="radio"' in src)
    c.add("aria-checked={isActive}",
          "aria-checked={isActive}" in src)
    c.add("aria-label فارسی",
          'aria-label="نوع تقویم"' in src)
    c.add("preview تاریخ امروز (بدون ساعت)",
          "formatDate(new Date(), value)" in src)
    c.add("preview همراه ساعت",
          "withTime: true" in src)
    c.add("بدنه preview: var(--color-bg-elevated)",
          'background: "var(--color-bg-elevated)"' in src)

    ok, bad = check_no_hex(src)
    c.add("بدون hex hardcoded", ok, f"hex: {bad}" if bad else "")

    # ============================================================
    # ۶) SettingsPage.jsx
    # ============================================================
    c.print_section("۶) SettingsPage.jsx")
    src = SETTINGS_PAGE.read_text(encoding="utf-8")

    c.add("import usePreferencesStore",
          'from "../stores/preferencesStore.js"' in src)
    c.add("import CalendarToggle",
          'from "../components/settings/CalendarToggle.jsx"' in src)
    c.add("calendar از store",          "s.calendar" in src)
    c.add("setCalendar از store",       "s.setCalendar" in src)
    c.add("resetPreferences از store",  "s.reset" in src or "resetPreferences" in src)
    c.add("بخش 'زبان و تقویم'",
          "زبان و تقویم" in src)
    c.add("<CalendarToggle value={calendar}",
          "<CalendarToggle" in src and "value={calendar}" in src)
    c.add("handleReset: resetTheme()",  "resetTheme()" in src)
    c.add("handleReset: resetPreferences()", "resetPreferences()" in src)
    c.add("variant: 'warning' حفظ شد",  '"warning"' in src)
    # regression
    c.add("ThemeCard حفظ شد (regression)",
          "<ThemeCard" in src)
    c.add("FontSizeControl حفظ شد (regression)",
          "<FontSizeControl" in src)

    ok, bad = check_no_hex(src)
    c.add("بدون hex hardcoded", ok, f"hex: {bad}" if bad else "")

    # ============================================================
    # ۷) ChartPage.jsx
    # ============================================================
    c.print_section("۷) ChartPage.jsx")
    src = CHART_PAGE.read_text(encoding="utf-8")

    c.add("import usePreferencesStore",
          'from "../stores/preferencesStore.js"' in src)
    c.add("import formatNumber",
          'from "../utils/numberFormat.js"' in src)
    c.add("import formatDate",
          'from "../utils/dateFormat.js"' in src)
    c.add("calendar = usePreferencesStore",
          "s.calendar" in src)
    c.add("calendar در useEffect deps",
          "calendar]" in src)
    c.add("localization.dateFormat",
          "dateFormat:" in src and "formatDate(d, calendar)" in src)
    c.add("localization.priceFormatter",
          "priceFormatter:" in src and "formatNumber" in src)
    c.add("استفاده از formatNumber در متادیتا",
          "formatNumber(meta.count)" in src and "formatNumber(meta.total)" in src)
    # regression از زیرگام ۸.۳
    c.add("SkeletonBlock حفظ شد (regression ۸.۳)",
          "import SkeletonBlock" in src and "<SkeletonBlock" in src)
    c.add("themeId در deps حفظ شد",     "themeId" in src)
    c.add("useThemeStore حفظ شد (regression)",
          "useThemeStore" in src)
    # check that the 1714 hardcoded string is gone
    c.add("متن 1714 hardcoded حذف شد",
          "1714 کندل" not in src)

    # ============================================================
    # نتایج تست‌های استاتیک
    # ============================================================
    static_passed = c.passed
    static_failed = c.failed

    if static_failed > 0:
        c.print_results()
        print()
        print("=" * 64)
        print(f"❌ {static_failed} چک استاتیک ناموفق")
        print("=" * 64)
        return 1

    # ============================================================
    # ۸) Runtime test با Node.js
    # ============================================================
    c.print_section("۸) Runtime test (Node.js)")
    runtime_test_node(c)

    # ============================================================
    # چاپ نتایج
    # ============================================================
    c.print_results()

    if c.failed > 0:
        print()
        print("=" * 64)
        print(f"❌ {c.failed} چک ناموفق از {c.passed + c.failed}")
        print("=" * 64)
        return 1

    print()
    print(f"✅ تمام {c.passed} چک سبز.")

    # ============================================================
    # ۹) npm run build
    # ============================================================
    print()
    print("=" * 64)
    print("۹) npm run build (smoke test)")
    print("=" * 64)

    if not (FRONTEND / "node_modules").exists():
        print("⚠️  node_modules موجود نیست — build skipped.")
        return 0

    npm = shutil.which("npm") or shutil.which("npm.cmd")
    if not npm:
        print("⚠️  npm یافت نشد — build skipped.")
        return 0

    print(f"اجرای: {npm} run build  (در {FRONTEND})")
    print("(ممکن است ۳۰-۹۰ ثانیه طول بکشد...)")
    print()

    try:
        result = subprocess.run(
            [npm, "run", "build"],
            cwd=str(FRONTEND),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=180,
        )
    except subprocess.TimeoutExpired:
        print("❌ npm build timeout (>180s).")
        return 1

    stdout = result.stdout or ""
    stderr = result.stderr or ""
    for line in stdout.strip().split("\n")[-15:]:
        print(f"  {line}")

    if result.returncode == 0:
        print()
        print("=" * 64)
        print(f"✅ تمام تست‌ها سبز: {c.passed} چک + npm build")
        print("=" * 64)
        print()
        print("🎉 فاز ۰ ۱۰۰٪ تکمیل شد!")
        print()
        print("چک بصری در 🟧 tab «3 frontend»:")
        print("  ۱) /chart/1 → متادیتا 'X,XXX از X,XXX کندل' (با کاما)")
        print("  ۲) hover روی شمعی نمودار → tooltip تاریخ به فرمت میلادی")
        print("  ۳) /settings → بخش 'زبان و تقویم' با preview تاریخ امروز")
        print("  ۴) کلیک 'شمسی' → preview آنی به ۱۴۰۲/۰۲/۲۷ تغییر")
        print("  ۵) برگشت /chart/1 → tooltip تاریخ به شمسی")
        print("  ۶) refresh مرورگر → calendar persist می‌ماند")
        print("  ۷) کلیک '🔄 بازگشت به پیش‌فرض' → همه ریست + Toast سبز")
        return 0
    else:
        print()
        print("--- stderr ---")
        for line in stderr.strip().split("\n")[-15:]:
            print(f"  {line}")
        print()
        print(f"❌ npm build شکست خورد (exit code: {result.returncode})")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
