# -*- coding: utf-8 -*-
"""
scripts/64_generate_manifest.py - PROJECT_MANIFEST.md generator (D2 of MDRS v2)

Purpose:
    Scan the project filesystem and generate docs/PROJECT_MANIFEST.md
    as a Source-of-Truth index of all role-classified artifacts.

Core principle (Golden Rule):
    Tier classification is based on ROLE in the project,
    NOT on git tracking status. Some files in the manifest are
    gitignored (e.g., data/excel_imports/*.xlsx) but tracked here
    for drift detection.

Anti-Z3.8 (Hidden Regeneration Hazard):
    This generator does NOT hardcode content rows. Each row is built
    dynamically from filesystem walk. Only the SCAFFOLD/header is
    hardcoded. Manifest self-reference uses "<self>" placeholder.

Tier rules (priority order, first match wins):
    T1   - Constitution + State (live governance)
    T2   - Reference docs (stable governance, catch-all in docs/)
    T3   - Code (production)
    T4.1 - Config (Build/Compile/Runtime)
    T4.2 - Assets (External system persistent)
    -    - (no match) silent skip = effectively T5 EXCLUDED

Usage:
    python scripts/64_generate_manifest.py            # full generate
    python scripts/64_generate_manifest.py --dry-run  # report counts, no write
    python scripts/64_generate_manifest.py --verbose  # show each file during scan

Exit codes:
    0 - success
    1 - write error
    2 - argument error
"""

