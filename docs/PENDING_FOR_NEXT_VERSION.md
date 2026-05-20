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

**نسخه:** v0.4 (2026-05-20 — پایان چت ۱۰: افزودن Z2.3-Z2.7 برای ادغام در v2.12)  
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
| **Z2.9** 🆕 | 🔴 **important** | قانون #۶۶ — Backup اجباری در پایان هر چت (ساخته در چت ۱۰) |

**تعداد:** ۹ آیتم  
**اولویت ادغام:** Z2.4 (critical bug)، Z2.1 (already-fixed lesson)، بقیه

---

> 💡 **نکته برای چت ۱۱:** این فایل را خوانده و در پایان چت ۱۱ اگر آیتم جدیدی کشف شد، طبق قانون #۶۰ در همین فایل ثبت شود.
