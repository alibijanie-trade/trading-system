# -*- coding: utf-8 -*-
"""
48_atomic_governance_update.py — به‌روزرسانی اتمیک ۵ سند Governance

مطابق قانون #۲۶ (Atomic Updates)، این اسکریپت همراه با اسکریپت
`47_upgrade_doc_to_v28.py` اجرا می‌شود تا تمام اسناد مرتبط با قوانین #۲۳-#۳۲
به‌صورت یک‌نوبت به‌روز شوند.

اسناد متأثر:
  ۱. CLAUDE_CHECKLIST.md       — افزودن قوانین به فازهای مرتبط
  ۲. PROJECT_GOVERNANCE.md     — افزودن مسئولیت‌های C16-C20 + Audit جدید
  ۳. TASK_BACKLOG.md           — افزودن T2.12 + علامت‌گذاری T2.11
  ۴. CHAT_LOG.md               — یکپارچه‌سازی شمارش چت‌ها (۵→۵.الف، ۶→۵.ب، ۷→۶)
  ۵. SESSION_STATUS.md         — یکپارچه‌سازی شمارش چت‌ها

همه تغییرات idempotent هستند. اجرای دوم تغییری ایجاد نمی‌کند.

استفاده:
  python scripts\\48_atomic_governance_update.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

CHECKLIST = DOCS / "CLAUDE_CHECKLIST.md"
GOVERNANCE = DOCS / "PROJECT_GOVERNANCE.md"
BACKLOG = DOCS / "TASK_BACKLOG.md"
CHATLOG = DOCS / "CHAT_LOG.md"
SESSION = DOCS / "SESSION_STATUS.md"


def write_if_changed(path: Path, content: str) -> bool:
    if path.exists():
        if path.read_text(encoding="utf-8") == content:
            return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


# =================================================================
# SECTION A: CLAUDE_CHECKLIST.md
# =================================================================

CHECKLIST_RULES_BLOCK = """
---

## قوانین قفل‌شده مرتبط با چک‌لیست (مرجع سریع)

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
"""


def update_checklist(text: str) -> tuple[str, list[str]]:
    """به‌روزرسانی CLAUDE_CHECKLIST.md — افزودن بخش قوانین + پیش‌شرط فاز ۳."""
    changes = []

    # Idempotency: اگر قبلاً اضافه شده، skip
    if "قوانین قفل‌شده مرتبط با چک‌لیست (مرجع سریع)" in text:
        return text, ["[skip] قوانین مرجع از قبل افزوده شده"]

    # Anchor: قبل از پایان فایل (قبل از "## 📌 پایان CLAUDE_CHECKLIST")
    end_anchor = "## 📌 پایان CLAUDE_CHECKLIST"
    if end_anchor not in text:
        raise RuntimeError(f"انکر پایان CLAUDE_CHECKLIST پیدا نشد: {end_anchor!r}")

    text = text.replace(
        end_anchor,
        CHECKLIST_RULES_BLOCK.strip() + "\n\n---\n\n" + end_anchor,
        1,
    )
    changes.append("افزودن بخش «قوانین قفل‌شده مرتبط با چک‌لیست» + پیش‌شرط فاز ۳")

    # Bump version: v1.0 → v1.1
    if "**نسخه:** v1.0 (2026-05-17)" in text:
        text = text.replace(
            "**نسخه:** v1.0 (2026-05-17)",
            "**نسخه:** v1.1 (2026-05-18) — افزودن مرجع قوانین #۲۳-#۳۲ + پیش‌شرط فاز ۳",
            1,
        )
        changes.append("ارتقای نسخه v1.0 → v1.1")

    return text, changes


# =================================================================
# SECTION B: PROJECT_GOVERNANCE.md
# =================================================================

GOVERNANCE_AUDIT_ADDITION = """
### Audit مرتبط با قوانین #۲۷-#۳۲ (🆕 v1.1)

- [ ] **#۲۷:** آیا قبل از فاز ۳، تأیید صریح کاربر را گرفتم؟ (نه «گام بعدی چیست» را تأییدیه گرفتم)
- [ ] **#۲۸:** آیا در صورت خطا، فقط اقدامات اجرایی را دادم — نه توضیح فنی طولانی؟
- [ ] **#۲۹:** آیا فایل‌ها به‌صورت Artifact یا code block ارائه شدند — نه paste متن خام؟
- [ ] **#۳۰:** آیا برای اصلاحات کوچک، اسکریپت idempotent ساختم — نه دستور دستی؟
- [ ] **#۳۱:** آیا بالای هر کادر کد، شماره + رنگ tab نوشتم؟
- [ ] **#۳۲:** آیا برای npm install، روش mirror ایران را پیشنهاد دادم؟

