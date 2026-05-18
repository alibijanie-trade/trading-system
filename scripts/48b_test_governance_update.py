# -*- coding: utf-8 -*-
"""
48b_test_governance_update.py — تست به‌روزرسانی ۵ سند Governance

تست‌های شامل:
  CLAUDE_CHECKLIST.md:
    ۱. بخش «قوانین قفل‌شده مرتبط با چک‌لیست» موجود
    ۲. پیش‌شرط بحرانی فاز ۳ (قانون #۲۷) موجود
    ۳. جدول رنگ‌های tab (#۳۱) موجود
    ۴. نسخه v1.1 شده

  PROJECT_GOVERNANCE.md:
    ۵. مسئولیت‌های C16-C20 افزوده
    ۶. Audit قوانین #۲۷-#۳۲ افزوده
    ۷. نسخه v1.1 شده

  TASK_BACKLOG.md:
    ۸. T2.11 = IN-PROGRESS
    ۹. T2.12 موجود
    ۱۰. آمار به‌روز
    ۱۱. نسخه v1.3 شده

  CHAT_LOG.md:
    ۱۲. چت ۵.الف موجود (heading)
    ۱۳. چت ۵.ب موجود (heading)
    ۱۴. چت ۶ — phase0-part06 موجود
    ۱۵. یادداشت یکپارچه‌سازی شمارش موجود
    ۱۶. نسخه v1.1 شده

  SESSION_STATUS.md:
    ۱۷. یادداشت چت ۷ افزوده (یک بار، نه دوبار)
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

CHECKLIST = DOCS / "CLAUDE_CHECKLIST.md"
GOVERNANCE = DOCS / "PROJECT_GOVERNANCE.md"
BACKLOG = DOCS / "TASK_BACKLOG.md"
CHATLOG = DOCS / "CHAT_LOG.md"
SESSION = DOCS / "SESSION_STATUS.md"

PASS = "✅"
FAIL = "❌"


def check(condition: bool, msg: str, passes: list[str], failures: list[str]):
    (passes if condition else failures).append(msg)


def main() -> int:
    passes: list[str] = []
    failures: list[str] = []

    # ---------- CLAUDE_CHECKLIST.md ----------
    if not CHECKLIST.exists():
        failures.append(f"فایل پیدا نشد: {CHECKLIST.name}")
    else:
        t = CHECKLIST.read_text(encoding="utf-8")
        check(
            "قوانین قفل‌شده مرتبط با چک‌لیست (مرجع سریع)" in t,
            "CHECKLIST: بخش «قوانین قفل‌شده مرتبط با چک‌لیست» موجود",
            passes,
            failures,
        )
        check(
            "پیش‌شرط بحرانی فاز ۳ — قانون #۲۷" in t,
            "CHECKLIST: پیش‌شرط بحرانی فاز ۳ موجود",
            passes,
            failures,
        )
        check(
            "🟦" in t and "🟩" in t and "🟧" in t and "🟥" in t,
            "CHECKLIST: ۴ رنگ tab (🟦🟩🟧🟥) موجود",
            passes,
            failures,
        )
        check(
            "v1.1 (2026-05-18" in t,
            "CHECKLIST: نسخه v1.1 (2026-05-18) ارتقا یافته",
            passes,
            failures,
        )
        check(
            "چت رو ببند" in t and "end of chat" in t,
            "CHECKLIST: تأییدیه‌های صریح پایان چت ذکر شده",
            passes,
            failures,
        )

    # ---------- PROJECT_GOVERNANCE.md ----------
    if not GOVERNANCE.exists():
        failures.append(f"فایل پیدا نشد: {GOVERNANCE.name}")
    else:
        t = GOVERNANCE.read_text(encoding="utf-8")
        check(
            "| C16 |" in t and "| C20 |" in t,
            "GOVERNANCE: مسئولیت‌های C16-C20 افزوده",
            passes,
            failures,
        )
        check(
            "Audit مرتبط با قوانین #۲۷-#۳۲" in t or "قوانین #۲۷-۳۲" in t or "قوانین #۲۷" in t,
            "GOVERNANCE: یادآور قوانین #۲۷-#۳۲ موجود (Audit یا G7)",
            passes,
            failures,
        )
        check(
            "v1.1 (به‌روز: 2026-05-18)" in t or "v1.1 (2026-05-18" in t,
            "GOVERNANCE: نسخه v1.1 ارتقا یافته",
            passes,
            failures,
        )
        # چک کنیم همه ۵ قانون جدید در C16-C20 ذکر شده‌اند
        for rule in ["#۲۷", "#۲۸", "#۲۹", "#۳۰", "#۳۱"]:
            check(
                rule in t,
                f"GOVERNANCE: قانون {rule} در سند موجود",
                passes,
                failures,
            )

    # ---------- TASK_BACKLOG.md ----------
    if not BACKLOG.exists():
        failures.append(f"فایل پیدا نشد: {BACKLOG.name}")
    else:
        t = BACKLOG.read_text(encoding="utf-8")
        check(
            "| T2.11 |" in t and "🚧 IN-PROGRESS" in t,
            "BACKLOG: T2.11 = IN-PROGRESS",
            passes,
            failures,
        )
        check(
            "| T2.12 |" in t and "Claude Code" in t,
            "BACKLOG: T2.12 (Claude Code migration) موجود",
            passes,
            failures,
        )
        # Tier 2 ممکن است ۱۲ یا ۱۳ باشد (اگر T2.13 هم اضافه شده)
        check(
            "Tier 2 | 12 |" in t or "Tier 2 | 13 |" in t,
            "BACKLOG: آمار Tier 2 ≥ ۱۲ task",
            passes,
            failures,
        )
        # مجموع باید حداقل ۶۶ باشد (۶۶ یا ۶۸ بسته به T2.13)
        check(
            "**66**" in t or "**67**" in t or "**68**" in t,
            "BACKLOG: آمار کل ≥ ۶۶ task",
            passes,
            failures,
        )
        check(
            "v1.3" in t and "2026-05-18" in t,
            "BACKLOG: نسخه v1.3 ارتقا یافته",
            passes,
            failures,
        )

    # ---------- CHAT_LOG.md ----------
    if not CHATLOG.exists():
        failures.append(f"فایل پیدا نشد: {CHATLOG.name}")
    else:
        t = CHATLOG.read_text(encoding="utf-8")
        check(
            "## چت ۵.الف — phase0-part04-theme-engine" in t,
            "CHATLOG: heading «چت ۵.الف» موجود",
            passes,
            failures,
        )
        check(
            "## چت ۵.ب — phase0-part05-ui-polish-and-governance" in t,
            "CHATLOG: heading «چت ۵.ب» موجود",
            passes,
            failures,
        )
        check(
            "## چت ۶ — phase0-part06-quality-hardening" in t,
            "CHATLOG: heading «چت ۶ — part06» موجود",
            passes,
            failures,
        )
        check(
            "یادداشت یکپارچه‌سازی شمارش" in t,
            "CHATLOG: یادداشت یکپارچه‌سازی شمارش موجود",
            passes,
            failures,
        )
        check(
            "v1.1 (2026-05-18)" in t or "v1.2 (2026-05-18" in t,
            "CHATLOG: نسخه ≥ v1.1 (2026-05-18)",
            passes,
            failures,
        )
        # چت قدیمی «## چت ۷» نباید بماند (مگر در یادداشت)
        # خط دقیق `## چت ۷ — phase0-part06` نباید موجود باشد
        check(
            "## چت ۷ — phase0-part06-quality-hardening" not in t,
            "CHATLOG: heading قدیمی «چت ۷ — part06» حذف شد",
            passes,
            failures,
        )

    # ---------- SESSION_STATUS.md ----------
    if not SESSION.exists():
        failures.append(f"فایل پیدا نشد: {SESSION.name}")
    else:
        t = SESSION.read_text(encoding="utf-8")
        check(
            "**یادداشت چت ۷:**" in t,
            "SESSION: یادداشت چت ۷ موجود",
            passes,
            failures,
        )
        # نباید دوبار افزوده شده باشد
        count = t.count("**یادداشت چت ۷:**")
        check(
            count == 1,
            f"SESSION: یادداشت چت ۷ فقط یک بار (count={count})",
            passes,
            failures,
        )

    return _report(passes, failures)


def _report(passes: list[str], failures: list[str]) -> int:
    total = len(passes) + len(failures)
    print()
    print("=" * 64)
    print(f"  گزارش تست — 48b_test_governance_update")
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
