# -*- coding: utf-8 -*-
"""
55_upgrade_doc_to_v29.py -- ارتقای سند جامع v2.8 -> v2.9 (CHAT7 FINALIZE)

تغییرات v2.8 -> v2.9:
  1. Header: v2.8 -> v2.9, ماه: خرداد (June 2026)
  2. ۴ بخش جدید در پایان سند:
     - بخش ۱۸ -- درس‌نامه اشتباهات Claude (M1-M21)
     - بخش ۱۹ -- Claude MAX Real-Time Configuration Guide
     - بخش ۲۰ -- Pre-commit Hooks Philosophy (Hybrid mode)
     - بخش ۲۱ -- اتصال به GitHub در شروع پروژه
  3. ۱۵ ردیف جدید به جدول ۱.۹ (قوانین #۳۳-۴۷)
  4. به‌روزرسانی فهرست مطالب
  5. بلوک changelog v2.8 -> v2.9 قبل از بلوک v2.7 -> v2.8

این اسکریپت idempotent:
  - ورودی: docs/سند_جامع_v2_8.md (دست‌نخورده می‌ماند طبق قانون #۲۴)
  - خروجی: docs/سند_جامع_v2_9.md

استفاده:
  python scripts\\55_upgrade_doc_to_v29.py
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

# UTF-8 stdout
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

ROOT = Path(__file__).resolve().parent.parent
DOC_V28 = ROOT / "docs" / "سند_جامع_v2_8.md"
DOC_V29 = ROOT / "docs" / "سند_جامع_v2_9.md"


# ============================================================
# PATCH 1 -- Header
# ============================================================

HEADER_OLD = """# سامانه هوشمند ترید — سند جامع v2.8"""
HEADER_NEW = """# سامانه هوشمند ترید — سند جامع v2.9"""

DATE_OLD = "📅 نسخه ۲.۸ — اردیبهشت ۱۴۰۵ (May 2026)"
DATE_NEW = "📅 نسخه ۲.۹ — خرداد ۱۴۰۵ (June 2026)"


# ============================================================
# PATCH 2 -- TOC link for v2.8 -> v2.9
# ============================================================

TOC_OLD_LINK = "- [**خلاصه تغییرات v2.7 → v2.8 🆕**](#خلاصه-تغییرات-v27--v28)"
TOC_NEW_LINK = """- [**خلاصه تغییرات v2.8 → v2.9 🆕**](#خلاصه-تغییرات-v28--v29)
- [خلاصه تغییرات v2.7 → v2.8](#خلاصه-تغییرات-v27--v28)"""


# ============================================================
# PATCH 3 -- Changelog block v2.8 -> v2.9
# ============================================================

