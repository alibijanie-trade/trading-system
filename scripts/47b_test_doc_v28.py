# -*- coding: utf-8 -*-
"""
47b_test_doc_v28.py — تست ارتقای سند جامع به v2.8

تست‌های شامل:
  ۱. فایل v2.8 موجود است
  ۲. Header به v2.8 ارتقا یافته
  ۳. شناسه «نسخه ۲.۸» در header
  ۴. ۱۰ ردیف جدید (#۲۳-#۳۲) در جدول ۱.۹
  ۵. بخش «خلاصه تغییرات v2.7 → v2.8» در ابتدا
  ۶. ترتیب صحیح بخش‌های changelog
  ۷. لینک‌های جدید در فهرست مطالب
  ۸. متن قانون #۲۷ صحیح (شامل «چت رو ببند»)
  ۹. رنگ‌های tab در قانون #۳۱
  ۱۰. registry mirror در قانون #۳۲
  ۱۱. سند v2.7 دست‌نخورده (No-Deletion)
  ۱۲. حجم سند v2.8 > حجم سند v2.7

خروجی: exit code 0 (همه pass) یا 1 (لااقل یک fail)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DST = ROOT / "docs" / "سند_جامع_v2_8.md"
SRC = ROOT / "docs" / "سند_جامع_v2_7.md"

PASS = "✅"
FAIL = "❌"


def main() -> int:
    failures: list[str] = []
    passes: list[str] = []

    # Test 1: فایل v2.8 موجود است
    if not DST.exists():
        failures.append(f"فایل v2.8 پیدا نشد: {DST.name}")
        return _report(passes, failures)
    passes.append(f"فایل v2.8 موجود است ({DST.name})")

    text = DST.read_text(encoding="utf-8")

    # Test 2: header به v2.8 ارتقا یافته
    if "# سامانه هوشمند ترید — سند جامع v2.8" in text:
        passes.append("Header به v2.8 ارتقا یافته")
    else:
        failures.append("Header همچنان v2.7 است یا تغییر نکرده")

    # Test 3: شناسه فارسی نسخه
    if "نسخه ۲.۸" in text:
        passes.append("شناسه «نسخه ۲.۸» در header موجود")
    else:
        failures.append("شناسه «نسخه ۲.۸» پیدا نشد")

    # Test 4: قوانین ۲۷-۳۲ همگی موجود در جدول ۱.۹
    for n in ["۲۷", "۲۸", "۲۹", "۳۰", "۳۱", "۳۲"]:
        marker = f"**{n} 🆕 v2.8**"
        if marker in text:
            passes.append(f"قانون #{n} در جدول ۱.۹ موجود")
        else:
            failures.append(f"قانون #{n} در جدول ۱.۹ گم است (marker: {marker})")

    # Test 5: قوانین ۲۳-۲۶ هم به جدول ۱.۹ اضافه شدند
    # marker قابل قبول: شروع ردیف با شماره + 🆕 v2.7
    for n in ["۲۳", "۲۴", "۲۵", "۲۶"]:
        # نسخه‌های مختلف format ها قابل پذیرش‌اند:
        # «**{n} 🆕 v2.7**» یا «**{n} 🆕 v2.7 (جدول v2.8)**»
        if f"**{n} 🆕 v2.7" in text:
            passes.append(f"قانون #{n} (از v2.7) به جدول ۱.۹ اضافه شد")
        else:
            failures.append(f"قانون #{n} (از v2.7) در جدول ۱.۹ گم است")

    # Test 6: بخش «خلاصه تغییرات v2.7 → v2.8»
    if "# 📋 خلاصه تغییرات v2.7 → v2.8" in text:
        passes.append("بخش «خلاصه تغییرات v2.7 → v2.8» موجود")
    else:
        failures.append("بخش «خلاصه تغییرات v2.7 → v2.8» گم است")

    # Test 7: ترتیب صحیح changelog ها
    idx_28 = text.find("# 📋 خلاصه تغییرات v2.7 → v2.8")
    idx_27 = text.find("# 📋 خلاصه تغییرات v2.6 → v2.7")
    if idx_28 > 0 and idx_27 > 0 and idx_28 < idx_27:
        passes.append("ترتیب صحیح: v2.7→v2.8 قبل از v2.6→v2.7")
    else:
        failures.append(f"ترتیب نادرست changelog: idx_28={idx_28}, idx_27={idx_27}")

    # Test 8: لینک v2.7→v2.8 در فهرست
    toc_link_28 = "[**خلاصه تغییرات v2.7 → v2.8 🆕**](#خلاصه-تغییرات-v27--v28)"
    if toc_link_28 in text:
        passes.append("لینک v2.7→v2.8 در فهرست مطالب موجود")
    else:
        failures.append("لینک v2.7→v2.8 در فهرست مطالب گم است")

    # Test 9: heading v2.6→v2.7 (یا لینک TOC) موجود
    toc_link_27 = "[خلاصه تغییرات v2.6 → v2.7](#خلاصه-تغییرات-v26--v27)"
    heading_27 = "# 📋 خلاصه تغییرات v2.6 → v2.7"
    if toc_link_27 in text or heading_27 in text:
        passes.append("بخش v2.6→v2.7 (heading یا TOC) موجود")
    else:
        failures.append("بخش v2.6→v2.7 گم است")

    # Test 10: قانون #۲۷ — متن خاص
    if "تأیید صریح کاربر برای پایان چت" in text and "چت رو ببند" in text:
        passes.append("متن قانون #۲۷ صحیح (شامل «چت رو ببند»)")
    else:
        failures.append("متن قانون #۲۷ ناقص")

    # Test 11: قانون #۳۱ — رنگ‌ها
    color_tabs = ["🟦", "🟩", "🟧", "🟥"]
    missing_colors = [c for c in color_tabs if c not in text]
    if not missing_colors:
        passes.append("همه ۴ رنگ tab (🟦🟩🟧🟥) در سند موجود")
    else:
        failures.append(f"رنگ‌های گم: {missing_colors}")

    # Test 12: قانون #۳۲ — registry mirror
    if "registry.npmmirror.com" in text:
        passes.append("قانون #۳۲ شامل registry.npmmirror.com")
    else:
        failures.append("registry.npmmirror.com در قانون #۳۲ گم است")

    # Test 13: No-Deletion — سند v2.7 دست‌نخورده
    if not SRC.exists():
        failures.append("⚠️ سند v2.7 ناپدید شد! (نقض قانون #۲۴ No-Deletion)")
    else:
        passes.append("سند v2.7 دست‌نخورده باقی ماند (No-Deletion ✓)")

    # Test 14a: تعداد ردیف‌های 🆕 در جدول قوانین — حداقل ۱۹ ردیف انتظار
    # (۹ ردیف v2.1-v2.6 + ۴ ردیف v2.7 + ۶ ردیف v2.8 = ۱۹)
    # regex جامع: هر ردیف جدول که با شماره فارسی شروع شود و 🆕 داشته باشد
    new_rule_rows = re.findall(r"^\| \*\*[۰-۹]+ 🆕[^|]*\*\* \|", text, re.MULTILINE)
    if len(new_rule_rows) >= 19:
        passes.append(f"تعداد ردیف‌های 🆕 در جدول قوانین: {len(new_rule_rows)} ≥ ۱۹")
    else:
        failures.append(f"تعداد ردیف‌های 🆕 ناکافی: {len(new_rule_rows)} < ۱۹")

    # Test 14: حجم سند v2.8 > حجم سند v2.7
    if SRC.exists():
        src_text = SRC.read_text(encoding="utf-8")
        src_lines = src_text.count("\n")
        dst_lines = text.count("\n")
        if dst_lines > src_lines:
            passes.append(f"سند v2.8 طولانی‌تر: {dst_lines} > {src_lines} خط")
        else:
            failures.append(f"سند v2.8 کوتاه‌تر یا برابر: {dst_lines} vs {src_lines}")

    # Test 16: تعداد دفعات «v2.8» در سند (حداقل ~۱۰)
    v28_count = text.count("v2.8")
    if v28_count >= 10:
        passes.append(f"تعداد ارجاع به v2.8 در سند: {v28_count} (≥ ۱۰)")
    else:
        failures.append(f"تعداد ارجاع به v2.8 ناکافی: {v28_count} < ۱۰")

    return _report(passes, failures)


def _report(passes: list[str], failures: list[str]) -> int:
    total = len(passes) + len(failures)
    print()
    print("=" * 64)
    print(f"  گزارش تست — 47b_test_doc_v28")
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
