# -*- coding: utf-8 -*-
"""
55_create_v2_11.py - Atomic Update v2.10 -> v2.11

Builds docs/سند_جامع_v2_11.md from docs/سند_جامع_v2_10.md by applying
7 string-based edits to integrate:
  - 4 new rules (#62-#65) in section 1.9 (UX hardening)
  - 1 new lesson (M63) in section 18.2 (handoff status discipline)
  - New "Changes v2.10 -> v2.11" section at top
  - Updated TOC, header, version line, footer

Compliance:
  - Rule #24 (No-Deletion): v2.10 file is NOT touched
  - Rule #30 (Idempotent): re-running produces identical output
  - Rule #37 (read-back verify): verifies output after write
  - Rule #46 (ASCII-only in print): no Unicode in stdout

Usage:
  python scripts/55_create_v2_11.py
"""
import sys
from pathlib import Path

# ---- Encoding setup (rule #46, M9) ----
try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass  # Python < 3.7 fallback (not expected on 3.11)


# ---- Paths (relative to script location) ----
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
SOURCE = DOCS_DIR / "سند_جامع_v2_10.md"
TARGET = DOCS_DIR / "سند_جامع_v2_11.md"


# ============================================================
# EDIT DEFINITIONS
# ============================================================

# --- Edit 1: Header ---
EDIT_1_OLD = "# سامانه هوشمند ترید — سند جامع v2.10"
EDIT_1_NEW = "# سامانه هوشمند ترید — سند جامع v2.11"

# --- Edit 2: Version line ---
EDIT_2_OLD = "📅 نسخه ۲.۱۰ — اردیبهشت ۱۴۰۵ (May 2026)"
EDIT_2_NEW = "📅 نسخه ۲.۱۱ — اردیبهشت ۱۴۰۵ (May 2026)"

# --- Edit 3: TOC entry ---
EDIT_3_OLD = "- [**خلاصه تغییرات v2.9 → v2.10 🆕**](#خلاصه-تغییرات-v29--v210)"
EDIT_3_NEW = (
    "- [**خلاصه تغییرات v2.10 → v2.11 🆕**](#خلاصه-تغییرات-v210--v211)\n"
    "- [خلاصه تغییرات v2.9 → v2.10](#خلاصه-تغییرات-v29--v210)"
)