CHANGELOG_V29_BLOCK = """
# 📋 خلاصه تغییرات v2.8 → v2.9

این نسخه یک **Atomic Update** طبق قانون #۲۶ است که در پایان چت ۷ (`phase0-part07-quality-hardening-continued`) تولید می‌شود.

## محتوای اصلی این نسخه

۱۵ قانون رفتاری جدید (#۳۳-۴۷) که در طول چت‌های ۶ و ۷ از اشتباهات Claude کشف شدند، رسماً در جدول قوانین قفل‌شده (بخش ۱.۹) ادغام می‌شوند. هم‌چنین ۴ بخش جدید (۱۸-۲۱) برای جلوگیری از تکرار اشتباهات، راهنمای استفاده از Claude MAX، فلسفه pre-commit، و اتصال GitHub اضافه می‌شوند.

## ۱۵ قانون جدید (#۳۳-۴۷) -- خلاصه

| # | قانون | کشف در |
|---|---|---|
| **#۳۳** | Backup فقط در پایان چت (نه قبل از هر commit) | چت ۷ |
| **#۳۴** | zip ها در root پروژه دانلود می‌شوند | چت ۷ M2 |
| **#۳۵** | pip flags ≠ npm flags (`--no-audit` فقط npm) | چت ۷ M5 |
| **#۳۶** | verify signature قبل از تست‌نویسی | چت ۷ M6 |
| **#۳۷** | read-back verify بعد از write | چت ۷ M1 |
| **#۳۸** | `.py` تنها → scripts/، zip → root | چت ۷ M8 |
| **#۳۹** | multi-root zip → `python -m zipfile -e` | چت ۷ M4 |
| **#۴۰** | verify argparse syntax قبل از پیشنهاد | چت ۷ M3 |
| **#۴۱** | `.get()` به‌جای `[]` در `or` assertion | چت ۷ M7 |
| **#۴۲** | `--no-verify` با `[skip-hooks: REASON]` | چت ۷ |
| **#۴۳** | Hybrid hook mode: critical اجباری، minor warning | چت ۷ |
| **#۴۴** | `.gitattributes` به‌جای hook برای line ending | چت ۷ M13 |
| **#۴۵** | entry در pre-commit همیشه `python wrapper.py` | چت ۷ M14 |
| **#۴۶** | ASCII-only در print() اسکریپت‌های Windows | چت ۷ M9 |
| **#۴۷** | تست hook روی کل codebase قبل از deploy | چت ۷ M20 |

## بخش‌های جدید این نسخه

این نسخه شامل **۴ بخش جدید** است:

- **بخش ۱۸ — درس‌نامه اشتباهات Claude (M1-M21)** -- ثبت ۲۱ اشتباه شناسایی‌شده با علت ریشه‌ای + راه‌حل
- **بخش ۱۹ — Claude MAX Real-Time Configuration Guide** -- راهنمای انتخاب Model و تنظیمات بر اساس فاز
- **بخش ۲۰ — Pre-commit Hooks Philosophy (Hybrid mode)** -- توجیه طراحی Hybrid و trade-offs
- **بخش ۲۱ — اتصال به GitHub در شروع پروژه** -- چک‌لیست + commands

## Task های DONE شده در چت ۷

- **T2.05** -- Git Workflow doc + tests (commit `4a17f0a`)
- **T2.09** -- API Docs (6 endpoints) (commit `5b6d8d4`)
- **T2.07** -- Anti-Patterns A1-A10 (commit `409cab9`)
- **T2.08** -- Backend pytest + 25 smoke tests (commit `32e85f4`)
- **T2.06** -- Pre-commit hooks Hybrid mode (commit `532fc9f`)
- **T2.11** -- Atomic update rules #23-32 (commit `91704ca`)

## آمار

- تعداد قوانین قفل‌شده: ۳۲ → **۴۷** (+۱۵)
- تعداد بخش‌های سند: ۱۷ → **۲۱** (+۴)
- درس‌نامه اشتباهات: 0 → **۲۱ مورد ثبت شده**

---

"""


# ============================================================
# PATCH 4 -- Section 1.9 rows for rules #33-47
# ============================================================

# Marker: We append after row #32 which we know exists
ROW_32_MARKER = "| **۳۲ 🆕 v2.8"  # partial match

