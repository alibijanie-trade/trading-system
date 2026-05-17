# -*- coding: utf-8 -*-
"""
اسکریپت ۳۶b — تست خودکار اصلاحیه ۳۶ (Vitest setup)
================================================================
طبق قانون #۲۲ سند v2.7.

پوشش تست (static checks، بدون نیاز به npm):

  Section A — وجود فایل‌ها
    ۱) package.json
    ۲) vite.config.js
    ۳) src/test/setup.js
    ۴) ۵ فایل تست

  Section B — package.json محتوای صحیح
    ۱) JSON معتبر است
    ۲) همه ۴ script جدید (test/test:watch/test:coverage/test:ui) موجود
    ۳) همه ۶ devDependency (vitest، coverage، jsdom، testing-library×3)
    ۴) scripts موجود قبلی (dev, build, lint, preview) حفظ شدند
    ۵) dependencies موجود (react, axios, ...) دست‌نخورده باقی ماندند

  Section C — vite.config.js محتوای صحیح
    ۱) plugins: [react()] حفظ شد
    ۲) بلوک test موجود
    ۳) environment: 'jsdom'
    ۴) globals: true
    ۵) setupFiles: ['./src/test/setup.js']
    ۶) coverage.provider: 'v8'

  Section D — setup.js صحیح
    ۱) import '@testing-library/jest-dom/vitest'

  Section E — محتوای فایل‌های تست
    ۱) numberFormat.test.js شامل describe('formatNumber')
    ۲) dateFormat.test.js شامل describe('formatDate
    ۳) confirmStore.test.js شامل beforeEach + resetStore
    ۴) ErrorBoundary.test.jsx شامل Bomb component + role='alert'
    ۵) LoginPage.test.jsx شامل MemoryRouter

  Section F — Runtime (اگر node_modules موجود)
    ۱) npm test ۵ فایل تست را اجرا و pass می‌کند
    — اگر node_modules غایب، skip می‌شود

نحوه اجرا:
    python scripts/36b_test_vitest_setup.py
================================================================
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
FRONTEND = PROJECT_ROOT / "frontend"
SRC = FRONTEND / "src"

PACKAGE_JSON = FRONTEND / "package.json"
VITE_CONFIG  = FRONTEND / "vite.config.js"
SETUP_JS     = SRC / "test" / "setup.js"

TEST_FILES = [
    SRC / "utils" / "numberFormat.test.js",
    SRC / "utils" / "dateFormat.test.js",
    SRC / "stores" / "confirmStore.test.js",
    SRC / "components" / "common" / "ErrorBoundary.test.jsx",
    SRC / "pages" / "LoginPage.test.jsx",
]

EXPECTED_SCRIPTS = ["test", "test:watch", "test:coverage", "test:ui"]

EXPECTED_DEV_DEPS = [
    "vitest",
    "@vitest/coverage-v8",
    "jsdom",
    "@testing-library/react",
    "@testing-library/jest-dom",
    "@testing-library/user-event",
]

PRESERVED_SCRIPTS = ["dev", "build", "lint", "preview"]

PRESERVED_DEPS = ["react", "react-dom", "react-router-dom", "axios", "zustand"]


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
# Section A — files
# ────────────────────────────────────────────────────────────────
def section_a_files(c):
    c.section("A) وجود فایل‌ها")
    c.add("package.json موجود", PACKAGE_JSON.exists(), str(PACKAGE_JSON))
    c.add("vite.config.js موجود", VITE_CONFIG.exists(), str(VITE_CONFIG))
    c.add("src/test/setup.js موجود", SETUP_JS.exists(), str(SETUP_JS))
    for tf in TEST_FILES:
        rel = tf.relative_to(FRONTEND)
        c.add(f"تست موجود: {rel}", tf.exists(), "")


# ────────────────────────────────────────────────────────────────
# Section B — package.json
# ────────────────────────────────────────────────────────────────
def section_b_package_json(c):
    c.section("B) package.json محتوا")
    if not PACKAGE_JSON.exists():
        return
    try:
        pkg = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        c.add("JSON معتبر", False, str(e))
        return
    c.add("JSON معتبر", True, "")

    scripts = pkg.get("scripts", {})
    for s in EXPECTED_SCRIPTS:
        c.add(f"script '{s}' موجود", s in scripts, f"value: {scripts.get(s)!r}")
    for s in PRESERVED_SCRIPTS:
        c.add(f"script قبلی '{s}' حفظ شد", s in scripts, "")

    devdeps = pkg.get("devDependencies", {})
    for d in EXPECTED_DEV_DEPS:
        c.add(f"devDep '{d}' موجود", d in devdeps, f"version: {devdeps.get(d)!r}")

    deps = pkg.get("dependencies", {})
    for d in PRESERVED_DEPS:
        c.add(f"dependency قبلی '{d}' حفظ شد", d in deps, "")


# ────────────────────────────────────────────────────────────────
# Section C — vite.config.js
# ────────────────────────────────────────────────────────────────
def section_c_vite_config(c):
    c.section("C) vite.config.js محتوا")
    if not VITE_CONFIG.exists():
        return
    content = VITE_CONFIG.read_text(encoding="utf-8")

    checks = [
        ("plugins: [react()] حفظ شد", "plugins:" in content and "react()" in content),
        ("بلوک test موجود", "test:" in content or "test :" in content),
        ("environment: 'jsdom'", "'jsdom'" in content or '"jsdom"' in content),
        ("globals: true", "globals: true" in content or "globals:true" in content),
        (
            "setupFiles: ['./src/test/setup.js']",
            "./src/test/setup.js" in content,
        ),
        (
            "coverage.provider: 'v8'",
            "'v8'" in content or '"v8"' in content,
        ),
    ]
    for name, ok in checks:
        c.add(name, ok, "")


# ────────────────────────────────────────────────────────────────
# Section D — setup.js
# ────────────────────────────────────────────────────────────────
def section_d_setup(c):
    c.section("D) src/test/setup.js محتوا")
    if not SETUP_JS.exists():
        return
    content = SETUP_JS.read_text(encoding="utf-8")
    c.add(
        "import '@testing-library/jest-dom/vitest'",
        "@testing-library/jest-dom/vitest" in content,
        "",
    )


# ────────────────────────────────────────────────────────────────
# Section E — test files content
# ────────────────────────────────────────────────────────────────
def section_e_test_contents(c):
    c.section("E) محتوای فایل‌های تست")

    cases = [
        (TEST_FILES[0], "numberFormat", "describe('formatNumber'"),
        (TEST_FILES[1], "dateFormat",   "describe('formatDate"),
        (TEST_FILES[2], "confirmStore", "beforeEach"),
        (TEST_FILES[2], "confirmStore — Promise behavior", ".resolves.toBe(true)"),
        (TEST_FILES[3], "ErrorBoundary — Bomb", "function Bomb"),
        (TEST_FILES[3], "ErrorBoundary — role='alert'", "getByRole('alert')"),
        (TEST_FILES[3], "ErrorBoundary — Persian text", "خطایی رخ داد"),
        (TEST_FILES[4], "LoginPage — MemoryRouter", "MemoryRouter"),
        (TEST_FILES[4], "LoginPage — labels", "نام کاربری"),
    ]
    for path, label, marker in cases:
        if not path.exists():
            c.add(f"{label}: {marker[:30]!r}", False, "file missing")
            continue
        content = path.read_text(encoding="utf-8")
        c.add(f"{label}: شامل {marker[:30]!r}", marker in content, "")


# ────────────────────────────────────────────────────────────────
# Section F — runtime npm test (skippable)
# ────────────────────────────────────────────────────────────────
def section_f_runtime(c):
    c.section("F) Runtime — npm test")

    node_modules = FRONTEND / "node_modules"
    if not node_modules.exists():
        c.add(
            "npm test (skipped)",
            True,
            "node_modules غایب — این OK است در محیط Claude/CI. "
            "روی ماشین کاربر: cd frontend && npm install ابتدا",
        )
        return

    # بررسی نصب vitest
    vitest_bin = node_modules / ".bin" / "vitest"
    if not vitest_bin.exists() and not (node_modules / ".bin" / "vitest.cmd").exists():
        c.add(
            "vitest نصب شده",
            False,
            "vitest در node_modules/.bin/ نیست — npm install را اجرا کنید",
        )
        return

    npm = shutil.which("npm") or shutil.which("npm.cmd")
    if not npm:
        c.add("npm test (skipped)", True, "npm در PATH نیست")
        return

    try:
        result = subprocess.run(
            ["npm", "test", "--silent"],
            cwd=str(FRONTEND),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        c.add("npm test", False, f"{type(e).__name__}: {e}")
        return

    ok = result.returncode == 0
    detail = ""
    if not ok:
        last_lines = (result.stderr or result.stdout).strip().split("\n")[-15:]
        detail = "\n          ".join(last_lines)
    c.add(
        f"npm test pass شد (exit code {result.returncode})",
        ok,
        detail,
    )


# ────────────────────────────────────────────────────────────────
# Main
# ────────────────────────────────────────────────────────────────
def main() -> int:
    print("=" * 64)
    print("اسکریپت ۳۶b — تست Vitest setup")
    print("=" * 64)

    c = Checks()
    section_a_files(c)
    section_b_package_json(c)
    section_c_vite_config(c)
    section_d_setup(c)
    section_e_test_contents(c)
    section_f_runtime(c)

    print()
    print("=" * 64)
    print(f"خلاصه: {c.passed} ✅   |   {c.failed} ❌   |   جمع: {len(c.results)}")
    print("=" * 64)
    return 0 if c.all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
