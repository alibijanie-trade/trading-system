# -*- coding: utf-8 -*-
"""
47_upgrade_doc_to_v28.py — ارتقای سند جامع v2.7 → v2.8

تغییرات این ارتقا (Session 7 / چت ۷):
  1. افزودن ۱۰ ردیف جدید به جدول ۱.۹ (قوانین قفل‌شده):
     - #۲۳-#۲۶ از v2.7 (قبلاً فقط در سند ۱۶ توضیح داشتند، به جدول راه نیافتند)
     - #۲۷-#۳۲ کشف‌شده در چت ۶ (Session 6) — حالا formal می‌شوند
  2. افزودن بخش «خلاصه تغییرات v2.7 → v2.8» در ابتدا
  3. به‌روزرسانی header (نسخه ۲.۷ → ۲.۸)
  4. افزودن لینک‌های جدید به فهرست مطالب
  5. قانون #۲۴ (No-Deletion): سند v2.7 دست‌نخورده باقی می‌ماند.

روش: فایل v2.7 خوانده می‌شود، patch زده می‌شود، خروجی در v2.8 ذخیره می‌شود.

Idempotent: اجرای دوم تغییری ایجاد نمی‌کند.

استفاده:
  python scripts\\47_upgrade_doc_to_v28.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# ---------- مسیرها ----------
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "سند_جامع_v2_7.md"
DST = ROOT / "docs" / "سند_جامع_v2_8.md"

# ---------- متن قوانین جدید برای جدول ۱.۹ ----------
NEW_RULES_BLOCK = """| **۲۳ 🆕 v2.7** | **به‌روزرسانی CHAT_LOG.md در پایان هر چت** — Claude موظف است در پایان هر چت یک بخش جدید به `docs/CHAT_LOG.md` اضافه کند با گام‌ها، اسکریپت‌ها، Bugها و تصمیمات. (جزئیات: سند ۱۶.۲) |
| **۲۴ 🆕 v2.7** | **No-Deletion در سند جامع** — حذف بخش‌ها ممنوع. در صورت منسوخ‌شدن، علامت `[منسوخ — vX.Y]` با ارجاع به جایگزین. (جزئیات: سند ۱۶.۳) |
| **۲۵ 🆕 v2.7** | **چک‌لیست اجباری شروع چت (۸ مرحله)** — Claude در شروع هر چت ۸ مرحله فاز ۱ `CLAUDE_CHECKLIST.md` را اجرا می‌کند: بازشناسی پیوست → استخراج zip → خواندن اسناد → بررسی محیط → درک Bugها → تعیین Tier → گزارش آمادگی → صبر برای تأیید. (جزئیات: سند ۱۶.۴) |
| **۲۶ 🆕 v2.7** | **Atomic Updates** — قانون جدید باید **در یک نوبت** در همه اسناد مرتبط ادغام شود: سند جامع + CHAT_LOG + PROJECT_GOVERNANCE + TASK_BACKLOG. در غیر این صورت، فاجعه آینده. (جزئیات: سند ۱۶.۶) |
| **۲۷ 🆕 v2.8** | **تأیید صریح کاربر برای پایان چت** — Claude **هرگز** فرآیند پایان چت (۱۲ مرحله فاز ۳) را خودکار شروع نمی‌کند. تأییدیه‌های صریح: «چت رو ببند»، «end of chat»، «zip نهایی بساز و چت رو ببند». جملاتی مثل «گام بعدی چیست؟» تأییدیه نیستند. استثنا: نزدیک‌شدن به سقف context window — با هشدار قبلی. |
| **۲۸ 🆕 v2.8** | **کوتاه گفتن خطا** — وقتی کد به خطا می‌خورد، **فقط اقدامات اجرایی** که کاربر باید انجام دهد گفته شود — بدون توضیحات فنی طولانی درباره علت یا روش تشخیص. ❌ «این خطا به این دلیل است که...»  ✅ «این دستور را بزنید: [دستور]». |
| **۲۹ 🆕 v2.8** | **ارائه فایل با Artifact یا code block** — فایل‌های ساخت/اصلاح **همیشه** به‌صورت Artifact یا code block با دکمه Copy ارائه شوند. paste متن خام برای copy دستی در Notepad ممنوع است. برای Python script ها، Artifact پشتیبانی نمی‌شود ولی code block استاندارد قابل قبول است. (تکمیل و توسعه قانون #۱۴) |
| **۳۰ 🆕 v2.8** | **اصلاحات کوچک فایل = اسکریپت Python idempotent** — برای اصلاح روی فایل موجود (افزودن خط، تغییر مقدار، fix کوچک)، اسکریپت Python ساخته شود — نه دستور دستی. اسکریپت **باید idempotent** باشد (اجرای دوم تغییری ندهد). |
| **۳۱ 🆕 v2.8** | **شماره tab + رنگ tab بالای هر کادر کد** — بالای هر کادر کد، **هم شماره tab و هم رنگ tab** ذکر شود. رنگ‌بندی پیش‌فرض ۴ tab: 🟦 tab «1 backend» (سرور+تست backend+venv، پوشه `backend/`) / 🟩 tab «2 scripts» (اسکریپت‌های Python، پروژه root) / 🟧 tab «3 frontend» (React+تست frontend، پوشه `frontend/`) / 🟥 tab «4 BACKUP» (git+backup+sync، پروژه root). (توسعه قانون #۱۷) |
| **۳۲ 🆕 v2.8** | **npm install در ایران: روش قطعی** — به دلیل فیلتر `registry.npmjs.org` در ایران: `npm config set registry https://registry.npmmirror.com/` + flags `--no-audit --no-fund --prefer-offline`. زمان نصب ۱۴۸ پکیج با این روش: **۱ دقیقه** (تست‌شده 2026-05-17). اسکریپت `00b_post_unzip_setup.py` راه fallback خودکار دارد. |"""

# ---------- بخش «خلاصه تغییرات v2.7 → v2.8» ----------
V28_CHANGELOG_SECTION = """# 📋 خلاصه تغییرات v2.7 → v2.8

این نسخه شامل **۶ قانون رفتاری جدید** (#۲۷-#۳۲) + **یکپارچه‌سازی ۴ قانون قبلی** (#۲۳-#۲۶ که در v2.7 فقط در سند ۱۶ توضیح داشتند) + **بدون Bug Fix یا تصمیم معماری جدید** است.

این نسخه یک **ارتقای رفتاری Governance** است: قوانین کشف‌شده در چت ۶ (`phase0-part06-quality-hardening`) به‌صورت formal در جدول ۱.۹ ثبت می‌شوند تا Claude های آینده آن‌ها را به‌عنوان قانون قفل‌شده ببینند.

## دستاوردهای Session 7 (این چت — `phase0-part07-quality-hardening-continued`)

- **مرحله A:** Atomic Update قوانین #۲۳-#۳۲ در جدول ۱.۹ (این ارتقا)
- **مرحله B:** ادامه Tier 2 — T2.05 (Git workflow) → T2.09 (API_DOCS)
- یکپارچه‌سازی شمارش چت‌ها در همه اسناد (چت ۵ = ۵.الف + ۵.ب، چت ۶ = part06، چت ۷ = این چت)
- ثبت T2.12 در TASK_BACKLOG: ارزیابی Claude Code / GitHub MCP workflow (Tier 3)

## قوانین رفتاری جدید این نسخه (#۲۷-#۳۲)

این قوانین در چت ۶ کشف شدند ولی به‌صورت formal ادغام نشده بودند. حالا در جدول ۱.۹ ثبت می‌شوند:

- **#۲۷:** تأیید صریح کاربر برای پایان چت (Claude خودکار نبندد)
- **#۲۸:** کوتاه گفتن خطا (فقط اقدامات اجرایی)
- **#۲۹:** ارائه فایل با Artifact یا code block (نه paste متن خام)
- **#۳۰:** اصلاحات کوچک = اسکریپت Python idempotent
- **#۳۱:** شماره + رنگ tab بالای هر کادر کد (🟦 backend / 🟩 scripts / 🟧 frontend / 🟥 BACKUP)
- **#۳۲:** npm install در ایران با registry.npmmirror.com + flags بهینه

## قوانین قبلی (v2.7) که در این نسخه به جدول ۱.۹ افزوده شدند

این قوانین در v2.7 فقط در «سند ۱۶ — مدیریت دانش» شرح داده شدند. در v2.8 برای consistency با بقیه قوانین، به جدول مرکزی ۱.۹ هم اضافه شدند:

- **#۲۳:** به‌روزرسانی CHAT_LOG.md در پایان هر چت
- **#۲۴:** No-Deletion در سند جامع
- **#۲۵:** چک‌لیست اجباری شروع چت (۸ مرحله)
- **#۲۶:** Atomic Updates (قانون جدید در یک نوبت در همه اسناد)

## فایل‌های متأثر در این چت

- `docs/سند_جامع_v2_8.md` (جدید)
- `docs/CLAUDE_CHECKLIST.md` (ادغام در فازهای ۲ و ۳)
- `docs/PROJECT_GOVERNANCE.md` (جدول قوانین قفل‌شده)
- `docs/TASK_BACKLOG.md` (افزودن T2.12 + علامت T2.11 IN-PROGRESS)
- `docs/CHAT_LOG.md` (یکپارچه‌سازی شمارش چت‌ها)
- `docs/SESSION_STATUS.md` (یکپارچه‌سازی شمارش)

## هیچ‌چیز حذف نشد — قانون #۲۴ No-Deletion

- `docs/سند_جامع_v2_7.md` دست‌نخورده باقی می‌ماند (مرجع تاریخی)
- `docs/سند_جامع_v2_6.md` همچنان موجود است (مرجع تاریخی)

---

"""


# ---------- توابع کمکی ----------
def write_if_changed(path: Path, content: str) -> bool:
    """فقط اگر محتوا تغییر کرده باشد، می‌نویسد. خروجی: آیا نوشته شد؟"""
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if existing == content:
            return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def upgrade_to_v28(src_text: str) -> str:
    """اعمال patches روی متن v2.7 و تولید متن v2.8."""
    text = src_text

    # 1) Header: v2.7 → v2.8
    if "# سامانه هوشمند ترید — سند جامع v2.7" not in text:
        raise RuntimeError("Header v2.7 در فایل منبع پیدا نشد!")
    text = text.replace(
        "# سامانه هوشمند ترید — سند جامع v2.7",
        "# سامانه هوشمند ترید — سند جامع v2.8",
        1,
    )

    if "نسخه ۲.۷ — اردیبهشت ۱۴۰۵" not in text:
        raise RuntimeError("شناسه نسخه ۲.۷ پیدا نشد!")
    text = text.replace(
        "📅 نسخه ۲.۷ — اردیبهشت ۱۴۰۵ (May 2026)",
        "📅 نسخه ۲.۸ — خرداد ۱۴۰۵ (May 2026)",
        1,
    )

    # 2) فهرست مطالب — افزودن لینک‌های جدید قبل از v2.5→v2.6
    toc_anchor = "- [**خلاصه تغییرات v2.5 → v2.6 🆕**](#خلاصه-تغییرات-v25--v26)"
    if toc_anchor not in text:
        raise RuntimeError("انکر فهرست مطالب (v2.5→v2.6) پیدا نشد!")
    toc_new = (
        "- [**خلاصه تغییرات v2.7 → v2.8 🆕**](#خلاصه-تغییرات-v27--v28)\n"
        "- [خلاصه تغییرات v2.6 → v2.7](#خلاصه-تغییرات-v26--v27)\n"
        + toc_anchor
    )
    text = text.replace(toc_anchor, toc_new, 1)

    # 3) محتوا — افزودن بخش جدید قبل از «# 📋 خلاصه تغییرات v2.6 → v2.7»
    content_anchor = "# 📋 خلاصه تغییرات v2.6 → v2.7"
    if content_anchor not in text:
        raise RuntimeError("انکر بخش v2.6→v2.7 در محتوا پیدا نشد!")
    text = text.replace(content_anchor, V28_CHANGELOG_SECTION + content_anchor, 1)

    # 4) جدول ۱.۹ — افزودن ۱۰ ردیف جدید بعد از ردیف ۲۲
    # ردیف ۲۲ تنها ردیفی است که با «| **۲۲ 🆕 v2.6**» شروع می‌شود.
    row_22_match = re.search(r"(\| \*\*۲۲ 🆕 v2\.6\*\* \| [^\n]+\|)", text)
    if not row_22_match:
        raise RuntimeError("ردیف ۲۲ در جدول ۱.۹ پیدا نشد!")
    row_22_line = row_22_match.group(1)
    text = text.replace(row_22_line, row_22_line + "\n" + NEW_RULES_BLOCK, 1)

    return text


def main() -> int:
    if not SRC.exists():
        print(f"❌ فایل منبع پیدا نشد: {SRC}")
        return 1

    # idempotent check: اگر v2.8 از قبل کامل است، skip
    if DST.exists():
        existing = DST.read_text(encoding="utf-8")
        if (
            "تأیید صریح کاربر برای پایان چت" in existing
            and "**۳۲ 🆕 v2.8**" in existing
            and "**۲۳ 🆕 v2.7**" in existing
        ):
            print(f"✓ سند v2.8 از قبل به‌روز است: {DST.name}")
            print("  هیچ تغییری اعمال نشد (idempotent).")
            return 0
        else:
            print(f"⚠️ سند v2.8 وجود دارد ولی ناقص است — بازنویسی می‌شود.")

    src_text = SRC.read_text(encoding="utf-8")
    try:
        new_text = upgrade_to_v28(src_text)
    except RuntimeError as e:
        print(f"❌ خطا در ارتقا: {e}")
        return 1

    written = write_if_changed(DST, new_text)
    if written:
        size_kb = len(new_text.encode("utf-8")) // 1024
        line_count = new_text.count("\n") + 1
        print(f"✅ سند v2.8 ساخته شد: {DST.name}")
        print(f"   اندازه: {size_kb} KB | خطوط: {line_count}")
        print(f"   ۱۰ ردیف جدید (#۲۳-#۳۲) به جدول ۱.۹ افزوده شد.")
        print(f"   بخش «خلاصه تغییرات v2.7 → v2.8» در ابتدا افزوده شد.")
        print(f"   سند v2.7 دست‌نخورده باقی ماند (قانون #۲۴ No-Deletion).")
    else:
        print(f"✓ سند v2.8 از قبل کامل بود (no-op).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
