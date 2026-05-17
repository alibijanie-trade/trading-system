# -*- coding: utf-8 -*-
"""
اسکریپت ۳۰b — تست خودکار زیرگام ۸.۴ (Settings Page)
================================================================
طبق قانون #۲۲ سند v2.6 (هر اسکریپت {N}_*.py باید {N}b_test_*.py همراه داشته باشد).

پوشش تست:
  ۱) وجود فایل‌ها
  ۲) ThemeCard.jsx
       - props: theme, isActive, onClick
       - aria-pressed
       - preview از theme.vars (نه CSS vars)
       - بدنه از تم فعلی (var(--color-card))
       - badge "فعال" روی isActive
       - بدون hex hardcoded
  ۳) FontSizeControl.jsx
       - props: value, onChange
       - ۴ preset (12, 14, 16, 18)
       - role="radiogroup" + role="radio" + aria-checked
       - preview با fontSize: ${value}px
       - بدون hex hardcoded
  ۴) SettingsPage.jsx
       - استفاده از themeStore (themeId, setTheme, fontSize, setFontSize, resetAll)
       - استفاده از confirmStore (await askConfirm)
       - استفاده از toastStore (success)
       - import ThemeCard + FontSizeControl
       - listThemes از themes.js
       - SectionHeader inline
       - دکمه ریست با variant: "warning"
       - بدون hex hardcoded
  ۵) App.jsx
       - import SettingsPage
       - route /settings داخل ProtectedRoute
       - حفظ route های قبلی (regression)
  ۶) HomePage.jsx
       - حذف dropdown موقت تم (regression)
       - Link به /settings با ⚙️
       - حفظ handleLogout (regression)

سپس smoke test:
  ۷) npm run build (اگر node_modules موجود)
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

THEME_CARD = SRC / "components" / "settings" / "ThemeCard.jsx"
FONT_SIZE_CTRL = SRC / "components" / "settings" / "FontSizeControl.jsx"
SETTINGS_PAGE = SRC / "pages" / "SettingsPage.jsx"
APP_JSX = SRC / "App.jsx"
HOME_JSX = SRC / "pages" / "HomePage.jsx"

HEX_PATTERN = re.compile(r'#[0-9a-fA-F]{3,8}\b')


class Checks:
    def __init__(self):
        self.results = []

    def add(self, name: str, ok: bool, detail: str = ""):
        self.results.append((name, ok, detail))

    @property
    def passed(self):
        return sum(1 for _, ok, _ in self.results if ok)

    @property
    def failed(self):
        return sum(1 for _, ok, _ in self.results if not ok)

    def print_section(self, title: str):
        print()
        print(f"--- {title} ---")

    def print_results(self):
        for name, ok, detail in self.results:
            mark = "✅" if ok else "❌"
            print(f"  {mark} {name}")
            if not ok and detail:
                print(f"      ↳ {detail}")


def check_no_hex(src: str) -> tuple:
    """چک hex hardcoded — همه کامنت‌ها حذف می‌شوند."""
    cleaned = re.sub(r'/\*.*?\*/', '', src, flags=re.DOTALL)
    cleaned = re.sub(r'//.*$', '', cleaned, flags=re.MULTILINE)
    matches = HEX_PATTERN.findall(cleaned)
    return (len(matches) == 0, ", ".join(sorted(set(matches))[:5]) if matches else "")


def main() -> int:
    print("=" * 64)
    print("اسکریپت ۳۰b — تست خودکار زیرگام ۸.۴")
    print("=" * 64)

    c = Checks()

    # ============================================================
    # ۱) وجود فایل‌ها
    # ============================================================
    c.print_section("۱) وجود فایل‌ها")
    files = {
        "ThemeCard.jsx":       THEME_CARD,
        "FontSizeControl.jsx": FONT_SIZE_CTRL,
        "SettingsPage.jsx":    SETTINGS_PAGE,
        "App.jsx":             APP_JSX,
        "HomePage.jsx":        HOME_JSX,
    }
    for label, path in files.items():
        c.add(f"موجود است: {label}", path.exists())

    if any(not p.exists() for p in files.values()):
        c.print_results()
        print()
        print("=" * 64)
        print(f"❌ {c.failed} چک ناموفق از {c.passed + c.failed}")
        print("   ابتدا اسکریپت ۳۰ را اجرا کنید.")
        print("=" * 64)
        return 1

    # ============================================================
    # ۲) ThemeCard.jsx
    # ============================================================
    c.print_section("۲) ThemeCard.jsx")
    src = THEME_CARD.read_text(encoding="utf-8")

    c.add("props: theme, isActive, onClick",
          "theme" in src and "isActive" in src and "onClick" in src)
    c.add("aria-pressed={isActive}", "aria-pressed={isActive}" in src)
    c.add("type=\"button\" (نه type submit)",
          'type="button"' in src)
    c.add("preview از theme.vars",
          'v["--color-bg"]' in src or 'theme.vars' in src)
    c.add("preview شامل --color-primary",
          'v["--color-primary"]' in src or '"--color-primary"' in src)
    c.add("preview شامل --color-success",
          'v["--color-success"]' in src or '"--color-success"' in src)
    c.add("preview شامل --color-danger",
          'v["--color-danger"]' in src or '"--color-danger"' in src)
    c.add("بدنه کارت از تم فعلی: var(--color-card)",
          'background: "var(--color-card)"' in src)
    c.add("border فعال: var(--color-primary)",
          'var(--color-primary)' in src)
    c.add("متن از var(--color-text)",
          '"var(--color-text)"' in src)
    c.add('badge "فعال" روی isActive',
          "isActive &&" in src and "فعال" in src)
    c.add("textAlign: start (RTL-safe)",
          'textAlign: "start"' in src)

    ok, bad = check_no_hex(src)
    c.add("بدون hex hardcoded",
          ok, f"hex: {bad}" if bad else "")

    # ============================================================
    # ۳) FontSizeControl.jsx
    # ============================================================
    c.print_section("۳) FontSizeControl.jsx")
    src = FONT_SIZE_CTRL.read_text(encoding="utf-8")

    c.add("props: value, onChange",
          "value" in src and "onChange" in src)
    c.add("preset 12px", "value: 12" in src)
    c.add("preset 14px", "value: 14" in src)
    c.add("preset 16px", "value: 16" in src)
    c.add("preset 18px", "value: 18" in src)
    c.add('role="radiogroup"', 'role="radiogroup"' in src)
    c.add('role="radio"',      'role="radio"' in src)
    c.add("aria-checked={isActive}",
          "aria-checked={isActive}" in src)
    c.add("aria-label فارسی",
          'aria-label="اندازه فونت"' in src)
    c.add("preview با fontSize: `${value}px`",
          "`${value}px`" in src)
    c.add("preview background: var(--color-bg-elevated)",
          'background: "var(--color-bg-elevated)"' in src)
    c.add("preview color: var(--color-text)",
          'color: "var(--color-text)"' in src)

    ok, bad = check_no_hex(src)
    c.add("بدون hex hardcoded",
          ok, f"hex: {bad}" if bad else "")

    # ============================================================
    # ۴) SettingsPage.jsx
    # ============================================================
    c.print_section("۴) SettingsPage.jsx")
    src = SETTINGS_PAGE.read_text(encoding="utf-8")

    c.add("import useThemeStore",
          'from "../stores/themeStore.js"' in src)
    c.add("import useConfirmStore",
          'from "../stores/confirmStore.js"' in src)
    c.add("import useToastStore",
          'from "../stores/toastStore.js"' in src)
    c.add("import ThemeCard",
          'from "../components/settings/ThemeCard.jsx"' in src)
    c.add("import FontSizeControl",
          'from "../components/settings/FontSizeControl.jsx"' in src)
    c.add("import listThemes",
          "listThemes" in src and 'from "../themes/themes.js"' in src)
    c.add("themeId از store",        "s.themeId" in src)
    c.add("setTheme از store",       "s.setTheme" in src)
    c.add("fontSize از store",       "s.fontSize" in src)
    c.add("setFontSize از store",    "s.setFontSize" in src)
    c.add("resetAll از store",       "s.resetAll" in src)
    c.add("askConfirm = s.confirm",  "s.confirm" in src)
    c.add("toastSuccess = s.success", "s.success" in src)
    c.add("await askConfirm({...})", "await askConfirm" in src)
    c.add('variant: "warning"',      '"warning"' in src)
    c.add("if (!ok) return",         "if (!ok) return" in src)
    c.add("resetAll() پس از تأیید",  "resetAll()" in src)
    c.add("toastSuccess پس از ریست", "toastSuccess(" in src)
    c.add("listThemes().map → ThemeCard",
          "themes.map" in src and "<ThemeCard" in src)
    c.add("<FontSizeControl value={fontSize}",
          "<FontSizeControl" in src and "value={fontSize}" in src)
    c.add("SectionHeader کامپوننت inline",
          "function SectionHeader" in src)
    c.add("لینک بازگشت به /",        '<Link to="/">' in src)

    ok, bad = check_no_hex(src)
    c.add("بدون hex hardcoded",
          ok, f"hex: {bad}" if bad else "")

    # ============================================================
    # ۵) App.jsx
    # ============================================================
    c.print_section("۵) App.jsx")
    src = APP_JSX.read_text(encoding="utf-8")

    c.add("import SettingsPage",
          'import SettingsPage from "./pages/SettingsPage.jsx"' in src)
    c.add('route /settings',
          'path="/settings"' in src)
    c.add("SettingsPage داخل ProtectedRoute",
          # Settings باید بعد از ProtectedRoute Wrapper بیاید
          "ProtectedRoute" in src and 'path="/settings"' in src)
    # regression
    c.add("ConfirmDialog حفظ شد (regression)",
          "<ConfirmDialog />" in src)
    c.add("ToastContainer حفظ شد (regression)",
          "<ToastContainer />" in src)
    c.add("route /chart حفظ شد (regression)",
          'path="/chart/:symbolId"' in src)
    c.add("route /login حفظ شد (regression)",
          'path="/login"' in src)

    # بررسی ساختاری: /settings داخل بلوک ProtectedRoute باشد
    # روش ساده: همه route ها inside Route element={<ProtectedRoute />} باشند
    protected_match = re.search(
        r"<Route\s+element=\{<ProtectedRoute\s*/>\}>(.*?)</Route>",
        src, re.DOTALL
    )
    inside_protected = (
        protected_match is not None and 'path="/settings"' in protected_match.group(1)
    )
    c.add("/settings داخل ProtectedRoute wrapper",
          inside_protected,
          "ساختار route باید داخل بلوک ProtectedRoute باشد")

    # ============================================================
    # ۶) HomePage.jsx
    # ============================================================
    c.print_section("۶) HomePage.jsx")
    src = HOME_JSX.read_text(encoding="utf-8")

    c.add("Link به /settings",
          'to="/settings"' in src)
    c.add("آیکن ⚙️ موجود",
          "⚙️" in src)
    c.add('aria-label="تنظیمات"',
          'aria-label="تنظیمات"' in src)
    c.add("حذف dropdown موقت تم: useThemeStore",
          "useThemeStore" not in src,
          "useThemeStore باید از HomePage حذف شده باشد")
    c.add("حذف dropdown موقت تم: listThemes",
          "listThemes" not in src,
          "listThemes نباید در HomePage باشد")
    c.add("حذف <select value={themeId}",
          "value={themeId}" not in src)

    # regression
    c.add("askConfirm حفظ شد (regression از زیرگام ۸.۳)",
          "await askConfirm" in src)
    c.add("handleLogout async حفظ شد",
          "const handleLogout = async" in src)
    c.add("لینک نمودار BTC حفظ شد",
          'to="/chart/1"' in src)
    c.add("data-card-link حفظ شد",
          'data-card-link="true"' in src)

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
    print(f"✅ تمام {c.passed} چک استاتیک سبز.")

    # ============================================================
    # ۷) npm run build
    # ============================================================
    print()
    print("=" * 64)
    print("۷) npm run build (smoke test)")
    print("=" * 64)

    if not (FRONTEND / "node_modules").exists():
        print("⚠️  node_modules موجود نیست — build skipped.")
        return 0

    npm = shutil.which("npm") or shutil.which("npm.cmd")
    if not npm:
        print("⚠️  npm در PATH یافت نشد — build skipped.")
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
    last_lines = stdout.strip().split("\n")[-15:]
    print("--- خروجی build (آخرین خطوط) ---")
    for line in last_lines:
        print(f"  {line}")

    if result.returncode == 0:
        print()
        print("=" * 64)
        print(f"✅ تمام تست‌ها سبز: {c.passed} چک استاتیک + npm build")
        print("=" * 64)
        print()
        print("چک بصری در 🟧 tab «3 frontend»:")
        print("  ۱) refresh مرورگر → /")
        print("  ۲) hover روی ⚙️ → tooltip 'تنظیمات'")
        print("  ۳) کلیک روی ⚙️ → رفتن به /settings")
        print("  ۴) ۵ کارت تم با preview رنگ — کارت فعال با badge '✓ فعال'")
        print("  ۵) کلیک روی هر کارت → اعمال آنی تم سراسری")
        print("     - HomePage هم رنگ‌های جدید را می‌گیرد (مشاهده در بازگشت)")
        print("  ۶) ۴ دکمه preset اندازه فونت — preview پایین زنده تغییر کند")
        print("  ۷) دکمه «بازگشت به پیش‌فرض»:")
        print("     - ConfirmDialog نارنجی ظاهر شود")
        print("     - تأیید → تم/فونت ریست + Toast سبز موفقیت")
        print("     - انصراف → بدون تغییر")
        print("  ۸) refresh مرورگر → تم و فونت persist می‌مانند")
        return 0
    else:
        print()
        print("--- stderr ---")
        for line in stderr.strip().split("\n")[-15:]:
            print(f"  {line}")
        print()
        print("=" * 64)
        print(f"❌ npm build شکست خورد (exit code: {result.returncode})")
        print("=" * 64)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
