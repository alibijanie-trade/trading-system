# 📋 PENDING_FOR_NEXT_VERSION

> **هدف:** ثبت در لحظه آیتم‌های PENDING برای ادغام بعدی در سند جامع.  
> **پروتکل ۷.۳:** پس از ادغام در نسخه بعدی، آیتم‌ها از این فایل پاک می‌شوند و در نسخه v(X+1) باقی می‌مانند.  
> **قانون مرجع:** #۶۰ (PENDING-EOC در لحظه ثبت با MCP)

---

## 🆕 آیتم‌های فعلی — برای ادغام در v2.12

### Z2.1: M64 — تنظیم JSX runtime در plugin-react به test pipeline منتقل نمی‌شود

**کشف‌شده در:** چت ۹ (2026-05-20) — پس از Bug #50 cleanup  
**وضعیت:** 🟢 راه‌حل اعمال شد در چت ۹ (`frontend/vite.config.js` با افزودن `esbuild: { jsx: 'automatic' }`)  
**اثر فعلی:** ۳۰/۳۰ تست vitest pass — پروژه پایدار است

**درس کلی (M64) — برای ادغام در v2.12:**

هنگام تنظیم JSX runtime یا transform options در پروژه‌های Vite + Vitest، **دو سطح جداگانه** باید تنظیم شود:

1. **`plugins: [react({ jsxRuntime: 'automatic' })]`** → برای production build و dev server (HMR)
2. **`esbuild: { jsx: 'automatic' }`** (top-level) → برای vitest test pipeline (و هر ابزاری که از esbuild داخلی Vite استفاده می‌کند)

تنظیم فقط در plugin-react کافی نیست — vitest config plugin را نمی‌بیند.

**اقدامات لازم در v2.12:**

