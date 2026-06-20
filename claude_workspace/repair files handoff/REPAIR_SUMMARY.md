# خلاصه عملیاتی بررسی Governance — مرجع سریع چت بعدی
**تاریخ تکمیل ممیزی:** 2026-06-19
**فایل تفصیلی:** `repair_files_handoff.md` در همین پوشه (باید کامل خوانده شود)
**فایل‌های بررسی‌شده:** ۳۹ فایل + scan کامل `docs/` و `claude_workspace/`
**وضعیت:** مرحله ممیزی کامل — هیچ تغییری در فایل‌های پروژه اعمال نشده

---

## جدول مشکلات (۱۷ مورد، به ترتیب اولویت)

| # | مشکل | اولویت | فایل(های) درگیر |
|---|---|---|---|
| 1 | SESSION_STATUS.md سه part عقب است (header=part13، بدنه=part17، واقعیت=part19) | 🔴 فوری | SESSION_STATUS.md |
| 2 | حجم 01_rules.md به ۷۵KB رسیده (۵۰٪ بالاتر از حد هشدار ۵۰KB) | 🔴 فوری | 01_rules.md |
| 3 | تناقض سه‌طرفه CMD vs PowerShell (01_rules.md ≠ 05_architecture.md ≠ PART20_HANDOFF) | 🔴 فوری | 01_rules.md, 05_architecture.md |
| 6 | LOCKED_RULES_INBOX.md (۶ قانون binding فعال) از main.md Quick-start غایب است | 🔴 فوری | main.md |
| 7 | ترتیب boot sequence در سه منبع متفاوت است؛ PHASE_LEDGER.md از CHAT_BOOT_TRIGGER_TEMPLATE غایب است | 🔴 فوری | CHAT_BOOT_TRIGGER_TEMPLATE.md, PROJECT_INSTRUCTIONS.md |
| 10 | header همه ۶ فایل constitution همچنان «v2.14» است (واقعیت: v2.17) | 🔴 فوری | main.md + 5 ماژول |
| 5 | main.md آمار اندازه فایل‌ها را اشتباه دارد (~50KB گفته، واقعیت 73KB) | 🟡 متوسط | main.md |
| 8 | Rule #77 در HELPER_PROTOCOL.md هنوز «candidate» است (در واقع Locked شده) | 🟡 متوسط | HELPER_PROTOCOL.md |
| 9 | 05_architecture.md می‌گوید React 18؛ واقعیت React 19.2 است (package.json تأیید کرده) | 🟡 متوسط | 05_architecture.md |
| 13 | footer 05_architecture.md از Atomic Update S3.x جا مانده (می‌گوید «commit 6» نه «S3.x») | 🟡 متوسط | 05_architecture.md |
| 15 | CUSTOM_INSTRUCTIONS.md در snapshots/ بسیار قدیمی است — ارجاع به فایل‌های منسوخ دارد | 🟡 متوسط | snapshots/CUSTOM_INSTRUCTIONS.md |
| 16 | PROJECT_MANIFEST.md چهار چت عقب است (آخرین بار part14/15 بود، الان part19 است) | 🟡 متوسط | PROJECT_MANIFEST.md |
| 4 | CLAUDE_CHECKLIST.md منسوخ است (خودش DEPRECATED اعلام کرده، هیچ boot به آن ارجاع نمی‌دهد) | 🟢 پایین | CLAUDE_CHECKLIST.md |
| 11 | TODO منسوخ shell در 05_architecture.md (کار انجام شده ولی TODO پاک نشده) | 🟢 پایین | 05_architecture.md |
| 14 | PROJECT_CONSTITUTION.md یک redirect stub است با آمارهای شدیداً outdated | 🟢 پایین | PROJECT_CONSTITUTION.md |
| 17 | PROJECT_GOVERNANCE.md منسوخ است (مثل CLAUDE_CHECKLIST — DEPRECATED از part17) | 🟢 پایین | PROJECT_GOVERNANCE.md |
| 12 | (سالم) M-series count در 02_lessons.md بررسی شد و درست بود | ✅ سالم | 02_lessons.md |

---

## فایل‌های نخوانده با اولویت متوسط (برای چت بعدی)

این فایل‌ها بررسی نشدند — ممکن است مشکلات اضافی داشته باشند:
- `docs/REVIEW_LOG.md`
- `docs/PROJECT_CONTEXT.md`
- `docs/TROUBLESHOOTING.md`
- `docs/HANDOFF_TEMPLATE.md`
- `docs/PRECOMMIT.md` (⚠️ قبل از نوشتن هر Check جدید باید خوانده شود — تکمیلی ۴)

---

## اقدامات پیشنهادی (از بخش ۶ و ۷ فایل تفصیلی)

**اصلاحات فوری (batch اول):**
- مشکل ۱۰: header همه ۶ فایل constitution → «v2.17» (اسکریپت `63_pre_commit_audit.py` check جدید هم اضافه شود — بخش ۷.۱)
- مشکل ۶: افزودن LOCKED_RULES_INBOX.md به Quick-start در main.md
- مشکل ۷: افزودن PHASE_LEDGER.md به STEP 1 در CHAT_BOOT_TRIGGER_TEMPLATE.md
- مشکل ۱: بازنویسی SESSION_STATUS.md طبق PHASE_LEDGER (part19، HEAD=`5de05e0`)

**اصلاحات گروه دوم (نیاز به تصمیم کاربر):**
- مشکل ۲: حجم 01_rules.md — تقسیم یا ساخت فایل خلاصه؟
- مشکل ۳: تناقض shell — PowerShell یا CMD؟ (باید با M105 و part20 هماهنگ شود)
- مشکل ۱۶: اجرای `python scripts/64_generate_manifest.py` و commit

**اتوماسیون (بخش ۷ فایل تفصیلی):**
- check_14: header version sync در `63_pre_commit_audit.py`
- check_15: boot sequence sync بین main.md و CHAT_BOOT_TRIGGER_TEMPLATE

---

## نکات مهم برای چت بعدی

۱. این فایل **جایگزین** `repair_files_handoff.md` نیست — خلاصه عملیاتی آن است. فایل تفصیلی باید هم خوانده شود.
۲. قبل از هر اصلاح، boot رسمی پروژه را اجرا کن (`CHAT_BOOT_TRIGGER_TEMPLATE.md` STEP 0-4).
۳. هر اصلاح نیاز به Scope Contract دارد (Rule #78) — به‌خصوص مشکل ۳ که سه فایل را درگیر می‌کند.
۴. بعد از هر batch، `scripts/63_pre_commit_audit.py` را اجرا کن.
۵. در پایان چت، SESSION_STATUS + CHAT_LOG + PHASE_LEDGER را atomic به‌روز کن.
