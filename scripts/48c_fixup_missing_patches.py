# -*- coding: utf-8 -*-
"""
48c_fixup_missing_patches.py — رفع پچ‌های ازدست‌رفته از اسکریپت ۴۸

اسکریپت ۴۸ در اجرای قبلی برخی پچ‌ها را به‌صورت ناقص اعمال کرد
(version bump شد اما block content اضافه نشد در ۴ فایل از ۵ فایل).

این اسکریپت ۴ پچ ازدست‌رفته را با حفظ idempotency اضافه می‌کند:
  ۱. CLAUDE_CHECKLIST.md       — افزودن بخش قوانین قفل‌شده + پیش‌شرط فاز ۳ + رنگ tab
  ۲. PROJECT_GOVERNANCE.md     — افزودن ردیف‌های C16-C20
  ۳. CHAT_LOG.md               — افزودن یادداشت یکپارچه‌سازی شمارش
  ۴. SESSION_STATUS.md         — افزودن یادداشت چت ۷

استفاده:
  python scripts\\48c_fixup_missing_patches.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

CHECKLIST = DOCS / "CLAUDE_CHECKLIST.md"
GOVERNANCE = DOCS / "PROJECT_GOVERNANCE.md"
CHATLOG = DOCS / "CHAT_LOG.md"
SESSION = DOCS / "SESSION_STATUS.md"


def write_if_changed(path: Path, content: str) -> bool:
    if path.exists():
        if path.read_text(encoding="utf-8") == content:
            return False
    path.write_text(content, encoding="utf-8")
    return True


# =================================================================
# PATCH 1 — CHECKLIST: افزودن بخش قوانین قفل‌شده + پیش‌شرط فاز ۳
# =================================================================

CHECKLIST_BLOCK = """## قوانین قفل‌شده مرتبط با چک‌لیست (مرجع سریع)

این جدول قوانینی را که به‌طور خاص به اجرای این چک‌لیست مربوط هستند فهرست می‌کند. **مرجع کامل قوانین:** جدول ۱.۹ در سند جامع v2.8.

| # | قانون | کجای چک‌لیست اعمال می‌شود |
|---|---|---|
| #۲۵ | چک‌لیست اجباری شروع چت (۸ مرحله) | فاز ۱ — کامل |
| #۲۷ | تأیید صریح کاربر برای پایان چت | فاز ۳ — قبل از مرحله ۱ |
| #۲۸ | کوتاه گفتن خطا | فاز ۲ — حین کار |
| #۲۹ | ارائه فایل با Artifact یا code block | فاز ۲ — قبل از تحویل |
| #۳۰ | اصلاحات کوچک = اسکریپت Python idempotent | فاز ۲ — قبل از تولید اسکریپت |
| #۳۱ | شماره + رنگ tab بالای هر کادر کد | فاز ۲ — قبل از تحویل |
| #۳۲ | npm install در ایران: registry.npmmirror.com + flags | چک محیط (مرحله ۴ فاز ۱) |

---

## ⛔ پیش‌شرط بحرانی فاز ۳ — قانون #۲۷

**قبل از شروع هر یک از ۱۲ مرحله فاز ۳ (پایان چت)، Claude باید تأیید صریح کاربر را دریافت کرده باشد.**

### تأییدیه‌های صریح که فاز ۳ را trigger می‌کنند:
- «چت رو ببند»
- «end of chat»
- «zip نهایی بساز و چت رو ببند»
- «پایان چت»
- «بسته کن این چت رو»

### جملاتی که تأییدیه نیستند (نباید فاز ۳ را trigger کنند):
- «گام بعدی چیست؟»
- «کار دیگری هست؟»
- «چی مونده؟»
- «خسته شدیم»

### استثنا
نزدیک‌شدن به سقف context window — با هشدار قبلی و انتظار تأیید کاربر برای ادامه به‌صورت پایان چت.

### رفتار صحیح بعد از اتمام task
1. Claude خلاصه آنچه انجام داد را ارائه می‌دهد
2. Claude پیشنهاد گام بعدی می‌دهد (مثلاً «task بعدی T2.06 است — شروع کنم؟»)
3. Claude **منتظر دستور بعدی می‌ماند** — نه به فاز ۳ می‌رود نه به task بعدی

