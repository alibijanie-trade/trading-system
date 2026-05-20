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

**ادغام در:** v2.12 (احتمالاً پایان چت ۱۰ یا چت ۱۱)  
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

در چت ۸، Bug #52 با `$env:PYTHONIOENCODING = "utf-8"` رفع شد، ولی وقتی در چت ۹ دوباره در CMD تلاش شد، خطا داد: "The filename, directory name, or volume label syntax is incorrect." چون CMD این syntax را تفسیر نمی‌کند.

**اقدامات لازم در v2.12:**

1. افزودن M65 به جدول ۱۸.۲ سند جامع (درس‌نامه)
2. به‌روزرسانی Bug #52 در TROUBLESHOOTING.md با هر دو سینتکس (CMD + PowerShell)
3. بررسی افزودن قانون جدید یا اصلاح قانون #۳۱ (Convention tab) تا توانایی تشخیص shell اضافه شود
4. در ONBOARDING_GUIDE.md، توصیه به تنظیم دائمی `PYTHONIOENCODING=utf-8` در سیستم env vars (مستقل از shell)

**ادغام در:** v2.12 (در همان batch با Z2.1)  
**ثبت‌شده توسط:** قانون #۶۰ + قانون #۶۵ (درس با نمایش)  
**نشان داده شده به کاربر:** ✅ (طبق قانون #۶۵)

---

## 📜 آیتم‌های ادغام‌شده در v2.11 (تاریخچه — حذف شد)

تمام آیتم‌های زیر در پایان چت ۹ (فاز A) با ساخت سند جامع v2.11 ادغام شدند و طبق پروتکل ۷.۳ از این فایل پاک شدند:

| کد | عنوان | محل ادغام |
|---|---|---|
| B5.1 | فرمت `.gitignore` با `*` + `!.gitkeep` | فایل `.gitignore` (نه v2.11 — سند درست بود) |
| B2.1 | اصلاح مسیر Memory toggles | سند ۲۳.۱ v2.11 |
| C1.1 | Settings audit کامل (12 ردیف) | سند ۲۳.۴ v2.11 |
| D1.1 | مستندسازی Bug pre-commit + فارسی | Bug #52 در TROUBLESHOOTING v1.1 |
| E2.1 | Bug #50 cleanup (React import) | `vite.config.js` + ۱۷ JSX file (فعلی) |
| G5.1 | قانون #۶۲ (فایل handoff دائمی) | جدول ۱.۹ v2.11 |
| UX1.1 | قانون #۶۳ (Convention 🟢 ▶️ EXECUTE) | جدول ۱.۹ v2.11 |
| UX2.1 | قانون #۶۴ (عدم نمایش جزئیات تصحیح خطا) | جدول ۱.۹ v2.11 |
| UX3.1 | قانون #۶۵ (نمایش درس از اشتباهات) | جدول ۱.۹ v2.11 |
| Z1.1 | M63 (status صریح در handoff) | جدول ۱۸.۲ v2.11 |

**مجموع:** ۱۰ آیتم ادغام شد. برای جزئیات کامل هر یک، رجوع به CHAT_LOG چت ۹ یا سند جامع v2.11 (بخش «خلاصه تغییرات v2.10 → v2.11»).

---

## آیتم‌های موکول (نه برای v2.12 بلکه برای بعدتر)

### D2.1 + D3.1: ارزیابی Claude Code + GitHub MCP

**موکول به:** فاز ۴+ (پس از تثبیت معماری backend و کاربرد روزانه پروژه)  
**علت:** در فاز ۰-۱ Filesystem MCP کفایت می‌کند. Claude Code برای automation پیچیده و GitHub MCP برای PR workflow در فازهای بالاتر مفید است.

---

## 📌 پایان فایل

**نسخه:** v0.3 (2026-05-20 — پایان چت ۹: پاک‌سازی پس از ادغام v2.11 + Z2.1 (M64) + Z2.2 (M65))  
**ساخته توسط:** Claude در چت ۸ (`TRADING-phase0-part08-pre-phase1-setup`)  
**به‌روز توسط:** Claude در پایان چت ۹ طبق پروتکل ۷.۳  
**ادغام بعدی:** سند جامع v2.12 (در چت ۱۰+)

## 📊 خلاصه آیتم های PENDING برای v2.12

| آیتم | سطح | توضیح |
|---|---|---|
| **Z2.1** 🆕 | 🎯 important | M64 — JSX runtime در plugin-react vs esbuild (دو سطح جداگانه) |
| **Z2.2** 🆕 | 🟡 medium | M65 — تشخیص shell از prompt و adaptation دستورات (CMD vs PowerShell vs bash) |

**تعداد:** ۲ آیتم  
**اولویت ادغام:** Z2.1 و Z2.2 در v2.12

---

> 💡 **نکته برای چت ۱۰:** این فایل را خوانده و در پایان چت ۱۰ اگر آیتم جدیدی کشف شد، طبق قانون #۶۰ در همین فایل ثبت شود. آیتم‌های فعلی (Z2.1، Z2.2) فقط پس از تأیید کاربر در زمان ادغام v2.12 پاک خواهند شد.