NEW_RULES_ROWS = """
| **۳۳ 🆕 v2.9** | **Backup فقط در پایان چت** -- قبل از هر commit نیازی به backup نیست. Git خودش history را نگه می‌دارد. استثنا: migration های DB و تغییرات destructive خارج از Git. | چت ۷ |
| **۳۴ 🆕 v2.9** | **zip در root پروژه دانلود شود** -- نه به Downloads مرورگر. کاربر فایل zip را مستقیم در `D:\\Projects\\trading-system\\` دانلود می‌کند تا مرحله copy حذف شود. | چت ۷ M2 |
| **۳۵ 🆕 v2.9** | **pip flags ≠ npm flags** -- `--no-audit --no-fund` فقط برای npm. برای pip از mirror مثل `mirrors.aliyun.com/pypi/simple/` + `-i` استفاده شود. | چت ۷ M5 |
| **۳۶ 🆕 v2.9** | **verify signature قبل از تست‌نویسی** -- قبل از نوشتن تست برای تابع موجود، `findstr /N "def funcname"` برای دیدن signature واقعی اجرا شود، نه فرض. | چت ۷ M6 |
| **۳۷ 🆕 v2.9** | **read-back verify بعد از write** -- بعد از هر write file در اسکریپت، فایل را دوباره بخوان و verify کن. هرگز به status `updated` اعتماد نکن. | چت ۷ M1 |
| **۳۸ 🆕 v2.9** | **`.py` تنها → scripts/، zip → root** -- اسکریپت‌های Python تک‌فایلی در `scripts/` کپی می‌شوند، فایل‌های zip در ریشه پروژه. | چت ۷ M8 |
| **۳۹ 🆕 v2.9** | **multi-root zip → `python -m zipfile -e`** -- اسکریپت `43_sync_from_zip.py` فقط برای zip تک‌root (`docs/`) طراحی شده. برای multi-root از `python -m zipfile` استفاده شود. | چت ۷ M4 |
| **۴۰ 🆕 v2.9** | **verify argparse syntax** -- قبل از پیشنهاد syntax یک command موجود، argparse آن با `findstr "add_argument"` یا `--help` چک شود تا positional vs named درست باشد. | چت ۷ M3 |
| **۴۱ 🆕 v2.9** | **`.get()` به‌جای `[]` در `or` assertion** -- در Python `or` short-circuit به‌خاطر exception کار نمی‌کند. در assertion های تست با fallback، همیشه `.get()` استفاده شود. | چت ۷ M7 |
| **۴۲ 🆕 v2.9** | **`--no-verify` با `[skip-hooks: REASON]`** -- bypass pre-commit hooks فقط در اضطرار + commit message باید reason مشخص داشته باشد. | چت ۷ |
| **۴۳ 🆕 v2.9** | **Hybrid hook mode** -- critical hooks (format, A1/A4/A8/A10, fast tests) اجباری، minor hooks (A6 print, slow tests) warning. | چت ۷ |
| **۴۴ 🆕 v2.9** | **`.gitattributes` به‌جای hook برای CRLF** -- `mixed-line-ending` hook با cp1252 ویندوز کرش می‌کند. به‌جای آن از `.gitattributes` با `text eol=lf` استفاده شود. | چت ۷ M13 |
| **۴۵ 🆕 v2.9** | **pre-commit entry → `python wrapper.py`** -- entry های `.cmd` و `.bat` در Windows با pre-commit tokenizer ناسازگار. wrapper Python (cross-platform) استفاده شود. | چت ۷ M14 |
| **۴۶ 🆕 v2.9** | **ASCII-only در print() اسکریپت‌های Windows** -- Unicode emoji/symbol در cp1252 ویندوز کرش می‌کند. از `[OK]`، `[FAIL]`، `[WARN]` استفاده شود + `sys.stdout.reconfigure(encoding="utf-8")` در ابتدای اسکریپت. | چت ۷ M9 |
| **۴۷ 🆕 v2.9** | **تست hook قبل از deploy** -- قبل از enable کردن یک hook جدید، روی کل codebase دستی اجرا شود. false positive های زیاد یعنی regex بد است. | چت ۷ M20 |
"""


# ============================================================
# PATCH 5 -- New sections 18-21 at end of document
# ============================================================

