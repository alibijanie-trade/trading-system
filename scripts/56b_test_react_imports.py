# -*- coding: utf-8 -*-
"""
56b_test_react_imports.py - Smoke tests for Bug #50 cleanup

Verifies that 56_fix_react_imports.py produced correct state:
  - vite.config.js has explicit jsxRuntime: 'automatic'
  - main.jsx uses named StrictMode import
  - No .jsx file has raw 'import React from "react";'
  - .jsx files that legitimately need React.* are flagged (none expected)

Exit codes:
  0 - all tests passed
  1 - one or more tests failed

NOTE: Does NOT run `npm test` - that's a separate user action.
"""
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass


PROJECT_ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
SRC_DIR = FRONTEND_DIR / "src"
VITE_CONFIG = FRONTEND_DIR / "vite.config.js"
MAIN_JSX = SRC_DIR / "main.jsx"

REACT_IMPORT_PATTERN = re.compile(r"^import React from ['\"]react['\"];\r?\n?", re.MULTILINE)


def check(name, condition, detail=""):
    if condition:
        print("[PASS] " + name)
        return True
    else:
        print("[FAIL] " + name + (": " + detail if detail else ""))
        return False


def main():
    print("=" * 60)
    print("  56b_test_react_imports.py - Smoke tests")
    print("=" * 60)
    print()

    results = []

    # ---- Group 1: File existence ----
    print("Group 1: Required files exist")
    print("-" * 60)
    results.append(check("vite.config.js exists", VITE_CONFIG.exists()))
    results.append(check("main.jsx exists", MAIN_JSX.exists()))
    results.append(check("src/ directory exists", SRC_DIR.exists()))
    if not (VITE_CONFIG.exists() and MAIN_JSX.exists() and SRC_DIR.exists()):
        print()
        print("ABORT: required files missing")
        return 1
    print()

    # ---- Group 2: vite.config.js ----
    print("Group 2: vite.config.js has explicit jsxRuntime")
    print("-" * 60)
    vite_content = VITE_CONFIG.read_text(encoding="utf-8")
    results.append(
        check("Contains 'jsxRuntime: \\'automatic\\''", "jsxRuntime: 'automatic'" in vite_content)
    )
    results.append(
        check(
            "Does NOT contain bare 'react()'",
            "react()" not in vite_content,
            "bare react() found - jsxRuntime not explicit",
        )
    )
    print()

    # ---- Group 3: main.jsx ----
    print("Group 3: main.jsx uses named StrictMode")
    print("-" * 60)
    main_content = MAIN_JSX.read_text(encoding="utf-8")
    results.append(
        check("Has 'import { StrictMode }' from react", "import { StrictMode }" in main_content)
    )
    results.append(
        check(
            "Does NOT have 'import React from'",
            "import React from" not in main_content,
            "default React import still present",
        )
    )
    results.append(
        check(
            "Uses '<StrictMode>' (not <React.StrictMode>)",
            "<StrictMode>" in main_content and "<React.StrictMode>" not in main_content,
        )
    )
    results.append(
        check(
            "Uses '</StrictMode>' (closing)",
            "</StrictMode>" in main_content and "</React.StrictMode>" not in main_content,
        )
    )
    print()

    # ---- Group 4: Other .jsx files ----
    print("Group 4: Other .jsx files have no raw 'import React'")
    print("-" * 60)
    jsx_files = sorted(SRC_DIR.rglob("*.jsx"))
    violations = []
    for f in jsx_files:
        if f.resolve() == MAIN_JSX.resolve():
            continue
        content = f.read_text(encoding="utf-8")
        if REACT_IMPORT_PATTERN.search(content):
            try:
                relpath = f.relative_to(SRC_DIR).as_posix()
            except ValueError:
                relpath = str(f)
            violations.append(relpath)

    results.append(
        check(
            "No .jsx file has raw 'import React from \"react\";'",
            len(violations) == 0,
            "violations: " + ", ".join(violations) if violations else "",
        )
    )
    print("     (scanned " + str(len(jsx_files) - 1) + " .jsx files excluding main.jsx)")
    print()

    # ---- Group 5: React.* usage check (informational) ----
    print("Group 5: Files using React.* (informational - none expected)")
    print("-" * 60)
    react_dot_users = []
    for f in jsx_files:
        if f.resolve() == MAIN_JSX.resolve():
            continue
        content = f.read_text(encoding="utf-8")
        if re.search(r"\bReact\.", content):
            try:
                relpath = f.relative_to(SRC_DIR).as_posix()
            except ValueError:
                relpath = str(f)
            react_dot_users.append(relpath)

    if react_dot_users:
        print(
            "[INFO] " + str(len(react_dot_users)) + " file(s) use React.* (review if intentional):"
        )
        for p in react_dot_users:
            print("     - " + p)
    else:
        print("[PASS] No file uses React.* (all migrated to named imports or JSX-only)")
    print()

    # ---- Summary ----
    print("=" * 60)
    passed = sum(1 for r in results if r)
    total = len(results)
    if passed == total:
        print("ALL TESTS PASSED (" + str(passed) + "/" + str(total) + ")")
        print()
        print("Next step: cd frontend && npm test")
        print("Expected: 30/30 tests pass")
        print("=" * 60)
        return 0
    else:
        failed = total - passed
        print("FAILED: " + str(failed) + " / " + str(total) + " tests")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
