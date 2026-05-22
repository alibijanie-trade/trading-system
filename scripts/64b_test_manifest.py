# -*- coding: utf-8 -*-
"""
scripts/64b_test_manifest.py - Test suite for 64_generate_manifest.py

Per Rule #22: every {N}_*.py must have {N}b_test_*.py companion.

Tests:
    test_1_script_imports           - generator script imports without error
    test_2_constants_valid          - PROJECT_ROOT, MANIFEST_PATH, TIER_RULES, SKIP_DIRS valid
    test_3_glob_segment_based       - single * is single-segment; ** is multi-segment
    test_4_classify_priority_order  - T1 wins over T2 for files in both
    test_5_classify_no_match        - files with no tier match return None
    test_6_should_skip_dir          - SKIP_DIRS properly skip nested paths
    test_7_dry_run_subprocess       - --dry-run executes successfully (exit 0)
    test_8_help_output              - --help prints expected flags

Exit codes:
    0 - all tests passed
    1 - one or more failures
"""

import importlib.util
import subprocess
import sys
from pathlib import Path

# Force UTF-8 stdout on Windows (Rule #46)
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

THIS_DIR = Path(__file__).resolve().parent
GENERATOR_SCRIPT = THIS_DIR / "64_generate_manifest.py"
REPO_ROOT = THIS_DIR.parent