# --- Edit 4: New "Changes v2.10 -> v2.11" section ---
EDIT_4_OLD = "# 📋 خلاصه تغییرات v2.9 → v2.10"
EDIT_4_NEW = """# 📋 خلاصه تغییرات v2.10 → v2.11

این نسخه یک **Atomic Update + UX Hardening** طبق قانون #۲۶ است. حاصل چت ۸ (`TRADING-phase0-part08-pre-phase1-setup`) و چت ۹ (`TRADING-phase1-part01-ccxt-websocket-setup`) که قوانین UX کشف‌شده در پایان چت ۸ + درس M63 (ابتدای چت ۹) را به‌صورت رسمی ادغام می‌کند.

## دستاوردهای ساختاری

- **چهار قانون UX جدید (#۶۲-۶۵)** که سبک تعامل Claude-کاربر را به نقطه پایدارتری می‌رساند
- **یک درس جدید (M63)** درباره مدیریت status صریح در handoff
- **حل ریشه‌ای ابهام handoff** — هر گام آینده با prefix صریح (✅ DONE / 📋 TODO / ⚠️ CHECK / 💡 NOTE) همراه است

## قوانین رفتاری جدید Claude (#۶۲ تا #۶۵)

- **#۶۲** ⭐: **فایل handoff دائمی** — در پایان هر چت، فایل `claude_workspace/incoming_permanent/CHAT{N+1}_HANDOFF.txt` ساخته شود. متن inline تنها کافی نیست (M58). هر آیتم باید با یکی از prefix های `✅ DONE`، `📋 TODO`، `⚠️ CHECK`، `💡 NOTE` همراه باشد (افزوده در v2.11 بر اساس M63).
- **#۶۳** ⭐: **Convention `🟢 ▶️ EXECUTE`** — هر گام اجرایی که نیاز به copy-paste/اجرای فرمان توسط کاربر دارد، با تیتر سبز `## 🟢 ▶️ EXECUTE — اقدام لازم` شروع می‌شود + شامل نام tab + رنگ tab مطابق قانون #۳۱. هدف: تشخیص بصری سریع تفاوت بین «توضیح» و «اقدام لازم».
- **#۶۴** ⭐: **عدم نمایش جزئیات تصحیح خطای کد** — وقتی کد به خطا می‌خورد، Claude (الف) علت را در ذهن خود بررسی می‌کند (ب) **توضیحات «چرا خطا داد» و «چطور تشخیص دادم» را به کاربر نشان نمی‌دهد** (ج) فقط گام اجرایی کد اصلاحی را با Convention #۶۳ ارائه می‌دهد. استثنا: گزارش کارها، درس M-numbered، توضیح معماری.
- **#۶۵** ⭐: **ثبت درس از اشتباهات با نمایش** — درس کلی (M-numbered) به کاربر **نمایش داده می‌شود** (نه پنهان). تفاوت با #۶۴: درس **چه** آموختیم → نمایش، **چرا** خطا داد و **چطور** تشخیص → پنهان.

## درس‌نامه جدید (M63)

- **M63:** **فرض نکردن وضعیت کارهای infrastructure در handoff** — اگر در handoff موردی ذکر شده ولی status صریح ندارد، Claude باید بپرسد، نه فرض کند. خصوصاً برای کارهای خارج فایل‌سیستم پروژه (Project در Claude Desktop، GitHub settings، Connectors، ...). کشف شد در ابتدای چت ۹.

## فلسفه این نسخه — تثبیت سبک تعامل

- **پیش از v2.11:** سبک تعامل Claude در هر چت ممکن بود از چت قبل متفاوت باشد (پیچیده‌تر یا ساده‌تر، با جزئیات بیش از حد یا کمتر از نیاز).
- **پس از v2.11:** سبک تعامل با ۴ قانون UX به نقطه پایدار می‌رسد — کاربر می‌داند **انتظار** چه فرمتی را داشته باشد.

🔒 **هیچ بخش قبلی حذف نشد** — تمام قوانین v2.10 و درس‌های M1-M62 و بخش‌های ۱-۲۵ دست‌نخورده ماندند. این نسخه فقط افزایش است.

## بدون تغییر در:

- سند ۲-۲۵ — معماری، DB، API، UI، امنیت، Roadmap، MCP، Claude Desktop config، Skills
- درس‌نامه v2.10 (M1-M62) — تماماً حفظ شده
- قوانین v2.10 (#۱-۶۱) — تماماً حفظ شده

---

# 📋 خلاصه تغییرات v2.9 → v2.10"""

