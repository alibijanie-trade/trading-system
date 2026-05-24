# -*- coding: utf-8 -*-
"""
Pre-commit Audit Script (Layer 1) - Constitution v2.14

Purpose: Documentation consistency check before each commit.

Coverage of M-rules (lessons):
    M71 - HEAD Self-Reference Paradox       -> check_5
    M72 - End-of-Chat Verification          -> all checks
    M73 - Cross-Document Consistency        -> checks 1, 2, 7
    M74 - Full-Range Decision Audit         -> check_3
    M75 - Within-File Consistency           -> checks 1, 2, 6
    M77 - HEAD Never Hardcode               -> check_5
    M79 - Reserved IDs Explicit             -> check_4

Usage:
    python scripts/63_pre_commit_audit.py
    python scripts/63_pre_commit_audit.py --verbose
    python scripts/63_pre_commit_audit.py --check 5

Exit codes:
    0 - all checks passed
    1 - one or more checks failed
"""

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, List

# Force UTF-8 stdout on Windows (Rule #46)
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# =============================================================================
# Constants
# =============================================================================

# Persian/Arabic-Indic digits -> ASCII conversion (Rule #46 compliance)
PERSIAN_TO_ASCII = str.maketrans(
    "\u06f0\u06f1\u06f2\u06f3\u06f4\u06f5\u06f6\u06f7\u06f8\u06f9", "0123456789"
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS = REPO_ROOT / "docs"
CONSTITUTION = DOCS / "constitution"
ARCHIVE = CONSTITUTION / "archive"

# Files containing the modular constitution
MAIN_MD = CONSTITUTION / "main.md"
RULES_MD = CONSTITUTION / "01_rules.md"
LESSONS_MD = CONSTITUTION / "02_lessons.md"
BUGS_MD = CONSTITUTION / "03_bugs.md"
PRINCIPLES_MD = CONSTITUTION / "04_principles.md"
ARCH_MD = CONSTITUTION / "05_architecture.md"
META_MD = CONSTITUTION / "06_meta.md"

MODULAR_FILES = [MAIN_MD, RULES_MD, LESSONS_MD, BUGS_MD, PRINCIPLES_MD, ARCH_MD, META_MD]

SESSION_STATUS_MD = DOCS / "SESSION_STATUS.md"
DECISIONS_LOG_MD = DOCS / "DECISIONS_LOG.md"
PENDING_MD = DOCS / "PENDING_FOR_NEXT_VERSION.md"

# Reserved M-IDs (must be explicitly marked in 02_lessons.md)
RESERVED_LESSON_IDS = {22, 24, 29}
RESERVED_LESSON_IDS.update(range(32, 44))  # M32-M43
RESERVED_LESSON_IDS.update(range(45, 56))  # M45-M55
RESERVED_LESSON_IDS.add(80)
RESERVED_LESSON_IDS.add(81)
RESERVED_LESSON_IDS.update(range(89, 93))  # M89-M92 v2.14

# Reserved rule IDs
RESERVED_RULE_IDS = {52, 53}

# Current active version of Constitution + acceptable versions in module headers.
# Module headers may reference previous (v2.13) or current (v2.14).
# Both are valid - check_6 accepts any version in ACCEPTABLE_VERSIONS.
CURRENT_VERSION = "v2.14"
ACCEPTABLE_VERSIONS = ["v2.13", "v2.14"]

# Git hash pattern: 7-40 hex chars
GIT_HASH_PATTERN = re.compile(r"\b[a-f0-9]{7,40}\b")

# Allowed placeholder patterns for HEAD (do NOT flag these)
ALLOWED_HEAD_PLACEHOLDERS = [
    "<git log -1",
    "<HEAD>",
    "<git log",
    "git log -1 --format=%h",
    "HEAD-1",
]

# Known non-hash strings that look like git hashes (false positives)
# Add 7+ char hex-like strings that are NOT git hashes
KNOWN_NON_HASHES = {
    "ed25519",  # SSH key type
    "ed448",  # SSH key type
    "ecdsa",  # SSH key type
    "deadbeef",  # common placeholder
    "cafebabe",  # common placeholder
    "facade0",  # common placeholder
    "feedface",  # common placeholder
}

# Context substrings that mark legitimate non-HEAD hash references
# (e.g. Alembic migration heads which look like git hashes but aren't)
CONTEXT_EXEMPTIONS = [
    "Migration head",
    "migration head",
    "Alembic",
    "alembic",
    "ssh-keygen",
    "SSH key",
]

# Files where git hashes are EXPECTED (historical record - skip check_5 for these)
FILES_WHERE_HASHES_OK = {
    "CHAT_LOG.md",
    "CHANGELOG.md",
    "SESSION_STATUS.md",  # documents Git HEAD references
}


# =============================================================================
# Helpers
# =============================================================================


def to_ascii_digits(text: str) -> str:
    """Convert Persian/Arabic-Indic digits to ASCII digits."""
    return text.translate(PERSIAN_TO_ASCII)


def safe_read(path: Path) -> str:
    """Read file with UTF-8 encoding, return empty string if missing."""
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  WARN: failed to read {path}: {e}")
        return ""


@dataclass
class CheckResult:
    """Result of a single audit check."""

    name: str
    passed: bool
    message: str
    details: List[str] = field(default_factory=list)


# =============================================================================
# CHECK 1: Rule counts consistency
# =============================================================================


def check_1_rule_counts() -> CheckResult:
    """
    Verify Locked rule count is consistent across:
      - 01_rules.md: count table rows in section 1.9
      - main.md: number after "qowanin Locked" stat
      - SESSION_STATUS.md: number after "qowanin qoflshode"

    All three must match.
    """
    name = "check_1_rule_counts"
    details: List[str] = []

    # Count rule rows in 01_rules.md section 1.9 table
    rules_text = safe_read(RULES_MD)
    if not rules_text:
        return CheckResult(name, False, "01_rules.md not found or empty", [])

    rules_ascii = to_ascii_digits(rules_text)

    # Find section 1.9 boundaries (the rule table section)
    # Pattern: table rows start with "| **N |" or "| N |" where N is a number
    # We look ONLY in section 1.9 (between its header and next "---" or section)
    section_match = re.search(
        r"##\s*1\.9[^\n]*\n(.*?)(?=^##\s|\Z)",
        rules_ascii,
        re.DOTALL | re.MULTILINE,
    )

    if not section_match:
        return CheckResult(name, False, "section 1.9 not found in 01_rules.md", [])

    section_text = section_match.group(1)

    # Match table rows: "| <number> |" or "| **<number>" at line start
    row_pattern = re.compile(r"^\|\s*\*?\*?\s*(\d+)\b", re.MULTILINE)
    rule_ids = sorted(int(m.group(1)) for m in row_pattern.finditer(section_text))

    if not rule_ids:
        return CheckResult(name, False, "no rule rows found in section 1.9 table", [])

    count_in_rules = len(rule_ids)
    max_rule_id = max(rule_ids)
    details.append(f"01_rules.md: {count_in_rules} rules in table (max ID: {max_rule_id})")

    # Find count in main.md stats
    main_text = to_ascii_digits(safe_read(MAIN_MD))
    main_match = re.search(r"qowanin\s+Locked|Locked\s*\|\s*(\d+)", main_text, re.IGNORECASE)
    # Above is non-Persian; use a more robust pattern
    main_match = re.search(r"\|\s*(\d+)\s+sabt", main_text)  # "N sabt-shode"
    main_count = None
    if main_match:
        main_count = int(main_match.group(1))
        details.append(f"main.md stats: {main_count}")

    # Find count in SESSION_STATUS.md
    session_text = to_ascii_digits(safe_read(SESSION_STATUS_MD))
    # Pattern: "qowanin qoflshode:** **N**" - in ASCII after translation: number between **
    session_match = re.search(r"qoflshode[^*]*\*\*(\d+)\*\*", session_text)
    if not session_match:
        # Try simpler pattern for the bold number after the label
        session_match = re.search(r"Locked[^*\n]*\*\*(\d+)\*\*", session_text)
    session_count = None
    if session_match:
        session_count = int(session_match.group(1))
        details.append(f"SESSION_STATUS.md: {session_count}")

    # Compare
    discrepancies = []
    if main_count is not None and main_count != count_in_rules:
        discrepancies.append(f"main.md ({main_count}) != 01_rules.md ({count_in_rules})")
    if session_count is not None and session_count != count_in_rules:
        discrepancies.append(
            f"SESSION_STATUS.md ({session_count}) != 01_rules.md ({count_in_rules})"
        )

    if discrepancies:
        return CheckResult(name, False, "rule count drift detected", details + discrepancies)

    return CheckResult(name, True, f"rule counts consistent ({count_in_rules} rules)", details)


# =============================================================================
# CHECK 2: Lesson counts consistency
# =============================================================================


def check_2_lesson_counts() -> CheckResult:
    """
    Verify lesson count is consistent across 02_lessons.md, main.md, SESSION_STATUS.md.
    """
    name = "check_2_lesson_counts"
    details: List[str] = []

    lessons_text = to_ascii_digits(safe_read(LESSONS_MD))
    if not lessons_text:
        return CheckResult(name, False, "02_lessons.md not found", [])

    # Find all M{N} or M{N}-M{M} entries
    # Match both:
    #   - table rows: "| **M64** |"
    #   - bullets:    "- **M64** Description"
    #   - ranges:     "**M32-M43**", "**M80, M81**"
    # Pattern matches **M<num>** with optional range/pair
    lesson_pattern = re.compile(
        r"\*\*M(\d+)(?:\s*[-,]\s*M?(\d+))?\*\*",
        re.IGNORECASE,
    )
    found_ids = set()
    for m in lesson_pattern.finditer(lessons_text):
        start = int(m.group(1))
        end = int(m.group(2)) if m.group(2) else start
        for i in range(start, end + 1):
            found_ids.add(i)
    # Also catch "**M80, M81**" pair pattern (two separate IDs in one bold)
    pair_pattern = re.compile(r"\*\*M(\d+),\s*M(\d+)\*\*", re.IGNORECASE)
    for m in pair_pattern.finditer(lessons_text):
        found_ids.add(int(m.group(1)))
        found_ids.add(int(m.group(2)))

    if not found_ids:
        return CheckResult(name, False, "no lesson entries found in 02_lessons.md", [])

    max_lesson_id = max(found_ids)
    count_in_lessons = len(found_ids)
    details.append(f"02_lessons.md: {count_in_lessons} lesson IDs found, max M{max_lesson_id}")

    # Quick sanity: max should be at least 86 (M1-M86)
    if max_lesson_id < 86:
        details.append(f"WARNING: max lesson ID {max_lesson_id} is below expected M86")

    # main.md should mention M1-M{N}
    main_text = to_ascii_digits(safe_read(MAIN_MD))
    main_match = re.search(r"M1-M(\d+)", main_text)
    if main_match:
        main_max = int(main_match.group(1))
        details.append(f"main.md: M1-M{main_max}")
        if main_max != max_lesson_id:
            return CheckResult(
                name,
                False,
                "lesson max ID drift",
                details
                + [f"main.md says M1-M{main_max} but 02_lessons.md goes to M{max_lesson_id}"],
            )

    # SESSION_STATUS.md
    session_text = to_ascii_digits(safe_read(SESSION_STATUS_MD))
    session_match = re.search(r"M1-M(\d+)", session_text)
    if session_match:
        session_max = int(session_match.group(1))
        details.append(f"SESSION_STATUS.md: M1-M{session_max}")
        if session_max != max_lesson_id:
            return CheckResult(
                name,
                False,
                "lesson max ID drift",
                details
                + [
                    f"SESSION_STATUS.md says M1-M{session_max} but 02_lessons.md goes to M{max_lesson_id}"
                ],
            )

    return CheckResult(name, True, f"lesson counts consistent (M1-M{max_lesson_id})", details)


# =============================================================================
# CHECK 3: Decision Max ID
# =============================================================================


def check_3_decision_max_id() -> CheckResult:
    """
    Verify DECISIONS_LOG.md has consistent numbering:
      - Find max decision ID
      - Verify it matches "Max ID" stated in SESSION_STATUS.md if present
    """
    name = "check_3_decision_max_id"
    details: List[str] = []

    log_text = to_ascii_digits(safe_read(DECISIONS_LOG_MD))
    if not log_text:
        return CheckResult(name, True, "DECISIONS_LOG.md not found (skipping)", [])

    # Find all decision IDs - look for patterns like:
    #   "## Decision #N", "### #N", "## #N", "#N:", "Decision N"
    id_pattern = re.compile(r"(?:Decision\s*#?|##+\s*#)(\d+)\b", re.IGNORECASE)
    found_ids = set(int(m.group(1)) for m in id_pattern.finditer(log_text))

    if not found_ids:
        return CheckResult(name, True, "no decision IDs found (skipping)", [])

    max_id = max(found_ids)
    count = len(found_ids)
    details.append(f"DECISIONS_LOG.md: Max ID = {max_id}, Recorded count = {count}")

    # Check SESSION_STATUS.md for stated Max ID
    session_text = to_ascii_digits(safe_read(SESSION_STATUS_MD))
    stated_max = re.search(r"Max\s+ID\s*=?\s*(\d+)", session_text, re.IGNORECASE)
    if stated_max:
        stated = int(stated_max.group(1))
        details.append(f"SESSION_STATUS.md stated Max ID: {stated}")
        if stated != max_id:
            return CheckResult(
                name,
                False,
                "Decision Max ID drift",
                details + [f"SESSION_STATUS says Max={stated} but DECISIONS_LOG has Max={max_id}"],
            )

    return CheckResult(name, True, f"Decision Max ID consistent ({max_id})", details)


# =============================================================================
# CHECK 4: Reserved IDs explicit
# =============================================================================


def check_4_reserved_ids_explicit() -> CheckResult:
    """
    Verify each reserved M-ID is explicitly marked in 02_lessons.md.
    Mark = the lesson row mentions "Reserved" near the M-ID.
    """
    name = "check_4_reserved_ids_explicit"
    details: List[str] = []

    lessons_text = to_ascii_digits(safe_read(LESSONS_MD))
    if not lessons_text:
        return CheckResult(name, False, "02_lessons.md not found", [])

    # Extract all rows that look like "| **M<id>** | Reserved..."
    # Or ranges like "**M32-M43** | Reserved..."
    reserved_in_doc = set()

    # Pattern for single reserved
    single_pattern = re.compile(
        r"\*\*?M(\d+)\*?\*?\s*\|.*Reserved",
        re.IGNORECASE,
    )
    for m in single_pattern.finditer(lessons_text):
        reserved_in_doc.add(int(m.group(1)))

    # Pattern for ranges
    range_pattern = re.compile(
        r"\*\*?M(\d+)-M?(\d+)\*?\*?\s*\|.*Reserved",
        re.IGNORECASE,
    )
    for m in range_pattern.finditer(lessons_text):
        start = int(m.group(1))
        end = int(m.group(2))
        for i in range(start, end + 1):
            reserved_in_doc.add(i)

    # Also accept entries like "**M80, M81** ... Reserved"
    pair_pattern = re.compile(
        r"\*\*?M(\d+),\s*M(\d+)\*?\*?[^|]*Reserved",
        re.IGNORECASE,
    )
    for m in pair_pattern.finditer(lessons_text):
        reserved_in_doc.add(int(m.group(1)))
        reserved_in_doc.add(int(m.group(2)))

    # Expected reserved IDs
    missing = RESERVED_LESSON_IDS - reserved_in_doc
    extra = reserved_in_doc - RESERVED_LESSON_IDS

    details.append(
        f"Expected {len(RESERVED_LESSON_IDS)} reserved IDs, found {len(reserved_in_doc)} marked"
    )

    if missing:
        return CheckResult(
            name,
            False,
            "Reserved IDs missing explicit mark",
            details + [f"Missing 'Reserved' mark for: M{sorted(missing)}"],
        )

    if extra:
        # Extra is not necessarily an error but noteworthy
        details.append(f"Extra Reserved IDs marked (not in expected list): M{sorted(extra)}")

    return CheckResult(name, True, "all Reserved IDs explicitly marked", details)


# =============================================================================
# CHECK 5: HEAD hash not hardcoded
# =============================================================================


def check_5_head_hardcode() -> CheckResult:
    """
    Scan modular constitution files for hardcoded git hashes (M77).
    Allowed: placeholders like "<git log -1 ...>"
    Skip: files documenting commits historically (CHAT_LOG, CHANGELOG, SESSION_STATUS)
    """
    name = "check_5_head_hardcode"
    details: List[str] = []

    files_to_scan = MODULAR_FILES.copy()
    violations: List[str] = []

    for fpath in files_to_scan:
        if not fpath.exists():
            continue

        text = fpath.read_text(encoding="utf-8")
        # Find all hashes
        for m in GIT_HASH_PATTERN.finditer(text):
            hash_str = m.group(0)
            # Skip known non-hashes (ed25519, etc.)
            if hash_str.lower() in KNOWN_NON_HASHES:
                continue
            # Get wider context (100 chars around) for exemption check
            start = max(0, m.start() - 100)
            end = min(len(text), m.end() + 100)
            context = text[start:end]

            # Skip if hash is inside an allowed placeholder pattern
            if any(placeholder in context for placeholder in ALLOWED_HEAD_PLACEHOLDERS):
                continue

            # Skip if context indicates legitimate non-HEAD reference
            # (Alembic migration head, SSH key type, etc.)
            if any(exemption in context for exemption in CONTEXT_EXEMPTIONS):
                continue

            violations.append(
                f"{fpath.name}: hash '{hash_str}' at char {m.start()} - context: ...{context.strip()[:80]}..."
            )

    details.append(f"Scanned {len(files_to_scan)} modular files")
    details.append(f"Allowed placeholder patterns: {ALLOWED_HEAD_PLACEHOLDERS}")

    if violations:
        return CheckResult(
            name,
            False,
            f"{len(violations)} hardcoded git hash(es) found in modular files",
            details + violations[:10],  # show first 10
        )

    return CheckResult(name, True, "no hardcoded git hashes in modular files", details)


# =============================================================================
# CHECK 6: Version consistency
# =============================================================================


def check_6_version_consistency() -> CheckResult:
    """
    Verify all modular constitution files reference an acceptable version.
    Each file's header section (first 30 lines) should mention one of ACCEPTABLE_VERSIONS.
    Module headers may reference structural version (v2.12 Modular) or current (v2.13).
    """
    name = "check_6_version_consistency"
    details: List[str] = []

    missing_version: List[str] = []

    for fpath in MODULAR_FILES:
        if not fpath.exists():
            continue

        # Read first 30 lines (header section)
        with fpath.open("r", encoding="utf-8") as f:
            header = "".join(f.readline() for _ in range(30))

        # Accept if ANY of the acceptable versions appears in header
        if not any(v in header for v in ACCEPTABLE_VERSIONS):
            missing_version.append(fpath.name)

    details.append(
        f"Checked {len(MODULAR_FILES)} modular files for any of {ACCEPTABLE_VERSIONS} in header"
    )

    if missing_version:
        return CheckResult(
            name,
            False,
            f"{len(missing_version)} file(s) missing acceptable version in header",
            details + [f"Missing: {f}" for f in missing_version],
        )

    return CheckResult(
        name,
        True,
        f"all modular files reference acceptable version ({ACCEPTABLE_VERSIONS})",
        details,
    )


# =============================================================================
# CHECK 7: PENDING count
# =============================================================================


def check_7_pending_count() -> CheckResult:
    """
    Verify PENDING_FOR_NEXT_VERSION.md item count matches its own stated total.
    """
    name = "check_7_pending_count"
    details: List[str] = []

    pending_text = to_ascii_digits(safe_read(PENDING_MD))
    if not pending_text:
        return CheckResult(name, True, "PENDING_FOR_NEXT_VERSION.md not found (skipping)", [])

    # Count Z2.N items
    item_pattern = re.compile(r"\|\s*\*\*Z2\.(\d+)\*\*", re.IGNORECASE)
    found_ids = set(int(m.group(1)) for m in item_pattern.finditer(pending_text))

    actual_count = len(found_ids)
    max_id = max(found_ids) if found_ids else 0
    details.append(f"PENDING: {actual_count} items found, max Z2.{max_id}")

    # Look for stated total
    stated_match = re.search(r"te'?dad[^\n]*?(\d+)\s*ay?tom", pending_text, re.IGNORECASE)
    # If no Persian-translated match, try direct count statement
    if not stated_match:
        stated_match = re.search(r"\*\*(\d+)\*\*\s+ay?tom", pending_text)

    if not stated_match:
        # Allow this - stated count may not be in machine-parseable form
        return CheckResult(
            name, True, f"PENDING has {actual_count} items (stated total not parsed)", details
        )

    stated = int(stated_match.group(1))
    details.append(f"Stated total: {stated}")

    if stated != actual_count:
        return CheckResult(
            name,
            False,
            "PENDING count drift",
            details + [f"Stated {stated} items but found {actual_count}"],
        )

    return CheckResult(name, True, f"PENDING count consistent ({actual_count} items)", details)


# =============================================================================
# Main runner
# =============================================================================

ALL_CHECKS: List[Callable[[], CheckResult]] = [
    check_1_rule_counts,
    check_2_lesson_counts,
    check_3_decision_max_id,
    check_4_reserved_ids_explicit,
    check_5_head_hardcode,
    check_6_version_consistency,
    check_7_pending_count,
]


def main():
    parser = argparse.ArgumentParser(
        description="Pre-commit Audit (Layer 1) for Constitution v2.14",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Show details for passing checks too"
    )
    parser.add_argument(
        "--check",
        type=int,
        default=0,
        help="Run only check N (1-7); default 0 = run all",
    )
    args = parser.parse_args()

    if args.check:
        if not (1 <= args.check <= len(ALL_CHECKS)):
            print(f"ERROR: --check must be 1-{len(ALL_CHECKS)}")
            return 2
        checks_to_run = [ALL_CHECKS[args.check - 1]]
    else:
        checks_to_run = ALL_CHECKS

    print("Pre-commit Audit (Layer 1) - Constitution v2.14")
    print("=" * 60)
    print(f"Repo root: {REPO_ROOT}")
    print(f"Running {len(checks_to_run)} check(s)...")
    print()

    results = []
    for check_fn in checks_to_run:
        try:
            result = check_fn()
        except Exception as e:
            result = CheckResult(check_fn.__name__, False, f"check raised exception: {e}", [])
        results.append(result)

    # Print results
    print("-" * 60)
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        marker = "[" + status + "]"
        print(f"  {marker} {r.name}")
        print(f"        {r.message}")
        if (not r.passed) or args.verbose:
            for d in r.details:
                print(f"          - {d}")
        print()

    # Summary
    passed_count = sum(1 for r in results if r.passed)
    total = len(results)
    print("=" * 60)
    if passed_count == total:
        print(f"Result: ALL {total} CHECK(S) PASSED [OK]")
        return 0
    else:
        print(
            f"Result: {passed_count}/{total} passed - {total - passed_count} FAILED [BLOCK COMMIT]"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
