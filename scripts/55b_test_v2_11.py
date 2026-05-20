# -*- coding: utf-8 -*-
"""
55b_test_v2_11.py - Smoke test for v2.11 creation

Verifies that 55_create_v2_11.py produced a correct v2.11 file:
  - File exists
  - Has new header (v2.11)
  - Has 4 new rules (#62-#65)
  - Has new lesson M63
  - Has new "Changes v2.10 -> v2.11" section
  - Preserves all v2.10 content (No-Deletion check)
  - v2.10 source file untouched

Exit codes:
  0 - all tests passed
  1 - one or more tests failed
"""
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
SOURCE_V210 = DOCS_DIR / "سند_جامع_v2_10.md"
TARGET_V211 = DOCS_DIR / "سند_جامع_v2_11.md"


def check(name, condition, detail=""):
    """Run a single check; return True if passed."""
    if condition:
        print("[PASS] " + name)
        return True
    else:
        print("[FAIL] " + name + (": " + detail if detail else ""))
        return False


def main():
    print("=" * 60)
    print("  55b_test_v2_11.py - Smoke tests for v2.11")
    print("=" * 60)
    print()

    results = []

    # ---- 1. File existence ----
    print("Group 1: File existence")
    print("-" * 60)
    results.append(check("v2.11 file exists", TARGET_V211.exists(), "Run 55_create_v2_11.py first"))
    results.append(
        check(
            "v2.10 file still exists (No-Deletion)",
            SOURCE_V210.exists(),
            "v2.10 was deleted - critical bug",
        )
    )
    if not TARGET_V211.exists():
        # Can't continue without target
        print()
        print("ABORT: target file missing, stopping further tests")
        return 1
    print()

    # Load content once
    v211 = TARGET_V211.read_text(encoding="utf-8")
    v210 = SOURCE_V210.read_text(encoding="utf-8") if SOURCE_V210.exists() else ""

    # ---- 2. Header / version markers ----
    print("Group 2: Header & version markers")
    print("-" * 60)
    results.append(check("Header is v2.11", "# سامانه هوشمند ترید — سند جامع v2.11" in v211))
    results.append(check("Version line shows 2.11", "📅 نسخه ۲.۱۱" in v211))
    results.append(check("Footer is v2.11", "**📌 پایان سند جامع v2.11**" in v211))
    results.append(check("Footer rule count = 65", "**قوانین:** ۶۵" in v211))
    print()

    # ---- 3. New rules #62-#65 ----
    print("Group 3: New rules in table 1.9")
    print("-" * 60)
    results.append(
        check(
            "Rule #62 present (handoff file)",
            "**۶۲ ⭐ 🆕 v2.11**" in v211 and "فایل handoff دائمی" in v211,
        )
    )
    results.append(
        check(
            "Rule #63 present (Convention EXECUTE)",
            "**۶۳ ⭐ 🆕 v2.11**" in v211 and "▶️ EXECUTE" in v211,
        )
    )
    results.append(
        check(
            "Rule #64 present (hide error details)",
            "**۶۴ ⭐ 🆕 v2.11**" in v211 and "عدم نمایش جزئیات تصحیح" in v211,
        )
    )
    results.append(
        check(
            "Rule #65 present (show lessons)",
            "**۶۵ ⭐ 🆕 v2.11**" in v211 and "ثبت درس از اشتباهات با نمایش" in v211,
        )
    )
    print()

    # ---- 4. New lesson M63 ----
    print("Group 4: New lesson in section 18.2")
    print("-" * 60)
    results.append(
        check(
            "Lesson M63 present",
            "**M63** ⭐ 🆕 v2.11" in v211 and "infrastructure در handoff" in v211,
        )
    )
    print()

    # ---- 5. New changes section ----
    print("Group 5: New 'Changes v2.10 -> v2.11' section")
    print("-" * 60)
    results.append(check("Section heading present", "# 📋 خلاصه تغییرات v2.10 → v2.11" in v211))
    results.append(
        check("TOC link to new section present", "[**خلاصه تغییرات v2.10 → v2.11 🆕**]" in v211)
    )
    results.append(
        check(
            "Section appears BEFORE v2.9->v2.10",
            v211.index("# 📋 خلاصه تغییرات v2.10 → v2.11")
            < v211.index("# 📋 خلاصه تغییرات v2.9 → v2.10"),
        )
    )
    print()

    # ---- 6. No-Deletion: v2.10 content preserved ----
    print("Group 6: No-Deletion - v2.10 content preserved")
    print("-" * 60)
    preserved_markers = [
        "# 📋 خلاصه تغییرات v2.9 → v2.10",
        "# 📋 خلاصه تغییرات v2.8 → v2.9",
        "# 📋 خلاصه تغییرات v2.7 → v2.8",
        "# سند ۱ — قوانین همکاری و نقش‌های هوش مصنوعی",
        "# سند ۲۲ — Filesystem MCP Integration",
        "# سند ۲۵ — Skills اختصاصی پروژه",
        "**M62**",  # last v2.10 lesson
        "**۶۱ ⭐ 🆕 v2.10**",  # last v2.10 rule
    ]
    for marker in preserved_markers:
        results.append(check("Preserved: " + marker[:50], marker in v211))
    print()

    # ---- 7. Size sanity ----
    print("Group 7: Size sanity")
    print("-" * 60)
    v210_size = len(v210)
    v211_size = len(v211)
    delta = v211_size - v210_size
    results.append(check("v2.11 larger than v2.10 (delta = +" + str(delta) + " chars)", delta > 0))
    results.append(
        check(
            "Delta is reasonable (1000 < delta < 20000)",
            1000 < delta < 20000,
            "delta = " + str(delta) + " is suspiciously small or large",
        )
    )
    print()

    # ---- Summary ----
    print("=" * 60)
    passed = sum(1 for r in results if r)
    total = len(results)
    if passed == total:
        print("ALL TESTS PASSED (" + str(passed) + "/" + str(total) + ")")
        print("=" * 60)
        return 0
    else:
        failed = total - passed
        print("FAILED: " + str(failed) + " / " + str(total) + " tests")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
