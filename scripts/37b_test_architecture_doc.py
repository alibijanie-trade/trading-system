# -*- coding: utf-8 -*-
"""
اسکریپت ۳۷b — تست خودکار اصلاحیه ۳۷ (ARCHITECTURE.md)
================================================================
طبق قانون #۲۲ سند v2.7.

پوشش تست:

  Section A — وجود فایل
    ۱) docs/ARCHITECTURE.md ساخته شد

  Section B — header و metadata
    ۱) با عنوان درست شروع می‌شود
    ۲) شامل «نسخه پروژه در زمان نگارش»
    ۳) شامل «آخرین به‌روزرسانی»

  Section C — همه ۹ بخش موجود
    "## ۱.", "## ۲.", ..., "## ۹." همگی پیدا شوند

  Section D — دیاگرام‌های Mermaid
    ۱) شمارش ```mermaid blocks (دقیقاً ۶ تا)
    ۲) هر ``` بسته می‌شود (شمارش متعادل)
    ۳) نوع‌های مختلف دیاگرام موجودند:
       - flowchart (3 بار: overview + backend + frontend)
       - sequenceDiagram (2 بار: theme + auth)
       - classDiagram (1 بار: DataSource)

  Section E — محتوای کلیدی
    ۱) ذکر «۵-لایه» یا «5-لایه» در backend section
    ۲) ذکر ErrorBoundary در frontend section
    ۳) جدول stores شامل ۵ store
    ۴) ذکر BaseDataSource، ExcelDataSource، CCXTDataSource
    ۵) ذکر JWT/bcrypt در auth section
    ۶) درخت فایل‌ها شامل backend/ و frontend/

  Section F — cross-references
    ۱) لینک به سند جامع v2.7
    ۲) لینک به PROJECT_CONTEXT.md
    ۳) لینک به TASK_BACKLOG.md

نحوه اجرا:
    python scripts/37b_test_architecture_doc.py
================================================================
"""

import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
ARCHITECTURE_MD = PROJECT_ROOT / "docs" / "ARCHITECTURE.md"


# ────────────────────────────────────────────────────────────────
# Checks utility
# ────────────────────────────────────────────────────────────────
class Checks:
    def __init__(self):
        self.results = []
        self._section = ""

    def section(self, name):
        self._section = name
        print()
        print(f"--- {name} ---")

    def add(self, name, ok, detail=""):
        full = f"[{self._section}] {name}" if self._section else name
        self.results.append((full, ok, detail))
        mark = "✅" if ok else "❌"
        print(f"  {mark} {name}")
        if not ok and detail:
            print(f"     ↳ {detail}")

    @property
    def passed(self):
        return sum(1 for _, ok, _ in self.results if ok)

    @property
    def failed(self):
        return sum(1 for _, ok, _ in self.results if not ok)

    @property
    def all_pass(self):
        return self.failed == 0


# ────────────────────────────────────────────────────────────────
# Helpers
# ────────────────────────────────────────────────────────────────
PERSIAN_NUMS = "۱۲۳۴۵۶۷۸۹"


def section_a_file(c):
    c.section("A) وجود فایل")
    c.add(
        "docs/ARCHITECTURE.md موجود",
        ARCHITECTURE_MD.exists(),
        str(ARCHITECTURE_MD),
    )


def section_b_header(c, content):
    c.section("B) Header و metadata")
    first_line = content.splitlines()[0] if content else ""
    c.add(
        "عنوان درست (# 🏛️ ARCHITECTURE)",
        first_line.startswith("# 🏛️ ARCHITECTURE"),
        f"اولین خط: {first_line[:60]!r}",
    )
    c.add(
        "ذکر «نسخه پروژه در زمان نگارش»",
        "نسخه پروژه در زمان نگارش" in content,
        "",
    )
    c.add(
        "ذکر «آخرین به‌روزرسانی»",
        "آخرین به‌روزرسانی" in content,
        "",
    )


def section_c_all_sections(c, content):
    c.section("C) همه ۹ بخش موجود")
    for i, num in enumerate(PERSIAN_NUMS[:9], start=1):
        header = f"## {num}."
        c.add(
            f"بخش {num} ({header})",
            header in content,
            "",
        )


