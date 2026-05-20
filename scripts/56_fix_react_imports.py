# -*- coding: utf-8 -*-
"""
56_fix_react_imports.py - Bug #50 cleanup (E2.1)

Applies the permanent fix for the temporary import-React workaround
from chat 6 (script 45). With React 17+ automatic JSX runtime,
`import React from 'react'` is no longer needed for JSX.

Three operations:
  1. vite.config.js: react() -> react({ jsxRuntime: 'automatic' })
  2. main.jsx: convert React.StrictMode to named StrictMode
  3. Other .jsx files: remove `import React from 'react';` if React.* not used

Compliance:
  - Rule #22 (companion test): 56b_test_react_imports.py
  - Rule #30 (idempotent): re-running produces same output
  - Rule #37 (read-back verify): verifies after each write
  - Rule #46 (ASCII-only in print): no Unicode chars in stdout

Usage:
  python scripts/56_fix_react_imports.py
"""
import re
import sys
from pathlib import Path

# Encoding setup
try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass


# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
SRC_DIR = FRONTEND_DIR / "src"
VITE_CONFIG = FRONTEND_DIR / "vite.config.js"
MAIN_JSX = SRC_DIR / "main.jsx"


# Pattern: matches `import React from 'react';` or with double quotes,
# at start of a line, followed by newline
REACT_IMPORT_PATTERN = re.compile(r"^import React from ['\"]react['\"];\r?\n", re.MULTILINE)


def fix_vite_config():
    """Add jsxRuntime: 'automatic' to react() plugin in vite.config.js."""
    if not VITE_CONFIG.exists():
        print("[FAIL] vite.config.js not found at: " + str(VITE_CONFIG))
        return None

    content = VITE_CONFIG.read_text(encoding="utf-8")
    target_new = "plugins: [react({ jsxRuntime: 'automatic' })],"
    target_old = "plugins: [react()],"

    if target_new in content:
        print("[SKIP] vite.config.js already has jsxRuntime: 'automatic' (idempotent)")
        return False

    if target_old not in content:
        print("[FAIL] vite.config.js: expected pattern 'plugins: [react()],' not found")
        print("       (file may have been modified - manual review needed)")
        return None

    new_content = content.replace(target_old, target_new, 1)
    VITE_CONFIG.write_text(new_content, encoding="utf-8", newline="\n")

    # read-back verify (rule #37)
    actual = VITE_CONFIG.read_text(encoding="utf-8")
    if target_new not in actual:
        print("[FAIL] vite.config.js read-back: new content not present")
        return None
    if target_old in actual:
        print("[FAIL] vite.config.js read-back: old content still present")
        return None

    print("[OK] vite.config.js updated: react() -> react({ jsxRuntime: 'automatic' })")
    return True


def fix_main_jsx():
    """Special case: main.jsx uses React.StrictMode -> use named import."""
    if not MAIN_JSX.exists():
        print("[FAIL] main.jsx not found at: " + str(MAIN_JSX))
        return None

    content = MAIN_JSX.read_text(encoding="utf-8")

    # Check if already fixed
    already_fixed = (
        "import React from" not in content
        and "import { StrictMode }" in content
        and "<React.StrictMode>" not in content
    )
    if already_fixed:
        print("[SKIP] main.jsx already converted to named StrictMode (idempotent)")
        return False

    # Apply 4 replacements (handle both quote styles)
    new_content = content
    replacements = [
        ('import React from "react";', 'import { StrictMode } from "react";'),
        ("import React from 'react';", "import { StrictMode } from 'react';"),
        ("<React.StrictMode>", "<StrictMode>"),
        ("</React.StrictMode>", "</StrictMode>"),
    ]
    changes_made = []
    for old, new in replacements:
        if old in new_content:
            new_content = new_content.replace(old, new)
            changes_made.append(
                old.split(" from ")[0] if "import" in old else old.replace("<", "").replace(">", "")
            )

    if not changes_made:
        print("[INFO] main.jsx: no expected patterns found (manual review may be needed)")
        return False

    MAIN_JSX.write_text(new_content, encoding="utf-8", newline="\n")

    # read-back verify
    actual = MAIN_JSX.read_text(encoding="utf-8")
    if "<React.StrictMode>" in actual:
        print("[FAIL] main.jsx read-back: still has <React.StrictMode>")
        return None
    if 'import React from "react"' in actual or "import React from 'react'" in actual:
        print("[FAIL] main.jsx read-back: still has 'import React from'")
        return None
    if "import { StrictMode }" not in actual:
        print("[FAIL] main.jsx read-back: missing 'import { StrictMode }'")
        return None
    if "<StrictMode>" not in actual:
        print("[FAIL] main.jsx read-back: missing '<StrictMode>'")
        return None

    print("[OK] main.jsx converted: React.StrictMode -> named StrictMode")
    return True