---

## 🎨 رعایت قانون #۳۱ — شماره + رنگ tab

**بالای هر کادر کد دستوری، Claude باید این کار را انجام دهد:**

````markdown
**🟦 tab «1 backend»**
```cmd
cd backend
venv\\Scripts\\activate
pytest
```
````

### رنگ‌بندی پیش‌فرض ۴ tab

| Tab | رنگ | کاربرد | پوشه فعال پیش‌فرض |
|---|---|---|---|
| `1 backend` | 🟦 آبی | سرور + تست backend + venv | `backend/` |
| `2 scripts` | 🟩 سبز | اسکریپت‌های Python | پروژه root |
| `3 frontend` | 🟧 نارنجی | React + تست frontend | `frontend/` |
| `4 BACKUP` | 🟥 قرمز | git + backup + sync | پروژه root |

### استثنا
کادرهای کد non-executable (مثل کد JSX برای نشان دادن، YAML برای توضیح، JSON نمونه) نیاز به برچسب tab ندارند.

---

"""


def patch_checklist(text: str) -> tuple[str, list[str]]:
    changes: list[str] = []

    # Idempotency
    if "قوانین قفل‌شده مرتبط با چک‌لیست (مرجع سریع)" in text:
        return text, ["[skip] قوانین مرجع از قبل افزوده شده"]

    end_anchor = "## 📌 پایان CLAUDE_CHECKLIST"
    if end_anchor not in text:
        changes.append("[err] انکر '## 📌 پایان CLAUDE_CHECKLIST' پیدا نشد")
        return text, changes

    text = text.replace(
        end_anchor,
        CHECKLIST_BLOCK + end_anchor,
        1,
    )
    changes.append("افزودن بخش «قوانین قفل‌شده مرتبط» + پیش‌شرط فاز ۳ + رنگ tab")
    return text, changes


# =================================================================
# PATCH 2 — GOVERNANCE: افزودن C16-C20
# =================================================================

GOVERNANCE_C16_C20 = """| C16 | **تأیید صریح قبل از فاز ۳ پایان چت** (قانون #۲۷) | پایان task ها |
| C17 | **خطای کوتاه: فقط اقدامات اجرایی** (قانون #۲۸) | هنگام خطا |
| C18 | **Artifact یا code block** (قانون #۲۹) | تحویل فایل |
| C19 | **اسکریپت idempotent برای اصلاح کوچک** (قانون #۳۰) | اصلاح فایل موجود |
| C20 | **شماره + رنگ tab بالای کادر کد** (قانون #۳۱) | همه کادرهای دستور |"""


def patch_governance(text: str) -> tuple[str, list[str]]:
    changes: list[str] = []

    # Sub-patch A: C16-C20 rows
    if "| C16 |" not in text:
        c15_anchor = "| C15 | تعهد به فاز ۰ → ۸ | ندیدن task ها به‌صورت ایزوله |"
        if c15_anchor not in text:
            changes.append("[err] انکر C15 پیدا نشد")
            return text, changes

        text = text.replace(
            c15_anchor,
            c15_anchor + "\n" + GOVERNANCE_C16_C20,
            1,
        )
        changes.append("افزودن C16-C20 (مسئولیت‌های جدید Claude)")

    # Sub-patch B: bump version v1.0 → v1.1
    version_anchor = "**نسخه:** v1.0 (تاریخ ایجاد: 2026-05-17)"
    if version_anchor in text:
        text = text.replace(
            version_anchor,
            "**نسخه:** v1.1 (2026-05-18 — افزودن C16-C20 + یادآور قوانین #۲۷-#۳۲)",
            1,
        )
        changes.append("ارتقای نسخه GOVERNANCE v1.0 → v1.1")

    if not changes:
        changes.append("[skip] GOVERNANCE از قبل به‌روز است")

    return text, changes


# =================================================================
# PATCH 3 — CHATLOG: افزودن یادداشت یکپارچه‌سازی
# =================================================================

CHATLOG_NOTE = """## ⚠️ یادداشت یکپارچه‌سازی شمارش (v1.1 — چت ۷)

در چت ۷ (`phase0-part07-quality-hardening-continued`)، شمارش چت‌ها یکپارچه شد:

| شمارش قدیمی | شمارش جدید | علت تغییر |
|---|---|---|
| چت ۵ | **چت ۵.الف** | chat اصلی Session 5 (theme-engine، part04) |
| چت ۶ | **چت ۵.ب** | ادامه Session 5 (ui-polish-and-governance، part05) |
| چت ۷ | **چت ۶** | Session 6 مستقل (quality-hardening، part06) — منطبق با CHAT6_FINALIZE.md |
| (این چت) | **چت ۷** | Session 7 (quality-hardening-continued، part07) |

این یکپارچه‌سازی باعث می‌شود «چت N» در CHAT_LOG با Session N در سایر اسناد (CHAT6_FINALIZE، SESSION_STATUS) همراستا شود.

---

"""


def patch_chatlog(text: str) -> tuple[str, list[str]]:
    changes: list[str] = []

    # Idempotency
    if "یادداشت یکپارچه‌سازی شمارش" in text:
        return text, ["[skip] یادداشت یکپارچه‌سازی از قبل افزوده شده"]

    guide_anchor = "## راهنمای استفاده"
    if guide_anchor not in text:
        changes.append("[err] انکر '## راهنمای استفاده' پیدا نشد")
        return text, changes

    text = text.replace(guide_anchor, CHATLOG_NOTE + guide_anchor, 1)
    changes.append("افزودن یادداشت یکپارچه‌سازی شمارش")
    return text, changes


# =================================================================
# PATCH 4 — SESSION: افزودن یادداشت چت ۷
# =================================================================

SESSION_NOTE = """
> ⚠️ **یادداشت چت ۷:** این فایل وضعیت **پایان چت ۶** را نشان می‌دهد. در پایان چت ۷ (با تأیید صریح کاربر طبق قانون #۲۷)، این فایل بازنویسی می‌شود.
"""


def patch_session(text: str) -> tuple[str, list[str]]:
    changes: list[str] = []

    # Idempotency
    if "یادداشت چت ۷" in text:
        return text, ["[skip] یادداشت چت ۷ از قبل افزوده شده"]

    anchor = "**آخرین به‌روزرسانی:** 2026-05-17 (پایان چت ۶)"
    if anchor not in text:
        changes.append("[err] انکر SESSION پیدا نشد")
        return text, changes

    text = text.replace(anchor, anchor + SESSION_NOTE, 1)
    changes.append("افزودن یادداشت چت ۷")
    return text, changes


# =================================================================
# Main
# =================================================================

PATCHES = [
    ("CLAUDE_CHECKLIST.md", CHECKLIST, patch_checklist),
    ("PROJECT_GOVERNANCE.md", GOVERNANCE, patch_governance),
    ("CHAT_LOG.md", CHATLOG, patch_chatlog),
    ("SESSION_STATUS.md", SESSION, patch_session),
]


def main() -> int:
    print("=" * 64)
    print("  48c_fixup_missing_patches — رفع ۴ پچ ازدست‌رفته")
    print("=" * 64)
    print()

    any_error = False
    total = 0

    for name, path, patch_fn in PATCHES:
        if not path.exists():
            print(f"❌ فایل پیدا نشد: {name}")
            any_error = True
            continue

        original = path.read_text(encoding="utf-8")
        new_text, changes = patch_fn(original)

        if new_text == original:
            status = "✓ no-op"
        else:
            write_if_changed(path, new_text)
            status = "✏️ updated"

        # بررسی [err] در پیام‌ها
        had_err = any(c.startswith("[err]") for c in changes)
        if had_err:
            any_error = True

        print(f"{status}  {name}")
        for ch in changes:
            print(f"           - {ch}")
            if not ch.startswith("[skip]") and not ch.startswith("[err]"):
                total += 1
        print()

    print("=" * 64)
    if any_error:
        print(f"❌ FAILED — حداقل یک پچ دچار خطا شد (انکر پیدا نشد)")
        print("=" * 64)
        return 1
    print(f"✅ موفق — {total} پچ اعمال شد")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    sys.exit(main())