1. افزودن M64 به جدول ۱۸.۲ سند جامع (درس‌نامه)
2. بازنگری سند معماری فاز ۰ (frontend setup) با ذکر این دو سطح تنظیم
3. بررسی افزودن Bug #53 به TROUBLESHOOTING.md (پیوست Bug #50)
4. بررسی افزودن قانون جدید (شاید #۶۶) درباره `esbuild.jsx` و `plugin-react jsxRuntime` به‌عنوان دو سطح مستقل

**ادغام در:** v2.12 (احتمالاً پایان چت ۱۱ یا چت ۱۲)  
**ثبت‌شده توسط:** قانون #۶۰ + قانون #۶۵ (درس با نمایش)  
**نشان داده شده به کاربر:** ✅ (طبق قانون #۶۵)

---

### Z2.2: M65 — تشخیص shell از prompt و adaptation دستورات

**کشف‌شده در:** چت ۹ (2026-05-20) — در لحظه git commit پایان چت  
**وضعیت:** 🟢 راه‌حل فوری در چت ۹ اعمال شد (تغییر از `$env:` به `set`)  
**اثر فعلی:** Workflow git commit پایان چت درست کار کرد

**درس کلی (M65):**

Claude باید از prompt ترمینال شناسایی کند کاربر در کدام shell است:

| prompt | shell | env var syntax |
|---|---|---|
| `D:\path>` | **CMD** (Command Prompt) | `set VAR=value` |
| `PS D:\path>` | **PowerShell** | `$env:VAR = "value"` |
| `(venv) D:\path>` | CMD با venv فعال | `set VAR=value` |
| `(venv) PS D:\path>` | PowerShell با venv فعال | `$env:VAR = "value"` |
| `user@host:~/path$` | bash (Linux/macOS/WSL/Git Bash) | `export VAR=value` |

**اقدامات لازم در v2.12:**

1. افزودن M65 به جدول ۱۸.۲ سند جامع (درس‌نامه)
2. به‌روزرسانی Bug #52 در TROUBLESHOOTING.md با هر دو سینتکس (CMD + PowerShell)
3. بررسی افزودن قانون جدید یا اصلاح قانون #۳۱ (Convention tab) تا توانایی تشخیص shell اضافه شود
4. در ONBOARDING_GUIDE.md، توصیه به تنظیم دائمی `PYTHONIOENCODING=utf-8` در سیستم env vars (مستقل از shell)

**ادغام در:** v2.12 (در همان batch با Z2.1)  
**ثبت‌شده توسط:** قانون #۶۰ + قانون #۶۵ (درس با نمایش)  
**نشان داده شده به کاربر:** ✅

---

### Z2.3: M66 — Filesystem MCP و فایل‌های بزرگ

**کشف‌شده در:** چت ۱۰ (2026-05-20) — هنگام تلاش برای خواندن سند جامع v2.11 (216KB)  
**وضعیت:** 🟢 workaround در چت ۱۰: استفاده از conversation_search + خواندن CHAT_LOG برای محتوای بخش‌های مرتبط  
**اثر فعلی:** هیچ کار از دست نرفت — اطلاعات از منابع جایگزین به‌دست آمد

**درس کلی (M66):**

فایل‌های `>200KB` (مثل سند جامع v2.11) ممکن است Filesystem MCP را hang کنند، **حتی با `head=N`/`tail=N` parameter**. اگر MCP hang کرد، بقیه دستورات همان session هم timeout می‌دهند — نیاز به ری‌استارت Claude Desktop.

**استراتژی توصیه‌شده:**

1. در شروع چت، اول `list_allowed_directories` (سریع) برای تأیید responsive بودن MCP
2. برای فایل‌های بزرگ، استفاده از `search_files` با pattern برای یافتن خط/بخش مرتبط
3. خواندن chunk کوچک با `view_range` در فایل‌های >100KB
4. اگر CHAT_LOG را خوانده‌اید، اطلاعات بخش‌های مهم سند جامع معمولاً در summary چت‌های قبل موجود است — کفایت‌بخش‌تر از خواندن مجدد

**اقدامات لازم در v2.12:**

1. افزودن M66 به جدول ۱۸.۲ سند جامع
2. به‌روزرسانی سند ۲۲ (Filesystem MCP Integration) با محدودیت اندازه فایل
3. بررسی افزودن قانون جدید: «در شروع چت، اگر سند جامع >200KB است، فقط بخش‌های مرتبط با scope چت با `view_range` خوانده شوند»

**ادغام در:** v2.12  
**ثبت‌شده توسط:** قانون #۶۰ + قانون #۶۵  
**نشان داده شده به کاربر:** ✅

---

### Z2.4: M67 — BOM در فایل‌های UTF-8 با متن غیر-ASCII روی Windows

**کشف‌شده در:** چت ۱۰ (2026-05-20) — هنگام pip install پس از تغییر requirements.txt  
**وضعیت:** 🟢 رفع شد در چت ۱۰ با اسکریپت `59_fix_requirements_encoding.py` (افزودن BOM با utf-8-sig)  
**اثر فعلی:** pip install حالا کار می‌کند. **Bug #53 در TROUBLESHOOTING ثبت شد.**

**درس کلی (M67):**

وقتی فایلی شامل کاراکترهای غیر-ASCII (متن فارسی، em-dash `—`، …) دارد و **BOM ندارد**، pip روی Windows با locale فارسی سعی می‌کند با codec سیستمی (cp1252) آن را decode کند و crash می‌کند با:
```
UnicodeDecodeError: 'charmap' codec can't decode byte 0xXX in position N
```

**علت ریشه‌ای:** ابزارهایی مثل `Filesystem:write_file` (Claude Desktop) به‌صورت پیش‌فرض **بدون BOM** می‌نویسند. اگر فایل قبلی BOM داشته، با rewrite اول BOM از دست می‌رود.

**راه‌حل دائمی برای v2.12:**

1. **policy A (preferred):** فایل‌های dependency (requirements.txt، package.json، pyproject.toml) **فقط ASCII** باشند — همه کامنت‌های فارسی به انگلیسی ترجمه شوند
2. **policy B (workaround):** اگر فارسی لازم است، با utf-8-sig (با BOM) ذخیره شود

**اقدامات لازم در v2.12:**

1. افزودن M67 به جدول ۱۸.۲ سند جامع
2. افزودن Anti-pattern A11 به ANTI_PATTERNS.md: «متن غیر-ASCII در فایل dependency بدون BOM»
3. بررسی افزودن قانون جدید: «فایل‌های dependency باید ASCII-only باشند یا با BOM ذخیره شوند»
4. تصمیم نهایی: ترجمه کامنت‌های فارسی requirements.txt به انگلیسی (policy A) یا حفظ BOM (policy B)

**ادغام در:** v2.12  
**ثبت‌شده توسط:** قانون #۶۰ + قانون #۶۵  
**نشان داده شده به کاربر:** ✅

---

### Z2.5: M68 — نسخه‌های pinned باید با PyPI verify شوند

**کشف‌شده در:** چت ۱۰ (2026-05-20) — هنگام تلاش pip install ccxt==4.3.0  
**وضعیت:** 🟢 رفع شد در چت ۱۰: pin به `4.3.98` (آخرین stable در 4.3.x) — اسکریپت `60_pin_ccxt_to_4_3_98.py`  
**اثر فعلی:** ccxt و websockets با موفقیت نصب شدند

**درس کلی (M68):**

سند جامع v2.11 بخش ۲.۲ (Stack) نسخه `ccxt 4.3.0` را pin کرده بود — این نسخه **هرگز در PyPI منتشر نشد** (یا توسط author yank شد). تنها هنگام تلاش نصب fail کشف شد.

**این یک Documentation Drift است:** documentation با reality نمی‌خواند، چون در زمان نوشتن سند، نسخه با PyPI verify نشد.

**اقدامات لازم در v2.12:**

1. **اصلاح سند جامع v2.11 → v2.12 بخش ۲.۲:** `ccxt 4.3.0` → `ccxt 4.3.98`
2. افزودن M68 به جدول ۱۸.۲ سند جامع
3. بررسی افزودن قانون جدید: «وقتی نسخه‌ای را در سند pin می‌کنیم، آن را با `pip index versions <pkg>` در همان لحظه verify کنیم»
4. بررسی pre-commit hook A12: cross-check نسخه‌های requirements.txt با PyPI

**ادغام در:** v2.12  
**ثبت‌شده توسط:** قانون #۶۰ + قانون #۶۵  
**نشان داده شده به کاربر:** ✅

---

### Z2.6: M69 — `asyncio.run()` در FastAPI handler crash می‌کند

**کشف‌شده در:** چت ۱۰ (2026-05-20) — هنگام طراحی sync wrapper برای CCXTDataSource.read_ohlcv  
**وضعیت:** 🟡 **در docstring CCXTDataSource تذکر داده شد** — ولی هنوز در سند رسمی نیست  
**اثر فعلی:** فعلاً مشکلی ایجاد نکرده چون sync wrapper فقط در test plain script استفاده می‌شود

**درس کلی (M69):**

`asyncio.run()` event loop جدید می‌سازد. اگر در محیط async (مثل FastAPI handler) فراخوانی شود، خطای زیر می‌دهد:
```
RuntimeError: asyncio.run() cannot be called from a running event loop
```

**در CCXTDataSource:** `read_ohlcv` (sync wrapper) از `asyncio.run(read_ohlcv_async(...))` استفاده می‌کند. **هرگز** نباید در FastAPI handler صدا زده شود — همیشه `await source.read_ohlcv_async(...)` استفاده شود.

**اقدامات لازم در v2.12:**

1. افزودن M69 به جدول ۱۸.۲ سند جامع
2. افزودن Anti-pattern A13: «asyncio.run() در FastAPI handler»
3. بررسی افزودن یک linter check: scan کد FastAPI handlers برای `asyncio.run` calls
4. در ARCHITECTURE.md، بخش CCXTDataSource، تأکید روی این تذکر

**ادغام در:** v2.12  
**ثبت‌شده توسط:** قانون #۶۰ + قانون #۶۵  
**نشان داده شده به کاربر:** ✅

---

### Z2.7: اصلاحیه سند جامع v2.11 بخش ۲.۲ (Stack)

**کشف‌شده در:** چت ۱۰ — مرتبط با Z2.5 (M68)  
**وضعیت:** 📌 یادآوری برای v2.12 — هنوز در v2.11 نوشته شده

**تغییر لازم:**

در سند `docs/سند_جامع_v2_11.md` بخش ۲.۲ (Stack):
- `ccxt 4.3.0` → `ccxt 4.3.98`
- اضافه کردن یادداشت: «در 2026-05-20 با PyPI verify شد»

**ادغام در:** v2.12  
**ثبت‌شده توسط:** قانون #۶۰ + قانون #۲۴ (No-Deletion — اصلاح در نسخه بعد، نه edit مستقیم)

---

### Z2.8: خط cosmetic در CHAT_LOG (bytes خراب)

**کشف‌شده در:** چت ۱۰ (پایان)  
**وضعیت:** 🟡 cosmetic only — اطلاعات نادرست (~۶۴ به‌جای ~۷۴)  
**رفع:** با اسکریپت Python (read_bytes/write_bytes) در v2.12

---

### Z2.9: قانون #۶۶ — Backup اجباری در پایان هر چت 🆕

**درخواست کاربر در:** پایان چت ۱۰ (2026-05-20)  
**وضعیت:** 🟢 پیاده‌سازی اولیه در چت ۱۰ (اسکریپت `63_backup_project.py`)

**🆕 متن نهایی قانون #۶۶ (تصمیم پایان چت ۱۰):**

> **قانون #۶۶ — Push اجباری در پایان هر چت:**
>
> در پایان هر چت، Claude باید مطمئن شود همه تغییرات commit و به GitHub push شده‌اند. **GitHub خودش backup primary است** — کاربر می‌تواند با `git clone` در هر ماشینی یک نسخه backup داشته باشد.
>
> **پروتکل پایان چت:**
> ۱. wrap-up اسناد (PENDING، CHAT_LOG، SESSION_STATUS، CHAT[N+1]_HANDOFF)
> ۲. ساخت اسکریپت backup در ابتدای چت (طبق قانون #۶۲)
> ۳. تحویل دستور `git add . && git commit -m "..." && git push origin main` با Convention 🟢 ▶️ EXECUTE
> ۴. تأیید HEAD جدید پس از کاربر
>
> **نکات امنیتی:**
> - `.env` هرگز در git نباشد — فقط `.env.example` (با dummy values)
> - DB در `.gitignore` می‌ماند (`*.db`) — کاربر مسئول backup شخصی DB است
> - secrets هرگز در commit messages یا code نباشد
>
> **Recovery از GitHub در صورت disaster:**
> - ماشین آماده (Python+Node+Git نصب): **~۴۵-۶۰ دقیقه**
> - ماشین خالی: **~۱.۵-۲ ساعت**
> - کیفیت: ۱۰۰٪ یکسان تا آخرین commit پوش شده
>
> **اسکریپت `scripts/63_backup_project.py` (optional):** برای کاربری که می‌خواهد backup شامل DB و .env (که در git نیستند) داشته باشد. در شرایط عادی نیازی نیست — GitHub کافی است.

**اقدامات لازم در v2.12:**

1. افزودن قانون #۶۶ به جدول ۱.۹ سند جامع (با اصلاحیه زیر)
2. افزودن backup step به CLAUDE_CHECKLIST فاز ۳ (پایان چت)
3. افزودن بخش جدید به سند جامع: «بخش ۲۶ — Backup Strategy»
4. بررسی rotation policy (نگه‌داری N بک‌آپ آخر)

**🔄 تحول مدل backup در طول چت ۱۰ (تاریخچه):**

- **v1 (اولیه):** Backup zip local + GitHub (دو لایه) — اسکریپت 63 ساخته شد
- **سؤال کاربر:** «بک‌آپ جدید را در گیتهاب گرفتی؟» — ابهام درباره اجرای خودکار vs دستی
- **پیشنهاد کاربر:** «همه چیز در GitHub، خودم clone می‌کنم» — ساده‌تر و استانداردتر
- **تصمیم نهایی:** نسخه بالا (Push اجباری در پایان هر چت)
- **سرنوشت اسکریپت 63:** optional — برای کاربری که می‌خواهد backup شامل DB و .env (که در git نیستند) داشته باشد

**درس نهایی (M70 — برای ادغام در v2.12):**

سادگی workflow > لایه‌بندی پیچیده. **یک source of truth (GitHub)** بهتر از دو منبع (GitHub + local zip) است در ۸۰٪ موارد. لایه دوم فقط برای محتوای حساس (DB با state، .env) ارزش دارد و اختیاری است.

**ثبت‌شده توسط:** قانون #۶۰ + قانون #۶۵  
**نشان داده شده به کاربر:** ✅

---

---

## 🆕 آیتم‌های کشف‌شده در پایان چت ۱۰ (Cleanup Round)

### Z2.10: M71 — Documentation Drift Self-Reference Paradox ⚠️

**کشف‌شده در:** چت ۱۱ (توسط Claude در audit) — پیگیری در پایان چت ۱۰

**درس (M71):**
وقتی فایلی شامل reference به خودش است (مثل "Git HEAD پایان چت" در فایلی که خودش commit می‌شود)، آن reference همیشه یک commit عقب می‌ماند — chicken-and-egg paradox.

**تجربه چت ۱۰:** در هر ۴ commit، HANDOFF و SESSION_STATUS HEAD reference قبلی را نگه داشتند تا Claude در چت ۱۱ متوجه شد.

**راه‌حل پیشنهادی برای v2.12:**
1. فایل جدا `docs/HEADS.md` برای HEAD پایان هر چت
2. رویکرد فعلی: دو commit (محتوا + HEAD backfill جداگانه)
3. placeholder `<TBD>` تا چت بعد

**ادغام در:** v2.12 — **نشان داده شده به کاربر:** ✅

---

### Z2.11: M72 — End-of-Chat Verification Checklist غایب ⚠️

**کشف‌شده در:** چت ۱۰ (audit پایان)  
**وضعیت:** برای افزودن به CLAUDE_CHECKLIST فاز ۳ در v2.12

**درس (M72):**
قانون #۴۸ فقط پروتکل **شروع** چت را پوشش می‌دهد. پروتکل **پایان** چت فاقد checklist verification است:
- چت ۹ Decisions #۵۸-۶۰ را در DECISIONS_LOG ثبت نکرد
- چت ۱۰ Decisions #۶۱-۶۶ را ثبت نکرد
- هرگز cross-check بین اسناد انجام نشد

**چک‌لیست پیشنهادی برای افزودن به CLAUDE_CHECKLIST فاز ۳:**
```
□ ۱. همه Decisions جدید در DECISIONS_LOG ثبت شدند؟ (sequential، بدون gap)
□ ۲. همه Bug های جدید در TROUBLESHOOTING ثبت شدند؟
□ ۳. همه درس‌های جدید (M*) در PENDING یا سند جامع ثبت شدند؟
□ ۴. همه قوانین جدید (#*) ثبت شدند؟
□ ۵. HEAD references در SESSION_STATUS و CHAT_LOG به‌روز هستند؟
□ ۶. آمار در SESSION_STATUS + CHAT_LOG + DECISIONS_LOG سازگارند؟
□ ۷. Git push موفق و HEAD نهایی ثبت شد؟
```

**ادغام در:** v2.12 — **نشان داده شده به کاربر:** ✅

---

### Z2.12: M73 — Cross-Document Consistency Audit ⚠️

**درس (M73):**
اسناد متعدد (CHAT_LOG, SESSION_STATUS, HANDOFF, DECISIONS_LOG, PENDING, TROUBLESHOOTING) باید با هم سازگار باشند.

**مثال از چت ۱۰:**
- HANDOFF: HEAD = `a29586e` ❌
- SESSION_STATUS: HEAD = `5cfc7e0` ❌
- DECISIONS_LOG: تعداد = ۵۷ ❌
- واقعی: HEAD = `f42d54f`، Decisions = ۶۶ ✅

**راه‌حل:** `scripts/audit_docs_consistency.py` که HEAD و آمار را cross-check کند.

**ادغام در:** v2.12 — **نشان داده شده به کاربر:** ✅

---

### Z2.13: Bug #54 — Decisions Numbering Gap ✅ حل‌شده

**وضعیت:** ✅ حل در پایان چت ۱۰ (DECISIONS_LOG v1.1 → v1.2 با backfill #۵۸-۶۶)

**علائم:** DECISIONS_LOG.md در #۵۷ متوقف بود، ولی در حقیقت #۵۸-#۶۶ در چت های ۸-۱۰ گرفته شده بودند.

**علت ریشه‌ای:** M72

**پیشگیری:** M72 باید اجباری شود تا تکرار نشود.

---

## 🆕 درس‌های پس از cleanup round (کشف‌شده در چت ۱۱ audit) — M74-M79

### Z2.14: M74 — Full-Range Decision Audit (نه Local) ⚠️

**کشف‌شده در:** چت ۱۱ (audit Claude) — پیگیری در پایان چت ۱۰

**درس (M74):**  
وقتی Bug غایب (gap) در سری‌بندی پیدا می‌کنید (مثل #۵۷→#۶۵)، **کل range را audit کن، نه فقط local**.

**تجربه چت ۱۰:**  
برای Bug #۵۴ (gap #۵۷→#۶۵) در پایان چت ۱۰، فقط #۵۸-۶۶ را backfill کردم. gap های قدیمی‌تر (#۱۶-۱۹ و #۴۹) را ندیدم. Claude در چت ۱۱ در audit جامع آن‌ها را پیدا کرد.

**راه‌حل:**  
در پایان هر چت، یک اسکریپت `scripts/audit_decisions_continuity.py` اجرا شود که از #۱ تا Max ID بررسی کند و gap ها را نشان دهد.

**ادغام در:** v2.12 — **نشان داده شده به کاربر:** ✅

---

### Z2.15: M75 — Within-File Consistency Check ⚠️

**درس (M75):**  
وقتی یک عدد در چند جای یک فایل تکرار می‌شود (مثل "تعداد PENDING")، تغییر فقط در یک جا ناسازگاری ایجاد می‌کند.

**تجربه چت ۱۰:**  
SESSION_STATUS دو بخش "تعداد PENDING" داشت:
- بخش آمار بالا: ۱۳ ✅
- بخش لیست پایین: ۷ ❌ (فقط Z2.1-Z2.7 لیست شده بود)

**راه‌حل:**  
در هر fields edit، کل فایل را search کن برای تکرار های همان مفهوم. یا Single Source of Truth pattern: یک بار عدد را تعریف کن و جاهای دیگر reference بده.

**ادغام در:** v2.12 — **نشان داده شده به کاربر:** ✅

---

### Z2.16: M76 — Decision vs Rule تمایز مبهم ⚠️

**درس (M76):**  
تمایز نیاز است:
- **Decision (در DECISIONS_LOG):** تصمیم گرفته شده در یک چت (Accepted ولی هنوز در constitution نیست)
- **Proposed Rule (در PENDING):** Decision پیشنهادی برای ادغام در vبعدی
- **Locked Rule (در سند جامع):** قانون رسمی اعمال شده در atomic update

**تجربه چت ۱۰:**  
«قانون #۶۶ Push اجباری» در HANDOFF به‌عنوان «feat» و در SESSION_STATUS به‌عنوان «غایب در constitution» صحبت شد. تمایز نامشخص بود. در حقیقت: Decision #۶۶ Accepted ✔ ، ولی Rule #۶۶ در Constitution ✖ (فقط Proposed).

**راه‌حل:**  
در HANDOFF و هر reference به قانون، صریح نوشته شود:
- "قانون #N (Locked)" → در Constitution
- "قانون #N (Proposed)" → در PENDING

**ادغام در:** v2.12 — **نشان داده شده به کاربر:** ✅

---

### Z2.17: M77 — HEAD Self-Reference نباید Hardcode باشد ⚠️

**درس (M77):**  
M71 گفت "دو commit جداگانه backfill بساز". این **هم کافی نیست** — commit backfill خودش یک HEAD جدید تولید می‌کند که فایل reflect نمی‌کند.

**راه‌حل واقعی:**  
HEAD reference در هر فایل که خودش commit می‌شود باید placeholder باشد:
```
Git HEAD: <با git log -1 در چت بعد پر کن>
```
یا فایل جدا `docs/HEADS.md` که فقط در شروع چت بعد پر می‌شود.

**ادغام در:** v2.12 — **نشان داده شده به کاربر:** ✅

---

### Z2.18: M78 — Re-read After Edit (عدم اتکا به diff) ⚠️

**درس (M78):**  
پس از هر file edit ، باید کل فایل re-read شود، نه فقط diff verify شود. diff فقط تغییرات را نشان می‌دهد، نه پیامدهای آن را در سایر جاهای فایل.

**تجربه چت ۱۰:**  
بعد از update بخش آمار SESSION_STATUS، فرض کردم fine است. چت ۱۱ نشان داد بخش دیگری هم تعداد قدیمی داشت.

**راه‌حل:**  
پس از هر batch edit، فایل را کامل با read_text_file بخوان. در خودبینی بدون verification اعتماد نکن.

**ادغام در:** v2.12 — **نشان داده شده به کاربر:** ✅

---

### Z2.19: M79 — Reserved IDs باید Explicit مستند شوند ⚠️

**درس (M79):**  
Decisions #۱۶-۱۹ و #۴۹ در دسته‌بندی موضوعی DECISIONS_LOG "reserved" هستند، ولی این فقط در categorization معلوم بود. در جدول آمار ("Accepted: ۶۶") تمایز بین "Max ID" و "Recorded" غایب بود.

**راه‌حل:**  
در جدول آمار DECISIONS_LOG دو عدد جدا:
- **Max ID:** ۶۶
- **Recorded:** ~۶۱
- **Reserved (غیر ثبت‌شده):** #۱۶-۱۹، #۴۹ — توضیح: برای renumbering یا reservation آینده

همچنین باید تصمیم گرفت:
- (الف) Reserved بماند → رفتار فعلی، ولی صریح مستند
- (ب) Renumber → همه Decisions پیوسته شوند (پیچیده: رفرنس‌ها در چت ها تغییر نمی‌کنند)
- (ج ⭐) Backfill تصمیمات واقعی از تاریخچه پروژه برای پر‌کردن gap (اگر قابل پیدا کردن)

**ادغام در:** v2.12 — **نشان داده شده به کاربر:** ✅

---

## 📜 آیتم‌های ادغام‌شده در v2.11 (تاریخچه — حذف شد)

تمام آیتم‌های زیر در پایان چت ۹ (فاز A) با ساخت سند جامع v2.11 ادغام شدند و طبق پروتکل ۷.۳ از این فایل پاک شدند:

| کد | عنوان | محل ادغام |
|---|---|---|
| B5.1 | فرمت `.gitignore` با `*` + `!.gitkeep` | فایل `.gitignore` |
| B2.1 | اصلاح مسیر Memory toggles | سند ۲۳.۱ v2.11 |
| C1.1 | Settings audit کامل (12 ردیف) | سند ۲۳.۴ v2.11 |
| D1.1 | مستندسازی Bug pre-commit + فارسی | Bug #52 در TROUBLESHOOTING v1.1 |
| E2.1 | Bug #50 cleanup (React import) | `vite.config.js` + ۱۷ JSX file |
| G5.1 | قانون #۶۲ (فایل handoff دائمی) | جدول ۱.۹ v2.11 |
| UX1.1 | قانون #۶۳ (Convention 🟢 ▶️ EXECUTE) | جدول ۱.۹ v2.11 |
| UX2.1 | قانون #۶۴ (عدم نمایش جزئیات تصحیح خطا) | جدول ۱.۹ v2.11 |
| UX3.1 | قانون #۶۵ (نمایش درس از اشتباهات) | جدول ۱.۹ v2.11 |
| Z1.1 | M63 (status صریح در handoff) | جدول ۱۸.۲ v2.11 |

**مجموع:** ۱۰ آیتم ادغام شد.

---

## آیتم‌های موکول (نه برای v2.12 بلکه برای بعدتر)

### D2.1 + D3.1: ارزیابی Claude Code + GitHub MCP

**موکول به:** فاز ۴+  
**علت:** در فاز ۰-۲ Filesystem MCP کفایت می‌کند.

---

## 📌 پایان فایل

**نسخه:** v0.6 (2026-05-20 — پایان چت ۱۰ round 2 cleanup: افزودن Z2.14-Z2.19 — M74-M79 کشف‌شده در چت ۱۱ audit)  
**ساخته توسط:** Claude در چت ۸ (`TRADING-phase0-part08-pre-phase1-setup`)  
**به‌روز توسط:** Claude در پایان چت ۱۰ طبق پروتکل ۷.۳  
**ادغام بعدی:** سند جامع v2.12 (در چت ۱۱ یا چت ۱۲)

## 📊 خلاصه آیتم‌های PENDING برای v2.12

| آیتم | سطح | توضیح |
|---|---|---|
| **Z2.1** | 🎯 important | M64 — JSX runtime در plugin-react vs esbuild |
| **Z2.2** | 🟡 medium | M65 — تشخیص shell از prompt و adaptation دستورات |
| **Z2.3** 🆕 | 🎯 important | M66 — Filesystem MCP و فایل‌های بزرگ (>200KB hang) |
| **Z2.4** 🆕 | 🔴 important | M67 — BOM لازم برای فایل UTF-8 با غیر-ASCII روی Windows pip |
| **Z2.5** 🆕 | 🎯 important | M68 — نسخه‌های pinned باید با PyPI verify شوند |
| **Z2.6** 🆕 | 🟡 medium | M69 — `asyncio.run()` در FastAPI handler crash می‌کند |
| **Z2.7** 🆕 | 💡 minor | اصلاحیه سند جامع v2.11 بخش ۲.۲ (ccxt 4.3.0 → 4.3.98) |
| **Z2.8** 🆕 | 💡 minor (cosmetic) | خط cosmetic در CHAT_LOG (bytes خراب) |
| **Z2.9** 🆕 | 🔴 **important** | قانون #۶۶ — Push اجباری در پایان هر چت (ساخته در چت ۱۰) |
| **Z2.10** 🆕⚠️ | 🔴 **important** | M71 — Documentation Drift Self-Reference Paradox |
| **Z2.11** 🆕⚠️ | 🔴 **important** | M72 — End-of-Chat Verification Checklist غایب در قانون #۴۸ |
| **Z2.12** 🆕⚠️ | 🔴 **important** | M73 — Cross-Document Consistency Audit اجباری در پایان چت |
| **Z2.13** ✅ | 🟡 medium | Bug #54 — Decisions منقطع (#57→#65) — حل شد در پایان چت ۱۰ |
| **Z2.14** 🆕⚠️ | 🔴 **important** | M74 — Full-Range Decision Audit (نه Local) — کشف gap های قدیمی‌تر در چت ۱۱ |
| **Z2.15** 🆕⚠️ | 🔴 **important** | M75 — Within-File Consistency Check (دو بخش SESSION_STATUS متناقض) |
| **Z2.16** 🆕⚠️ | 🔴 **important** | M76 — Decision vs Rule تمایز مبهم (Locked vs Proposed) |
| **Z2.17** 🆕⚠️ | 🔴 **critical** | M77 — HEAD Self-Reference نباید Hardcode باشد (placeholder الزامی) |
| **Z2.18** 🆕⚠️ | 🎯 important | M78 — Re-read After Edit (عدم اتکا به diff) |
| **Z2.19** 🆕⚠️ | 🎯 important | M79 — Reserved IDs باید Explicit مستند شوند (#۱۶-۱۹، #۴۹) |
| **Z2.20** ✅ RESOLVED v2.13 | 🔴 **critical** | M87 ثبت شد به‌عنوان درس جداگانه از M62. تبدیل از PENDING به Locked در v2.13 با راه‌حل سه‌لایه: قانون #۶۷ (Positive Constraint) + Template 9 Pre-EXECUTE verification (Visible) + Layer 1 audit (آینده). جزئیات: 02_lessons.md بخش ۲.۸ M87.

**تعداد:** ۰ آیتم باز (همه Z2.۱-Z2.۲۰ در v2.12 و v2.13 ادغام شدند)
**وضعیت v2.14:** در ادامه بخش جدید پایین

---

> 💡 **نکته برای چت ۱۱:** این فایل را خوانده و در پایان چت ۱۱ اگر آیتم جدیدی کشف شد، طبق قانون #۶۰ در همین فایل ثبت شود.

---

## 🔴 آیتم‌های جدید — برای ادغام در v2.14 (MDRS v2)

**منبع:** Atomic transfer از tracker `claude_workspace/MDRS_V2_PENDING_DRAFT.md` در پایان چت `TRADING-phase1-part03-mdrs-v2-implementation` (2026-05-22 — پایان Stage S2)

**وضعیت پروژه:** S1+S2 کامل (D1-D7 از D1-D23). S3 (atomic update v2.13 → v2.14) باقی در چت بعد.

**تعداد:** **۱۷ Z3.x drift** + **۹ M-candidate lessons** + **۱ Principle (Golden Rule)** = ۲۷ آیتم

### خلاصه جدول Z3.x دریفت‌ها — برای S8 cleanup در v2.14

| ID | Severity | Source | Action در S8 |
|---|---|---|---|
| Z3.1 | medium | Batch 5 | Decision reference drift در backend code |
| Z3.2 | high | Batch 5 | Migrations directory drift (backend/alembic to backend/migrations) |
| Z3.3 | low | Batch 5 | CCXTDataSource deferred (tracked only) |
| Z3.4 | medium | Batch 5 | alembic.ini ASCII-only constraint undocumented |
| Z3.5 | medium | Batch 7 | Duplicate script numbering (55, 56, 63) |
| Z3.6 | high | Batch 7 | Anti-Pattern implementation gap (5/10 in check_anti_patterns.py) |
| Z3.7 | high | Batch 7 | install_git_hooks.py emoji violation rule 46 |
| Z3.8 | critical | Batch 7 | Hidden Regeneration Hazard in doc generators (M88 candidate) |
| Z3.9 | high | Batch 8 | CHANGELOG.md 2 versions behind |
| Z3.10 | critical | Batch 8 | claude_workspace/snapshots/* outdated (Project Settings hazard) |
| Z3.11 RESOLVED | high | Phase 3 | Triple-Rule violation, fixed in 5730173, lesson formalization in M93 |
| Z3.12 RESOLVED v2.14 | low | Phase 3 | Pre-commit hook label drift — RESOLVED in S3.3 part08 (`35ea822`)، .pre-commit-config.yaml hook name → v2.14 |
| Z3.13 | high | S1 D2 | 6 Pre-Modular legacy sand-documents misplaced (~1MB) |
| Z3.14 | medium | S1 D2 | v2.11 sand-document duplication |
| Z3.15 | medium | S1 D2 | Self-reference first-run gap (D2 manifest) |
| Z3.16 | medium | S2.2 | Review numbering integrity audit |
| Z3.17 | high | S2.2 | Z-ID Permanence anti-pattern (M96 candidate) |

### M-lesson candidates — برای افزودن به 02_lessons.md در S3 atomic update v2.14

| ID | عنوان | Severity | منبع |
|---|---|---|---|
| M88 | Hidden Regeneration Hazard | critical | Z3.8 (Batch 7) |
| M93 | Triple-Rule Atomic Boundary | high | Z3.11 (Phase 3) |
| M94 | Black Auto-Reformat Re-Stage Pattern | positive | S1 sub-commits 2, 3 |
| M95 | CMD Pipe Character in Commit Messages | high | S2.1 attempt 1 |
| M96 | Z-ID Permanence Anti-pattern | high | Z3.17 (S2.2 design, user catch) |
| M97 | CMD Quote-Tracking Catastrophic Failure (em-dash + redirect) | critical | S2.2 attempt 1 (stray file M evidence) |
| M98 | Review Scope Closure (Temporally Closed Reviews) | high | S2.3 design (user trio catches) |
| M99 | CMD Long-Command Paste-Break + -F Flag Standard | critical | S2.3 attempt 1 (100% inline failure) |
| M100 | Hidden-Checklist Completion (Implicit Validation Failure) | high | S2.4 design (user catch) |

### Principle جدید — برای افزودن به 04_principles.md در S3

**Golden Rule** — Tier rules در manifest ≠ git tracking. Scope by **role** in project, not by **tracked** in git. منبع: S1 D2 design discovery (کاربر).

### Rules جدید پیشنهادی برای 01_rules.md در S3 (D8)

| ID پیشنهادی | عنوان | منبع |
|---|---|---|
| #68 | MDRS v2 Source-of-Truth Hierarchy (Tier 1-5 enforcement) | MDRS framework |
| #69 | Review Trigger Enforcement (PRE_ADD_CHECKLIST + REVIEW_PROTOCOL) | S2 governance |
| #70 | Path Validator Enforcement | D19-D21 |
| #71 | VERSION Single Source of Truth | D22-D23 |
| #72 | Manifest Self-Awareness (D2 + Audit Check #8-9) | D12 audit extensions |
| #73 | Atomic Stage-end State Reconciliation | M93 enforcement |
| #74 | Z-ID Permanence Boundary | M96 enforcement |
| #75 | Review Scope Closure Mandate | M98 enforcement |
| #76 | Pre-Action Checklist Visibility | M100 enforcement |

### Templates جدید پیشنهادی — برای 06_meta.md در S3

| ID | عنوان | منبع |
|---|---|---|
| Template 11 | Commit Message Short (inline -m pattern) | M95 + M97 prevention |
| Template 12 | Commit Message Long (-F flag pattern with temp file) | M99 standard |

### Audit Checks جدید پیشنهادی — برای scripts/63_pre_commit_audit.py در S4 (D12)

| ID پیشنهادی | عنوان | منشأ |
|---|---|---|
| Check #8 | Detect uncommitted state files (SESSION_STATUS/PENDING/CHAT_LOG modified) | M93 enforcement |
| Check #9 | Manifest self-row existence + first-run gap detection | Z3.15 |
| Check #10 | Review numbering integrity (LOG to docs/reviews/) | Z3.16 |
| Check #11 | Z-ID Permanence (no Z-refs in permanent docs) | Z3.17 + M96 |

### جزئیات کامل هر آیتم

جزئیات کامل هر Z3.x، هر M-candidate، هر Rule پیشنهادی، و هر Template در commit history برانچ `infra/v2.14-source-of-truth` دسترس پذیر است:
- چت: `TRADING-phase1-part03-mdrs-v2-implementation`
- Branch: `infra/v2.14-source-of-truth`
- Final commit S2: `af63e9b` (docs(state): stage-end S2)
- Tracker source: `claude_workspace/MDRS_V2_PENDING_DRAFT.md` (در پایان چت delete می‌شود)

برای بازیابی جزئیات، در چت `TRADING-phase1-part04-mdrs-v2-completion`:
1. خواندن transcript chat قبل برای full reasoning هر lesson/Z-item
2. خواندن handoff file `claude_workspace/incoming_permanent/PHASE1_PART04_MDRS_V2_S3_TO_S8_HANDOFF.txt`
3. گرفتن commits S2 (`4726b38`, `d9747b5`, `35a634f`, `c18f132`, `af63e9b`) برای context implementation

### Action در چت بعد (`TRADING-phase1-part04-mdrs-v2-completion`)

Stage S3 — Atomic Update Constitution v2.13 to v2.14:
- D8: docs/constitution/01_rules.md — 9 rule جدید (#68-76)
- D9: docs/constitution/02_lessons.md — 9 M-lesson (M88, M93-M100)
- D10: docs/constitution/04_principles.md — Golden Rule
- D11: docs/constitution/main.md — version bump v2.13 to v2.14 + stats refresh
- D13: scripts/63_pre_commit_audit.py — CURRENT_VERSION update + ACCEPTABLE_VERSIONS list extend
- Plus: 06_meta.md — Templates 11-12 جدید

Stage S4-S8 طبق plan اصلی MDRS v2 (handoff file جزئیات را دارد).

**تعداد:** 27 آیتم باز برای v2.14 (17 Z3.x + 9 M-lessons + 1 Principle)
**وضعیت:** آماده atomic update در S3 چت `TRADING-phase1-part04-mdrs-v2-completion`
**آخرین به‌روزرسانی:** 2026-05-22 (پایان چت `TRADING-phase1-part03-mdrs-v2-implementation` در پایان Stage S2)

---

## 🔴 آیتم‌های جدید — کشف‌شده در چت `TRADING-phase1-part04-mdrs-v2-completion`

**منبع:** Discoveries Log consolidated در پایان چت (per R-NEW پیشنهادی کاربر — Rule #۷۷ candidate). این چت S3.0 را کامل کرد (Review #۰۰۲ Draft + LOG row Approved در commit `15e8e37`)، ولی S3.1 (Rules + Lessons) مدد در چت بعد تکمیل خواهد شد.

### Z3.18: stale workspace handoff file cleanup

**کشف‌شده در:** boot چت part04 (git status) — untracked file `claude_workspace/incoming_permanent/PHASE1_PART02_BINANCE_CLIENT_HANDOFF.txt`
**Severity:** 🟢 low
**درجه برخورداری:** این فایل از قبل از Decision #۶۵ (pivot از binance-client به MDRS v2 در part02 deep-audit) باقی مانده و stale است. نام "PHASE1_PART02_BINANCE_CLIENT" دیگر reflect realityaste.
**Action:** در S8 cleanup hybrid policy (به همراه Z3.13 archive moves) consolidate شود.

### Z3.19: هدر "Constitution v2.12 (Modular)" در ماژول های constitution drift

**✅ RESOLVED in S3.3 part08** (commit `35ea822`) — همه ۶ ماژول header + main.md frontmatter به v2.14 update + audit script ACCEPTABLE_VERSIONS extended atomically.

**کشف‌شده در:** S3.1 design phase (Discovery #۲۱ توسط Claude در reading 01_rules.md)
**Severity:** 🟡 medium
**درجه برخورداری:** هدر ماژول های constitution (01_rules.md, 02_lessons.md و غیره) می‌گوید "Constitution v2.12 (Modular)" در حالی که constitution الان v2.13 است (per main.md). این خانواده Z3.12 (yaml label drift) است و توسط Rule #۷۱ (Single Source of Truth for Version Identifier) coverage دارد.
**Action:** در S3.3 atomic update با audit script (CURRENT_VERSION + ACCEPTABLE_VERSIONS extension to include v2.14) در یک عمل reconcile شود. باید در اولین stage-end commit چت part05 backfill شود یا در S3.3 atomic. **دلیل defer:** ordering dependency — ACCEPTABLE_VERSIONS فعلاً ["v2.12", "v2.13"] است، update header به v2.14 تنهایی audit fail می‌دهد.

### Z3.20: MCP edit_file payload limit — large multi-row table append ممکن است timeout شود

**کشف‌شده در:** Lessons table append در S3.1 (چت part04) — Discovery #۲۷
**Severity:** 🟠 high (workflow blocking pattern)
**درجه برخورداری:** `edit_file` MCP با پیلود‌های خیلی بزرگ (>~5KB oldText+newText combined, multi-byte Persian content) ممکن است به 4-minute timeout برسد. Edit 1 (پیلود کوچک ‍~1KB) موفق، Edit 2 (پیلود بزرگ ‍~6KB با 11 row Persian-heavy) timeout شد.
**Mitigation strategy:**
- Split large edits به multiple smaller edits (یک row per edit یا چند row)
- یا fallback به write_file با full content (لی این هم پیلود دارد)
- M83 (Retry First, Restructure Last) honored: retry probably won't help here چون علت payload-based است
**Action:** در چت part05 S3.1 redo، استراتژی split-edit استفاده شود. اگر pattern تکرار شد در چت های بعد، M-candidate (شاید M103) formalize شود.

### درس‌های M-candidate جدید (در چت part05 در S3.1 redo فرمالیزه شوند)

| ID | عنوان | Severity | منبع |
|---|---|---|---|
| M101 | Post-Handoff State Drift (chicken-and-egg M77 extension) | high | part03->part04 transition (Discovery #۸) |
| M102 | Rule-Implementation Decoupling (Interface-Implementation separation) | high | S3.1 design phase Q3 user catch (Discovery #۱) |

**پلان برای چت part05:** هر دو لسون در S3.1 همراه M88 + M93-M100 فرمالیزه شوند (M101 کل جمع درس ها به ۱۰ لسون و M102 ۱۱ لسون تبدیل می‌کند).

### Rule جدید #۷۷ پیشنهادی (R-NEW) — در S3.1 redo Locked شود

**نام:** Continuous Discovery Logging at Chat Boundaries
**توسط کاربر پیشنهاد شد در:** پایان turn 2 چت part04 (پیام اولیه کاربر — "در پایان هر چت Discoveries Log consolidated داشته باشد")
**متن:** در طول هر چت، Claude باید Discoveries Log نگه دارد (bugs کشف‌شده، ابهامات، patterns جدید، edge cases، tool quirks، communication friction). Discoveries در chat surface در sign-off milestones explicit + در handoff پایان چت consolidated.
**Plan:** در S3.1 redo به‌عنوان یکی از ۱۰ rule (غالباً last) فرمالیزه شود. این باعث می‌شود Rules چت part05 توسط #۶۸-#۷۷ (10 rule جدید) پوشش داده شوند.

### توضیح S3 صورتپذیرفته در چت part04 و پلان برای part05

**وضعیت S3 در پایان چت part04:**
- S3.0 (Review #۰۰۲ Draft + LOG row Approved): ✅ تکمیل در commit `15e8e37` (push shod)
- S3.1 (Rules + Lessons + Reserved + sections + tables + footer atomic): ⛔ incomplete
  - Rules edits در 01_rules.md اعمال شد ولی توسط `git checkout` revert شد (Z3.20 timeout در Lessons edit پاداری Option A handoff)
  - 02_lessons.md categories edit در Edit 1 (~6 row) اعمال ولی revert شد برای clean state
  - Rule content + Lesson content + sections + tables در Turn 1 + Turn 2 previews تولید شدند و در chat history part04 را موجودند (reference در handoff)
- S3.2-S3.4: ⛔ deferred
- S4-S8: ⛔ deferred

**Plan برای چت part05 (جدید):**
1. Boot reading + handoff file readout
2. M101 backfill mechanism (اولین atomic operation چت part05 باید درج کند که chat-end commit چت part04 = `15e8e37` در CHAT_LOG/SESSION_STATUS)
3. S3.1 redo با strategy split-edit (per Z3.20)
4. S3.2 (D10: Principles + Templates)
5. S3.3 (D11 + D13: Version + Audit + Z3.19 fix)
6. S3.4 (atomic stage-end — Triple-Rule applied)
7. S4-S8 per original MDRS v2 plan

**تعداد:** 30 آیتم باز برای v2.14 (17 Z3.x + 3 Z3.x جدید Z3.18-Z3.20 + 9 M-lessons existing + 2 M-lessons جدید M101-M102 + 1 Principle + 1 R-NEW Rule #۷۷)
**آخرین به‌روزرسانی:** 2026-05-22 (پایان چت `TRADING-phase1-part04-mdrs-v2-completion` در پایان S3.0)

---

## 🔴 آیتم‌های جدید — کشف‌شده در چت `TRADING-phase1-part05-mdrs-v2-s31-redo` boot (post-part04 audit)

**منبع:** Helper chat post-part04 audit (Z3.21, Z3.22, Z3.23) + Claude part05 boot reasoning (Z3.24 — Discovery #4 escalated to high در turn 4).

**ثبت در S3.0.5 (atomic sub-commit جدا، نه carry-in-S3.1)** — per Rule #60 spirit (PENDING-EOC in-the-moment extended to Z-drift) + M98 (Review Scope Closure: prevent S3.1 constitution-content scope contamination).

### Z3.21: Manifest re-run policy at chat-end mid-stage

**Category:** open policy question (not state drift). Decision-pending در S3.4 یا v2.14 design.
**Severity:** 🟡 medium
**Discovered by:** helper chat post-part04 audit

**Description:** HANDOFF_TEMPLATE explicit state-of-record list (SESSION_STATUS + CHAT_LOG + PENDING) شامل PROJECT_MANIFEST نیست. این conscious architectural decision است (manifest re-run فقط در stage-end per Triple-Rule M93). ولی chat-end mid-stage manifest drift از Review #002 file revealed: S2.5 manifest timestamp `2026-05-22T09:37:59Z` قبل از S3.0 commit `15e8e37` بود، Review #002 file ساخته شده در S3.0 در manifest نیست.

**Options:**
- A. Keep current (manifest only at stage-end) — accept mid-stage drift as expected
- B. Extend Triple-Rule (manifest re-run also در chat-end mid-stage)
- C. New 4th doc category (state-of-record-at-boundary vs at-stage-end)

**Action:** در S3.4 یا v2.14 design decided شود.

---

### Z3.22: Rule #60 text expansion — scope clarification

**Category:** rule text refinement
**Direction:** Z3.22 -> Rule #60 text update در v2.14 (Z-to-Rule allowed). NOT reverse.
**Severity:** 🟢 low
**Discovered by:** helper chat + Claude part05 reasoning

**Description:** Rule #60 text صریح "[PENDING-EOC]" می‌گوید (work items only). ولی فایل `PENDING_FOR_NEXT_VERSION.md` در عمل ۵ نوع item را hold می‌کند: Z-drift در state، M-candidate lessons، Rule candidates، policy questions، work-EOC items. Rule text vs file usage drift دارد.

**Action:** در v2.14، Rule #60 text expand شود تا scope file را accurately reflect کند، یا namespace split implement شود (هماهنگ با Z3.24 broader meta-design).

---

### Z3.23: Workspace handoff files lifecycle policy

**Category:** open policy question
**Severity:** 🟢 low
**Discovered by:** helper chat post-part04 audit (broader pattern from Z3.18)

**Description:** `claude_workspace/incoming_permanent/` در طول زمان accumulate می‌کند. در حال حاضر: part02 (stale, Z3.18)، part04 (consumed by part05 boot)، part05 (will be consumed by part06). part06+ خواهند آمد. Z3.18 فقط یک stale file را cover می‌کند، broader lifecycle policy غایب: کدام archive، کدام delete، چه زمان، چه retention?

**Options:**
- A. Keep-all (no deletion، honors Rule #24 strictly)
- B. Archive after N chats (نقل مکان به `archive/` subfolder)
- C. Delete after explicit "no longer needed" approval per file
- D. Hybrid (consumed handoffs archived، stale ones deleted post-decision)

**Action:** policy design در S8 cleanup یا v2.14.

---

### Z3.24: Namespace categorization gap in PENDING_FOR_NEXT_VERSION.md

**Category:** meta-design / broader namespace issue
**Severity:** 🟠 high (escalated from medium per M75 within-file consistency reasoning)
**Discovered by:** Claude part05 turn 3 (Discovery #4، escalated turn 4)

**Note (self-reference):** این Z-item خود نمونه‌ای از mixed namespace است که توصیف می‌کند — یک meta-observation/policy-question که در Z-namespace ثبت شده. این self-reference explicit است (M77 spirit honored).

**Description:** `docs/PENDING_FOR_NEXT_VERSION.md` در حال حاضر ۵ نوع item را mixed hold می‌کند: Z-drift در state، M-candidate lessons، Rule candidates، policy questions، work-EOC items. هیچ namespace separation وجود ندارد.

**Related:** Z3.22 (narrow Rule #60 text expand)، Rule #60 (PENDING-EOC concept)

**Resolution dependency direction:** Z3.24 broader than Z3.22.
- Z3.22 alone insufficient — حتی اگر Rule #60 text expanded to cover current usage، namespace mixed باقی می‌ماند.
- Z3.24 needs explicit decision (Option A/B/C below) independent of Z3.22 text scope.
- Misread risk: "Z3.22 resolved -> Z3.24 auto-resolved" — FALSE.

**Options for v2.14 (or later):**
- A. Keep mixed (current) — accept categorization ambiguity. Z3.22 resolution expands Rule #60 text to acknowledge mixed scope.
- B. Add category markers in headers — formalize as required field. Current entry texts (Z3.21-Z3.24) already use "Category:" line. Make mandatory for all future entries.
- C. Split namespaces — `Z3.x` state drift، `P3.x` policy questions، `W3.x` work-EOC، M-candidate (existing), Rule-candidate (existing). Most invasive but cleanest.

**Action:** decision deferred به v2.14 design phase or later.

**Migration note (if Option C selected):**
- Z3.21 -> P3.1 (policy question)
- Z3.23 -> P3.2 (policy question)
- Z3.24 -> meta (or P3.3)
- Z3.22 stays as Z (rule text refinement)
- M-candidates and Rule-candidates already separate namespaces

---

**این sub-section 4 آیتم اضافه می‌کند: Z3.21-Z3.24.**

⚠️ **Note on aggregate count:** خط count موجود ("30 آیتم باز برای v2.14") arithmetic discrepancy دارد (17+3+9+2+1+1=33، نه 30) + Rule candidates list (#68-#77 = 10) شمارش نشده. این Discovery #8 از boot چت part05 است. کل count بازنویسی + reconciliation در S3.4 PENDING cleanup انجام می‌شود، نه اینجا (S3.0.5 scope closure M98).

**آخرین به‌روزرسانی sub-section:** 2026-05-23 (boot چت `TRADING-phase1-part05-mdrs-v2-s31-redo` در S3.0.5)

---

## 🔴🔴🔴 آیتم‌های استراتژیک — کشف‌شده در چت `TRADING-phase1-part05-mdrs-v2-s31-redo` در پایان (chat-end)

**منبع:** در تلاش S3.1 (Rules + Lessons drafting)، pattern "Late-Catch Cascade" شناسایی شد — ۳ iteration روی Chunk 1 با ۱۰ helper catches (Concerns C1-C6 + Sub-issue + sub-cascade). تصمیم strategic: defer S3.1 تا D24 (Helper Infrastructure) پایه‌ریزی شود.

---

### D24: Helper Infrastructure (MDRS v2 دلیورابل جدید)

**Category:** MDRS v2 deliverable (parallel به D8-D23)
**Severity:** 🔴 critical (blocker برای S3.1+ efficient execution)
**Discovered by:** Claude + user post-Chunk 1 چت part05
**Status:** Designed in helper sandbox post-S3.0.5، implementation در چت جدید `TRADING-mdrs-v2-D24-helper-infrastructure`
**Position:** parallel deliverable به D8-D23 (نه سریال در stages)

**Scope (high-level):**

1. **Persistent Context Layer** — Project Knowledge + Instructions در helper environment
2. **Helper Operating Protocol** — `docs/HELPER_PROTOCOL.md` (T1 governance doc)
3. **Comprehensive Review Framework** — 7-layer review (currently ad-hoc bridge)
4. **Cross-Chat Learning Continuity** — Helper Lessons sub-section در `02_lessons.md`
5. **Triggers و Operating Modes صریح** — کی helper نیاز است، کی نه؛ severity-based (per Rule #77 candidate Hybrid C)

**Implementation chat:** `TRADING-mdrs-v2-D24-helper-infrastructure`
**After D24:** چت `TRADING-phase1-part06-mdrs-v2-s31-redo-with-helper-infra` برای S3.1 redo با benefit از D24 infrastructure

**Evidence base برای D24 necessity:**
- چت part05 turn 1-2: ۳-۴ helper-round (review % افزایش ۸۵→۹۲→۹۵→۹۷→۹۸٪) با diminishing returns observed
- چت part05 turn 8-10: Chunk 1 helper review، C1 (M88 self-violation) caught — این pattern سیستمی است، نه isolated catch
- pattern: substantive content drafting بدون proper helper integration = late-catch cascade

---

### M-candidate: Late-Catch Cascade Pattern

**Category:** M-lesson candidate
**Severity:** 🔴 critical (process anti-pattern)
**Number assignment:** در S3.1 redo (part06) decide شود (consistent با Reserved IDs philosophy، avoid collision با Discovery #9 helper-side که هنوز formalize نشده)
**Discovered by:** Claude + user post-Chunk 1 چت part05 turn 10

**Description:** وقتی draft در چند iteration helper review می‌شود و در هر iteration N catches ظاهر می‌شوند (pattern: 6 catches turn N → 1-3 catches turn N+1 → 1 catch turn N+2)، این signal است که process upstream نیاز به تغییر دارد، نه drafting. ادامه iteration در همان mode = quadratic cost increase بدون fundamental improvement.

**Symptoms:**
- ۳+ iteration روی یک chunk
- ۲+ structural concerns (نه precision)
- self-violation از rules ای که خود نوشتیم (e.g. M88 genus در Rule #68 turn 10 — eat-your-own-dogfood failure)
- Helper reviews می‌گویند "X% ready" که در هر round افزایش می‌یابد ولی fundamental concerns همچنان appear می‌کنند

**Trigger برای action:** ۳ iteration روی یک substantive chunk با ۱۰+ total catches → stop، evaluate process، not draft

**Action proposed:** D24 (Helper Infrastructure) addresses root cause:
- Persistent context = helper sees full pattern history، نه fragmented prompts
- Operating protocol explicit = mode-switching deterministic
- 7-layer review = systematic، نه ad-hoc

**Evidence:** چت part05 خود (turn 1-10) = full evidence trace

---

### Discoveries Log چت part05 (per Rule #77 candidate continuous logging — final consolidation در chat-end)

| # | Type | Severity | Description | Surfacing |
|---|---|---|---|---|
| #1 | tool | 💡 cosmetic | MCP transient timeout × 2 (PENDING read + read_multiple_files batch) — resolved by retry | handoff (logged here) |
| #2 | discovery | 🟡 medium | helper findings × 3 (manifest drift، SESSION_STATUS inconsistency، CHAT_LOG revert clarity) — accepted، plan S3.4 (deferred to part06) | turn 2 |
| #3 | process | 🟠 high | M98 self-correction → S3.0.5 sub-commit جدا (نه carry-in-S3.1) | turn 3 |
| #4 | meta | 🟠 high (escalated) | Namespace gap → Z3.24 added (broader Z+M+Rule+policy+work mix) | turn 4 |
| #5 | design | 🟠 high | Rule #77 ۶-aspect explicit (trigger + format + numbering=per-chat-reset + surfacing=Hybrid-C + escalation + relationships) | turn 4 |
| #6 | tradeoff | 🟡 medium | Concern 1+2 judgment decisions (Z3.24-now + combined Rule #77) | turn 5 |
| #7 | meta | 🟡 medium | Dependency-direction field broader gap (Z-items "Related:" undefined) — partial Z3.24 coverage | turn 6 (handoff) |
| #8 | drift | 🟡 medium | PENDING aggregate count arithmetic discrepancy (17+3+9+2+1+1=33، listed 30) + Rule candidates list (#68-#77 = 10) un-counted | turn 7 |
| #9 | process | 🟠 high | EXECUTE-block separation between user-actions and Claude-actions ambiguous (Phase 1 vs Phase 2 mix) — corrected | turn 8 |
| #10 | process | 🟡 medium | Helper-gate misinterpretation — helper consultative، نه approval gate per Rule #51 | turn 8 |
| #11 | process | 🟠 high | Anti-pattern self-violation in active drafting (Rule #68 explicit list نقض M88 genus) — caught by helper Concern C1 | turn 9 |
| #12 | process | 🟡 medium | M88 genus second-order anti-pattern (endorsing deprecated files as positive examples) — caught by helper Sub-issue | turn 9 |
| #13 | process | 🔴 critical | **Late-Catch Cascade Pattern recognized** — strategic decision: defer S3.1، deliver D24 first | turn 10 (this chat-end) |

---

### Stale handoff file note

`claude_workspace/incoming_permanent/PHASE1_PART05_MDRS_V2_S31_REDO_HANDOFF.txt` becomes stale due to S3.1 deferral. Cleanup deferred to S8 per Z3.18/Z3.23 policy (existing). NOT removed in این chat-end commit.

---

**تعداد سطح-strategic items اضافه شده در این chat-end:** D24 (deliverable) + M-candidate (Late-Catch Cascade) + 13 Discoveries (#1-#13 consolidated).

**آخرین به‌روزرسانی strategic section:** 2026-05-23 (chat-end چت `TRADING-phase1-part05-mdrs-v2-s31-redo`)

---

## 🔴🔴🔴 آیتم‌های D24 chat-end (چت `TRADING-phase1-part06-mdrs-v2-D24-helper-infrastructure`)

**منبع:** D24 implementation chat. HELPER_PROTOCOL.md created (commit `bed06b3`), Review #003 Implemented (`daf2020` → `bed06b3` → this chat-end), helper round 1 داد 9 findings (all applied), 7 Discoveries logged.

**Status:** D24 5-scope design + HELPER_PROTOCOL.md T1 governance doc تولید شد. baqi items (HM-series implementation, main.md cross-ref, etc.) به part07 S3.1 redo deferred.

---

### K1: HM-namespace target sub-section

**Category:** D24 Design Deferred for part07

**M-candidate Late-Catch Cascade implementation در part07 S3.1:** target sub-section **"Helper Consultation Lessons (HM-series)"** در `02_lessons.md` §۲.۹ (after current §۲.۸). Design pattern در HELPER_PROTOCOL.md §۵ تعریف شد.

**First HM entries candidates (per part07 implementation):**
- HM-1: Helper Consultative Misinterpretation (from Discovery #10 part05)
- HM-2: Late-Catch Cascade Pattern (from Discovery #13 part05)
- HM-3: Chat Naming Convention Adherence (from Discovery #5 D24)
- HM-4: Modified Round-1.5 edge case (from Discovery #1 D24)
- HM-5: Self-Referential First-Application chicken-and-egg (from Discovery #3 D24)
- HM-6: Post-Correction Propagation Audit (from Discovery #6 D24)
- HM-7: D24 Iteration Budget Self-Assessment (from Discovery #7 D24)

---

### K2: main.md cross-ref edit

**Category:** D24 Design Deferred for part07

`docs/constitution/main.md` "Cross-references اصلی" section — add entry برای `docs/HELPER_PROTOCOL.md` در part07 S3.1 atomic.

---

### K3: Helper-discovered patterns در D24 round 1

**Category:** D24 Helper-Discovered Patterns

**Helper round 1 results (per HELPER_PROTOCOL §۴ 8-Layer Framework, retroactively codified):**
- Total: 9 findings (0 critical, 2 high, 6 medium, 1 low)
- L1.1 [CRITICAL eat-your-own-dogfood]: §۲.۲ Layer A explicit-list (M88 genus) — applied
- L1.2 [medium]: pattern violation in §۸ — implicitly resolved by L1.1 fix
- L2.1 [medium]: Rule #51 over-claim "absolute" — applied (scope specified)
- L2.2 [medium]: CLAUDE_CHECKLIST.md missing cross-ref — applied
- L4.1 [medium]: §۵.۶ forward-reference disclaimer — applied (M98 caveat)
- L5.1 [low]: Rule #77 (candidate) tagging — applied
- L7.1 [medium]: M82 verify §۲.۸/§۲.۹ section refs — applied (verified pre-write)
- L8.1 [HIGH]: §۲.۴ Project K refresh enforcement — applied (4-sub-section overhaul)
- L8.2 [medium]: §۲.۵ Persian hardcode — applied (principle-reference)
- Section 3 (Review #003): clean (1 minor consistency check passed)

**Escalation:** Modified Round-1.5 (L1.1 critical + 8 medium/low → single batch fix + skip round 2 per §۳.۴ intent). Proof of Bounded Bootstrap criteria functional.

---

### K4: Discoveries Log D24 (per-chat reset, anticipated mutual M101)

**Category:** Discoveries Log per-chat

| # | Type | Severity | Description |
|---|---|---|---|
| #1 | meta | 🟠 high | §۳.۴ Modified Round-1.5 edge case absent (post-helper-round-1 single-batch fix without helper round 2). HM-candidate part07 |
| #2 | validation | 💡 cosmetic | Bounded Bootstrap criteria §۳.۴ validated functional — caught L1.1 critical + 8 medium/low. Proof of process |
| #3 | process | 🟡 medium | Self-application: helper applies 8-Layer Framework defined در subject under review (self-referential chicken-and-egg pattern, genus M77/M101). HM-candidate part07 |
| #4 | recursion | 🟡 medium | L1.1 خود همان pattern است که D24 was created to prevent. Counter-factual: if L1.1 caught نمی‌شد, D24 با خود-violation deliver می‌شد. Most-important catch چت |
| #5 | process | 🟠 high | Chat Naming Convention Drift — boot files صراحت در next-chat-name pattern نداشتند → Claude initial naming drifted از `TRADING-phaseX-partY-{topic}`. User manual corrected به `TRADING-phase1-part06-mdrs-v2-D24-helper-infrastructure`. HM-candidate part07 |
| #6 | process | 🟠 high | Naming Correction Lag — corrections در یک layer (chat name) applied, ولی downstream numbering (handoff filename, PENDING references) با old mental model continued. Micro Late-Catch Cascade. HM-candidate part07 |
| #7 | process | 🟡 medium | D24 iteration budget assessment: ~15+ turn, 2 helper round, 7+ Discovery — over-budget برای T1 doc creation per industry standard. Justifiable چون D24 خود infrastructure را می‌سازد (self-application). HM-candidate part07: post-D24 deploy, helper consultation efficiency باید measurably بهبود یابد |

**Anticipated Discovery #1 D24-chat-end (mutual M101 chain):** D24 chat-end hash needs backfill در part07 (mirroring `91d20d8` backfill در این چت). This forward-anticipation explicit per K4.

---

### K5: Z3.24 Option B interim caveat

**Category:** Z3.24-related interim convention

D24 پیشدستانه Z3.24 Option B ("Category:" field) را اعمال می‌کند. **caveat:** Interim convention adopted (D24): Category: field per Z3.24 Option B (formal decision deferred به v2.14 design). اگر Option C selected, migration لازم. Parallel با ACCEPTABLE_VERSIONS pattern M102 (transitional safety).

---

### K6: Project Knowledge refresh enforcement integration

**Category:** D24 Design — stage-end protocol extension

از HELPER_PROTOCOL §۲.۴.۲: Project K refresh check باید در main chat stage-end protocol integrated شود (visible per M100). Implementation در part07 S3.1 یا later stage. Candidates:

1. (الف) Add as Pre-Add Check 11 در PRE_ADD_CHECKLIST.md
2. (ب) Add as explicit step در stage-end Triple-Rule (M93 extension)
3. (ج) Standalone protocol section در HELPER_PROTOCOL §۲.۴

Decision deferred به part07.

---

### K7: Chat Naming Convention Formalization (HM-candidate)

**Category:** D24 Helper-Discovered Patterns

**Discovery source:** D24 turn 12 — user caught initial chat name `TRADING-mdrs-v2-D24-helper-infrastructure` drifted از pattern. Corrected manual به `TRADING-phase1-part06-mdrs-v2-D24-helper-infrastructure`.

Discovery #6 (naming correction lag) sub-discovery: post-correction propagation pending قبل از Phase 1 — off-by-one در handoff filename + K7 reference text.

**Pattern (project standard):** `TRADING-phase{N}-part{NN}-{topic-slug}`

- phase{N}: تک-رقم 0-based
- part{NN}: incremental number
- topic-slug: kebab-case description

**HM-candidate scope:** Chat Naming Convention Adherence
- Each chat-end handoff explicit declare next chat name pattern
- SESSION_STATUS "next chat" section explicit با pattern reference
- New-chat Claude boot procedure includes naming verification check (alert if drift detected)
- Boot mandatory file reads include chat-name self-check
- Post-correction propagation audit (Discovery #6 sub-genus): هر naming correction باید explicit cascade check به downstream artifacts را trigger کند

**Implementation در part07 S3.1 (with constitution v2.14 atomic update):**
- HM-3 entry در `docs/constitution/02_lessons.md` §۲.۹ HM-series
- Update HANDOFF_TEMPLATE.md to add "NEXT CHAT NAME (MANDATORY PATTERN)" section (per D24 Action 1 precedent)
- Optional: Audit Check #12 candidate (pre-add chat-name validation)

---

### Stale handoff files note

`claude_workspace/incoming_permanent/PHASE1_PART05_..._HANDOFF.txt` و `PHASE1_D24_HELPER_INFRA_HANDOFF.txt` به دلیل consumption در چت‌های بعد stale می‌شوند. Cleanup deferred به S8 per Z3.18/Z3.23 policy (existing). NOT removed در این chat-end commit.

---

**تعداد items اضافه شده در D24 chat-end:** K1-K7 (7 deferred items) + 7 Discoveries (#1-#7 consolidated).

**آخرین به‌روزرسانی D24 section:** 2026-05-23 (chat-end چت `TRADING-phase1-part06-mdrs-v2-D24-helper-infrastructure`)

---

## 🔴🔴🔴 آیتم‌های part07 chat-end (چت `TRADING-phase1-part07-mdrs-v2-s31-redo-with-helper-infra`)

**منبع:** S3.1 + S3.2 implementation chat. در part07، S3.1 (Constitution v2.14 atomic update) و S3.2 (Principles Golden Rule + Templates 11-12) تکمیل شدند. S3.3 + S3.4 به part08 deferred (Option B wrap-up per HM-2 prevention).

**Status K1-K7 update (پس از part07):**
- **K1** (HM-namespace target sub-section): ✅ **Implemented** در S3.1 — §۲.۹ NEW با HM-1 to HM-7 (7 entries first corpus)
- **K2** (main.md cross-ref edit): ✅ **Implemented** در S3.1 — Helper Consultation NEW subsection در «Cross-references اصلی»
- **K3** (Helper-discovered patterns D24 round 1): 🔴 باقی — فقط reference در HM-series، full integration در future maintenance
- **K4** (Discoveries Log D24): 🔴 باقی — D24 Discoveries reference در HM-series، ولی full integration پستار D24 Discovery #1 D24-chat-end mutual M101 backfill (`3bf66bf`) ✅ در part07 boot confirmed
- **K5** (Z3.24 Option B interim caveat): 🔴 باقی — decision deferred به v2.14 design phase یا later
- **K6** (Project K refresh enforcement integration): 🔴 باقی — candidates A/B/C decision deferred
- **K7** (Chat Naming Convention HM-candidate): ✅ **Partially Implemented** در S3.1 — HM-3 entry در §۲.۹. HANDOFF_TEMPLATE.md "NEXT CHAT NAME" section در D24 (precedent)، part08 boot mandatory check

---

### K8 (جدید part07): HELPER_PROTOCOL §۷ refinement + main.md Quick-start update

**Category:** D24 Design Deferred for S3.2-S3.3 — Expanded با part07 Discoveries learning

**Severity:** 🟡 medium

**Discovered by:** Discovery #1 + #3 part07 (multi-table sync hazard + SESSION_STATUS descriptive M-range drift) — user-predicted در turn S3.1 audit fail evaluation

**Description:** دو تعدیل مرتبط برای HELPER_PROTOCOL / Quick-start مورد نیاز است:

**۱. main.md Quick-start (linked به Rule #۴۸):**
facenati Quick-start section فعلاً HELPER_PROTOCOL.md را در mandatory reading list ندارد. اگر helper consultation در یک stage انتظار می‌رود، boot procedure آن را skip می‌کند. **Timing:** همراه با Rule #۴۸ refresh در S3.2 یا S3.3.

**۲. HELPER_PROTOCOL §۷ Upfront Constraint Checklist Pattern refinement:**
constraint checklist باید explicit step **«scan کامل T1 docs برای descriptive references به ID ranges (M-range، Rule-range)»** را include کند — نه فقط counts/headings. این user-predicted improvement در part07 S3.2 empirically validated (۰ audit fail vs ۳ audit fail در S3.1).

**Action proposed:** part08 یا future maintenance pass:
- Add new sub-step §۷.X (یا §۷.۲ extend) در HELPER_PROTOCOL.md
- mandatory descriptive scan: M-range ، #-range، Template-count ، version label ، ID enumeration همگی
- Pattern signature: «هر number-range در prose در T1 doc = potential drift target»

**Source:** Discovery #1 (multi-table sync hazard) + Discovery #3 (SESSION_STATUS descriptive M-range drift) + Discovery #4 (proactive scan applied learning).

**Severity rationale:** medium — boot completeness + constraint checklist completeness. helper usable بدون boot mention، ولی Discovery #1+#3 در audit fail show شدند، نه silent break.

---

### Discoveries Log part07 (4 total, per-chat reset, consolidated)

| # | Type | Severity | Description |
|---|---|---|---|
| #1 | process | 🟡 medium | آمار table updated در main.md ولی ساختار ماژول‌ها table missed — multiple-table sync hazard (caught by Layer 1 Audit round 1). resolved by surgical fix «ساختار ماژول‌ها» table M1-M87 → M1-M102. → K8 expansion |
| #2 | validation | 🟠 high | M101 self-referential paradox — درس M101 می‌گوید «hash hardcode نکن» ولی جزئیات M101 در ۴ جا ۶ hardcoded hash داشت (caught by audit check_5). resolved by abstract placeholder + CHAT_LOG.md authoritative source reference + explanatory note (M101 honored its own lesson). audit working as designed |
| #3 | validation | 🟡 medium | SESSION_STATUS.md descriptive M-range reference drift (M1-M87) پس از 02_lessons.md update به M102. Same genus as #1، confirmation full T1 scan در constraint checklist لازم (caught by Layer 1 Audit round 2). resolved by surgical fix «درس‌نامه» line M1-M87 → M1-M102 + ۳۲ Reserved + HM-series. → K8 expansion |
| #4 | process | ✨ positive | Proactive full T1 scan در S3.2 prevented audit fail — Discovery #1+#3 learning applied از helper constraint checklist user-predicted improvement. ۰ audit fail در S3.2 vs ۳ audit fail در S3.1. **HELPER_PROTOCOL infrastructure value empirically demonstrated**. HM-7 metric validation: S3.1=۹ turn (reactive)، S3.2=۲ turn (proactive applied learning). |

**Most critical:** **Discovery #2 — M101 self-referential paradox** — درس خود را نقض کرد، audit آن را caught کرد.
**Most insightful:** **Discovery #4 — Proactive applied learning** — user-predicted improvement empirically validated.

---

### Stale handoff file note (تصمیم cleanup deferred)

`claude_workspace/incoming_permanent/PHASE1_PART07_HANDOFF.txt` پس از part07 boot stale می‌شود. Cleanup deferred به S8 per Z3.18/Z3.23 policy (existing). NOT removed در این chat-end commit.

### Commit message workspace files (Z3.18/Z3.23 policy)

untracked files در `claude_workspace/`:
- `commit_msg_chat_end_part05.txt`
- `commit_msg_d24_0.txt`
- `commit_msg_d24_1.txt`
- `commit_msg_d24_chat_end.txt`
- `commit_msg_s3_0_5.txt`
- `commit_msg_s3_1.txt` (🆕 part07)
- `commit_msg_s3_2.txt` (🆕 part07)
- `commit_msg_part07_chat_end.txt` (🆕 part07)

همه preserved per Z3.18/Z3.23 policy (consumed by -F flag، نه committed در git، ولی historical reference حفظ شود). cleanup decision در S8 hybrid policy.

---

**تعداد items اضافه شده در part07 chat-end:** K8 (new) + K1-K2 implemented + K3-K7 status update + 4 Discoveries (#1-#4 consolidated).

**آخرین به‌روزرسانی part07 section:** 2026-05-23 (chat-end چت `TRADING-phase1-part07-mdrs-v2-s31-redo-with-helper-infra`)

---

## 🔴🔴🔴 آیتم‌های part08 chat-end (چت `TRADING-phase1-part08-mdrs-v2-s33-s34-completion`)

**منبع:** S3.3 + S3.4 implementation chat. در part08، S3.3 (Module Headers + Audit + Z3.19/Z3.12 RESOLVED — commit `35ea822`) و S3.4 (Triple-Rule atomic stage-end + Review #۰۰۲ Implemented + Manifest D2 re-run + handoff part09) تکمیل شدند. S4 (D12 Audit Checks #۸-۱۱) defer به part09 per conservative budget policy. **Stage S3 رسماً COMPLETE.**

**Status K1-K8 update (post-part08):**
- **K1, K2:** ✅ Implemented در part07 — unchanged
- **K3-K7:** 🔴 باقی — defer به part09 یا future maintenance
- **K8** (HELPER_PROTOCOL §۷ refinement + main.md Quick-start): 🔴 باقی — defer به part09

---

### K9 (NEW part08): HM-candidate — Tool Discovery First

**Category:** D24 Helper-Discovered Pattern
**Severity:** 🟠 medium-high
**Discovered by:** Discovery #1 boot چت part08

**Pattern:** Claude initial response در fresh chat با visible tool list مشاهده می‌کند ولی deferred tools (Filesystem MCP، Memory، Computer use) معمولاً نمی‌بیند تا `tool_search` صدا بزند. در part08 boot، Claude اولاً ادعا کرد "filesystem access ندارم"، که factual incorrect بود — نیاز به `tool_search` بود.

**Lesson candidate (HM-8):** قبل از declaring capability gap، Claude باید `tool_search` با keywords مرتبط (e.g., `filesystem`، `git`، `browser`) صدا بزند. system prompt صراحت می‌گوید: "Treat tool_search as free and call it before assuming a capability is unavailable."

**Prevention:** اضافه کردن explicit step به boot protocol (Rule #۴۸ یا HELPER_PROTOCOL §۲): "before declaring capability unavailable، call tool_search."

**Genus:** capability assumption failure. parent از HM-1 (Helper Consultative Misinterpretation) genus — both involve premature conclusion before checking.

---

### K10 (NEW part08): HM-candidate — MCP Liveness Mid-Conversation

**Category:** External dependency reliability + Helper-Operating Protocol
**Severity:** 🟠 medium-high (escalated از 🟡 medium پس از observation #۲)
**Discovered by:** Discovery #2 boot چت part08 + recurrence در S3.4 Phase 1

**Pattern (refined per 2 empirical observations):** MCP server liveness across single chat not guaranteed. server که N turn پیش موفقیت‌آمیز جواب داد، می‌تواند بدون warning hang کند.

**Observations:**
- **Obs 1 (boot turn part08):** اولین `read_file` پس از successful `list_directory` × ۲ به timeout 4-minute رسید. user restart resolved.
- **Obs 2 (S3.4 Phase 1):** اولین `edit_file` در S3.4 (REVIEW_LOG.md) پس از successful S3.3 batch از ۸ × edit_file calls در turn قبل، به timeout رسید. user restart resolved + retry موفق بود.

**Refined pattern:** MCP server hang ممکن است پس از idle period، specific operation sequences، یا بدون deterministic cause اتفاق بیفتد. حتی mid-batch می‌تواند hang کند.

**Lesson candidate (HM-9):** boot protocol و mid-chat operation protocol باید:
- sanity-ping pattern (lightweight `list_allowed_directories` or `list_directory`) قبل از batch operations سنگین
- recovery procedure explicit: user restart → sanity-ping → verify state via read → retry from exact point
- failed call باید state روی disk verify شود قبل از retry (timeout response را نمی‌دهد که server-side عمل کرده یا نه)

**Prevention:** HELPER_PROTOCOL §۲.۴ یا boot procedure: explicit sanity-ping pattern + recovery procedure documented.

**Genus:** external dependency reliability. parent از HM-3 (Chat Naming Convention) genus — both involve environment-assumption failure.

---

### Discoveries Log part08 (8 total, per-chat reset, consolidated)

| # | Type | Severity | Description |
|---|---|---|---|
| #1 | meta | 🟠 high | Tool-discovery-first violation در boot turn — capability claim بدون tool_search. → K9 HM-candidate (HM-8) |
| #2 | tool | 🟠 medium-high | MCP filesystem server hang mid-conversation × ۲ (boot + S3.4 Phase 1) — restart × ۲ resolved. → K10 HM-candidate (HM-9) |
| #3 | drift | 💡 cosmetic | HANDOFF_TEMPLATE.md §۷ "Rule #68.2 Boot Protocol" typo (should be #۴۸). defer maintenance pass. |
| #4 | timing | 💡 cosmetic | PHASE1_PART08_HANDOFF.txt گفت "§۶.۸ Custom Instructions" ولی location actual §۶.۴. defer. |
| #5 | drift | 💡 cosmetic | Module sub-headers descriptive prose (`#۱-۶۵ تا v2.11`، `M1-M63 از v2.11`) — describes historical migration source. defer. |
| #6 | communication | 💡 cosmetic | User constraint added: "helper ambiguities in copy-able box". adopted from turn 14. Plus "USER DECISIONS NEEDED" box pattern (turn before Phase 1). |
| #7 | validation | ✨ positive | **HM-7 metric empirically validated** — S3.3 part08 = ۱ commit، ۰ audit fail (proactive scan applied). Post-D24 efficiency demonstrated empirically. |
| #8 | communication | 💡 cosmetic | CMD silent-on-success confusion (user thought `cd`/`git add` didn't run) — explained. lesson: note silent commands in future EXECUTE blocks. |

**Most critical:** Discovery #۷ — HM-7 metric positive validation. infrastructure value demonstrated empirically (۳ datapoints: S3.1 = ۳ audit fail, S3.2 = ۰, S3.3 = ۰).
**Most insightful:** Discovery #۱ + #۲ — HM-8 + HM-9 candidates (capability assumption + external dependency reliability).

---

### Stale handoff files note (Z3.18/Z3.23 broader policy)

`claude_workspace/incoming_permanent/PHASE1_PART07_HANDOFF.txt` و `PHASE1_PART08_HANDOFF.txt` پس از part08 boot stale می‌شوند. Cleanup deferred به S8 per Z3.18/Z3.23 policy (existing). NOT removed در این chat-end commit.

### Commit message workspace files (Z3.18/Z3.23 policy)

untracked files در `claude_workspace/`:
- `commit_msg_chat_end_part05.txt`، `commit_msg_d24_*.txt`، `commit_msg_part07_chat_end.txt`، `commit_msg_s3_0_5.txt`، `commit_msg_s3_1.txt`، `commit_msg_s3_2.txt`
- `commit_msg_s3_3.txt` (🆕 part08)
- `commit_msg_s3_4_chat_end.txt` (🆕 part08)

همه preserved per Z3.18/Z3.23 policy (consumed by -F flag، نه committed در git، historical reference). cleanup decision در S8 hybrid policy.

---

**تعداد items اضافه شده در part08 chat-end:** K9 + K10 (NEW HM-candidates) + Z3.19 RESOLVED + Z3.12 RESOLVED + 8 Discoveries (#1-#8 consolidated) + K1-K8 status update.

**آخرین به‌روزرسانی part08 section:** 2026-05-24 (chat-end چت `TRADING-phase1-part08-mdrs-v2-s33-s34-completion`)

---

## 🔴🔴🔴 آیتم‌های part09 chat-end (چت `TRADING-phase1-part09-mdrs-v2-s4-audit-checks`)

**منبع:** part09 → S4 (D12 Audit Checks #۸-۱۱) commit `234ba2f` (push شده، 11/11 pass). chat-end Triple-Rule **defer** شد (HM-2 escape، HM-9 cumulative ۶ event part09). جزئیات کامل deferred در `incoming_permanent/PART09_CHAT_END_DEFERRED_NOTE.txt` + `claude_workspace/HELPER_SESSION_TODO_part09_final.md` (۳۸ observation، ۱۹ user catch، Mechanism A-E، Criteria C1-C9، W1-W3، L1-L2) — این بخش reference list است (per M59/F41 anti-over-compression).

### Z3.x RESOLVED در S4 part09 (`234ba2f`)
- **Z3.15** (S1 D2 self-reference first-run gap) → ✅ RESOLVED in S4 part09 (`234ba2f`).
- **Z3.16** (Review numbering integrity audit) → ✅ RESOLVED in S4 part09 (`234ba2f`).
- **Z3.17** (Z-ID Permanence anti-pattern / M96) → ✅ RESOLVED in S4 part09 (`234ba2f`).
- **Z3.25** → ✅ RESOLVED in S4 part09 (`234ba2f`) per deferred note. ⚠️ یادداشت صداقت (#۸۴): Z3.25 به‌صورت ردیف مستقل در جدول Z3.x این فایل **تعریف نشده** (جدول تا Z3.17، و Z3.18-24 در بخش‌های متنی‌اند). اینجا per منبع deferred note ثبت می‌شود؛ شمارهٔ Z3.25 در جدول جعل نمی‌شود.

### ۸ P10-candidate (carry-forward، اکثراً معلق)
1. Helper-Sandbox Synthesis Drift (M-candidate، meta).
2. Bootstrap Paradox of Cross-Chat Infrastructure (M-candidate، meta).
3. Cross-Side Decision Sync Failure (M-candidate، process).
4. live_inbox setup formalization (design، با residual decision F40).
5. W3 Chat-End File Sync Verification → Rule candidate.
6. HM-9 Tool-Level Reliability → Rule-promotion candidate (cumulative؛ به part10 ادامه).
7. File-Based Decision Tracking Registry for helper sessions (process، automation per HM-META-K).
8. L1 Persian Language Preference → universal rule formalization.

### PERSIST TASKS A-G (معلق part09/10)
وضعیت: 📋 معلق — verify جذب در part11 (THEN-IF-BUDGET این چت). شامل HM-META-H/I/J/K + W4-W5 + B1-B4 boot discipline + Mechanism A-E + Criteria C1-C9 + CHAT_BOOT_TRIGGER_TEMPLATE (که در part09 turn ۷۹ ساخته شد). منبع paste-ready: helper chat part09 turn ۶۹+ (per PART10_BOOT_ESCAPE_NOTE).

### Discoveries part09 (۱۲ — reference)
Discovery #1-#12 part09 در batch preview turn ۲۵ main chat. logging در part10 CHAT_LOG (انجام نشد چون handoff part10 ساخته نشد — رجوع به بخش part10 زیر).

**آخرین به‌روزرسانی part09 section:** 2026-05-30 (full-refresh اتمیک part14، reconcile معوق).

---

## 🔴🔴🔴 آیتم‌های part10 (چت `TRADING-phase1-part10-mdrs-v2-infrastructure-sprint`)

**منبع:** PART10_BOOT_ESCAPE_NOTE.txt + ردیف part10 در PHASE_LEDGER. part10 = Infrastructure Sprint + audit session. HEAD بدون تغییر `90db89f`. **PART10 handoff ساخته نشد** (زنجیرهٔ تک‌حلقه یک‌بار شکست — مدرک پایه‌گذاری PHASE_LEDGER دوحلقه).

### M103 genesis (مهم‌ترین)
**M103 — Audit Over-Promise Pattern** در همین part10 audit session کشف شد: ادعای «deep-scan تقریباً کامل» با ~۳۵٪ coverage واقعی (۳۵-۴۰ از ۲۷۸ classified)، «~۹۸٪ coverage» که مربوط به screenshots بود نه پروژه، و skip خودسرانهٔ Tier 3 (۲۱۴ فایل) + Legacy سند جامع بدون permission. → پشتیبان ۸ Trust Rule #۷۸-۸۵ (codify در part11).

### HM-9 escalation
Cumulative ۱۰ event (part08: 2 + part09: 6 + part10: 2). HM-9 #۹ (boot attempt #1) + #۱۰ (boot attempt #2، edit_file atomic timeout روی PART09_CHAT_END_DEFERRED_NOTE). Rule-promotion candidate تأیید شد. Heavy-write smoke test → Mechanism D (F49).

### P10-CANDIDATEs 9-14
reference در PART10_BOOT_ESCAPE_NOTE (content در helper chat part09 turn ۶۹+: F42-F53، W4-W5، B1-B4، CHAT_BOOT_TRIGGER_TEMPLATE full). همگی معلق/جذب‌شده در مسیر part11.

**آخرین به‌روزرسانی part10 section:** 2026-05-30 (full-refresh اتمیک part14).

---

## 🔴🔴🔴 آیتم‌های part11 (چت codify Trust Rules → v2.15)

**منبع:** ردیف part11 در PHASE_LEDGER. codify ۸ Trust Rule **#۷۸-۸۵** + درس **M103** → Constitution **v2.15** (commit `59c075a`، audit 11/11 PASS). **PART11 handoff ساخته نشد** (مستقیم PART12، `bb964cf`).

- ✅ Trust Rules #۷۸-۸۵ از candidate → **Locked v2.15** (SCM/QHP/NSISN/RDEM/MPTC/HAT/APMM/Self-Activation Lock).
- ✅ M103 از candidate → **Locked v2.15** (§۲.۸ 02_lessons).

**آخرین به‌روزرسانی part11 section:** 2026-05-30 (full-refresh اتمیک part14).

---

## 🔴🔴🔴 آیتم‌های part12 chat-end (`5173e6f`)

**منبع:** ردیف part12 در PHASE_LEDGER. **Phase 2 CLOSED** (verify ۴/۴ فایل غول، backfill #۰۰۵=`59c075a` در REVIEW_LOG و review#005 §۴/§۶) + پایه‌گذاری `PHASE_LEDGER.md` + قانون تداوم دوحلقه‌ای (جایگزین تک‌حلقه). chat-end part12 = `5173e6f` + PART13 handoff.

**آخرین به‌روزرسانی part12 section:** 2026-05-30 (full-refresh اتمیک part14).

---

## 🔴🔴🔴 آیتم‌های part13 chat-end (`3eae91e`)

**منبع:** ردیف part13 در PHASE_LEDGER. **#۰ check_12_continuity** (file-based، invariant H==L+1، chicken-and-egg-safe؛ test_12/13) + **F-A** DECISIONS_LOG→v1.4 + **F-B** check_1 hardening (Latin→Persian/structural anchor، true-PASS ۸۵/۸۵/۸۵؛ test_14) + **F-C** backfill #۰۰۲=`3fd2405`/#۰۰۴=`234ba2f` + Review #۰۰۶/#۰۰۷ + M101 backfill part12. audit ۱۲/۱۲ + tests ۱۴/۱۴ PASS. chat-end part13 = `3eae91e`.

**آخرین به‌روزرسانی part13 section:** 2026-05-30 (full-refresh اتمیک part14).

---

## 🧮 آشتی Count مجموع (Discovery #۸ part05 — reconciled در part14)

خطوط stale «۳۰ آیتم باز برای v2.14» در بخش‌های part03/part04 یک arithmetic discrepancy داشتند. محاسبهٔ درست:

- Z3.x: ۱۷ + ۳ (Z3.18-20) = ۲۰ · M-lessons: ۹ + ۲ (M101-M102) = ۱۱ · Principle (Golden Rule): 1 · Rule candidates (#۶۸-۷۷): **۱۰ (در شمارش قدیمی نادیده)** · R-NEW (#۷۷): جزو همان ۱۰ · Z3.21-24: ۴.
- مجموع منبع: `17+3+9+2+1+1=33` (نه «۳۰») + ۱۰ Rule candidates + ۴ policy/meta = اختلاف ناشی از نشمردن Rule-candidates و sub-sectionهای بعدی.

**وضعیت فعلی (پایان part13/ورودی part14):** این شمارش‌ها **منقضی‌اند** — همهٔ آیتم‌های v2.14 (Rules #۶۸-۷۷ + M88/M93-M102 + Golden Rule + Templates 11-12) در part04-08 **ادغام/Locked** شدند، و آیتم‌های v2.15 (Trust #۷۸-۸۵ + M103) در part11 **Locked** شدند. خطوط «تعداد» قدیمی صرفاً تاریخی‌اند (#۲۴ No-Deletion — حفظ، نه حذف). شمارش معتبر فعلی در `SESSION_STATUS.md` (۸۵ قانون، M1-M103، ۷ Review) و `PHASE_LEDGER.md` است.

**آخرین به‌روزرسانی count-reconciliation:** 2026-05-30 (full-refresh اتمیک part14).

---

## 🔴🔴🔴 آیتم‌های part15 (چت `TRADING-phase1-part15-phase3-fullrefresh-resume`)

**منبع:** part15 = ادامهٔ part14 (PENDING reconcile + manifest D2 + commit اتمیک + chat-end). تعارض escape-note ↔ check_12 کشف و حل شد (گزینهٔ C: ردیف بازه‌ای part14-15، handoff PART16).

### P-candidate (part15) — M104 + Rule #۸۶: Escape-Aware Sequence Derivation ✅ CODIFIED v2.16

**وضعیت:** ✅ **CODIFIED v2.16** (در part16 — M104 §۲.۸ + قانون #۸۶ + main bump v2.16 + Review #۰۰۸ + Decision #۶۸ + audit CURRENT_VERSION→v2.16 + .pre-commit label + count درس ۷۱→۷۲). [تاریخچهٔ candidate + متن verbatim پایین per #۲۴ No-Deletion حفظ شد.] دلیل اولیهٔ سبک‌نگه‌داشتن part15: افزودن قانون+درس = تغییر constitution و کل زنجیره (01_rules + 02_lessons + main + Review #۰۰۸ + DECISIONS_LOG + audit CURRENT_VERSION + .pre-commit label + count درس ۷۱→۷۲) سنگین است.

**علت ریشه‌ای (اشتباه part14 که در part15 گرفته شد):** part14 escape-note شمارهٔ handoff را «PART16» hard-code کرد (از روی الگو/نام انسانی، نه اشتقاق مکانیکی)؛ چون part14 **escape** بود frontier جلو نرفت و مقدار درستِ مکانیکی **PART15** بود — تعارض با check_12 (H==L+1). نقض #۸۴ (APMM، extrapolation از الگو) + cross-check نکردن تعامل escape↔check_12.

**کار لازم در v2.16 (codify در part16):** درس **M104** + قانون **#۸۶** (متن verbatim پایین) + main.md (bump v2.16، آمار، version history) + Review **#۰۰۸** + DECISIONS_LOG + audit `CURRENT_VERSION`→v2.16 + `.pre-commit-config` label + count درس ۷۱→۷۲.

#### متن verbatim برای codify (part16) — عیناً در PART16_HANDOFF نیز هست

**[M104]**
> ### M104 — Mechanical-Claim Verification before Persisting
> Lesson (Normative): هر عدد/شناسهٔ مکانیکی در artifact پایدار (شمارهٔ handoff، hash، ردیف ledger، شمارهٔ قانون/درس/Review، نسخه) باید پیش از نوشتن از منبع زنده (اسکریپت/فایل/git) استخراج شود، نه از حافظه/الگو/استنتاج دنباله‌ای. اگر قابل‌استخراج نیست → فرمول/اشتقاق («بالاترین موجود + ۱») یا placeholder + TODO، نه hard-code.
> Corollary (Escape): پس از escape، شمارنده‌های frontier جلو نمی‌روند؛ هر عدد دنباله‌ای مشکوک است و باید با frontier واقعی + invariant فعال (check_12: H==L+1) cross-check شود.
> Genesis: part14 escape-note off-by-one (PART16 به‌جای مکانیکیِ PART15).
> Cross-refs: نمونهٔ خاص #۸۴ · مکمل #۸۶ · check_12 · M101 · M82.

**[#۸۶]**
> ### #۸۶ — Escape-Aware Sequence Derivation
> Normative: در هر artifact تداوم (escape/handoff/continuity/ledger row) هیچ شمارندهٔ دنباله‌ای literal از حافظه/الگو نوشته نشود؛ باید (الف) از frontier موجود مشتق شود («بالاترین + ۱») و (ب) پیش از قطعی‌شدن با invariant مکانیکی فعال (check_12، H==L+1) سازگار باشد. اگر چت escape شد، صریح ثبت شود frontier جلو نرفته.
> Implementation: قالب escape/handoff به‌جای عدد ثابت بنویسد «handoff بعدی = بالاترین PHASE1_PART{N}_HANDOFF موجود + ۱»؛ قبل از commitِ دارای گیت پیوستگی، audit واقعی اجرا شود؛ تمایز escape (frontier ثابت) ↔ chat-end (frontier +۱) صریح باشد.
> Genesis: part14 escape-note off-by-one.
> Cross-refs: عملیاتی‌کنندهٔ #۸۴ · پشتوانهٔ M104 · check_12 · #۷۹.

**آخرین به‌روزرسانی part15 section:** 2026-05-30 (chat-end چت part15، P-candidate ثبت‌شده در commit اتمیک part14-15).

---

## 🔴🔴🔴 آیتم‌های part17 (چت `TRADING-phase1-part17-phase3-deprecate-and-project-knowledge`)

**منبع:** boot part17 + کشف turn-level.

### M101 backfill part16 ✅ DONE (boot part17)
hash chat-end part16 = `81a3562` (cross-checked از `git rev-parse --short HEAD`، روح #۸۶) در ۲ placeholder از PHASE_LEDGER (ردیف part16 ستون آخر + بخش HEAD). uncommitted تا chat-end atomic.

### P17-candidate-1 — Elicitation-Tool Recommendation Drop (process/governance، severity: medium)
**مشاهده:** هنگام استفاده از ابزار elicitation/ranking برای گرفتن ترتیب Batch‌ها، تعهد #۶۱ (اعلام گزینهٔ مطلوبِ Claude) رها شد — انتخاب کامل به کاربر واگذار شد بدون پیشنهاد صریح. کاربر catch کرد.
**علت ریشه‌ای (دولایه):** (۱) tool-affordance override — هدف ابزار (گرفتن ترجیح کاربر) با #۶۱ (گفتن نظر Claude) تصادم کرد و هدف ابزار برنده شد (خانوادهٔ #۸۴ pattern-following). (۲) شکاف Self-Activation: #۸۵ فقط #۷۸-۸۴ را self-check می‌کند؛ قواعد advisory/format (#۶۱/#۵۹/#۳۱/#۲۹) یادآور مکانیکی ندارند → اتکا به حافظه (خانوادهٔ M23/M87).
**پیشنهاد codify (نسخهٔ بعد):** توسعهٔ #۸۵ self-check با خط «Advisory/Format Self-Check» (#۶۱ پیشنهاد مطلوب · #۵۹ مسیر دانلود · #۳۱/۶۳ tab+رنگ · #۲۹ Artifact)؛ یا درس M-candidate «Tool-Affordance نباید تعهد موازی قاعده را override کند».
**Mitigation in-session (فعال از part17):** Claude از این turn به بعد هدر self-check را به Advisory/Format گسترش داد.
**Cross-refs:** #۶۱ · #۸۴ · #۸۵ · #۲۹ · M87.

### NOTE — شکاف PENDING-section part16
بخش part16 در این فایل غایب است (مستقیم part15 → part17). reconcile در B5 (drift/catch-up) یا chat-end.

### Discovery part17 (chat-end) — check_5 self-catch (مثبت)
در B4، placeholder `Created in commit` در main.md را با هش literal `5285fb6` پر کردم؛ **check_5_head_hardcode** هنگام chat-end commit آن را block کرد. درس: هش/شناسهٔ مکانیکی نباید در ماژول‌های constitution literal شود (M77/M101/#۸۶)؛ placeholder باید non-literal بماند (الگوی مجاز `<git log...>`). هش در فایل‌های tracking (PHASE_LEDGER/SESSION_STATUS) مجاز است، نه در ماژول. **audit-as-safety-net کار کرد** — مصداق مثبت همان تم این چت (#۸۶/M104). Cross-refs: #۸۶ · M77 · M101 · M104 · check_5.

**آخرین به‌روزرسانی part17 section:** 2026-05-30 (chat-end part17 — fix check_5 + discovery).

---

## 🔴🔴🔴 آیتم‌های part18 (چت `TRADING-phase1-part18-phase3-b5-drift-backfill`)

**منبع:** درخواست صریح کاربر (part18، mid-chat) + boot.

### P18-candidate-1 — AI-Optimized Authoring Standard (process/governance، severity: high)

**دستور دائمی کاربر:** هر «artifact نوشتاری» پروژه — پرامپت چت بعد، handoff، متن Instructions/Project Knowledge، Scope Contract، هر دستور به Claude دیگر — باید طبق اصول prompt-engineering بهینهٔ مدل نوشته شود.

**استاندارد (Normative — ۸ بند «خوب نوشته‌شده»):**
1. نقش + هدف صریح در ابتدا (۱-۲ خط).
2. ساختار شماره‌دار/بخش‌بندی‌شده، نه متن یک‌تکه.
3. معیار موفقیت شمارش‌پذیر / Definition-of-Done (اعداد N/M، #۷۹) — نه واژهٔ مبهم.
4. قیدها و گاردهای صریح (چه نکن).
5. فرمت خروجی مشخص.
6. ترتیب گام‌به‌گام برای taskهای چندمرحله‌ای.
7. ارجاع به منبع زنده (git/فایل) نه حافظه (هم‌راستا #۸۶).
8. در صورت کمک‌کنندگی: مثال مثبت + مثال منفی.

**Rationale:** کیفیت + سرعت بالاتر چت بعد، کاهش خطای تفسیر/drift، تکرارپذیری، هم‌راستا با اصل ۳ (radical honesty).

**وضعیت:** 🟢 اعمال فوری از part18 (پیش از codify، مثل #۶۱) + خط Self-Check هر turn.

**codify پیشنهادی:** Rule **#۸۸** (نه #۸۷ — تصادم با Settings/Instructions Sync Reminder) «AI-Optimized Prompt/Artifact Authoring»، یا principle در 04_principles.md. batch اتمیک با Review **#۰۱۱** + Decision **#۷۰** + version (v2.17 اگر هم‌batch با #۸۷، یا v2.18 اگر جدا). سپس انعکاس در PROJECT_KNOWLEDGE + Instructions (#۵۵ + #۸۷).

**Cross-refs:** #۱۶ (کم‌حرفی) · #۳۱/#۶۳ (tab/EXECUTE) · #۵۹ (مسیر دانلود) · #۷۸ (SCM) · #۷۹ (QHP) · #۸۶ (منبع زنده) · اصل ۳ (radical honesty).

**ثبت‌شده توسط:** #۶۰ (با تأیید #۵۱) · نشان داده به کاربر: ✅ (#۶۵).
**وضعیت:** ✅ **CODIFIED v2.17** (part18 chat-end `29b2b56`) — قانون #۸۸ Locked + Review #۰۱۱ + Decision #۷۰.
**آخرین به‌روزرسانی part18 section:** 2026-05-30 (mid part18، P18-candidate).

---

## 🔴🔴🔴 آیتم‌های part18 chat-end (`29b2b56`) — P19-candidate

**منبع:** مشاهدات chat-end خود part18 (درخواست صریح کاربر برای قانون‌کردن مشکلات تکرارشونده).

### P19-candidate-1 — M106: Clean-Commit Pre-Stage + Untracked Audit (process، severity: medium)

**دو مشکل تکرارشونده در chat-end (part18 + چت‌های قبل):**

**(الف) دوبار-commit ناشی از hook whitespace fix (خانوادهٔ M94):** commit اول fail می‌شود چون pre-commit hook (trailing-whitespace/end-of-file-fixer) فایل‌های untracked با CRLF/trailing-space را اصلاح می‌کند → نیاز به `git add -A` + commit دوم. در part18 روی `question-answer.txt` + `HELPER_SANDBOX_*` رخ داد.
**راه‌حل (پیشگیرانه):** پیش از EXECUTE نهایی commit، یک گام پیش‌استیج + اجرای hook اضافه شود تا fixها قبل از commit اصلی اعمال شوند (یک EXECUTE جدا: `git add -A & pre-commit run --all-files`) — سپس commit در یک‌بار می‌گذرد. یا حداقل از ابتدا به کاربر بگو «commit اول ممکن است با hook fix دوبار شود (M94 طبیعی)» تا گیج نشود.

**(ب) `git add -A` فایل ناشناخته را بی‌صدا commit کرد:** `question-answer.txt` (فایلی که Claude ماهیتش را نمی‌دانست) در commit `29b2b56` وارد repo شد.
**راه‌حل (پیشگیرانه):** پیش از `git add -A` در chat-end، فایل‌های untracked ناشناخته (خارج از الگوی شناختهٔ commit_msg_*/handoff/manual_boxes) صریحاً به کاربر گزارش + تأیید گرفته شود (یا .gitignore شوند). هم‌راستا #۵۱ (تأیید قبل از write/commit).

**Genesis:** part18 chat-end (دو بار commit + ورود `question-answer.txt`).
**وضعیت:** 🟢 اعمال فوری رفتاری از part19 (پیش از codify، مثل #۶۱).
**codify پیشنهادی:** درس **M106** (رفتاری، مثل M94/M99/M105 — بدون version bump) در 02_lessons §۲.۸ + coupling check_2 (M105→M106 در lessons + main×2 + SESSION) + اشاره در Template ۱۲ (06_meta). در part19 یا بعد، هم‌batch با سایر candidateها.
**Cross-refs:** M94 (Black re-stage) · M99/M105 (CMD) · #۵۱ (تأیید) · #۶۶ (push).
**نشان داده به کاربر:** ✅ (#۶۵).

### P19-candidate-2 — Post-Handoff Sweep Commit (process، severity: medium)

**دستور دائمی کاربر (part18 chat-end):** پس از commit/push اصلی chat-end، اگر کارهای بعدی (مثل تولید سه کادر #۸۷، آرشیو snapshot، اصلاح مسیر) فایل‌های جدید uncommitted ساختند، باید **یک commit پایانیِ جاروب (sweep)** زده شود تا دیسک = GitHub یکی شود و هیچ کار uncommitted باقی نماند؛ سپس handoff به‌روز شود که «backfill از این هش آخر».

**علت ریشه‌ای:** chat-end معمولاً یک commit اتمیک دارد، ولی کارهای #۸۷ (Full-Text Delivery سه کادر) + #۵۵ (PROJECT_KNOWLEDGE) **بعد** از آن commit رخ می‌دهند → فایل‌های uncommitted باقی می‌مانند (نقض روح #۶۶ backup فوری + ریسک state-drift دیسک≠HEAD).

**راه‌حل (الزامی از part19):** ترتیب صحیح chat-end:
1. commit/push اصلی (codify + دو حلقه).
2. کارهای پساحلقه (#۸۷ سه کادر، #۵۵، آرشیو snapshot، اصلاح مسیر).
3. **commit پایانیِ جاروب** (sweep) برای همهٔ uncommittedهای گام ۲ + push.
4. به‌روزرسانی handoff: «backfill هش = آخرین HEAD (sweep)، از git زنده verify».

**نکته chicken-and-egg:** آخرین sweep خودش هش جدید می‌سازد که handoff نمی‌تواند ثبت کند (M77/M101). راه‌حل: handoff صراحتاً بنویسد «از git زنده بگیر، نه عدد ثابت». پس از sweep دیگر commit نزن (توقف — وگرنه حلقهٔ بی‌پایان).

**Genesis:** part18 chat-end (سه کادر #۸۷ + آرشیو snapshot بعد از commit اصلی → نیاز به sweep).
**وضعیت:** 🟢 اعمال فوری رفتاری از part18 (همین chat-end).
**codify پیشنهادی:** ادغام در درس **M106** (clean-commit family) یا درس مستقل، در part19 هم‌batch با M106. اشاره در پروتکل ۱۲-مرحلهٔ پایان چت (06_meta §۶.۱ مرحلهٔ ۱۲) + Template ۱۲.
**Cross-refs:** M106-candidate · #۶۶ (push) · #۸۷ (Full-Text) · #۵۵ · M101 (chicken-and-egg) · M93 (atomic state).
**نشان داده به کاربر:** ✅ (#۶۵).

### تصمیم معلق کاربر — `question-answer.txt`
این فایل در `29b2b56` commit شد. تصمیم part19: نگه‌داری یا منسوخی با banner (#۲۴) یا .gitignore. معلق تا تصمیم کاربر.

### 🆕 محل canonical فایل زندهٔ PROJECT_KNOWLEDGE (part18 chat-end discovery)
فایل زندهٔ PROJECT_KNOWLEDGE.md که کاربر در Project files بارگذاری می‌کند، محل canonical‌اش = `claude_workspace/snapshots/PROJECT_KNOWLEDGE.md` (نام ثابت). آرشیو نسخه‌های قبلی با الگوی `{تاریخ}-PROJECT_KNOWLEDGE-v{X}.md` در همان پوشه. سند 06_meta §۶.۹ این نقش دوگانهٔ snapshots (هم زنده هم آرشیو) را صریح نگفته بود → باعث اشتباه مکان‌گذاری root در part18 شد (اصلاح شد). codify در part19: افزودن این صراحت به §۶.۹.

### 🎯 META-DELIVERABLE انتهای‌فاز — ممیزی اطمینان‌پذیری قوانین (Reliability Audit)

**درخواست صریح کاربر (part18 chat-end):** وقتی فاز جاری تمام شد و همهٔ قوانین/درس‌ها/تناقض‌ها/پارادکس‌ها/ابهام‌ها برطرف و **تثبیت** شدند، یک جلسهٔ کامل اختصاص داده شود به:

1. **ممیزی همهٔ قوانین (#۱-N) و درس‌ها (M/HM)** و دسته‌بندی صریح هر کدام به:
   - **مکانیکی (enforced by audit):** یک check آن را اجبار می‌کند (مستقل از حافظهٔ Claude) — قابل اعتماد.
   - **رفتاری (وابسته به self-discipline):** فقط به رعایت Claude در هر turn وابسته — ذاتاً نامطمئن.
2. **بحث کامل** دربارهٔ اینکه چه چیزی اضافه/حذف/ادغام شود.
3. **تصمیم دربارهٔ انتقال هر مورد** به بخش مکانیکی (ساخت audit check جدید) یا غیرمکانیکی (یا تبدیل به checklist اجباریِ قابل‌مشاهده تا کاربر verify کند، نه اعتماد به ادعای Claude).

**دغدغهٔ ریشه‌ای کاربر:** «از کجا بدانم Claude در حین کار به کدام قانون/درس عمل می‌کند یا نه؟» — مشکل اصلی: بخش بزرگی از قوانین در دستهٔ رفتاری‌اند و ضمانت اجرای مکانیکی ندارند (مدرک: part17 #۶۱ drop، part18 نام چت ناقص). حتی #۸۵ (Self-Activation Lock) خودش رفتاری است.

**پیش‌نیاز (الزامی):** تثبیت کامل فاز — این ممیزی باید روی یک مجموعهٔ **پایدار و بسته‌شده** انجام شود، نه متحرک (وگرنه قانونی که امروز مکانیزه کنیم فردا حذف/ادغام می‌شود). **صریح: قبل از تثبیت کامل شروع نشود.**

**وضعیت:** 🔮 DEFERRED تا انتهای فاز (پس از رفع همهٔ تناقض/پارادکس/ابهام).
**Cross-refs:** #۸۳ (Honesty Audit visible) · #۸۵ (Self-Activation) · M100 (Hidden→Visible) · M87/M103 (نوشتن قانون ≠ رعایت) · check_1..12 (الگوی enforcement مکانیکی).
**نشان داده به کاربر:** ✅ (#۶۵).

**آخرین به‌روزرسانی part18 chat-end section:** 2026-05-30.
