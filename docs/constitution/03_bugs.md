# ماژول ۰۳ — کاتالوگ Bug ها

> بخشی از **Constitution v2.17 (Modular)** — [بازگشت به main](./main.md)
>
> **محتوا:** کاتالوگ Bug های پروژه (#1-#54) با علائم، علت ریشه‌ای، fix، تست regression.
> **منبع v2.11:**
> - Bug #1-#37: در `docs/TROUBLESHOOTING.md` (فایل جانبی، در این ماژول خلاصه + cross-ref)
> - Bug #38-#49: در changelog های v2.5-v2.7 (سند جامع — استخراج شد)
> - Bug #53-#54: در PENDING چت ۱۰
> **Created in commit:** `<git log -1 --format=%h پس از commit 4 پر شود>`
>
> **توجه:** Bug های جدید چت ۱۱.۰.الف انتظار نمی‌رود (این چت infra است، نه code).

---

## ۳.۰ فلسفه Bug Tracking

طبق سند ۱۱.۸ منبع v2.11:

- **Severity:** Critical، High، Medium، Low
- **Priority:** P0 (فوری)، P1، P2، P3
- **Status:** Open، In Progress، Resolved، Won't Fix
- **هر Bug باید Deadline داشته باشد** (در صورت Open بودن)

طبق قانون #۲۴ (No-Deletion): Bug های Resolved هم در این کاتالوگ نگه داشته می‌شوند برای تاریخچه و regression awareness.

---

## ۳.۱ خلاصه fast-look (دسته‌بندی)

### به Severity

| Severity | Bug ها |
|---|---|
| 🔴 **Critical** (crash/data loss) | #۳۸ APP_VERSION، #۳۹ passlib، #۴۰ npm registry، #۵۳ pip BOM |
| 🟠 **High** (functionality broken) | #۳۱ DATABASE_URL، #۳۲ alembic.ini encoding، #۴۱ seed order، #۴۶ ESM URL، #۴۷ Font scaling، #۴۸ Tooltip chart |
| 🟡 **Medium** (UX/style) | #۴۲ pip mirror، #۴۳ Binance colors، #۴۴ interactive states، #۴۵ Toast border، #۴۹ separator |
| 🟢 **Low** (cosmetic) | (در حال حاضر در دسته‌بندی فعلی) |
| ✅ **Resolved (همگی)** | #۵۴ Decisions Gap (cleanup چت ۱۰) |

### به منشأ

| منشأ | Bug ها |
|---|---|
| **Environment** (Windows، CMD، encoding) | #۳۲، #۴۰، #۴۶ ESM، #۵۳ |
| **Dependency mismatch** | #۳۹ passlib، #۴۷ font، #۴۸ tooltip |
| **Code logic** | #۳۸، #۴۱، #۴۲، #۴۳ |
| **Documentation drift** | #۵۴ |

### به فاز کشف

| فاز/Session | Bug ها |
|---|---|
| Session 4 (چت ۳، v2.4) | #۳۱، #۳۲ |
| Session 5 (چت ۴، v2.5) | #۳۸، #۳۹ |
| Session 6.الف (چت ۵.الف، v2.6) | #۴۰-۴۵ |
| Session 6.ب (چت ۵.ب، v2.7) | #۴۶-۴۹ |
| چت ۱۰ (v2.11) | #۵۳-۵۴ |

---

## ۳.۲ جدول کامل Bug ها (#31-#54)

> Bug های #۱-۳۰ که در `docs/TROUBLESHOOTING.md` (سند جانبی) ثبت شده‌اند، اینجا تکرار نمی‌شوند طبق DRY. برای جزئیات آنها به فایل جانبی مراجعه کنید.

| # | Bug | Severity | Status | منشأ | Session |
|---|---|---|---|---|---|
| 31 | DATABASE_URL relative path | 🟠 High | ✅ Resolved | Code logic | چت ۳ |
| 32 | alembic.ini encoding cp1252 | 🟠 High | ✅ Resolved | Environment | چت ۳ |
| 38 | APP_VERSION در .env بر default غلبه می‌کرد | 🔴 Critical | ✅ Resolved | Code logic | چت ۴ |
| 39 | passlib + bcrypt 4.x ValueError در login | 🔴 Critical | ✅ Resolved | Dependency | چت ۴ |
| 40 | npm registry در ایران فیلتر | 🔴 Critical | ✅ Resolved | Environment | چت ۵.الف |
| 41 | ترتیب seed scripts (14→17→19) | 🟠 High | ✅ Resolved | Code logic | چت ۵.الف |
| 42 | pip در ایران (پیشگیرانه) | 🟡 Medium | ✅ Resolved | Environment | چت ۵.الف |
| 43 | تم binance-dark با رنگ‌های TradingView | 🟡 Medium | ✅ Resolved | Code logic | چت ۵.الف |
| 44 | تم بدون interactive states | 🟡 Medium | ✅ Resolved | Code logic | چت ۵.الف |
| 45 | Toast با کادر رنگی نوع‌محور | 🟡 Medium | ✅ Resolved | Code logic | چت ۵.الف |
| 46 | ESM URL scheme در ویندوز | 🟠 High | ✅ Resolved | Environment | چت ۵.ب |
| 47 | Font Size scaling شکسته | 🟠 High | ✅ Resolved | Dependency | چت ۵.ب |
| 48 | tooltip تاریخ نمودار نمایش داده نمی‌شد | 🟠 High | ✅ Resolved | Dependency | چت ۵.ب |
| 49 | عدد ۱۷۱۴ کندل بدون کاما | 🟡 Medium | ✅ Resolved | Code logic | چت ۵.ب |
| 50-52 | (Reserved / Unknown) | — | — | — | — |
| 53 | pip روی Windows + UTF-8 بدون BOM crash | 🔴 Critical | ✅ Resolved | Environment | چت ۱۰ |
| 54 | Decisions Numbering Gap (#۵۷→#۶۵) | 🟢 Low | ✅ Resolved | Documentation drift | چت ۱۰ |

**جمع:** ۱۶ Bug ثبت‌شده (همگی Resolved)، ۳ Reserved (#۵۰-۵۲).

---

## ۳.۳ شرح کامل Bug های Critical

### Bug #38 — APP_VERSION در .env بر default غلبه می‌کرد

**نسخه:** v2.5، چت ۴ (Session 5)
**Severity:** 🔴 Critical
**Status:** ✅ Resolved
**Cross-refs:** قانون #۳۷ (read-back verify)

#### علائم
با وجود به‌روزرسانی `APP_VERSION = "0.2.0"` در `config.py`، uvicorn نسخه `0.1.1` نشان می‌داد.

#### علت ریشه‌ای
`pydantic-settings` مقدار `.env` را اولویت می‌دهد به مقدار default در class. در `.env` هنوز مقدار قدیمی `0.1.1` بود.

#### Fix
اسکریپت `22b_fix_env_app_version.py` خط `.env` را اصلاح کرد.

#### تست Regression
بعد از تغییر `APP_VERSION` در `config.py`، همیشه `.env` هم چک شود.

#### Lessons learned
درس عمومی: pydantic-settings ENV-first است. هرگز فقط `config.py` را تغییر ندهید.

---

### Bug #39 — passlib + bcrypt 4.x → ValueError در login

**نسخه:** v2.5، چت ۴
**Severity:** 🔴 Critical
**Status:** ✅ Resolved
**Cross-refs:** تصمیم #40 (DECISIONS_LOG)

#### علائم
هر تلاش login → `ValueError`.

#### علت ریشه‌ای
`passlib 1.7.4` با `bcrypt 4.x` ناسازگار است. `detect_wrap_bug` یک رشته >۷۲ بایت می‌فرستد که `bcrypt 4.x` reject می‌کند.

#### Fix
**تصمیم #40:** حذف `passlib`، استفاده مستقیم از `bcrypt 4.1.3` در `app/core/security.py`. seed قبلی هم با bcrypt مستقیم نوشته بود — کاملاً سازگار.

#### تست Regression
- `pip uninstall passlib`
- import `bcrypt` در `security.py`
- تست login admin/1 → موفق

#### Lessons learned
- قبل از pin کردن نسخه dependency، compatibility با dependent ها چک شود
- درس مرتبط: M68 (نسخه‌های pinned باید با PyPI verify شوند)

---

### Bug #40 — npm registry در ایران فیلتر

**نسخه:** v2.6، چت ۵.الف
**Severity:** 🔴 Critical
**Status:** ✅ Resolved
**Cross-refs:** قانون #۳۲

#### علائم
`npm install` timeout روی `registry.npmjs.org`.

#### علت ریشه‌ای
`registry.npmjs.org` در ایران فیلتر است. حتی با VPN آلمان گاهی کند.

#### Fix
```bash
npm config set registry https://registry.npmmirror.com/
npm install --save-dev --no-audit --no-fund --prefer-offline <packages>
```
- mirror چینی، تست شده 2026-05-17، عالی
- زمان نصب ۱۴۸ پکیج: ~۱ دقیقه
- اسکریپت `scripts/00b_post_unzip_setup.py` این روش را اتمیشن کرده

#### تست Regression
بعد از تغییر registry، یک package جدید نصب شود و موفق باشد.

#### Lessons learned
- mirror های منطقه‌ای را قبل از install تست کن
- قانون #۳۲ مستقیم از این Bug زاده شد

---

### Bug #53 — pip روی Windows + UTF-8 بدون BOM crash

**نسخه:** v2.11، چت ۱۰
**Severity:** 🔴 Critical
**Status:** ✅ Resolved (با utf-8-sig)
**Cross-refs:** درس M67

#### علائم
`pip install -r requirements.txt` → `UnicodeDecodeError` روی فایل `requirements.txt`.

#### علت ریشه‌ای
pip روی Windows از cp1252 برای خواندن فایل text استفاده می‌کند، نه UTF-8. اگر `requirements.txt` متن غیر-ASCII (مثل کامنت فارسی) داشته باشد و BOM نباشد، crash می‌کند.

#### Fix
ذخیره فایل با encoding **utf-8-sig** (utf-8 with BOM). در اسکریپت ۵۹:
```python
with open("requirements.txt", "w", encoding="utf-8-sig") as f:
    ...
```

#### تست Regression
خواندن `requirements.txt` با `pip install -r` در PowerShell + venv → بدون خطا.

#### Lessons learned
- درس M67: BOM لازم برای pip روی Windows
- Policy A پیشنهاد شد: ASCII-only برای حذف کامل ریسک

---

## ۳.۴ شرح کامل Bug های High

### Bug #31 — DATABASE_URL relative path

**نسخه:** v2.4، چت ۳
**Severity:** 🟠 High
**Status:** ✅ Resolved

#### علائم
backend از مسیر `scripts/` اجرا می‌شد، DB در `scripts/backend/trading.db` جستجو می‌شد به‌جای `backend/trading.db`.

#### علت ریشه‌ای
`DB_PATH` نسبت به CWD resolve می‌شد. اگر CWD تغییر کند، مسیر DB هم تغییر می‌کند.

#### Fix
`DB_PATH` نسبت به `BACKEND_DIR` (constant absolute path) resolve شد، نه CWD.

#### تست Regression
backend از مسیرهای مختلف اجرا شود — DB همیشه در `backend/trading.db` پیدا شود.

---

### Bug #32 — alembic.ini encoding cp1252

**نسخه:** v2.4، چت ۳
**Severity:** 🟠 High
**Status:** ✅ Resolved

#### علائم
`alembic upgrade head` → `UnicodeDecodeError` روی `alembic.ini`.

#### علت ریشه‌ای
`configparser` در ویندوز از cp1252 استفاده می‌کند. اگر `alembic.ini` متن غیر-ASCII داشته باشد، crash می‌کند.

#### Fix
`alembic.ini` فقط ASCII نگه داشته شد.

#### تست Regression
`alembic upgrade head` در PowerShell → بدون خطا.

#### Lessons learned
- Drop file: configparser و pip و subprocess.run همگی روی Windows با cp1252 مشکل دارند
- درس M67 خانواده

---

### Bug #41 — ترتیب seed scripts (14→17→19)

**نسخه:** v2.6، چت ۵.الف
**Severity:** 🟠 High
**Status:** ✅ Resolved
**Cross-refs:** اسکریپت `00b_post_unzip_setup.py`

#### علائم
اجرای اسکریپت ۱۴ → ۱۹ شکست خورد چون نماد BTC/USDT seed نشده بود.

#### علت ریشه‌ای
اسکریپت ۱۹ به نماد BTC/USDT وابسته است، که توسط اسکریپت ۱۷ seed می‌شود. ولی در راهنمای اولیه ترتیب ۱۴→۱۹ مستقیماً پیشنهاد شده بود.

#### Fix
ترتیب اجباری در `00b_post_unzip_setup.py`:
```
14_seed_data.py (admin + Excel)
↓
17_seed_btc_mapping.py (نماد BTC/USDT)
↓
19_test_excel_reader.py (1714 کندل)
```

#### تست Regression
اسکریپت `00b_post_unzip_setup.py` در پروژه تازه pull شده اجرا شود — همه ۳ مرحله موفق.

---

### Bug #46 — ESM URL scheme در ویندوز

**نسخه:** v2.7، چت ۵.ب
**Severity:** 🟠 High
**Status:** ✅ Resolved

#### علائم
`import` در ESM با مسیر absolute Windows (`C:\...`) → خطا.

#### علت ریشه‌ای
Node.js ESM requires URL scheme. `Path.as_posix()` فقط `/` separator می‌گذارد، ولی `file://` prefix نمی‌گذارد.

#### Fix
`Path.as_uri()` به‌جای `Path.as_posix()` — اضافه می‌کند `file:///`.

#### تست Regression
`npm run build` در Vite — بدون خطا.

---

### Bug #47 — Font Size scaling شکسته

**نسخه:** v2.7، چت ۵.ب
**Severity:** 🟠 High
**Status:** ✅ Resolved

#### علائم
کاربر font size سراسری را تغییر داد، فقط برخی component ها تغییر کردند.

#### علت ریشه‌ای
component هایی که `fontSize: N` (px ثابت) inline داشتند، از CSS variables پیروی نمی‌کردند.

#### Fix
همه inline `fontSize: N` → `'X.XXrem'` (نسبی)
+ `html { font-size: var(--font-size-base) }` در `index.css`

#### تست Regression
font size 14px → 18px → همه component ها scale می‌شوند.

---

### Bug #48 — tooltip تاریخ نمودار نمایش داده نمی‌شد

**نسخه:** v2.7، چت ۵.ب
**Severity:** 🟠 High
**Status:** ✅ Resolved

#### علائم
hover روی نمودار → tooltip نشان داده نمی‌شد.

#### علت ریشه‌ای
`localization.dateFormat` (string only) در lightweight-charts deprecated شده، باید از `timeFormatter` (function) استفاده شود.

#### Fix
```javascript
// Before:
chart.applyOptions({ localization: { dateFormat: "yyyy-MM-dd" } });

// After:
chart.applyOptions({ localization: { timeFormatter: (time) => formatDate(time) } });
```

#### تست Regression
hover روی هر کندل → tooltip تاریخ نمایش داده شود.

---

## ۳.۵ Bug های Medium

### Bug #42-#45 (Theme + Toast quality)

این چهار Bug در Session 6.الف کشف شدند و همگی به یک ریشه برمی‌گردند: **عدم درک کامل CSS variables و Theme Engine قبل از پیاده‌سازی**.

| # | علائم | Fix |
|---|---|---|
| **42** | pip در ایران (پیشگیرانه) | mirror پشتیبان `mirror-pypi.runflare.com/simple` |
| **43** | تم binance-dark با رنگ‌های TradingView | بازنویسی با رنگ‌های رسمی بایننس |
| **44** | تم بدون interactive states (hover/focus) | افزودن CSS rules در `index.css` |
| **45** | Toast با کادر رنگی نوع‌محور (نقض هویت تم) | کادر تم + `borderInlineStart 3px solid <نوع>` + icon رنگی |

**Lessons learned:**
- درس عمومی: قبل از پیاده‌سازی هر component با variant، Variant Indicator Pattern را consult کن (سند ۸.۸.۱ منبع، الان در `05_architecture.md`)
- تم complete باید شامل interactive states باشد، نه فقط رنگ‌های پایه

---

### Bug #49 — عدد ۱۷۱۴ کندل بدون کاما

**نسخه:** v2.7
**Severity:** 🟡 Medium

#### علائم
HomePage عدد `1714` را بدون separator نشان می‌داد.

#### Fix
استفاده از `formatNumber` (Intl.NumberFormat) → `1,714`.

---

## ۳.۶ Bug #54 — Decisions Numbering Gap (Documentation Drift)

**نسخه:** v2.11 (cleanup چت ۱۰)
**Severity:** 🟢 Low (no functional impact)
**Status:** ✅ Resolved در cleanup round 1
**Cross-refs:** درس M74، M79

### علائم
`DECISIONS_LOG.md` در #۵۷ متوقف بود. Decisions #۵۸-۶۶ که در چت‌های ۹ و ۱۰ گرفته شده بودند، در فایل ثبت نشده بودند.

### علت ریشه‌ای
چت ۹ Decisions #۵۸-۶۰ را ثبت نکرد، چت ۱۰ Decisions #۶۱-۶۶ را ثبت نکرد. این Bug ریشه‌ای از فقدان "End-of-Chat Verification Checklist" بود (M72).

### Fix
در cleanup round 1 پایان چت ۱۰:
- Decisions #۵۸-۶۶ backfill شد در `DECISIONS_LOG.md`
- v1.1 → v1.3
- Reserved IDs (#۱۶-۱۹، #۴۹) explicit مستند شدند (M79)

### تست Regression
- در پایان هر چت، شمارش `git log | grep "Decision #"` با تعداد Decisions در `DECISIONS_LOG.md` مقایسه شود
- قانون #۷۲ (در commit 8 افزوده می‌شود): End-of-Chat checklist اجباری

### Lessons learned
- درس M74: Full-Range Decision Audit (نه فقط اطراف تغییر)
- درس M79: Reserved IDs Explicit مستند شوند
- این Bug ریشه قانون #۶۶ (Push اجباری) را به‌وجود آورد — بدون push دائم، تناقض‌ها روی local باقی می‌مانند

---

## ۳.۷ Bug های Reserved (#۵۰-۵۲)

طبق سیاست Conservative Numbering (v2.10، M79):

| # | وضعیت | علت |
|---|---|---|
| 50 | ⚠️ Reserved / Unknown | placeholder در changelog |
| 51 | ⚠️ Reserved / Unknown | placeholder در changelog |
| 52 | ⚠️ Reserved / Unknown | placeholder در changelog |

اگر Bug جدیدی در آینده کشف شود که در chronology این Session‌ها قرار می‌گیرد، می‌تواند با این شماره‌ها backfill شود.

---

## 🚧 وضعیت این ماژول

✅ **Migration کامل** — ۱۶ Bug با شرح + ۳ Reserved + ۳۰ Bug قدیمی‌تر cross-ref به `docs/TROUBLESHOOTING.md`.

🔮 **افزوده‌های آینده در commit 8:**
- در حال حاضر هیچ Bug جدید open نداریم
- اگر در حین commits 5-8 یا در chat بعد Bug جدید کشف شد، اضافه می‌شود

---

**📌 پایان 03_bugs.md (commit 4 — migration completed)**