def fix_other_jsx_files():
    """Remove 'import React from 'react';' from all .jsx except main.jsx."""
    if not SRC_DIR.exists():
        print("[FAIL] src/ not found at: " + str(SRC_DIR))
        return None

    jsx_files = sorted(SRC_DIR.rglob("*.jsx"))
    cleaned = []
    already_clean = []
    needs_attention = []

    for f in jsx_files:
        if f.resolve() == MAIN_JSX.resolve():
            continue  # handled separately

        content = f.read_text(encoding="utf-8")
        try:
            relpath = f.relative_to(SRC_DIR).as_posix()
        except ValueError:
            relpath = str(f)

        if not REACT_IMPORT_PATTERN.search(content):
            already_clean.append(relpath)
            continue

        # Check if React.<something> is used after removing the import line
        # (we only check after the import to avoid matching the import itself)
        content_without_import = REACT_IMPORT_PATTERN.sub("", content, count=1)
        if re.search(r"\bReact\.", content_without_import):
            needs_attention.append(relpath)
            continue

        # Safe to remove
        new_content = REACT_IMPORT_PATTERN.sub("", content, count=1)
        f.write_text(new_content, encoding="utf-8", newline="\n")

        # read-back verify
        actual = f.read_text(encoding="utf-8")
        if REACT_IMPORT_PATTERN.search(actual):
            print("[FAIL] " + relpath + ": import not actually removed")
            return None

        cleaned.append(relpath)

    print("[OK] Cleaned " + str(len(cleaned)) + " file(s):")
    for p in cleaned:
        print("     - " + p)

    if already_clean:
        print("[SKIP] " + str(len(already_clean)) + " file(s) already had no React import:")
        for p in already_clean:
            print("     - " + p)

    if needs_attention:
        print("[WARN] " + str(len(needs_attention)) + " file(s) use React.* (need manual review):")
        for p in needs_attention:
            print("     - " + p)

    return cleaned


def main():
    print("=" * 60)
    print("  56_fix_react_imports.py - Bug #50 cleanup (E2.1)")
    print("=" * 60)
    print()

    # Step 1: vite.config.js
    print("Step 1: vite.config.js - explicit jsxRuntime")
    print("-" * 60)
    vite_result = fix_vite_config()
    if vite_result is None:
        return 1
    print()

    # Step 2: main.jsx (special)
    print("Step 2: main.jsx - React.StrictMode -> StrictMode")
    print("-" * 60)
    main_result = fix_main_jsx()
    if main_result is None:
        return 1
    print()

    # Step 3: Other .jsx files
    print("Step 3: Other .jsx files - remove 'import React'")
    print("-" * 60)
    cleaned = fix_other_jsx_files()
    if cleaned is None:
        return 1
    print()

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("vite.config.js:  " + ("updated" if vite_result else "no change (idempotent)"))
    print("main.jsx:        " + ("updated" if main_result else "no change (idempotent)"))
    print("other .jsx:      " + str(len(cleaned)) + " cleaned this run")
    print()
    print("Next steps:")
    print("  1. Run smoke tests:  python scripts/56b_test_react_imports.py")
    print("  2. Run vitest:       cd frontend && npm test")
    print("  3. Expect: 30/30 tests pass (no regressions)")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
