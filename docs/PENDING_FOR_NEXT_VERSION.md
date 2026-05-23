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
| Z3.12 | low | Phase 3 | Pre-commit hook label drift (v2.12 to v2.13 in yaml) |
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
