# -*- coding: utf-8 -*-
"""
50b_test_git_workflow.py — تست تولید docs/GIT_WORKFLOW.md

بررسی‌ها:
  ۱. فایل docs/GIT_WORKFLOW.md موجود
  ۲. حداقل ۱۴ بخش اصلی
  ۳. type های Conventional Commits (feat/fix/docs/refactor/test/chore/perf/style)
  ۴. scope های پروژه (backend/frontend/scripts/docs/governance/tier1/tier2/tier3/deps/migration)
  ۵. تنظیم core.autocrlf و core.quotepath ذکر شده
  ۶. ارجاع به قانون #۳۳ (Backup)
  ۷. ارجاع به قانون #۲۲ (تست همراه) و #۳۰ (idempotent)
  ۸. ارجاع به اسکریپت 43_sync_from_zip.py
  ۹. سناریو rollback (reset/revert/reflog)
  ۱۰. مثال‌های commit message صحیح
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "docs" / "GIT_WORKFLOW.md"

PASS = "✅"
FAIL = "❌"


def main() -> int:
    passes: list[str] = []
    failures: list[str] = []

    if not DOC.exists():
        failures.append(f"فایل پیدا نشد: {DOC.name}")
        return _report(passes, failures)
    passes.append(f"فایل {DOC.name} موجود است")

    text = DOC.read_text(encoding="utf-8")

    # ---------- ساختار کلی ----------
    sections = [
        "## ۱. استراتژی Branch",
        "## ۲. تنظیمات اولیه (Windows)",
        "## ۳. الگوی Commit Message — Conventional Commits",
        "## ۴. زمان Commit",
        "## ۵. Workflow اصلاح فایل از طریق Claude",
        "## ۶. Persian Filenames",
        "## ۷. مدیریت CRLF/LF",
        "## ۸. Rollback و Revert",
        "## ۹. Tag گذاری نسخه‌ها",
        "## ۱۰. Backup — رابطه با قانون #۳۳",
        "## ۱۱. .gitignore — تنظیم استاندارد پروژه",
        "## ۱۲. Alias های پیشنهادی",
        "## ۱۳. سناریوهای رایج",
        "## ۱۴. عیب‌یابی",
    ]
    for sec in sections:
        if sec in text:
            passes.append(f"بخش موجود: {sec[:55]}")
        else:
            failures.append(f"بخش گم: {sec}")

    # ---------- Conventional Commit types ----------
    types = ["feat", "fix", "docs", "refactor", "test", "chore", "perf", "style"]
    missing_types = [t for t in types if f"**{t}**" not in text]
    if not missing_types:
        passes.append(f"همه ۸ نوع Conventional Commit ذکر شده‌اند")
    else:
        failures.append(f"types گم: {missing_types}")

    # ---------- Scope ها ----------
    scopes = [
        "backend", "frontend", "scripts", "docs", "governance",
        "tier1", "tier2", "tier3", "deps", "migration",
    ]
    missing_scopes = [s for s in scopes if f"`{s}`" not in text]
    if not missing_scopes:
        passes.append(f"همه ۱۰ scope پروژه ذکر شده‌اند")
    else:
        failures.append(f"scopes گم: {missing_scopes}")

    # ---------- تنظیمات کلیدی ----------
    if "core.autocrlf" in text:
        passes.append("تنظیم core.autocrlf ذکر شده")
    else:
        failures.append("core.autocrlf گم است")

    if "core.quotepath" in text:
        passes.append("تنظیم core.quotepath ذکر شده (Persian filenames)")
    else:
        failures.append("core.quotepath گم است")

    # ---------- ارجاع به قوانین ----------
    if "قانون #۳۳" in text or "قانون #33" in text:
        passes.append("ارجاع به قانون #۳۳ (Backup در پایان چت) موجود")
    else:
        failures.append("ارجاع به قانون #۳۳ گم است")

    if "قانون #۳۰" in text or "idempotent" in text.lower():
        passes.append("ارجاع به قانون #۳۰ (idempotent) یا کلمه idempotent موجود")
    else:
        failures.append("اشاره به idempotent گم است")

    if "قانون #۲۲" in text or "*b_test_" in text:
        passes.append("ارجاع به قانون #۲۲ (تست همراه) موجود")
    else:
        failures.append("اشاره به تست همراه گم است")

    # ---------- ارجاع به اسکریپت‌ها ----------
    if "43_sync_from_zip" in text:
        passes.append("ارجاع به scripts/43_sync_from_zip.py موجود")
    else:
        failures.append("ارجاع به اسکریپت ۴۳ گم است")

    # ---------- Rollback ----------
    rollback_cmds = ["git reset --soft", "git reset --hard", "git revert", "git reflog"]
    missing_cmds = [c for c in rollback_cmds if c not in text]
    if not missing_cmds:
        passes.append("همه ۴ دستور rollback (reset/revert/reflog) ذکر شده‌اند")
    else:
        failures.append(f"دستورات rollback گم: {missing_cmds}")

    # ---------- Examples ----------
    if "feat(backend):" in text and "docs(governance):" in text:
        passes.append("نمونه‌های Commit message با scope معتبر موجود")
    else:
        failures.append("نمونه‌های Commit message ناقص یا گم")

    # ---------- Anti-patterns ----------
    if "Anti-patterns" in text or "WIP commit" in text:
        passes.append("Anti-patterns (مثل WIP commit) هشدار داده شده")
    else:
        failures.append("Anti-patterns ذکر نشده")

    return _report(passes, failures)


def _report(passes: list[str], failures: list[str]) -> int:
    total = len(passes) + len(failures)
    print()
    print("=" * 64)
    print(f"  گزارش تست — 50b_test_git_workflow")
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
        print(f"  ❌ FAILED — {len(failures)} مورد نیاز به اصلاح")
        print("=" * 64)
        return 1
    print(f"  ✅ همه {len(passes)} تست pass شدند")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    sys.exit(main())