# --- Edit 5: Rules #62-#65 in table 1.9 ---
EDIT_5_OLD = "| **۶۱ ⭐ 🆕 v2.10** | **پیشنهاد گزینه مطلوب در چندگزینه‌ای** -- وقتی Claude سؤال چندگزینه‌ای می‌پرسد، باید پیشنهاد مطلوب خود را صریح بگوید: گزینه‌ای که از نظر حرفه‌ای، انسجام پروژه، و بلندمدت بهتر است. شامل A/B/C، رتبه‌بندی، multi-select، و درخواست‌های open-ended. | چت ۸ |"
EDIT_5_NEW = """| **۶۱ ⭐ 🆕 v2.10** | **پیشنهاد گزینه مطلوب در چندگزینه‌ای** -- وقتی Claude سؤال چندگزینه‌ای می‌پرسد، باید پیشنهاد مطلوب خود را صریح بگوید: گزینه‌ای که از نظر حرفه‌ای، انسجام پروژه، و بلندمدت بهتر است. شامل A/B/C، رتبه‌بندی، multi-select، و درخواست‌های open-ended. | چت ۸ |
| **۶۲ ⭐ 🆕 v2.11** | **فایل handoff دائمی پایان چت** -- در پایان هر چت، فایل `claude_workspace/incoming_permanent/CHAT{N+1}_HANDOFF.txt` ساخته شود. متن inline در پیام چت به تنهایی کافی نیست (مشکل کشف‌شده در پایان چت ۸، M58). هر آیتم در فایل handoff باید با یکی از prefix های `✅ DONE` (انجام شده در چت قبل)، `📋 TODO` (کار آینده در چت بعد)، `⚠️ CHECK` (نیاز به تأیید/بررسی توسط کاربر در شروع چت بعد)، یا `💡 NOTE` (یادآوری/اطلاع، نه عمل) همراه باشد. این prefix ها در v2.11 بر اساس M63 افزوده شد. | چت ۸ + ۹ |
| **۶۳ ⭐ 🆕 v2.11** | **Convention بصری برای گام‌های اجرایی** -- هر گام اجرایی که نیاز به کپی-پیست/اجرای فرمان توسط کاربر دارد، با تیتر سبز `## 🟢 ▶️ EXECUTE — اقدام لازم` شروع می‌شود + شامل نام tab + رنگ tab مطابق قانون #۳۱. هدف: تشخیص بصری سریع تفاوت بین «توضیح» و «اقدام لازم». | چت ۸ |
| **۶۴ ⭐ 🆕 v2.11** | **عدم نمایش جزئیات تصحیح خطای کد** -- وقتی کد به خطا می‌خورد، Claude (الف) علت را در ذهن خود بررسی می‌کند (ب) **توضیحات «چرا خطا داد» و «چطور تشخیص دادم» را به کاربر نشان نمی‌دهد** (ج) فقط گام اجرایی کد اصلاحی را با Convention #۶۳ ارائه می‌دهد. استثناها (توضیح کامل لازم است): گزارش کارهای انجام‌شده، گزارش کارهای آینده، درس‌های M-numbered (بخش ۱۸)، توضیحات معماری و تصمیمات. | چت ۸ |
| **۶۵ ⭐ 🆕 v2.11** | **ثبت درس از اشتباهات با نمایش به کاربر** -- وقتی Claude اشتباهی می‌کند که منجر به ثبت درس عمومی می‌شود (M-numbered در بخش ۱۸)، (الف) درس را در `docs/PENDING_FOR_NEXT_VERSION.md` ثبت کند (برای ادغام بعدی) (ب) **درس کلی را به کاربر نمایش دهد** (نه جزئیات تشخیص) (ج) فرمت نمایش: «📌 درس جدید (M{N}): [درس کلی در یک جمله]». تفاوت با #۶۴: #۶۴ پنهان می‌کند «چرا/چطور خطا داد»، #۶۵ نمایش می‌دهد «چه آموختیم». | چت ۸ |"""

# --- Edit 6: M63 in section 18 table ---
EDIT_6_OLD = "| **M62** | Claude در پیامی قانون #۳۷ را ذکر کرد، ولی در پاسخ بعدی همان چت کاربر باید یادآوری کند که read-back لازم است. | قوانینی که خود Claude ذکر می‌کند priority پایین‌تر از یادآوری کاربر می‌گیرند (نقض self-enforcement). | قوانینی که در همان چت توسط Claude ذکر می‌شوند، باید **خودکار** در باقی همان چت اجرا شوند. self-binding: اگر Claude قانونی را ذکر کند، در همان چت ملزم به اجرای آن است. (چت ۸) |"
EDIT_6_NEW = """| **M62** | Claude در پیامی قانون #۳۷ را ذکر کرد، ولی در پاسخ بعدی همان چت کاربر باید یادآوری کند که read-back لازم است. | قوانینی که خود Claude ذکر می‌کند priority پایین‌تر از یادآوری کاربر می‌گیرند (نقض self-enforcement). | قوانینی که در همان چت توسط Claude ذکر می‌شوند، باید **خودکار** در باقی همان چت اجرا شوند. self-binding: اگر Claude قانونی را ذکر کند، در همان چت ملزم به اجرای آن است. (چت ۸) |
| **M63** ⭐ 🆕 v2.11 | Claude در ابتدای چت ۹ فرض کرد «ساخت Project در Claude Desktop» انجام نشده، چون در پیام handoff به‌عنوان «اولین گام» ذکر شده بود — درحالی‌که کاربر قبلاً ساخته بود. | پیام handoff کارهای آینده + کارهای انجام‌شده + یادآوری‌ها را در یک لیست ترکیب می‌کند، بدون status صریح (DONE/PENDING/TODO). Claude مجبور به استنتاج می‌شود — و گاهی اشتباه استنتاج می‌کند. | هر آیتم در پیام handoff باید با یکی از prefix های صریح همراه باشد: `✅ DONE`، `📋 TODO`، `⚠️ CHECK`، `💡 NOTE`. خصوصاً برای کارهایی که خارج از فایل‌سیستم پروژه انجام می‌شوند (Project در Claude Desktop، GitHub settings، Connectors، ...). افزوده در قانون #۶۲ نسخه v2.11. (چت ۹) |"""