"""

GOVERNANCE_RESPONSIBILITIES_ADDITION = """| C16 | **تأیید صریح قبل از فاز ۳ پایان چت** (قانون #۲۷) | پایان task ها |
| C17 | **خطای کوتاه: فقط اقدامات اجرایی** (قانون #۲۸) | هنگام خطا |
| C18 | **Artifact یا code block** (قانون #۲۹) | تحویل فایل |
| C19 | **اسکریپت idempotent برای اصلاح کوچک** (قانون #۳۰) | اصلاح فایل موجود |
| C20 | **شماره + رنگ tab بالای کادر کد** (قانون #۳۱) | همه کادرهای دستور |
"""


def update_governance(text: str) -> tuple[str, list[str]]:
    """به‌روزرسانی PROJECT_GOVERNANCE.md — افزودن C16-C20 + Audit جدید."""
    changes = []

    if "C16" not in text and "تأیید صریح قبل از فاز ۳ پایان چت" not in text:
        # افزودن C16-C20 بعد از C15
        c15_anchor = "| C15 | تعهد به فاز ۰ → ۸ | ندیدن task ها به‌صورت ایزوله |"
        if c15_anchor in text:
            text = text.replace(
                c15_anchor,
                c15_anchor + "\n" + GOVERNANCE_RESPONSIBILITIES_ADDITION.strip(),
                1,
            )
            changes.append("افزودن C16-C20 (مسئولیت‌های جدید Claude)")
        else:
            changes.append("[warn] انکر C15 پیدا نشد — C16-C20 افزوده نشد")

    if "Audit مرتبط با قوانین #۲۷-#۳۲" not in text:
        # افزودن Audit بعد از "### Audit در پایان چت"
        # دقیق‌تر: بعد از خط «اگر هر سؤالی **NO** بود ...»
        audit_anchor = "اگر هر سؤالی **NO** بود، Claude باید **توقف کند و اصلاح کند** قبل از تحویل."
        if audit_anchor in text:
            text = text.replace(
                audit_anchor,
                audit_anchor + "\n\n" + GOVERNANCE_AUDIT_ADDITION.strip() + "\n",
                1,
            )
            changes.append("افزودن «Audit مرتبط با قوانین #۲۷-#۳۲»")
        else:
            changes.append("[warn] انکر Audit پایان چت پیدا نشد")

    # Bump version: v1.0 → v1.1
    version_anchor = "**نسخه:** v1.0 (تاریخ ایجاد: 2026-05-17)"
    if version_anchor in text:
        text = text.replace(
            version_anchor,
            "**نسخه:** v1.1 (به‌روز: 2026-05-18) — افزودن C16-C20 + Audit قوانین #۲۷-#۳۲",
            1,
        )
        changes.append("ارتقای نسخه v1.0 → v1.1")

    if not changes:
        changes.append("[skip] PROJECT_GOVERNANCE از قبل به‌روز است")

    return text, changes


# =================================================================
# SECTION C: TASK_BACKLOG.md
# =================================================================


def update_backlog(text: str) -> tuple[str, list[str]]:
    """به‌روزرسانی TASK_BACKLOG.md — افزودن T2.12 + IN-PROGRESS برای T2.11."""
    changes = []

    # 1) T2.11 — تغییر از TODO به IN-PROGRESS
    t211_old = (
        "| T2.11 | ادغام قوانین #۲۷-#۳۲ در سند جامع | 📋 TODO | "
        "atomic update لازم در ابتدای چت ۷ |"
    )
    t211_new = (
        "| T2.11 | ادغام قوانین #۲۳-#۳۲ در سند جامع (Atomic Update) | "
        "🚧 IN-PROGRESS | در حال انجام در چت ۷ — اسکریپت‌های 47+48 |"
    )
    if t211_old in text:
        text = text.replace(t211_old, t211_new, 1)
        changes.append("T2.11 → IN-PROGRESS (با scope توسعه‌یافته به #۲۳-#۳۲)")
    elif t211_new in text:
        changes.append("[skip] T2.11 از قبل IN-PROGRESS است")

    # 2) افزودن T2.12 بعد از T2.11
    t212_marker = "T2.12"
    if t212_marker not in text:
        # Anchor: ردیف T2.11 (هر کدام از حالات بالا)
        if "| T2.11 |" in text:
            # پیدا کردن خط T2.11 و افزودن خط T2.12 بعد از آن
            lines = text.split("\n")
            new_lines = []
            for ln in lines:
                new_lines.append(ln)
                if ln.startswith("| T2.11 |"):
                    new_lines.append(
                        "| T2.12 | ارزیابی و مهاجرت به Claude Code / GitHub MCP "
                        "workflow | 📋 TODO | بحث در چت ۷ — اجرای واقعی در چت "
                        "۱۰+ یا فاز ۱ — جزئیات در Tier 3 |"
                    )
            text = "\n".join(new_lines)
            changes.append("افزودن T2.12 (Claude Code / GitHub MCP migration)")
        else:
            changes.append("[warn] انکر T2.11 پیدا نشد — T2.12 افزوده نشد")
    else:
        changes.append("[skip] T2.12 از قبل موجود است")

    # 3) به‌روزرسانی آمار
    stats_old = "| Tier 2 | 11 | 4 | 7 (T2.05-T2.09 + T2.10 + T2.11) |"
    stats_new = "| Tier 2 | 12 | 4 | 8 (T2.05-T2.09 + T2.10 + T2.11 + T2.12) |"
    if stats_old in text:
        text = text.replace(stats_old, stats_new, 1)
        changes.append("به‌روزرسانی آمار Tier 2: ۱۱→۱۲")

    # کل آمار
    total_old = "| **مجموع** | **65** | **20** | **45** |"
    total_new = "| **مجموع** | **66** | **20** | **46** |"
    if total_old in text:
        text = text.replace(total_old, total_new, 1)
        changes.append("به‌روزرسانی آمار کل: ۶۵→۶۶")

    # 4) Bump version Backlog
    backlog_v_old = "**نسخه این Backlog:** v1.2 (2026-05-17 — پایان چت ۶)"
    backlog_v_new = "**نسخه این Backlog:** v1.3 (2026-05-18 — در میانه چت ۷، مرحله A)"
    if backlog_v_old in text:
        text = text.replace(backlog_v_old, backlog_v_new, 1)
        changes.append("ارتقای نسخه Backlog v1.2 → v1.3")

    if not changes:
        changes.append("[skip] TASK_BACKLOG از قبل به‌روز است")

    return text, changes


# =================================================================
# SECTION D: CHAT_LOG.md — یکپارچه‌سازی شمارش
# =================================================================

# تغییرات شمارش:
#   چت ۵ (part04-theme-engine)           → چت ۵.الف
#   چت ۶ (part05-ui-polish-and-governance) → چت ۵.ب
#   چت ۷ (part06-quality-hardening)        → چت ۶
# این چت (part07-quality-hardening-continued) → چت ۷ — در فاز ۳ افزوده می‌شود

CHATLOG_RENUMBER_MAP = [
    # (old, new, کجا)
    # فهرست
    (
        "- [چت ۵ — phase0-part04-theme-engine](#چت-۵--phase0-part04-theme-engine) ",
        "- [چت ۵.الف — phase0-part04-theme-engine](#چت-۵الف--phase0-part04-theme-engine) ",
    ),
    (
        "- [چت ۶ — phase0-part05-ui-polish-and-governance](#چت-۶--phase0-part05-ui-polish-and-governance)",
        "- [چت ۵.ب — phase0-part05-ui-polish-and-governance](#چت-۵ب--phase0-part05-ui-polish-and-governance)",
    ),
    (
        "- [چت ۷ — phase0-part06-quality-hardening](#چت-۷--phase0-part06-quality-hardening) ← این چت",
        "- [چت ۶ — phase0-part06-quality-hardening](#چت-۶--phase0-part06-quality-hardening)",
    ),
    # heading ها
    (
        "## چت ۵ — phase0-part04-theme-engine",
        "## چت ۵.الف — phase0-part04-theme-engine",
    ),
    (
        "## چت ۶ — phase0-part05-ui-polish-and-governance",
        "## چت ۵.ب — phase0-part05-ui-polish-and-governance",
    ),
    (
        "## چت ۷ — phase0-part06-quality-hardening",
        "## چت ۶ — phase0-part06-quality-hardening",
    ),
]


def update_chatlog(text: str) -> tuple[str, list[str]]:
    """یکپارچه‌سازی شمارش چت‌ها در CHAT_LOG."""
    changes = []

    # Idempotency check: اگر «چت ۵.الف» موجود است، skip
    if "## چت ۵.الف — phase0-part04-theme-engine" in text:
        return text, ["[skip] شمارش چت‌ها از قبل یکپارچه شده"]

    # اعمال renamings
    for old, new in CHATLOG_RENUMBER_MAP:
        if old in text:
            text = text.replace(old, new, 1)
            changes.append(f"replace: {old[:60]}...")
        else:
            changes.append(f"[warn] انکر پیدا نشد: {old[:60]}...")

    # افزودن یادداشت در ابتدا
    note_marker = "## ⚠️ یادداشت یکپارچه‌سازی شمارش (v1.1 — چت ۷)"
    if note_marker not in text:
        note_block = """## ⚠️ یادداشت یکپارچه‌سازی شمارش (v1.1 — چت ۷)

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
        # افزودن قبل از "## راهنمای استفاده"
        guide_anchor = "## راهنمای استفاده"
        if guide_anchor in text:
            text = text.replace(guide_anchor, note_block + guide_anchor, 1)
            changes.append("افزودن یادداشت یکپارچه‌سازی شمارش در ابتدا")

    # Bump version CHAT_LOG: v1.0 → v1.1
    chatlog_v_old = "**نسخه این Log:** v1.0 (2026-05-17)"
    chatlog_v_new = "**نسخه این Log:** v1.1 (2026-05-18) — یکپارچه‌سازی شمارش چت‌ها در میانه چت ۷"
    if chatlog_v_old in text:
        text = text.replace(chatlog_v_old, chatlog_v_new, 1)
        changes.append("ارتقای نسخه CHAT_LOG v1.0 → v1.1")

    return text, changes


# =================================================================
# SECTION E: SESSION_STATUS.md
# =================================================================


def update_session(text: str) -> tuple[str, list[str]]:
    """به‌روزرسانی SESSION_STATUS.md — یکپارچه‌سازی شمارش."""
    changes = []

    # نکته: SESSION_STATUS فعلی مربوط به پایان چت ۶ است.
    # در فاز ۳ این چت (چت ۷)، فایل کاملاً بازنویسی می‌شود.
    # در مرحله A، فقط یک یادداشت اضافه می‌کنیم که این فایل برای چت ۶ است.

    note_marker = "**یادداشت چت ۷:**"
    if note_marker in text:
        return text, ["[skip] یادداشت چت ۷ از قبل افزوده شده"]

    note_block = """
> ⚠️ **یادداشت چت ۷:** این فایل وضعیت **پایان چت ۶** را نشان می‌دهد. در پایان چت ۷ (با تأیید صریح کاربر طبق قانون #۲۷)، این فایل بازنویسی می‌شود.

"""

    # افزودن بعد از خط «**آخرین به‌روزرسانی:** 2026-05-17 (پایان چت ۶)»
    anchor = "**آخرین به‌روزرسانی:** 2026-05-17 (پایان چت ۶)"
    if anchor in text:
        text = text.replace(anchor, anchor + "\n" + note_block, 1)
        changes.append("افزودن یادداشت موقت برای چت ۷")
    else:
        changes.append("[warn] انکر SESSION_STATUS پیدا نشد")

    if not changes:
        changes.append("[skip] SESSION_STATUS از قبل به‌روز است")

    return text, changes


# =================================================================
# Main
# =================================================================

UPDATERS = [
    ("CLAUDE_CHECKLIST.md", CHECKLIST, update_checklist),
    ("PROJECT_GOVERNANCE.md", GOVERNANCE, update_governance),
    ("TASK_BACKLOG.md", BACKLOG, update_backlog),
    ("CHAT_LOG.md", CHATLOG, update_chatlog),
    ("SESSION_STATUS.md", SESSION, update_session),
]


def main() -> int:
    print("=" * 64)
    print("  48_atomic_governance_update — Atomic Update قوانین #۲۳-#۳۲")
    print("=" * 64)
    print()

    any_failure = False
    total_changes = 0

    for name, path, updater in UPDATERS:
        if not path.exists():
            print(f"❌ فایل پیدا نشد: {name}")
            any_failure = True
            continue

        original = path.read_text(encoding="utf-8")
        try:
            new_text, changes = updater(original)
        except RuntimeError as e:
            print(f"❌ خطا در {name}: {e}")
            any_failure = True
            continue

        written = write_if_changed(path, new_text)
        status = "✏️ updated" if written else "✓ no-op"
        print(f"{status}  {name}")
        for ch in changes:
            print(f"           - {ch}")
            if not ch.startswith("[skip]") and not ch.startswith("[warn]"):
                total_changes += 1
        print()

    print("=" * 64)
    if any_failure:
        print(f"❌ FAILED — حداقل یک فایل دچار خطا شد")
        print("=" * 64)
        return 1
    print(f"✅ Atomic Update موفق — {total_changes} تغییر اعمال شد")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    sys.exit(main())