import argparse
import fnmatch
import hashlib
import os
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Force UTF-8 stdout on Windows (Rule #46)
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# =============================================================================
# Paths
# =============================================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
MANIFEST_PATH = PROJECT_ROOT / "docs" / "PROJECT_MANIFEST.md"


# =============================================================================
# Skip directories (never walk into these)
# =============================================================================

SKIP_DIRS = {
    # Python
    ".git",
    "venv",
    ".venv",
    "env",
    "ENV",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    # Node
    "node_modules",
    # IDE
    ".vscode",
    ".idea",
    # Build outputs
    "dist",
    "build",
    "htmlcov",
    "coverage",
    ".sync-backup",
    # Workspace (T5 by directory)
    "claude_workspace/zip_temp",
    "claude_workspace/screenshots",
    "claude_workspace/backups",
    "claude_workspace/old_versions",
    "claude_workspace/incoming_permanent",  # handoffs - transient
}


# =============================================================================
# Tier classification rules
# Patterns use glob semantics with segment-based matching:
#   *    matches a single path segment (no '/')
#   **   matches zero or more path segments
# First-match-wins in priority order: T1 -> T2 -> T3 -> T4.1 -> T4.2
# =============================================================================

# T1: Constitution + State (live governance)
T1_PATTERNS: List[str] = [
    "docs/constitution/*.md",
    "docs/constitution/archive/*.md",
    "docs/SESSION_STATUS.md",
    "docs/CLAUDE_CHECKLIST.md",
    "docs/DECISIONS_LOG.md",
    "docs/PENDING_FOR_NEXT_VERSION.md",
    "docs/PROJECT_GOVERNANCE.md",
    "docs/TASK_BACKLOG.md",
    "docs/CHAT_LOG.md",
    "docs/PROJECT_MANIFEST.md",
    "docs/PROJECT_CONSTITUTION.md",
    # Future S2 deliverables (planned MDRS v2):
    "docs/REVIEW_PROTOCOL.md",
    "docs/REVIEW_LOG.md",
    "docs/PRE_ADD_CHECKLIST.md",
    "docs/reviews/*.md",
    # Future S6 deliverables (planned MDRS v2):
    "docs/ISSUE_WORKFLOW.md",
    ".github/ISSUE_TEMPLATE/*.md",
]

# T2: Reference docs (stable governance, catch-all under docs/)
T2_PATTERNS: List[str] = [
    "docs/*.md",
]

# T3: Code (production)
T3_PATTERNS: List[str] = [
    "backend/main.py",
    "backend/app/**/*.py",
    "backend/tests/**/*.py",
    "backend/migrations/**/*.py",
    "backend/migrations/**/*.mako",
    "frontend/src/**/*.js",
    "frontend/src/**/*.jsx",
    "frontend/src/**/*.ts",
    "frontend/src/**/*.tsx",
    "frontend/src/**/*.css",
    "frontend/index.html",
    "scripts/**/*.py",
]

# T4.1: Config (Build/Compile/Runtime)
T4_1_PATTERNS: List[str] = [
    ".gitignore",
    ".gitattributes",
    ".pre-commit-config.yaml",
    "pyproject.toml",
    "backend/requirements.txt",
    "backend/alembic.ini",
    "backend/.env.example",
    "frontend/package.json",
    "frontend/vite.config.js",
    "frontend/eslint.config.js",
    "frontend/.env.example",
    "README.md",
    "CHANGELOG.md",
    # Future S7 deliverable:
    "VERSION",
]

# T4.2: Assets (External system persistent)
T4_2_PATTERNS: List[str] = [
    "data/excel_imports/*.xlsx",
    "data/excel_imports/*.xls",
    "claude_workspace/snapshots/*.md",
]

# Ordered tier rules: priority order matters
TIER_RULES: List[Tuple[str, List[str]]] = [
    ("T1", T1_PATTERNS),
    ("T2", T2_PATTERNS),
    ("T3", T3_PATTERNS),
    ("T4.1", T4_1_PATTERNS),
    ("T4.2", T4_2_PATTERNS),
]

# Display labels for tier sections in the manifest
TIER_LABELS: Dict[str, str] = {
    "T1": "Tier 1 -- Constitution + State (Live Governance)",
    "T2": "Tier 2 -- Reference Docs (Stable Governance)",
    "T3": "Tier 3 -- Code (Production)",
    "T4.1": "Tier 4.1 -- Config (Build/Compile/Runtime)",
    "T4.2": "Tier 4.2 -- Assets (External System Persistent)",
}


# =============================================================================
# Data structures
# =============================================================================


@dataclass
class FileEntry:
    """One row in the manifest output."""

    relpath: str  # POSIX-style relative path from PROJECT_ROOT
    tier: str  # T1, T2, T3, T4.1, or T4.2
    size_bytes: int
    sha256_prefix: str  # first 16 hex chars of SHA-256, or "<self>" / "<read-error>"
    last_modified: str  # ISO 8601 UTC, e.g. "2026-05-22T18:30:45Z"


# =============================================================================
# Glob matching (segment-based with ** support)
# =============================================================================


def _match_parts(path_parts: List[str], pattern_parts: List[str]) -> bool:
    """
    Recursive glob match with ** support.

    Rules:
      *     matches a single path segment (uses fnmatch.fnmatchcase per segment)
      **    matches zero or more path segments
      exact text matches segment exactly (via fnmatch for wildcards within segment)
    """
    if not pattern_parts:
        return not path_parts
    if not path_parts:
        # Remaining pattern must all be ** (each matches 0)
        return all(p == "**" for p in pattern_parts)

    head, *rest = pattern_parts

    if head == "**":
        # Match 0, 1, 2, ... path segments, then continue with rest
        for i in range(len(path_parts) + 1):
            if _match_parts(path_parts[i:], rest):
                return True
        return False

    # Non-** head: match exactly one path segment
    if fnmatch.fnmatchcase(path_parts[0], head):
        return _match_parts(path_parts[1:], rest)
    return False


def matches_any(relpath: str, patterns: List[str]) -> bool:
    """True if relpath matches any pattern (segment-based glob)."""
    path_parts = relpath.split("/")
    for pat in patterns:
        pattern_parts = pat.split("/")
        if _match_parts(path_parts, pattern_parts):
            return True
    return False


def classify(relpath: str) -> Optional[str]:
    """
    Return tier label (T1, T2, T3, T4.1, T4.2) for relpath,
    or None if no tier rule matches.
    """
    for tier_label, patterns in TIER_RULES:
        if matches_any(relpath, patterns):
            return tier_label
    return None


# =============================================================================
# Directory skipping
# =============================================================================


def should_skip_dir(relpath: str) -> bool:
    """True if this directory should be skipped during walk."""
    # Direct match for multi-segment skip paths
    if relpath in SKIP_DIRS:
        return True
    # Single-segment skip dir name matching any path segment
    parts = relpath.split("/")
    for skip in SKIP_DIRS:
        if "/" in skip:
            # Multi-segment skip: check if relpath starts with it
            skip_parts = skip.split("/")
            if len(parts) >= len(skip_parts) and parts[: len(skip_parts)] == skip_parts:
                return True
        else:
            # Single-segment skip name: match any segment
            if skip in parts:
                return True
    return False


# =============================================================================
# File metadata
# =============================================================================


def to_posix(path: Path) -> str:
    """Convert path to POSIX-style relative-to-root."""
    return str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")


def compute_sha256_prefix(path: Path, length: int = 16) -> str:
    """Compute sha256 of file content, return first N hex chars."""
    h = hashlib.sha256()
    try:
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()[:length]
    except (OSError, PermissionError):
        return "<read-error>"


def get_file_entry(path: Path, tier: str, is_self: bool = False) -> FileEntry:
    """Build a FileEntry for the given file."""
    relpath = to_posix(path)
    try:
        stat = path.stat()
        size_bytes = stat.st_size
        mtime_utc = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
        last_modified = mtime_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    except OSError:
        size_bytes = 0
        last_modified = "<stat-error>"

    sha = "<self>" if is_self else compute_sha256_prefix(path)

    return FileEntry(
        relpath=relpath,
        tier=tier,
        size_bytes=size_bytes,
        sha256_prefix=sha,
        last_modified=last_modified,
    )


# =============================================================================
# Filesystem walk + classification
# =============================================================================


def walk_project(verbose: bool = False) -> Tuple[List[FileEntry], dict]:
    """
    Walk PROJECT_ROOT, classify each file, return (entries, stats).
    """
    entries: List[FileEntry] = []
    stats = {
        "files_seen": 0,
        "files_classified": 0,
        "files_skipped_tier_none": 0,
        "dirs_skipped": 0,
        "tier_counts": defaultdict(int),
    }

    manifest_relpath = to_posix(MANIFEST_PATH)

    for dirpath, dirnames, filenames in os.walk(PROJECT_ROOT):
        dir_relpath = to_posix(Path(dirpath))
        if dir_relpath == ".":
            dir_relpath = ""

        # Prune subdirs IN-PLACE so os.walk skips them
        to_remove = []
        for d in dirnames:
            sub_relpath = f"{dir_relpath}/{d}" if dir_relpath else d
            if should_skip_dir(sub_relpath):
                to_remove.append(d)
                stats["dirs_skipped"] += 1
                if verbose:
                    print(f"  [SKIP-DIR] {sub_relpath}")
        for d in to_remove:
            dirnames.remove(d)

        # Classify each file in this directory
        for fname in filenames:
            file_path = Path(dirpath) / fname
            relpath = to_posix(file_path)
            stats["files_seen"] += 1

            tier = classify(relpath)
            if tier is None:
                stats["files_skipped_tier_none"] += 1
                if verbose:
                    print(f"  [SKIP-TIER] {relpath}")
                continue

            is_self = relpath == manifest_relpath
            entry = get_file_entry(file_path, tier, is_self=is_self)
            entries.append(entry)
            stats["files_classified"] += 1
            stats["tier_counts"][tier] += 1
            if verbose:
                print(f"  [{tier}] {relpath} ({entry.size_bytes} bytes)")

    return entries, stats


# =============================================================================
# Rendering
# =============================================================================


def format_size(n: int) -> str:
    """Human-readable size."""
    if n < 1024:
        return f"{n} B"
    if n < 1024 * 1024:
        return f"{n / 1024:.1f} KB"
    return f"{n / (1024 * 1024):.2f} MB"


def render_table_flat(entries: List[FileEntry]) -> str:
    """Render entries as a single flat markdown table."""
    if not entries:
        return "_(no files in this tier)_\n"
    lines = ["| Path | Size | SHA256 | Last Modified |", "|---|---|---|---|"]
    for e in sorted(entries, key=lambda x: x.relpath):
        lines.append(
            f"| `{e.relpath}` | {format_size(e.size_bytes)} | `{e.sha256_prefix}` | {e.last_modified} |"
        )
    return "\n".join(lines) + "\n"


def render_table_grouped(entries: List[FileEntry]) -> str:
    """Render entries grouped by parent directory (for T3 readability)."""
    if not entries:
        return "_(no files in this tier)_\n"

    groups: Dict[str, List[FileEntry]] = defaultdict(list)
    for e in entries:
        parent = "/".join(e.relpath.split("/")[:-1]) or "(root)"
        groups[parent].append(e)

    out: List[str] = []
    for parent in sorted(groups.keys()):
        out.append(f"\n#### `{parent}/`\n")
        out.append("| Path | Size | SHA256 | Last Modified |")
        out.append("|---|---|---|---|")
        for e in sorted(groups[parent], key=lambda x: x.relpath):
            fname = e.relpath.split("/")[-1]
            out.append(
                f"| `{fname}` | {format_size(e.size_bytes)} | `{e.sha256_prefix}` | {e.last_modified} |"
            )
    return "\n".join(out) + "\n"


def render_manifest(entries: List[FileEntry], stats: dict) -> str:
    """Build full markdown manifest content."""
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    total_size = sum(e.size_bytes for e in entries)

    out: List[str] = []

    # Header
    out.append("# PROJECT_MANIFEST -- Source-of-Truth Filesystem Index\n")
    out.append("")
    out.append(f"> **Generated by:** `scripts/64_generate_manifest.py`  ")
    out.append(f"> **Generated at:** `{now_iso}`  ")
    out.append(">")
    out.append("> WARNING: **DO NOT EDIT MANUALLY** -- Any manual edits will be silently")
    out.append("> overwritten on the next `python scripts/64_generate_manifest.py` run.")
    out.append("> To modify scope: edit `TIER_RULES` in the generator script.")
    out.append(">")
    out.append("> **Core principle (Golden Rule):** Tier classification is by **role**")
    out.append("> in the project, **not** by git tracking status. Some files here are")
    out.append("> gitignored (e.g., `data/excel_imports/*.xlsx`,")
    out.append("> `claude_workspace/snapshots/*.md`) but tracked here for drift detection.")
    out.append("")
    out.append("---\n")

    # Summary table
    out.append("## Summary Statistics\n")
    out.append("")
    out.append("| Tier | File Count | Description |")
    out.append("|---|---|---|")
    tier_counts = stats["tier_counts"]
    for tier_label in ["T1", "T2", "T3", "T4.1", "T4.2"]:
        cnt = tier_counts.get(tier_label, 0)
        out.append(f"| **{tier_label}** | {cnt} | {TIER_LABELS[tier_label]} |")
    out.append(f"| **Total** | **{stats['files_classified']}** | All classified files |")
    out.append(
        f"| _(no-tier skip)_ | _{stats['files_skipped_tier_none']}_ | _Files seen but no tier match (effectively T5 EXCLUDED)_ |"
    )
    out.append(
        f"| _(dirs skipped)_ | _{stats['dirs_skipped']}_ | _Directories not walked (cache/runtime/transient)_ |"
    )
    out.append("")
    out.append(f"**Total size of manifest scope:** {format_size(total_size)}")
    out.append("")
    out.append("---\n")

    # Per-tier sections
    for tier_label in ["T1", "T2", "T3", "T4.1", "T4.2"]:
        out.append(f"## {TIER_LABELS[tier_label]}\n")
        tier_entries = [e for e in entries if e.tier == tier_label]

        if tier_label == "T3":
            # Group by directory for readability (100+ files)
            out.append(render_table_grouped(tier_entries))
        elif tier_label == "T4.1":
            out.append("### T4.1 -- Config (Build/Compile/Runtime)\n")
            out.append(render_table_flat(tier_entries))
        elif tier_label == "T4.2":
            out.append("### T4.2 -- Assets (External System Persistent)\n")
            out.append(render_table_flat(tier_entries))
        else:
            out.append(render_table_flat(tier_entries))

        out.append("\n---\n")

    # Footer
    out.append("## Regenerate\n")
    out.append("```bash")
    out.append("python scripts/64_generate_manifest.py            # full generate (idempotent)")
    out.append("python scripts/64_generate_manifest.py --dry-run  # report counts, no write")
    out.append("python scripts/64_generate_manifest.py --verbose  # show each file during scan")
    out.append("```\n")

    out.append("## Notes\n")
    out.append(
        "- **Self-reference:** This file (`docs/PROJECT_MANIFEST.md`) appears with `sha256 = <self>` placeholder. Audit Check #9 (planned D12) will detect manual edits via two-pass comparison."
    )
    out.append(
        "- **Hash format:** `sha256[:16]` -- first 16 hex chars of SHA-256. Collision risk negligible at project scale (~500 files)."
    )
    out.append("- **Last Modified:** UTC ISO 8601 from filesystem `mtime` (not git history).")
    out.append(
        "- **Tier rule priority:** T1 -> T2 -> T3 -> T4.1 -> T4.2. First match wins. No match = silent skip (effectively T5 EXCLUDED)."
    )
    out.append("- **Golden Rule:** Tier classification by role, NOT by git tracking status.")
    out.append("")
    out.append("---\n")
    out.append("*End of manifest.*")
    out.append("")

    return "\n".join(out)


# =============================================================================
# Idempotent write
# =============================================================================


def write_if_changed(path: Path, content: str) -> str:
    """
    Write content to path only if different from current.
    Returns 'created', 'updated', or 'unchanged'.
    """
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        return "created"
    try:
        current = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        current = path.read_text(encoding="cp1252")
    if current == content:
        return "unchanged"
    path.write_text(content, encoding="utf-8", newline="\n")
    return "updated"


# =============================================================================
# Main
# =============================================================================


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Generate PROJECT_MANIFEST.md by scanning the filesystem. "
            "Content rows are NOT hardcoded -- they are built from the scan."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Scan and report counts, but do not write the manifest file.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show each file/directory during scan.",
    )
    args = parser.parse_args()

    print("=" * 64)
    print("PROJECT_MANIFEST Generator (D2 of MDRS v2)")
    print("=" * 64)
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Target file:  {MANIFEST_PATH.relative_to(PROJECT_ROOT)}")
    print()
    print("Scanning filesystem...")
    print("-" * 64)

    entries, stats = walk_project(verbose=args.verbose)

    print("-" * 64)
    print()
    print("Scan complete.")
    print(f"  Files seen:        {stats['files_seen']}")
    print(f"  Files classified:  {stats['files_classified']}")
    print(f"  Files skipped:     {stats['files_skipped_tier_none']} (no tier match)")
    print(f"  Dirs skipped:      {stats['dirs_skipped']}")
    print()
    print("Per-tier counts:")
    for tier_label in ["T1", "T2", "T3", "T4.1", "T4.2"]:
        cnt = stats["tier_counts"].get(tier_label, 0)
        print(f"  {tier_label:5s}: {cnt:4d} files  -- {TIER_LABELS[tier_label]}")
    print()

    if args.dry_run:
        print("[DRY-RUN] No file written. Exiting.")
        return 0

    # Build content and write
    content = render_manifest(entries, stats)
    status = write_if_changed(MANIFEST_PATH, content)
    icon = {"created": "[NEW]", "updated": "[CHG]", "unchanged": "[OK]"}[status]
    print(f"{icon} {status}: {MANIFEST_PATH.relative_to(PROJECT_ROOT)}")
    print()
    print("=" * 64)
    print("Done.")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    sys.exit(main())
