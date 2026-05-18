# -*- coding: utf-8 -*-
"""
54b_test_precommit_setup.py — تست راه‌اندازی pre-commit (T2.06)

بررسی فقط فایل‌ها و محتوا — نصب واقعی hooks جداگانه با install_git_hooks.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
DOCS = ROOT / "docs"
BACKEND = ROOT / "backend"

PASS = "✅"
FAIL = "❌"


def main() -> int:
    passes: list[str] = []
    failures: list[str] = []

    # ---------- فایل‌ها ----------
    expected = [
        ROOT / ".pre-commit-config.yaml",
        SCRIPTS / "check_anti_patterns.py",
        SCRIPTS / "run_pytest_unit.cmd",
        SCRIPTS / "run_vitest.cmd",
        SCRIPTS / "install_git_hooks.py",
        DOCS / "PRECOMMIT.md",
    ]
    for f in expected:
        if f.exists():
            passes.append(f"فایل موجود: {f.relative_to(ROOT)}")
        else:
            failures.append(f"فایل گم: {f.relative_to(ROOT)}")

    # ---------- requirements.txt ----------
    req = (BACKEND / "requirements.txt").read_text(encoding="utf-8")
    for pkg in ["pre-commit==", "black==", "isort=="]:
        if pkg in req:
            passes.append(f"requirements.txt شامل {pkg.rstrip('=')}")
        else:
            failures.append(f"requirements.txt گم: {pkg}")

    # ---------- .pre-commit-config.yaml ----------
    cfg_path = ROOT / ".pre-commit-config.yaml"
    if cfg_path.exists():
        cfg = cfg_path.read_text(encoding="utf-8")
        for key in [
            "trailing-whitespace",
            "end-of-file-fixer",
            "psf/black",
            "pycqa/isort",
            "check-anti-patterns",
            "pytest-unit",
            "vitest",
            "python: python3.11",
        ]:
            if key in cfg:
                passes.append(f".pre-commit-config دارد: {key[:45]}")
            else:
                failures.append(f".pre-commit-config گم: {key}")

    # ---------- check_anti_patterns.py ----------
    cap = SCRIPTS / "check_anti_patterns.py"
    if cap.exists():
        text = cap.read_text(encoding="utf-8")
        for key in [
            "CRITICAL",
            "MINOR",
            '"A1"',
            '"A4"',
            '"A8"',
            '"A10"',
            '"A6"',
            "get_staged_files",
        ]:
            if key in text:
                passes.append(f"check_anti_patterns دارد: {key}")
            else:
                failures.append(f"check_anti_patterns گم: {key}")

    # ---------- run_*.cmd ----------
    for fname, key in [
        ("run_pytest_unit.cmd", "pytest tests/unit"),
        ("run_vitest.cmd", "npm test"),
    ]:
        p = SCRIPTS / fname
        if p.exists() and key in p.read_text(encoding="utf-8"):
            passes.append(f"{fname} دارد: {key}")
        else:
            failures.append(f"{fname} ناقص یا گم")

    # ---------- install_git_hooks.py ----------
    igh = SCRIPTS / "install_git_hooks.py"
    if igh.exists():
        text = igh.read_text(encoding="utf-8")
        for key in ["pre-commit install", "shutil.which", "subprocess.run"]:
            if key in text:
                passes.append(f"install_git_hooks دارد: {key[:40]}")
            else:
                failures.append(f"install_git_hooks گم: {key}")

    # ---------- PRECOMMIT.md ----------
    pcm = DOCS / "PRECOMMIT.md"
    if pcm.exists():
        text = pcm.read_text(encoding="utf-8")
        sections = [
            "## ۱. مفهوم Hybrid Mode",
            "## ۲. هوک‌های فعال در پروژه",
            "## ۳. نصب اولیه",
            "## ۴. روال روزانه",
            "## ۵. Bypass در اضطرار",
            "## ۶. ساختار فایل‌ها",
            "## ۷. عیب‌یابی",
            "## ۸. هوک‌های سفارشی",
            "## ۹. CI/CD آینده",
            "## ۱۰. ارجاعات",
        ]
        for sec in sections:
            if sec in text:
                passes.append(f"PRECOMMIT.md دارد: {sec[:40]}")
            else:
                failures.append(f"PRECOMMIT.md گم: {sec}")

        for kw in ["Hybrid", "--no-verify", "[skip-hooks:", "قانون #۴۲", "قانون #۴۳"]:
            if kw in text:
                passes.append(f"PRECOMMIT.md کلیدواژه: {kw}")
            else:
                failures.append(f"PRECOMMIT.md گم: {kw}")

    return _report(passes, failures)


def _report(passes: list[str], failures: list[str]) -> int:
    total = len(passes) + len(failures)
    print()
    print("=" * 64)
    print(f"  گزارش تست — 54b_test_precommit_setup")
    print(f"  {len(passes)} pass / {len(failures)} fail / {total} total")
    print("=" * 64)
    print()
    for p in passes:
        print(f"  {PASS} {p}")
    for f in failures:
        print(f"  {FAIL} {f}")
    print()
    print("=" * 64)
    if failures:
        print(f"  ❌ FAILED — {len(failures)} مورد")
        print("=" * 64)
        return 1
    print(f"  ✅ همه {len(passes)} تست pass شدند")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    sys.exit(main())