NEW_SECTIONS_18_21 = """
---

# سند ۱۸ — درس‌نامه اشتباهات Claude (AI Mistakes Log) ⭐ 🆕 v2.9

> **هدف:** ثبت اشتباهاتی که Claude مرتکب می‌شود، علت ریشه‌ای، و راه‌حل برای جلوگیری از تکرار.
> **قانون:** هر چت جدید، Claude **باید** این بخش را قبل از نوشتن کد جدید بخواند.

## ۱۸.۱  چرا این بخش وجود دارد

Claude گاهی کد، دستور، یا پیشنهادی می‌دهد که در عمل کار نمی‌کند. وقتی این اتفاق می‌افتد:

1. کاربر خروجی اشتباه را به Claude گزارش می‌دهد
2. Claude کد اصلاحی می‌دهد
3. این چرخه گاهی چندبار تکرار می‌شود

این درس‌نامه، **هر اشتباه را با علت ریشه‌ای و راه‌حل** ثبت می‌کند، تا Claude در چت‌های آینده قبل از تکرار اشتباه، آن را بشناسد و اجتناب کند.

## ۱۸.۲  جدول اشتباهات شناسایی‌شده (M1-M21)

| # | اشتباه | علت ریشه‌ای | راه‌حل آینده |
|---|---|---|---|
| **M1** | اسکریپت ۴۸ گزارش «updated» داد، فایل‌ها به‌روز نشدند | اسکریپت به `/tmp/zip_stage/` می‌نوشت نه workspace | بعد از write، read-back verify (قانون #۳۷) |
| **M2** | فرض کردم zip در `%USERPROFILE%\\Downloads` است | مسیر دانلود کاربر متفاوت | پرسیدن یا قانون #۳۴ (zip در root) |
| **M3** | پیشنهاد `--zip ... --dry-run` برای اسکریپت ۴۳ | argparse positional بود | verify argparse (قانون #۴۰) |
| **M4** | اسکریپت ۴۳ فقط `docs/` را شناخت، `scripts/` گم شد | اسکریپت ۴۳ single-root است | multi-root → `python -m zipfile -e` (قانون #۳۹) |
| **M5** | پیشنهاد `pip install --no-audit --no-fund` | این flags فقط npm هستند | pip flags ≠ npm (قانون #۳۵) |
| **M6** | تست با `create_access_token(subject="...")` -- signature واقعی متفاوت | بدون چک signature فرض زدم | verify signature (قانون #۳۶) |
| **M7** | `payload["user_id"]` در `or` → KeyError | `or` short-circuit با exception کار نمی‌کند | `.get()` در `or` (قانون #۴۱) |
| **M8** | تک‌تک نگفتم فایل‌های `.py` کجا کپی شوند | فرض کردم کاربر می‌داند | همیشه مسیر کپی صریح (قانون #۳۸) |
| **M9** | Unicode `✓` در `print()` با cp1252 ویندوز کرش | Windows پیش‌فرض cp1252 است | ASCII-only + `reconfigure(encoding="utf-8")` (قانون #۴۶) |
| **M10** | مسیر relative در `entry:` pre-commit با Windows ناسازگار | tokenizer Windows | `python wrapper.py` (قانون #۴۵) |
| **M11** | Backslash double-escape در template string | template Python پیچیده | از `pathlib.Path` و read/replace استفاده شود |
| **M12** | فراموش کردن فعال‌سازی venv قبل از pre-commit | فرض global PATH | همیشه `venv\\Scripts\\activate` در راهنما |
| **M13** | built-in `mixed-line-ending` hook کرش با cp1252 | hook خود Unicode error می‌دهد | `.gitattributes` (قانون #۴۴) |
| **M14** | `entry: cmd /c scripts\\\\foo.cmd` ناسازگار | YAML escape + Windows tokenize | `python wrapper.py` cross-platform |
| **M15** | اولین pre-commit، 78 فایل reformat کرد | پروژه legacy با CRLF mixed | پذیرش mass-format در چت اول hook |
| **M16** | pytest hook با env var مشکل | env در hook موجود نیست | hook ها فقط سریع + بدون env |
| **M17** | نمی‌توانم تنظیمات کاربر را تغییر دهم | محدودیت طبیعی Claude | راهنمایی، نه تغییر مستقیم |
| **M18** | دادن دو فایل `54c`/`54d` با هدف مشابه کاربر را گیج کرد | فایل قدیمی hint نداشت | `[REPLACES PREVIOUS]` در نام |
| **M19** | کاربر فقط دستور‌های مهم را اجرا کرد، نه همه | دستور‌ها واضح branding نشده | شماره + نام مرحله برجسته |
| **M20** | A1 false positive روی `readVar("..", "#fallback")` | regex خیلی سختگیر | تست hook روی codebase قبل از deploy (قانون #۴۷) |
| **M21** | اسکریپت `54e` خودش fail شد به‌خاطر `\\\\\\\\b` template | template Python با backslash مضاعف | read/replace به‌جای template (قانون #۳۷) |

## ۱۸.۳  پروتکل اعمال این بخش

در ابتدای هر چت جدید، Claude باید:

1. **فایل `docs/سند_جامع_v2_*.md` بخش ۱۸ را بخواند**
2. قبل از نوشتن کد یا پیشنهاد، چک کند: **آیا این موقعیت یکی از M1-M21 را تکرار می‌کند؟**
3. اگر بله، از راه‌حل ثبت‌شده استفاده کند

این یک قانون قفل‌شده است (قانون #۴۸ در نسخه آینده اضافه می‌شود اگر این پروتکل کافی نبود).

---

# سند ۱۹ — Claude MAX Real-Time Configuration Guide ⭐ 🆕 v2.9

> **هدف:** راهنمایی کاربر برای استفاده بهینه از Claude MAX بر اساس فاز جاری پروژه.

## ۱۹.۱  محدودیت مهم

Claude **نمی‌تواند** به‌جای کاربر تنظیمات Settings را تغییر دهد. این بخش فقط راهنمایی می‌کند که کاربر چه چیزی فعال کند.

## ۱۹.۲  انتخاب Model بر اساس فاز پروژه

| فاز / موقعیت | Model پیشنهادی | Adaptive Thinking | علت |
|---|---|---|---|
| **Atomic End-of-Chat** | **Opus 4.7** | ON | manipulation همزمان چند سند |
| **Tier 2 Quality Hardening (روتین)** | Sonnet 4.6 | ON | سرعت + کیفیت کافی |
| **فاز ۱ — Repository Layer** | Sonnet 4.6 | ON | CRUD ساده |
| **فاز ۲ — Indicators (RSI/MACD)** | **Opus 4.7** | ON | منطق ریاضی |
| **فاز ۳ — Trading Strategies** | **Opus 4.7** | ON | الگوریتم پیچیده |
| **فاز ۴ — UI Components** | Sonnet 4.6 | OFF | template-heavy |
| **Debugging پیچیده** | **Opus 4.7** | ON | reasoning عمیق |
| **Refactoring بزرگ** | **Opus 4.7** | ON | حفظ ثبات معماری |
| **Documentation روتین** | Sonnet 4.6 | OFF | سریع کافی |
| **Code review** | **Opus 4.7** | ON | تشخیص anti-patterns |

**قانون عملی:** اگر کاری شامل ≥۳ مورد از این‌ها است → **Opus**: (a) چند فایل همزمان، (b) منطق پیچیده، (c) edge case های زیاد، (d) decision معماری، (e) debugging طولانی، (f) reasoning زنجیره‌ای.

## ۱۹.۳  تنظیمات Settings (Max 5x، Desktop App)

| Setting | Tab در Settings | حالت پیشنهادی | چرا |
|---|---|---|---|
| **Artifacts** | Feature Preview | ✅ ON | برای code snippets قابل کپی |
| **Analysis tool** | Feature Preview | ✅ ON | اجرای Python sandbox |
| **Extended thinking** | Feature Preview | ✅ ON | Opus reasoning |
| **File creation** | Feature Preview | ✅ ON | ساخت docx/pdf/xlsx |
| **Web search** | Feature Preview | ✅ ON | docs library های به‌روز |
| **Memory** | Profile | ✅ ON | حفظ context بین چت‌ها |
| **Custom instructions** | Profile | ✅ پر کنید | dictate قوانین پروژه |
| **GitHub Connector** | Connectors | بعد از setup repo | اتصال مستقیم |

## ۱۹.۴  Custom Instructions پیشنهادی

```
من روی پروژه trading-system (D:\\Projects\\trading-system) کار می‌کنم.
Stack: FastAPI + SQLAlchemy + React + Vite، Windows 11.
زبان ارتباط: فارسی، اصطلاحات فنی انگلیسی.

قوانین قفل‌شده پروژه (نسخه v2.9):
- قانون #27: پایان چت فقط با تأیید صریح کاربر
- قانون #30: اصلاحات کوچک = اسکریپت Python idempotent
- قانون #31: بالای هر کادر کد دستوری: 🟦/🟩/🟧/🟥 + شماره tab
- قانون #34: zip ها در ریشه پروژه دانلود می‌شوند
- قانون #38: اسکریپت‌های .py تنها → scripts/، zip → root
- قانون #46: ASCII-only در print() اسکریپت‌های Windows

مرجع کامل: docs/سند_جامع_v2_9.md (به‌خصوص بخش ۱۸ درس‌نامه اشتباهات)
```

## ۱۹.۵  پروتکل توصیه Real-Time

در هر شروع مرحله جدید، Claude باید:

```markdown
🤖 **توصیه Claude MAX برای [مرحله]:**
- Model پیشنهادی: [Opus 4.7 / Sonnet 4.6]
- Adaptive Thinking: [ON / OFF]
- علت: [توضیح ۱-۲ خط]
- آیا تأیید می‌کنید این تنظیم را اعمال کنید؟
```

---

# سند ۲۰ — Pre-commit Hooks Philosophy ⭐ 🆕 v2.9

> **هدف:** توجیه طراحی Hybrid mode و trade-offs آن.

## ۲۰.۱  ۳ گزینه ممکن

| حالت | اجباری/Warning | مزیت | عیب |
|---|---|---|---|
| **همه اجباری** | همه fail commit | کد بد وارد نمی‌شود | WIP موقت سخت، اگر hook bug، قفل |
| **همه warning** | فقط چاپ هشدار | workflow هرگز قفل نمی‌شود | معمولاً نادیده گرفته می‌شود |
| **Hybrid** ⭐ | critical اجباری، minor warning | تعادل | پیچیدگی config |

## ۲۰.۲  انتخاب پروژه: Hybrid

| Hook | حالت | چرا |
|---|---|---|
| `trailing-whitespace`, `end-of-file-fixer`, `check-yaml`, `check-json` | 🔴 اجباری (auto-fix) | استاندارد عمومی |
| `black`, `isort` | 🔴 اجباری (auto-fix) | یکنواختی مطلق Python |
| `check-anti-patterns` -- A1 (hex), A4 (secret), A8 (localStorage), A10 (sync I/O) | 🔴 اجباری | security/bug-prone |
| `check-anti-patterns` -- A6 (print) | 🟡 warning | dev موقت |
| `pytest-unit`, `vitest` | حذف از pre-commit | کند، انتقال به pre-push (آینده) |

## ۲۰.۳  Bypass در اضطرار (قانون #۴۲)

```cmd
git commit --no-verify -m "[skip-hooks: REASON] ..."
```

### موارد قابل قبول
- Hook خود bug دارد
- Migration حساس
- WIP موقت قبل از merge

### موارد غیرقابل قبول
- «hook کنده، صبر ندارم»
- «A1 violation است ولی موقتی»

## ۲۰.۴  Mass Reformat در شروع

اولین اجرای hooks در پروژه legacy، انبوه فایل را reformat می‌کند (در چت ۷، ۷۸ فایل + ۶۰ فایل CRLF). این طبیعی است:

```cmd
pre-commit run --all-files
git add -A
git commit --no-verify -m "style: apply black/isort to legacy files [skip-hooks: mass-format]"
```

---

# سند ۲۱ — اتصال به GitHub در شروع پروژه ⭐ 🆕 v2.9

> **هدف:** چک‌لیست استاندارد اتصال پروژه به GitHub که در شروع هر پروژه باید انجام شود.
> **نکته:** این کار در شروع این پروژه فراموش شد. در چت ۸ جبران می‌شود.

## ۲۱.۱  چرا اول پروژه؟

- Backup remote (در صورت crash hard disk)
- Time-machine کامل کد
- آمادگی برای CI/CD آینده
- آمادگی برای collaboration

## ۲۱.۲  چک‌لیست استاندارد

### مرحله ۱ -- ایجاد repository در GitHub

🟧 **tab «3 frontend»** (مرورگر)

1. ورود به github.com
2. کلیک `New repository`
3. نام: `trading-system`
4. **Private** (پیشنهاد - تا فاز ۴)
5. **بدون** README/license/.gitignore (چون از قبل داریم)
6. کلیک `Create repository`

### مرحله ۲ -- تأیید `.gitignore` شامل secrets

🟥 **tab «4 BACKUP»**

```cmd
findstr "\\.env" .gitignore
:: باید `.env` و `.env.local` و مشابه چاپ شوند
```

### مرحله ۳ -- اتصال local به remote

🟥 **tab «4 BACKUP»**

```cmd
cd D:\\Projects\\trading-system
git remote add origin https://github.com/<USERNAME>/trading-system.git
git branch -M main
git push -u origin main
```

اولین push کند است (همه history).

### مرحله ۴ -- تنظیم authentication

#### گزینه ۱ -- Personal Access Token (ساده‌تر)

1. GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (Classic)
3. Scope: `repo`
4. Token را کپی کنید
5. اولین `git push` username + token می‌خواهد

#### گزینه ۲ -- SSH key (امن‌تر، توصیه برای استفاده مکرر)

```cmd
ssh-keygen -t ed25519 -C "your_email@example.com"
type %USERPROFILE%\\.ssh\\id_ed25519.pub
```

سپس public key را در GitHub Settings → SSH and GPG keys اضافه کنید.

### مرحله ۵ -- تأیید push موفق

```cmd
git status
git log --oneline -5
```

## ۲۱.۳  Best Practices

- **هرگز** `.env` را commit نکنید
- **هرگز** API keys را در commit بگذارید
- از **branch protection** برای `main` در GitHub Settings استفاده کنید (آینده)
- **regular push** -- هر چند commit یک‌بار push کنید

---
"""


