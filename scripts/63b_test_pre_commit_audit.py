# -*- coding: utf-8 -*-
"""
Test Script for 63_pre_commit_audit.py

Per Rule #22: every {N}_*.py must have {N}b_test_*.py companion.

Tests:
    test_1_script_imports          - audit script imports without error
    test_2_all_check_functions     - all 13 check functions exist and callable
    test_3_run_on_real_project     - audit run on real project state (info only)
    test_4_persian_digit_translation - to_ascii_digits() works
    test_5_constants_valid         - all path constants resolve
    test_6_reserved_lesson_ids     - RESERVED_LESSON_IDS set is correct (32 IDs)
    test_7_help_output             - --help works (CLI sanity)
    test_8_check_8_runs            - check_8 (uncommitted state files) runs
    test_9_check_9_runs            - check_9 (manifest self-row) runs
    test_10_check_10_runs          - check_10 (Review numbering) runs
    test_11_check_11_runs          - check_11 (Z-ID permanence) runs
    test_12_check_12_runs          - check_12 (continuity chain) runs
    test_13_check_12_logic         - check_12 returns PASS on current healthy chain
    test_14_check_1_logic          - check_1 passes AND extracts main+session counts (F-B guard)
    test_15_check_13_runs          - check_13 (Review LOG<->file integrity) runs
    test_16_check_13_logic         - check_13 returns PASS on current healthy state

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
AUDIT_SCRIPT = THIS_DIR / "63_pre_commit_audit.py"
REPO_ROOT = THIS_DIR.parent


def load_audit_module():
    """Dynamically load the audit script as a module."""
    spec = importlib.util.spec_from_file_location("audit", str(AUDIT_SCRIPT))
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {AUDIT_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# =============================================================================
# Tests
# =============================================================================


def test_1_script_imports():
    """Audit script imports without syntax errors."""
    if not AUDIT_SCRIPT.exists():
        return False, f"audit script not found: {AUDIT_SCRIPT}"
    try:
        load_audit_module()
        return True, "audit script imports cleanly"
    except Exception as e:
        return False, f"import failed: {e}"


def test_2_all_check_functions():
    """All 13 check functions are exported and callable."""
    expected_names = [
        "check_1_rule_counts",
        "check_2_lesson_counts",
        "check_3_decision_max_id",
        "check_4_reserved_ids_explicit",
        "check_5_head_hardcode",
        "check_6_version_consistency",
        "check_7_pending_count",
        "check_8_uncommitted_state_files",
        "check_9_manifest_self_row",
        "check_10_review_numbering",
        "check_11_z_id_permanence",
        "check_12_continuity",
        "check_13_review_file_integrity",
    ]
    try:
        module = load_audit_module()
    except Exception as e:
        return False, f"cannot load module: {e}"

    missing = []
    for fname in expected_names:
        fn = getattr(module, fname, None)
        if fn is None:
            missing.append(fname + " (missing)")
        elif not callable(fn):
            missing.append(fname + " (not callable)")

    if missing:
        return False, f"problems: {missing}"

    # Also verify ALL_CHECKS list contains exactly 13 items
    all_checks = getattr(module, "ALL_CHECKS", None)
    if all_checks is None:
        return False, "ALL_CHECKS list not exported"
    if len(all_checks) != 13:
        return False, f"ALL_CHECKS has {len(all_checks)} items, expected 13"

    return True, "all 13 check functions present and callable"


def test_3_run_on_real_project():
    """
    Run the audit script as subprocess against real project.
    This is INFORMATIONAL - we report results but don't fail the test if
    some checks fail (real drift may exist; that is what the audit is for).
    """
    if not AUDIT_SCRIPT.exists():
        return False, "audit script missing"

    try:
        result = subprocess.run(
            [sys.executable, str(AUDIT_SCRIPT)],
            capture_output=True,
            text=True,
            encoding="utf-8",  # M67: avoid cp1252 crash on Persian output
            errors="replace",  # safety net for any decode issue
            timeout=30,
            cwd=str(REPO_ROOT),
        )
    except subprocess.TimeoutExpired:
        return False, "audit script timed out (>30s)"
    except Exception as e:
        return False, f"subprocess failed: {e}"

    # Report what we found
    info = []
    info.append(f"exit code: {result.returncode}")

    # stdout may be None if subprocess failed weirdly - defensive
    stdout = result.stdout or ""
    # Count PASS / FAIL in output
    pass_count = stdout.count("[PASS]")
    fail_count = stdout.count("[FAIL]")
    info.append(f"PASS: {pass_count}, FAIL: {fail_count}")

    # Test succeeds if script ran (returncode 0 or 1, not 2 or crash)
    if result.returncode not in (0, 1):
        return (
            False,
            f"audit exited with unexpected code {result.returncode}: {result.stderr[:200]}",
        )

    return True, "audit ran successfully (" + ", ".join(info) + ")"


def test_4_persian_digit_translation():
    """to_ascii_digits() correctly converts Persian to ASCII."""
    try:
        module = load_audit_module()
    except Exception as e:
        return False, f"cannot load module: {e}"

    fn = getattr(module, "to_ascii_digits", None)
    if fn is None:
        return False, "to_ascii_digits not exported"

    # Test cases (Persian numerals -> ASCII)
    test_cases = [
        ("\u06f1\u06f2\u06f3", "123"),  # 123
        ("\u06f6\u06f6", "66"),  # 66 (rule count)
        ("v\u06f2.\u06f1\u06f2", "v2.12"),  # version
        ("plain ASCII 123", "plain ASCII 123"),  # passthrough
        ("", ""),  # empty
    ]

    for src, expected in test_cases:
        got = fn(src)
        if got != expected:
            return False, f"to_ascii_digits('{src}') = '{got}', expected '{expected}'"

    return True, f"all {len(test_cases)} translation cases passed"


def test_5_constants_valid():
    """All path constants point to existing files (or are parent dirs of valid files)."""
    try:
        module = load_audit_module()
    except Exception as e:
        return False, f"cannot load module: {e}"

    # Files that MUST exist (the modular constitution)
    required_files = [
        "MAIN_MD",
        "RULES_MD",
        "LESSONS_MD",
        "BUGS_MD",
        "PRINCIPLES_MD",
        "ARCH_MD",
        "META_MD",
    ]

    missing = []
    for const_name in required_files:
        path = getattr(module, const_name, None)
        if path is None:
            missing.append(f"{const_name} (constant not defined)")
        elif not Path(path).exists():
            missing.append(f"{const_name} ({path}) - file not found")

    if missing:
        return False, f"missing: {missing}"

    return True, f"all {len(required_files)} required modular files exist"


def test_6_reserved_lesson_ids():
    """RESERVED_LESSON_IDS contains the expected 32 IDs (post-S3.3 + M89-M92 v2.14)."""
    try:
        module = load_audit_module()
    except Exception as e:
        return False, f"cannot load module: {e}"

    reserved = getattr(module, "RESERVED_LESSON_IDS", None)
    if reserved is None:
        return False, "RESERVED_LESSON_IDS not exported"

    expected = {22, 24, 29, 80, 81}
    expected.update(range(32, 44))  # M32-M43 = 12 IDs
    expected.update(range(45, 56))  # M45-M55 = 11 IDs
    expected.update(range(89, 93))  # M89-M92 = 4 IDs (v2.14 S3.3)

    if reserved != expected:
        diff_missing = expected - reserved
        diff_extra = reserved - expected
        return False, f"mismatch - missing: {sorted(diff_missing)}, extra: {sorted(diff_extra)}"

    if len(reserved) != 32:
        return False, f"expected 32 IDs, got {len(reserved)}"

    return True, "RESERVED_LESSON_IDS contains all 32 expected IDs"


def test_7_help_output():
    """--help works without error."""
    try:
        result = subprocess.run(
            [sys.executable, str(AUDIT_SCRIPT), "--help"],
            capture_output=True,
            text=True,
            encoding="utf-8",  # M67: avoid cp1252 crash
            errors="replace",
            timeout=10,
            cwd=str(REPO_ROOT),
        )
    except Exception as e:
        return False, f"subprocess failed: {e}"

    if result.returncode != 0:
        return False, f"--help exited {result.returncode}: {result.stderr[:200]}"

    if "verbose" not in result.stdout or "check" not in result.stdout:
        return False, "--help output missing expected flags"

    return True, "--help output looks correct"


# =============================================================================
# Helper for check-specific tests (DRY pattern)
# =============================================================================


def _run_specific_check(check_num: int) -> tuple:
    """Helper: run audit script with --check N and verify no crash."""
    try:
        result = subprocess.run(
            [sys.executable, str(AUDIT_SCRIPT), "--check", str(check_num)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
            cwd=str(REPO_ROOT),
        )
    except subprocess.TimeoutExpired:
        return False, f"check_{check_num} timed out (>30s)"
    except Exception as e:
        return False, f"subprocess failed: {e}"

    if result.returncode not in (0, 1):
        return False, (
            f"check_{check_num} exited {result.returncode}: " f"{(result.stderr or '')[:200]}"
        )

    return True, f"check_{check_num} ran cleanly (exit={result.returncode})"


def test_8_check_8_runs():
    """check_8 (uncommitted state files, M93) runs without crash."""
    return _run_specific_check(8)


def test_9_check_9_runs():
    """check_9 (manifest self-row, Z3.15) runs without crash."""
    return _run_specific_check(9)


def test_10_check_10_runs():
    """check_10 (Review numbering, Z3.16) runs without crash."""
    return _run_specific_check(10)


def test_11_check_11_runs():
    """check_11 (Z-ID permanence, Rule #74) runs without crash."""
    return _run_specific_check(11)


def test_12_check_12_runs():
    """check_12 (continuity chain, Rule #62/M23/M101) runs without crash."""
    return _run_specific_check(12)


def test_13_check_12_logic():
    """
    check_12_continuity() returns PASS on the current (healthy) chain.
    The two-loop invariant (handoff == ledger + 1) holds for any healthy
    state, so this is a stable regression guard, not a state-brittle test.
    """
    try:
        module = load_audit_module()
    except Exception as e:
        return False, f"cannot load module: {e}"

    fn = getattr(module, "check_12_continuity", None)
    if fn is None:
        return False, "check_12_continuity not exported"

    try:
        result = fn()
    except Exception as e:
        return False, f"check_12_continuity raised: {e}"

    if not getattr(result, "passed", False):
        return False, f"check_12 not green on current chain: {getattr(result, 'message', '?')}"

    return True, f"check_12 green on current chain ({result.message})"


def test_14_check_1_logic():
    """
    check_1 (rule counts) passes AND actually extracts the main.md + SESSION_STATUS
    counts (proven via details), not just count_in_rules. Guards against the F-B
    regression where transliteration mismatch left both counts None -> false-PASS.
    """
    try:
        module = load_audit_module()
    except Exception as e:
        return False, f"cannot load module: {e}"

    fn = getattr(module, "check_1_rule_counts", None)
    if fn is None:
        return False, "check_1_rule_counts not exported"

    try:
        result = fn()
    except Exception as e:
        return False, f"check_1_rule_counts raised: {e}"

    if not getattr(result, "passed", False):
        return False, f"check_1 not green: {getattr(result, 'message', '?')}"

    joined = " | ".join(result.details)
    if "main.md stats:" not in joined:
        return False, "check_1 did not extract main.md count (F-B regression?)"
    if "SESSION_STATUS.md:" not in joined:
        return False, "check_1 did not extract SESSION_STATUS count (F-B regression?)"

    return True, f"check_1 green + both counts extracted ({result.message})"


def test_15_check_13_runs():
    """check_13 (Review LOG<->file integrity, REVIEW_PROTOCOL section 4) runs without crash."""
    return _run_specific_check(13)


def test_16_check_13_logic():
    """
    check_13_review_file_integrity() returns PASS on the current state: every
    REVIEW_LOG row has its docs/reviews file and vice versa (part19 backfill of
    #010/#011 closed the gap that motivated this check).
    """
    try:
        module = load_audit_module()
    except Exception as e:
        return False, f"cannot load module: {e}"

    fn = getattr(module, "check_13_review_file_integrity", None)
    if fn is None:
        return False, "check_13_review_file_integrity not exported"

    try:
        result = fn()
    except Exception as e:
        return False, f"check_13_review_file_integrity raised: {e}"

    if not getattr(result, "passed", False):
        return False, f"check_13 not green: {getattr(result, 'message', '?')}"

    return True, f"check_13 green ({result.message})"


# =============================================================================
# Main
# =============================================================================

ALL_TESTS = [
    ("test_1_script_imports", test_1_script_imports),
    ("test_2_all_check_functions", test_2_all_check_functions),
    ("test_3_run_on_real_project", test_3_run_on_real_project),
    ("test_4_persian_digit_translation", test_4_persian_digit_translation),
    ("test_5_constants_valid", test_5_constants_valid),
    ("test_6_reserved_lesson_ids", test_6_reserved_lesson_ids),
    ("test_7_help_output", test_7_help_output),
    ("test_8_check_8_runs", test_8_check_8_runs),
    ("test_9_check_9_runs", test_9_check_9_runs),
    ("test_10_check_10_runs", test_10_check_10_runs),
    ("test_11_check_11_runs", test_11_check_11_runs),
    ("test_12_check_12_runs", test_12_check_12_runs),
    ("test_13_check_12_logic", test_13_check_12_logic),
    ("test_14_check_1_logic", test_14_check_1_logic),
    ("test_15_check_13_runs", test_15_check_13_runs),
    ("test_16_check_13_logic", test_16_check_13_logic),
]


def main():
    print("Test Suite: 63b_test_pre_commit_audit")
    print("=" * 60)
    print(f"Target: {AUDIT_SCRIPT}")
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

    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed (of {len(ALL_TESTS)})")

    if failed == 0:
        print("All tests passed [OK]")
        return 0
    else:
        print(f"{failed} test(s) FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