def section_d_mermaid(c, content):
    c.section("D) دیاگرام‌های Mermaid")

    # شمارش ```mermaid blocks
    open_count = len(re.findall(r"^```mermaid", content, flags=re.MULTILINE))
    c.add(
        f"تعداد ```mermaid blocks = ۶",
        open_count == 6,
        f"شمارش = {open_count}",
    )

    # شمارش fence های ``` کلی (باید زوج باشد)
    all_fences = len(re.findall(r"^```", content, flags=re.MULTILINE))
    c.add(
        "تعداد fence ها زوج (open/close متعادل)",
        all_fences % 2 == 0,
        f"شمارش کل ``` = {all_fences}",
    )

    # نوع‌های دیاگرام
    diagram_types = {
        "flowchart": 3,  # 1 overview + 1 backend + 1 frontend
        "sequenceDiagram": 2,  # theme + auth
        "classDiagram": 1,  # DataSource
    }
    for dtype, expected_count in diagram_types.items():
        # شمارش با regex: داخل bloks mermaid، خط شروع‌شده با dtype
        count = len(
            re.findall(
                rf"```mermaid\s*\n\s*{dtype}\b",
                content,
                flags=re.MULTILINE,
            )
        )
        c.add(
            f"نوع '{dtype}' = {expected_count}",
            count == expected_count,
            f"یافت‌شده = {count}",
        )


def section_e_content(c, content):
    c.section("E) محتوای کلیدی")

    checks = [
        (
            "ذکر ۵-لایه یا 5-لایه در backend",
            "۵-لایه" in content
            or "5-لایه" in content
            or "5 لایه" in content
            or "۵ لایه" in content,
        ),
        ("ذکر ErrorBoundary", "ErrorBoundary" in content),
        ("ذکر defense-in-depth", "defense-in-depth" in content),
        ("BaseDataSource", "BaseDataSource" in content),
        ("ExcelDataSource", "ExcelDataSource" in content),
        ("CCXTDataSource (آینده)", "CCXTDataSource" in content),
        ("ذکر JWT", "JWT" in content),
        ("ذکر bcrypt", "bcrypt" in content),
        ("ذکر Zustand", "Zustand" in content),
        ("درخت فایل شامل backend/", "backend/" in content),
        ("درخت فایل شامل frontend/", "frontend/" in content),
        ("درخت فایل شامل docs/", "docs/" in content),
        (
            "ذکر هر ۵ store در جدول",
            all(
                s in content
                for s in [
                    "authStore",
                    "themeStore",
                    "preferencesStore",
                    "toastStore",
                    "confirmStore",
                ]
            ),
        ),
    ]
    for name, ok in checks:
        c.add(name, ok, "")


def section_f_cross_refs(c, content):
    c.section("F) Cross-references به سایر اسناد")
    checks = [
        ("لینک به سند جامع v2.7", "سند_جامع_v2_7" in content or "سند جامع v2.7" in content),
        ("لینک به PROJECT_CONTEXT.md", "PROJECT_CONTEXT.md" in content),
        ("لینک به TASK_BACKLOG.md", "TASK_BACKLOG.md" in content),
        ("لینک به DECISIONS_LOG.md", "DECISIONS_LOG.md" in content),
        ("لینک به CLAUDE_CHECKLIST.md", "CLAUDE_CHECKLIST.md" in content),
    ]
    for name, ok in checks:
        c.add(name, ok, "")


# ────────────────────────────────────────────────────────────────
# Main
# ────────────────────────────────────────────────────────────────
def main() -> int:
    print("=" * 64)
    print("اسکریپت ۳۷b — تست ARCHITECTURE.md")
    print("=" * 64)

    c = Checks()
    section_a_file(c)

    if not ARCHITECTURE_MD.exists():
        print()
        print("=" * 64)
        print("❌ ARCHITECTURE.md موجود نیست — سایر بخش‌ها skip.")
        print("=" * 64)
        return 1

    content = ARCHITECTURE_MD.read_text(encoding="utf-8")

    section_b_header(c, content)
    section_c_all_sections(c, content)
    section_d_mermaid(c, content)
    section_e_content(c, content)
    section_f_cross_refs(c, content)

    print()
    print("=" * 64)
    print(f"خلاصه: {c.passed} ✅   |   {c.failed} ❌   |   جمع: {len(c.results)}")
    print("=" * 64)
    return 0 if c.all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