# --- Edit 7: Footer ---
EDIT_7_OLD = """**📌 پایان سند جامع v2.10**

این سند زنده است. تغییرات بعدی همراه با شماره نسخه جدید (v2.11, v2.12, ...) و یادداشت دقیق تغییرات اعمال خواهد شد.

**نسخه:** 2.10 — اردیبهشت ۱۴۰۵ (May 2026)
**حاصل چت:** ۸ (`TRADING-phase0-part08-pre-phase1-setup`)
**قوانین:** ۶۱ (با ۲ Reserved)
**درس‌نامه:** ۶۲ ردیف ثبت شده (با ۲۵ Reserved)
**بخش‌های جدید:** ۴ (سند ۲۲-۲۵)
**سیاست:** No-Deletion + Conservative Numbering + PENDING-EOC در لحظه ثبت"""
EDIT_7_NEW = """**📌 پایان سند جامع v2.11**

این سند زنده است. تغییرات بعدی همراه با شماره نسخه جدید (v2.12, v2.13, ...) و یادداشت دقیق تغییرات اعمال خواهد شد.

**نسخه:** 2.11 — اردیبهشت ۱۴۰۵ (May 2026)
**حاصل چت:** ۸ + ۹ (`TRADING-phase0-part08-pre-phase1-setup` + `TRADING-phase1-part01-ccxt-websocket-setup`)
**قوانین:** ۶۵ (با ۲ Reserved: #۵۲، #۵۳)
**درس‌نامه:** ۶۳ ردیف ثبت شده (با ۲۵ Reserved)
**بخش‌های:** ۲۵ (بدون افزایش — قوانین جدید در بخش ۱.۹ و درس در بخش ۱۸)
**سیاست:** No-Deletion + Conservative Numbering + PENDING-EOC در لحظه ثبت + UX hardening"""


# ============================================================
# MAIN
# ============================================================

EDITS = [
    ("Header v2.10 -> v2.11", EDIT_1_OLD, EDIT_1_NEW),
    ("Version line 2.10 -> 2.11", EDIT_2_OLD, EDIT_2_NEW),
    ("TOC entry", EDIT_3_OLD, EDIT_3_NEW),
    ("New 'Changes v2.10 -> v2.11' section", EDIT_4_OLD, EDIT_4_NEW),
    ("Rules #62-#65 in table 1.9", EDIT_5_OLD, EDIT_5_NEW),
    ("Lesson M63 in section 18.2", EDIT_6_OLD, EDIT_6_NEW),
    ("Footer v2.10 -> v2.11", EDIT_7_OLD, EDIT_7_NEW),
]