def load_generator_module():
    """Dynamically load the generator script as a module."""
    spec = importlib.util.spec_from_file_location("manifest_gen", str(GENERATOR_SCRIPT))
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {GENERATOR_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# =============================================================================
# Tests
# =============================================================================


def test_1_script_imports():
    """Generator script imports without syntax errors."""
    if not GENERATOR_SCRIPT.exists():
        return False, f"generator script not found: {GENERATOR_SCRIPT}"
    try:
        load_generator_module()
        return True, "generator script imports cleanly"
    except Exception as e:
        return False, f"import failed: {e}"


def test_2_constants_valid():
    """PROJECT_ROOT, MANIFEST_PATH, TIER_RULES, SKIP_DIRS are valid."""
    try:
        m = load_generator_module()
    except Exception as e:
        return False, f"cannot load module: {e}"

    errors = []

    # PROJECT_ROOT must exist as directory
    project_root = getattr(m, "PROJECT_ROOT", None)
    if project_root is None:
        errors.append("PROJECT_ROOT not defined")
    elif not Path(project_root).is_dir():
        errors.append(f"PROJECT_ROOT does not exist: {project_root}")

    # MANIFEST_PATH must be under PROJECT_ROOT
    manifest_path = getattr(m, "MANIFEST_PATH", None)
    if manifest_path is None:
        errors.append("MANIFEST_PATH not defined")
    else:
        try:
            Path(manifest_path).relative_to(project_root)
        except (ValueError, TypeError):
            errors.append(f"MANIFEST_PATH not under PROJECT_ROOT: {manifest_path}")

    # TIER_RULES must be a list of (label, patterns) tuples
    tier_rules = getattr(m, "TIER_RULES", None)
    if tier_rules is None:
        errors.append("TIER_RULES not defined")
    elif not isinstance(tier_rules, list):
        errors.append(f"TIER_RULES not a list: {type(tier_rules)}")
    else:
        expected_labels = ["T1", "T2", "T3", "T4.1", "T4.2"]
        actual_labels = [label for label, _ in tier_rules]
        if actual_labels != expected_labels:
            errors.append(f"TIER_RULES labels mismatch: {actual_labels} != {expected_labels}")

    # SKIP_DIRS must be a set or collection
    skip_dirs = getattr(m, "SKIP_DIRS", None)
    if skip_dirs is None:
        errors.append("SKIP_DIRS not defined")
    elif ".git" not in skip_dirs or "venv" not in skip_dirs or "node_modules" not in skip_dirs:
        errors.append("SKIP_DIRS missing common entries (.git, venv, node_modules)")

    if errors:
        return False, "; ".join(errors)
    return True, "all 4 constants valid"


def test_3_glob_segment_based():
    """Glob matching: single * is single-segment, ** is multi-segment."""
    try:
        m = load_generator_module()
    except Exception as e:
        return False, f"cannot load module: {e}"

    matches_any = getattr(m, "matches_any", None)
    if matches_any is None:
        return False, "matches_any not exported"

    cases = [
        # (relpath, patterns, expected, description)
        (
            "docs/constitution/main.md",
            ["docs/constitution/*.md"],
            True,
            "single * matches direct child",
        ),
        (
            "docs/constitution/archive/v2_11_legacy.md",
            ["docs/constitution/*.md"],
            False,
            "single * does NOT match nested file (segment-based)",
        ),
        (
            "docs/constitution/archive/v2_11_legacy.md",
            ["docs/constitution/archive/*.md"],
            True,
            "exact archive pattern matches",
        ),
        (
            "backend/app/models/user.py",
            ["backend/app/**/*.py"],
            True,
            "** matches multiple segments",
        ),
        (
            "backend/main.py",
            ["backend/main.py"],
            True,
            "exact path match",
        ),
        (
            "scripts/64_generate_manifest.py",
            ["scripts/**/*.py"],
            True,
            "** with single-file deep matches",
        ),
        (
            "frontend/src/components/common/Toast.jsx",
            ["frontend/src/**/*.jsx"],
            True,
            "** matches frontend nested jsx",
        ),
        (
            "backend/trading.db",
            ["backend/main.py", "backend/app/**/*.py"],
            False,
            "no pattern matches db file -> False",
        ),
    ]

    failures = []
    for relpath, patterns, expected, desc in cases:
        got = matches_any(relpath, patterns)
        if got != expected:
            failures.append(f"FAIL: {desc} (path='{relpath}' got={got} expected={expected})")

    if failures:
        return False, "; ".join(failures)
    return True, f"all {len(cases)} glob cases passed"


def test_4_classify_priority_order():
    """T1 wins over T2 for SESSION_STATUS.md (both could theoretically match)."""
    try:
        m = load_generator_module()
    except Exception as e:
        return False, f"cannot load module: {e}"

    classify = getattr(m, "classify", None)
    if classify is None:
        return False, "classify not exported"

    cases = [
        # (relpath, expected_tier, description)
        ("docs/SESSION_STATUS.md", "T1", "SESSION_STATUS hits T1 explicit before T2 catch-all"),
        ("docs/constitution/main.md", "T1", "constitution module is T1"),
        ("docs/ARCHITECTURE.md", "T2", "ARCHITECTURE not in T1, hits T2 catch-all"),
        ("docs/STYLE_GUIDE.md", "T2", "STYLE_GUIDE is T2"),
        ("backend/app/models/user.py", "T3", "backend code is T3"),
        ("scripts/64_generate_manifest.py", "T3", "scripts are T3"),
        (".gitignore", "T4.1", "gitignore is T4.1 config"),
        ("backend/requirements.txt", "T4.1", "requirements.txt is T4.1"),
        (
            "data/excel_imports/btcusdt-daily-20220426.xlsx",
            "T4.2",
            "excel data is T4.2 (Golden Rule)",
        ),
        (
            "claude_workspace/snapshots/PROJECT_KNOWLEDGE.md",
            "T4.2",
            "snapshot is T4.2 (Golden Rule - gitignored but tracked here)",
        ),
    ]

    failures = []
    for relpath, expected_tier, desc in cases:
        got = classify(relpath)
        if got != expected_tier:
            failures.append(f"FAIL: {desc} (path='{relpath}' got={got} expected={expected_tier})")

    if failures:
        return False, "; ".join(failures)
    return True, f"all {len(cases)} classification cases passed"


def test_5_classify_no_match():
    """Files with no tier match return None (effectively T5 EXCLUDED)."""
    try:
        m = load_generator_module()
    except Exception as e:
        return False, f"cannot load module: {e}"

    classify = getattr(m, "classify", None)
    if classify is None:
        return False, "classify not exported"

    cases = [
        ("random/unknown/file.xyz", "random unknown file"),
        ("backend/trading.db", "db file - no tier matches"),
        ("claude_workspace/MDRS_V2_PENDING_DRAFT.md", "tracker file not in T patterns"),
        ("frontend/coverage/index.html", "coverage output (but also in skip dir)"),
    ]

    failures = []
    for relpath, desc in cases:
        got = classify(relpath)
        if got is not None:
            failures.append(f"FAIL: {desc} (path='{relpath}' got={got} expected=None)")

    if failures:
        return False, "; ".join(failures)
    return True, f"all {len(cases)} no-match cases returned None"


def test_6_should_skip_dir():
    """SKIP_DIRS properly skip nested paths."""
    try:
        m = load_generator_module()
    except Exception as e:
        return False, f"cannot load module: {e}"

    should_skip = getattr(m, "should_skip_dir", None)
    if should_skip is None:
        return False, "should_skip_dir not exported"

    cases = [
        # (relpath, expected_skip, description)
        (".git", True, "top-level .git"),
        ("venv", True, "venv at root"),
        ("node_modules", True, "node_modules at root"),
        ("backend/__pycache__", True, "nested __pycache__"),
        ("claude_workspace/zip_temp", True, "explicit multi-segment skip"),
        ("claude_workspace/screenshots", True, "explicit screenshots skip"),
        ("claude_workspace/snapshots", False, "snapshots NOT skipped (Golden Rule -> T4.2)"),
        ("docs", False, "docs NOT skipped"),
        ("backend/app", False, "backend/app NOT skipped"),
    ]

    failures = []
    for relpath, expected_skip, desc in cases:
        got = should_skip(relpath)
        if got != expected_skip:
            failures.append(f"FAIL: {desc} (path='{relpath}' got={got} expected={expected_skip})")

    if failures:
        return False, "; ".join(failures)
    return True, f"all {len(cases)} skip-dir cases passed"


def test_7_dry_run_subprocess():
    """Running --dry-run completes successfully (exit 0)."""
    if not GENERATOR_SCRIPT.exists():
        return False, "generator script missing"

    try:
        result = subprocess.run(
            [sys.executable, str(GENERATOR_SCRIPT), "--dry-run"],
            capture_output=True,
            text=True,
            encoding="utf-8",  # M67: Persian-safe
            errors="replace",
            timeout=60,
            cwd=str(REPO_ROOT),
        )
    except subprocess.TimeoutExpired:
        return False, "generator timed out (>60s)"
    except Exception as e:
        return False, f"subprocess failed: {e}"

    if result.returncode != 0:
        return False, f"--dry-run exited {result.returncode}: stderr={result.stderr[:200]}"

    stdout = result.stdout or ""

    # Verify expected output markers
    required_markers = [
        "PROJECT_MANIFEST Generator",
        "Scan complete",
        "Per-tier counts",
        "T1",
        "T2",
        "T3",
        "T4.1",
        "T4.2",
        "[DRY-RUN] No file written",
    ]
    missing = [marker for marker in required_markers if marker not in stdout]
    if missing:
        return False, f"--dry-run output missing markers: {missing}"

    # Verify no file was actually written (manifest mtime should be same or non-existent)
    # We don't have a strong check here without snapshotting before; trust the marker.

    return True, "--dry-run executed cleanly with expected output markers"


def test_8_help_output():
    """--help works without error."""
    if not GENERATOR_SCRIPT.exists():
        return False, "generator script missing"

    try:
        result = subprocess.run(
            [sys.executable, str(GENERATOR_SCRIPT), "--help"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
            cwd=str(REPO_ROOT),
        )
    except Exception as e:
        return False, f"subprocess failed: {e}"

    if result.returncode != 0:
        return False, f"--help exited {result.returncode}: stderr={result.stderr[:200]}"

    stdout = result.stdout or ""
    if "dry-run" not in stdout or "verbose" not in stdout:
        return False, "--help output missing expected flags (--dry-run, --verbose)"

    return True, "--help output contains expected flags"


# =============================================================================
# Main
# =============================================================================

ALL_TESTS = [
    ("test_1_script_imports", test_1_script_imports),
    ("test_2_constants_valid", test_2_constants_valid),
    ("test_3_glob_segment_based", test_3_glob_segment_based),
    ("test_4_classify_priority_order", test_4_classify_priority_order),
    ("test_5_classify_no_match", test_5_classify_no_match),
    ("test_6_should_skip_dir", test_6_should_skip_dir),
    ("test_7_dry_run_subprocess", test_7_dry_run_subprocess),
    ("test_8_help_output", test_8_help_output),
]


def main():
    print("Test Suite: 64b_test_manifest")
    print("=" * 64)
    print(f"Target: {GENERATOR_SCRIPT}")
    print(f"Total tests: {len(ALL_TESTS)}")
    print()

    passed = 0
    failed = 0
    results = []

    for test_name, test_fn in ALL_TESTS:
        try:
            ok, msg = test_fn()
        except Exception as e:
            ok = False
            msg = f"test raised exception: {e}"

        status = "PASS" if ok else "FAIL"
        results.append((test_name, ok, msg))
        print(f"  [{status}] {test_name}")
        print(f"         {msg}")
        print()

        if ok:
            passed += 1
        else:
            failed += 1

    print("=" * 64)
    print(f"Results: {passed} passed, {failed} failed (of {len(ALL_TESTS)})")

    if failed == 0:
        print("All tests passed [OK]")
        return 0
    else:
        print(f"{failed} test(s) FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
