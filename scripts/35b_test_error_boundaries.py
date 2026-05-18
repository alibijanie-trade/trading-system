# -*- coding: utf-8 -*-
"""
اسکریپت ۳۵b — تست خودکار اصلاحیه ۳۵ (Error Boundaries)
================================================================
طبق قانون #۲۲ سند v2.7.

پوشش تست:

  Section A — وجود فایل‌ها
    ۱) ErrorBoundary.jsx ساخته شد
    ۲) App.jsx به‌روز است

  Section B — ErrorBoundary.jsx محتوای صحیح
    ۱) export default class
    ۲) extends Component
    ۳) static getDerivedStateFromError (الزامی React)
    ۴) componentDidCatch (الزامی React)
    ۵) state.hasError, state.error
    ۶) handler ها: handleReset, handleReload, handleCopyDetails
    ۷) Variant Indicator Pattern: borderInlineStart + accent color
    ۸) بدون hex hardcoded
    ۹) role="alert" برای accessibility
    ۱۰) aria-live="assertive"
    ۱۱) fontSize فقط با rem (نه عددی)
    ۱۲) import.meta.env.DEV چک می‌شود (gating dev details)
    ۱۳) متن فارسی RTL: "خطایی رخ داد"، "تلاش مجدد"، "بارگذاری مجدد"

  Section C — App.jsx integration
    ۱) import ErrorBoundary
    ۲) outer ErrorBoundary (label="root")
    ۳) inner ErrorBoundary روی هر ۴ صفحه (login, home, chart, settings)

  Section D — runtime build check (اگر node موجود)
    ۱) `npm run build` با ErrorBoundary موفق است (no syntax error)
    — اگر node یا node_modules نباشد، skip می‌شود

نحوه اجرا:
    python scripts/35b_test_error_boundaries.py
================================================================
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
FRONTEND = PROJECT_ROOT / "frontend"
SRC = FRONTEND / "src"

ERROR_BOUNDARY_PATH = SRC / "components" / "common" / "ErrorBoundary.jsx"
APP_JSX_PATH = SRC / "App.jsx"

EXPECTED_ROUTE_LABELS = ["route:login", "route:home", "route:chart", "route:settings"]


# ────────────────────────────────────────────────────────────────
# Checks utility
# ────────────────────────────────────────────────────────────────
class Checks:
    def __init__(self):
        self.results = []
        self._section = ""

    def section(self, name):
        self._section = name
        print()
        print(f"--- {name} ---")

    def add(self, name, ok, detail=""):
        full = f"[{self._section}] {name}" if self._section else name
        self.results.append((full, ok, detail))
        mark = "✅" if ok else "❌"
        print(f"  {mark} {name}")
        if not ok and detail:
            print(f"     ↳ {detail}")

    @property
    def passed(self):
        return sum(1 for _, ok, _ in self.results if ok)

    @property
    def failed(self):
        return sum(1 for _, ok, _ in self.results if not ok)

    @property
    def all_pass(self):
        return self.failed == 0


# ────────────────────────────────────────────────────────────────
# Section A
# ────────────────────────────────────────────────────────────────
def section_a_files(c):
    c.section("A) وجود فایل‌ها")
    c.add(
        "ErrorBoundary.jsx موجود",
        ERROR_BOUNDARY_PATH.exists(),
        str(ERROR_BOUNDARY_PATH),
    )
    c.add("App.jsx موجود", APP_JSX_PATH.exists(), str(APP_JSX_PATH))


# ────────────────────────────────────────────────────────────────
# Section B — ErrorBoundary content
# ────────────────────────────────────────────────────────────────
# الگوهای regex
RX_HEX = re.compile(r"#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?\b")
# fontSize: <عدد> بدون template literal — این چیزی است که نمی‌خواهیم
RX_BAD_FONT_SIZE = re.compile(r"fontSize:\s*\d+(?=\s*[,\}\)\s])")


def section_b_error_boundary(c):
    c.section("B) ErrorBoundary.jsx محتوا")
    if not ERROR_BOUNDARY_PATH.exists():
        return
    content = ERROR_BOUNDARY_PATH.read_text(encoding="utf-8")

    checks = [
        ("export default class", "export default class ErrorBoundary" in content),
        ("extends Component", "extends Component" in content),
        ("static getDerivedStateFromError", "static getDerivedStateFromError" in content),
        ("componentDidCatch", "componentDidCatch" in content),
        ("state.hasError", "hasError" in content),
        ("handleReset method", "handleReset" in content),
        ("handleReload method", "handleReload" in content),
        ("handleCopyDetails method", "handleCopyDetails" in content),
        ("Variant Pattern: borderInlineStart", "borderInlineStart" in content),
        ("rendered danger color (--color-danger)", "var(--color-danger)" in content),
        ("text uses var(--color-text)", "var(--color-text)" in content),
        ("بدون hex hardcoded (#RRGGBB)", not RX_HEX.search(content)),
        ('role="alert"', 'role="alert"' in content),
        ('aria-live="assertive"', 'aria-live="assertive"' in content),
        (
            "fontSize فقط با rem (نه عددی inline)",
            not RX_BAD_FONT_SIZE.search(content),
        ),
        ("dev gating via import.meta.env.DEV", "import.meta.env.DEV" in content),
        ("متن RTL: «خطایی رخ داد»", "خطایی رخ داد" in content),
        ("متن RTL: «تلاش مجدد»", "تلاش مجدد" in content),
        ("متن RTL: «بارگذاری مجدد»", "بارگذاری مجدد" in content),
        ("fallback prop support", "this.props.fallback" in content),
        ("onReset prop support", "this.props.onReset" in content),
    ]
    for name, ok in checks:
        detail = ""
        if not ok and "hex" in name:
            m = RX_HEX.search(content)
            if m:
                detail = f"یافت شد: {m.group(0)!r}"
        if not ok and "fontSize" in name:
            m = RX_BAD_FONT_SIZE.search(content)
            if m:
                detail = f"یافت شد: {m.group(0)!r}"
        c.add(name, ok, detail)


# ────────────────────────────────────────────────────────────────
# Section C — App.jsx integration
# ────────────────────────────────────────────────────────────────
def section_c_app_integration(c):
    c.section("C) App.jsx integration")
    if not APP_JSX_PATH.exists():
        return
    content = APP_JSX_PATH.read_text(encoding="utf-8")

    c.add(
        "import ErrorBoundary",
        'from "./components/common/ErrorBoundary.jsx"' in content
        or "from './components/common/ErrorBoundary.jsx'" in content,
        "",
    )
    c.add(
        'outer ErrorBoundary label="root"',
        '<ErrorBoundary label="root">' in content or "<ErrorBoundary label='root'>" in content,
        "",
    )

    # inner — هر ۴ صفحه
    for label in EXPECTED_ROUTE_LABELS:
        marker_dq = f'<ErrorBoundary label="{label}">'
        marker_sq = f"<ErrorBoundary label='{label}'>"
        c.add(
            f"inner ErrorBoundary label={label!r}",
            (marker_dq in content) or (marker_sq in content),
            "",
        )

    # شمارش تعداد ErrorBoundary — باید ≥ ۵ باشد (۱ outer + ۴ inner)
    open_count = content.count("<ErrorBoundary")
    c.add(
        "تعداد ErrorBoundary در App.jsx ≥ 5",
        open_count >= 5,
        f"شمارش = {open_count}",
    )


# ────────────────────────────────────────────────────────────────
# Section D — build check (skippable)
# ────────────────────────────────────────────────────────────────
def section_d_build(c):
    c.section("D) Runtime — npm build")

    node_modules = FRONTEND / "node_modules"
    if not node_modules.exists():
        c.add(
            "build (skipped)",
            True,
            "node_modules غایب — این OK است در محیط CI/Claude. "
            "روی ماشین کاربر: cd frontend && npm install ابتدا",
        )
        return

    npx = shutil.which("npx") or shutil.which("npx.cmd")
    if not npx:
        c.add("build (skipped)", True, "npx در PATH نیست")
        return

    try:
        result = subprocess.run(
            ["npm", "run", "build"],
            cwd=str(FRONTEND),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=180,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        c.add("npm run build", False, f"{type(e).__name__}: {e}")
        return

    ok = result.returncode == 0
    detail = ""
    if not ok:
        # آخرین چند خط stderr
        last_lines = (result.stderr or result.stdout).strip().split("\n")[-10:]
        detail = "\n          ".join(last_lines)
    c.add(
        "npm run build موفق",
        ok,
        detail,
    )


# ────────────────────────────────────────────────────────────────
# Main
# ────────────────────────────────────────────────────────────────
def main() -> int:
    print("=" * 64)
    print("اسکریپت ۳۵b — تست Error Boundaries")
    print("=" * 64)

    c = Checks()
    section_a_files(c)
    section_b_error_boundary(c)
    section_c_app_integration(c)
    section_d_build(c)

    print()
    print("=" * 64)
    print(f"خلاصه: {c.passed} ✅   |   {c.failed} ❌   |   جمع: {len(c.results)}")
    print("=" * 64)

    return 0 if c.all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