# ============================================================
# Helpers
# ============================================================


def write_if_changed(path: Path, content: str) -> bool:
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return True


def main() -> int:
    print("=" * 64)
    print("  55_upgrade_doc_to_v29 -- ارتقای سند v2.8 -> v2.9")
    print("=" * 64)
    print()

    if not DOC_V28.exists():
        print(f"[ERR] {DOC_V28.name} not found")
        return 1

    text = DOC_V28.read_text(encoding="utf-8")
    original = text

    # Patch 1: Header
    if HEADER_OLD in text:
        text = text.replace(HEADER_OLD, HEADER_NEW, 1)
        print("  [OK] Header v2.8 -> v2.9")
    if DATE_OLD in text:
        text = text.replace(DATE_OLD, DATE_NEW, 1)
        print("  [OK] Date اردیبهشت -> خرداد")

    # Patch 2: TOC link
    if TOC_OLD_LINK in text and TOC_NEW_LINK not in text:
        text = text.replace(TOC_OLD_LINK, TOC_NEW_LINK, 1)
        print("  [OK] TOC link for v2.8 -> v2.9 added")

    # Patch 3: Changelog block before v2.7->v2.8 changelog
    changelog_marker = "# 📋 خلاصه تغییرات v2.7 → v2.8"
    if changelog_marker in text and "خلاصه تغییرات v2.8 → v2.9" not in text:
        text = text.replace(
            changelog_marker,
            CHANGELOG_V29_BLOCK.strip() + "\n\n" + changelog_marker,
            1,
        )
        print("  [OK] Changelog block v2.8 -> v2.9 inserted")

    # Patch 4: New rows in table 1.9 after row #32
    if ROW_32_MARKER in text and "| **۳۳ 🆕 v2.9**" not in text:
        # Find the row #32 line and the next line (which is end of row)
        idx = text.find(ROW_32_MARKER)
        # Find end of that table row (next newline after the |)
        end_of_row = text.find("\n", idx)
        if end_of_row != -1:
            text = text[: end_of_row + 1] + NEW_RULES_ROWS.lstrip() + text[end_of_row + 1 :]
            print("  [OK] 15 new rules added to table 1.9 (rules #33-47)")

    # Patch 5: New sections at end of document
    if "# سند ۱۸ — درس‌نامه اشتباهات Claude" not in text:
        text = text.rstrip() + "\n" + NEW_SECTIONS_18_21
        print("  [OK] 4 new sections (18-21) appended")

    # Write
    if text == original:
        if DOC_V29.exists():
            print()
            print("  [SKIP] no changes (idempotent)")
            return 0

    write_if_changed(DOC_V29, text)
    print()
    print(f"  [WRITE] {DOC_V29.name}")
    print(f"  Size: {len(text):,} chars, {text.count(chr(10))} lines")
    print()
    print("=" * 64)
    print("  [OK] success")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    sys.exit(main())