def main():
    print("=" * 60)
    print("  55_create_v2_11.py - Atomic Update v2.10 -> v2.11")
    print("=" * 60)
    print()

    # --- 1. Check source exists ---
    if not SOURCE.exists():
        print("[FAIL] Source file not found:")
        print("       " + str(SOURCE))
        return 1
    print("[OK] Source found: " + SOURCE.name)

    # --- 2. Read source ---
    content = SOURCE.read_text(encoding="utf-8")
    source_size = len(content)
    print("[OK] Source loaded: " + str(source_size) + " chars")
    print()

    # --- 3. Apply edits ---
    print("Applying " + str(len(EDITS)) + " edits:")
    print("-" * 60)
    for i, (name, old, new) in enumerate(EDITS, 1):
        count = content.count(old)
        if count == 0:
            print("[FAIL] Edit " + str(i) + " (" + name + "): old text not found")
            print("       old text preview: " + repr(old[:80]) + "...")
            return 1
        if count > 1:
            print(
                "[FAIL] Edit "
                + str(i)
                + " ("
                + name
                + "): old text matched "
                + str(count)
                + " times (must be unique)"
            )
            return 1
        content = content.replace(old, new, 1)
        delta = len(new) - len(old)
        sign = "+" if delta >= 0 else ""
        print("[OK] Edit " + str(i) + ": " + name + " (delta " + sign + str(delta) + " chars)")

    new_size = len(content)
    print("-" * 60)
    print(
        "[OK] All "
        + str(len(EDITS))
        + " edits applied. New size: "
        + str(new_size)
        + " chars (delta "
        + ("+" if new_size >= source_size else "")
        + str(new_size - source_size)
        + ")"
    )
    print()

    # --- 4. Write target ---
    # Use newline='\n' for git consistency
    TARGET.write_text(content, encoding="utf-8", newline="\n")
    print("[OK] Wrote target: " + TARGET.name)

    # --- 5. Read-back verify (rule #37) ---
    actual = TARGET.read_text(encoding="utf-8")
    if actual != content:
        print("[FAIL] Read-back mismatch! Written content differs from in-memory content.")
        print("       in-memory size: " + str(len(content)))
        print("       on-disk   size: " + str(len(actual)))
        return 1
    print("[OK] Read-back verified: target matches in-memory (" + str(len(actual)) + " chars)")
    print()

    # --- 6. Smoke checks on target content ---
    smoke_checks = [
        ("v2.11 header", "# سامانه هوشمند ترید — سند جامع v2.11"),
        ("Rule #62", "**۶۲ ⭐ 🆕 v2.11**"),
        ("Rule #63", "**۶۳ ⭐ 🆕 v2.11**"),
        ("Rule #64", "**۶۴ ⭐ 🆕 v2.11**"),
        ("Rule #65", "**۶۵ ⭐ 🆕 v2.11**"),
        ("Lesson M63", "**M63** ⭐ 🆕 v2.11"),
        ("v2.11 footer", "**📌 پایان سند جامع v2.11**"),
        ("v2.10 preserved (No-Deletion)", "# 📋 خلاصه تغییرات v2.9 → v2.10"),
    ]
    print("Smoke checks:")
    print("-" * 60)
    all_pass = True
    for name, needle in smoke_checks:
        if needle in actual:
            print("[OK] " + name)
        else:
            print("[FAIL] " + name + " (not found: " + repr(needle[:60]) + "...)")
            all_pass = False
    print("-" * 60)

    if not all_pass:
        print("[FAIL] One or more smoke checks failed")
        return 1

    # --- 7. Confirm v2.10 untouched ---
    v210_size_after = SOURCE.stat().st_size
    if v210_size_after != source_size:
        # File size includes encoding; compare via re-reading
        v210_content_after = SOURCE.read_text(encoding="utf-8")
        if len(v210_content_after) != source_size:
            print("[FAIL] Source file v2.10 was modified! (No-Deletion violation)")
            return 1
    print("[OK] No-Deletion respected: v2.10 untouched")
    print()

    print("=" * 60)
    print("SUCCESS - v2.11 created and verified")
    print("=" * 60)
    print()
    print("Output file: " + str(TARGET))
    print("Size: " + str(new_size) + " chars (was " + str(source_size) + " in v2.10)")
    print()
    print("Next steps:")
    print("  1. Run smoke tests:   python scripts/55b_test_v2_11.py")
    print("  2. Verify visually:   open " + TARGET.name + " in editor")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
