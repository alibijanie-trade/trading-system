# -*- coding: utf-8 -*-
"""
52b_test_anti_patterns.py — تست تولید docs/ANTI_PATTERNS.md

بررسی‌ها:
  - فایل موجود
  - ۱۰ anti-pattern (A1-A10) با ساختار کامل
  - هر anti-pattern شامل ❌ و ✅
  - ارجاع به قوانین #۲۲، #۲۴، #۳۰
  - بخش self-check در پایان
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "docs" / "ANTI_PATTERNS.md"

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

    # ---------- 10 anti-patterns ----------
    anti_patterns = [
        ("A1", "Business Logic در Routes"),
        ("A2", "SQL Queries در Services"),
        ("A3", "بازگشت ORM Models مستقیم"),
        ("A4", "Hardcoded Secrets"),
        ("A5", "`print()` به‌جای Logger"),
        ("A6", "گرفتن `Exception` خالی"),
        ("A7", "فراخوانی Sync در Async"),
        ("A8", "اصلاح دستی فایل"),
        ("A9", "حذف محتوا از سند جامع"),
        ("A10", "اسکریپت بدون تست همراه"),
    ]
    for code, title in anti_patterns:
        marker = f"## {code} —"
        if marker in text:
            passes.append(f"{code} ({title[:35]}) — مستند شده")
        else:
            failures.append(f"{code} گم — marker: {marker}")

    # ---------- ساختار هر anti-pattern ----------
    if text.count("### ❌ نادرست") >= 9 or text.count("❌ نادرست") >= 10:
        passes.append("نمونه ❌ نادرست در همه/تقریباً همه anti-patterns موجود")
    else:
        wrong_count = text.count("❌ نادرست")
        failures.append(f"تعداد ❌ نادرست ناکافی: {wrong_count} < 10")

    if text.count("### ✅ صحیح") >= 9 or text.count("✅ صحیح") >= 10:
        passes.append("نمونه ✅ صحیح در همه/تقریباً همه anti-patterns موجود")
    else:
        right_count = text.count("✅ صحیح")
        failures.append(f"تعداد ✅ صحیح ناکافی: {right_count} < 10")

    if text.count("### 💥 تأثیر بلندمدت") >= 9:
        passes.append("بخش «تأثیر بلندمدت» در تقریباً همه anti-patterns")
    else:
        impact_count = text.count("💥 تأثیر بلندمدت")
        failures.append(f"تعداد «تأثیر بلندمدت» ناکافی: {impact_count}")

    # ---------- ارجاع به قوانین کلیدی ----------
    rules = ["#۲۲", "#۲۴", "#۳۰"]
    for rule in rules:
        if rule in text:
            passes.append(f"ارجاع به قانون {rule} موجود")
        else:
            failures.append(f"ارجاع به قانون {rule} گم")

    # ---------- ارجاع به لایه‌های معماری ----------
    layers = ["routes", "services", "repositories", "schemas"]
    missing_layers = [l for l in layers if l not in text]
    if not missing_layers:
        passes.append("همه ۴ لایه معماری (routes/services/repositories/schemas) ذکر شده")
    else:
        failures.append(f"لایه‌های گم: {missing_layers}")

    # ---------- Self-check در پایان ----------
    if "self-check" in text or "Audit دوره‌ای" in text:
        passes.append("بخش self-check / Audit دوره‌ای موجود")
    else:
        failures.append("بخش self-check گم")

    # شمارش checkbox های self-check (باید ۱۰ تا باشد)
    checkbox_count = text.count("- [ ] **A")
    if checkbox_count >= 10:
        passes.append(f"همه ۱۰ checkbox self-check (A1-A10) در پایان موجود ({checkbox_count})")
    else:
        failures.append(f"checkbox های self-check ناکافی: {checkbox_count} < 10")

    # ---------- ارجاع به سایر اسناد ----------
    refs = ["PROJECT_GOVERNANCE.md", "CLAUDE_CHECKLIST.md", "GIT_WORKFLOW.md", "API_DOCS.md"]
    missing_refs = [r for r in refs if r not in text]
    if not missing_refs:
        passes.append("ارجاع به ۴ سند Governance (GOVERNANCE/CHECKLIST/GIT/API)")
    else:
        failures.append(f"ارجاعات گم: {missing_refs}")

    # ---------- مثال‌های کد Python (def، async def، @router) ----------
    code_markers = ["async def", "@router", "AsyncSession", "logger"]
    missing_code = [c for c in code_markers if c not in text]
    if not missing_code:
        passes.append("نمونه‌های کد Python (async def/router/logger) موجود")
    else:
        failures.append(f"نمونه‌های کد گم: {missing_code}")

    # ---------- جدول خلاصه ----------
    if "خلاصه ۱۰ Anti-Pattern" in text and "🔴 بحرانی" in text:
        passes.append("جدول خلاصه با شدت‌بندی موجود")
    else:
        failures.append("جدول خلاصه ناقص")

    return _report(passes, failures)


def _report(passes: list[str], failures: list[str]) -> int:
    total = len(passes) + len(failures)
    print()
    print("=" * 64)
    print(f"  گزارش تست — 52b_test_anti_patterns")
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
