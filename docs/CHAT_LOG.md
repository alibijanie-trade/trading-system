# 📜 CHAT_LOG — تاریخچه کامل چت‌های پروژه

> **هدف یک‌خطی:** ثبت دقیق و قابل بازخوانی تمام کارهای انجام‌شده در هر چت — برای حفظ حافظه پروژه بین چت‌ها و handoff به برنامه‌نویس بعدی.

> **محل قرارگیری:** `docs/CHAT_LOG.md`  
> **به‌روز توسط:** Claude در پایان هر چت (CLAUDE_CHECKLIST فاز ۳ مرحله ۲ — قانون #۲۳)  
> **نسخه این Log:** v1.3 (2026-05-19 — چت ۸ T2.19: تکمیل چت ۷ stub + افزودن چت ۸ + اصلاح آمار)

---

## 📑 فهرست

- [راهنمای استفاده](#راهنمای-استفاده)
- [Template افزودن چت جدید](#template-افزودن-چت-جدید)
- [خلاصه گرافیکی timeline](#خلاصه-گرافیکی-timeline)
- [چت ۱ — phase0-part01-setup](#چت-۱--phase0-part01-setup)
- [چت ۲ — phase0-part02-backend-core](#چت-۲--phase0-part02-backend-core)
- [چت ۳ — phase0-part03-db-and-data](#چت-۳--phase0-part03-db-and-data)
- [چت ۴ — phase0-part04-auth-and-frontend](#چت-۴--phase0-part04-auth-and-frontend)
- [چت ۵.الف — phase0-part04-theme-engine](#چت-۵الف--phase0-part04-theme-engine)
- [چت ۵.ب — phase0-part05-ui-polish-and-governance](#چت-۵ب--phase0-part05-ui-polish-and-governance)
- [چت ۶ — phase0-part06-quality-hardening](#چت-۶--phase0-part06-quality-hardening)
- [چت ۷ — phase0-part07-quality-hardening-continued](#چت-۷--phase0-part07-quality-hardening-continued)
- [چت ۸ — phase0-part08-pre-phase1-setup](#چت-۸--phase0-part08-pre-phase1-setup) ← این چت

---

## ⚠️ یادداشت یکپارچه‌سازی شمارش (v1.1 — چت ۷)

در چت ۷ (`phase0-part07-quality-hardening-continued`)، شمارش چت‌ها یکپارچه شد:

| شمارش قدیمی | شمارش جدید | علت تغییر |
|---|---|---|
| چت ۵ | **چت ۵.الف** | chat اصلی Session 5 (theme-engine، part04) |
| چت ۶ | **چت ۵.ب** | ادامه Session 5 (ui-polish-and-governance، part05) |
| چت ۷ | **چت ۶** | Session 6 مستقل (quality-hardening، part06) — منطبق با CHAT6_FINALIZE.md |
| (این چت) | **چت ۷** | Session 7 (quality-hardening-continued، part07) |

این یکپارچه‌سازی باعث می‌شود «چت N» در CHAT_LOG با Session N در سایر اسناد (CHAT6_FINALIZE، SESSION_STATUS) همراستا شود.

---

## راهنمای استفاده

### قالب نام چت

طبق سند جامع v2.7 بخش ۱۳.۶:

```
TRADING-phase{N}-part{NN}-{topic-slug}
```

- `{N}`: تک‌رقم 0-based (`phase0`, `phase1`, …)
- `{NN}`: دو رقم (`part01`, `part02`, …)
- `{topic-slug}`: kebab-case بر اساس **موضوعات واقعی** انجام‌شده

### وقتی چت ناتمام رها شد

اگر چتی به نام `xxx-skeleton-confirm` شروع شد ولی موضوعات بیشتری انجام شد، **نام نهایی در پایان چت** متناسب با کل کارها انتخاب می‌شود (مثلاً `xxx-ui-polish-and-governance`).

### مبنای بازسازی چت‌های ۱-۴

اطلاعات چت‌های ۱ تا ۴ از منابع زیر **بازسازی** شده‌اند، چون CHAT_LOG قبل از این چت وجود نداشت:
- شماره اسکریپت‌ها (`01_create_structure.py` تا `28c_fix_toast_theme.py`)
- `CHANGELOG.md` (نسخه‌ها)
- `SESSION_STATUS.md` (آخرین بخش)
- Bug history در سند جامع v2.6
- Decisions در سند جامع v2.6
- معماری فایل‌ها و کامنت‌های اسکریپت

> ⚠️ **توجه برای حرفه‌ای‌گری:** تاریخ‌های دقیق چت‌های ۱-۴ تخمینی هستند (تنها از روی `created_at` فایل‌ها). از چت ۵ به بعد دقیق‌اند.

---

## Template افزودن چت جدید

هر چت جدید با این Template به این سند اضافه می‌شود:

```markdown
## چت {N} — {نام کامل چت}

**تاریخ:** YYYY-MM-DD  
**مدت:** تقریباً X ساعت  
**Claude version:** Claude X.Y  
**فاز پروژه در زمان شروع:** فاز N — Y%  
**فاز پروژه در زمان پایان:** فاز N — Y%

### 📌 موضوع کلی
[۲-۳ خط — هدف اصلی این چت]

### 📦 ورودی‌های چت
- سند جامع vX.Y (پیوست)
- trading-system.zip (پیوست)
- [اگر چیز خاصی]

### 🎯 گام‌های انجام‌شده
1. ...
2. ...

### 🛠️ اسکریپت‌های تولیدشده
| # | نام | شرح | تست همراه |
|---|---|---|---|
| N | xxx.py | ... | Nb_test_xxx.py |

### 📁 فایل‌های جدید/به‌روز
**جدید:**
- `path/to/file.ext` — [شرح]

**به‌روز:**
- `path/to/file.ext` — [شرح تغییر]

### 🐛 Bug ها رفع‌شده
- **#N:** [عنوان] — [۱ خط شرح]

### 🎨 Feature ها افزوده‌شده
- [feature 1]
- [feature 2]

### 🏛️ تصمیمات معماری
- **Decision #N:** [عنوان] — [۱ خط]

### 📜 قوانین جدید
- **#N:** [عنوان] — [۱ خط]

### ⚠️ نکات مهم برای آینده
- [نکته 1]
- [نکته 2]

### 📊 آمار
- تعداد چک‌های استاتیک: N
- تعداد چک‌های runtime: N
- npm build زمان: Xms

### 🔗 ارتباطات
- ادامه چت قبل: [نام چت قبل]
- پیشنهاد چت بعد: [نام پیشنهادی]
- TASK های DONE شده: T1.0X, T1.0Y, ...
- TASK های جدید کشف‌شده: T2.0Z, ...
```

---

## خلاصه گرافیکی timeline

```
چت ۱ ─ 2026-05-13 ─ راه‌اندازی پایه ─ [Setup + Docs + Decisions]
   │
چت ۲ ─ 2026-05-14 ─ Backend Core ─ [FastAPI + Logger + Exceptions]
   │
چت ۳ ─ 2026-05-15 ─ Database + Data ─ [Models + Repos + Alembic + DataSource]
   │
چت ۴ ─ 2026-05-16 ─ Auth + Frontend ─ [JWT + Login + ChartPage]
   │
چت ۵.الف ─ 2026-05-17 ─ Theme Engine ─ [۵ تم + Toast + 00b]
   │
چت ۵.ب ─ 2026-05-17 ─ UI Polish + Governance ─ [۸.۳/۸.۴/۸.۵ + اسناد]
   │
چت ۶ ─ 2026-05-17 ─ Quality Hardening ─ [Tier 2 — ۴/۹: ErrorBoundary + vitest + ARCHITECTURE + git]
   │
   ▼
چت ۷ ─ 2026-05-18 ─ Quality Hardening Continued ─ [Tier 2 — ۹/۹ ✅ + قوانین #۳۳-۴۷ + MCP setup]
   │
   ▼
چت ۸ ─ 2026-05-19 ─ Pre-Phase 1 Setup ─ [v2.10 + PENDING + #۴۸-۶۱ + Settings audit] ← این چت
```

---

## چت ۱ — phase0-part01-setup

**نام چت (با اصلاحیه v2.7):** `TRADING-phase0-part01-setup`  
**تاریخ تقریبی:** 2026-05-13  
**فاز شروع:** ─  
**فاز پایان:** فاز ۰ — ~۱۵٪

### 📌 موضوع کلی
راه‌اندازی اولیه پروژه. ایجاد ساختار پوشه، اسناد بنیادی، تصمیمات معماری کلیدی، DataSource Abstraction.

### 🎯 گام‌های انجام‌شده
1. ایجاد ساختار پایه پوشه‌ها (backend, frontend, scripts, docs)
2. تنظیم `.gitignore` حرفه‌ای برای Python + Node
3. ایجاد اسناد پایه (README، CHANGELOG، SESSION_STATUS، PROJECT_CONTEXT)
4. طراحی DataSource Abstraction در `backend/app/infrastructure/`
5. ثبت تصمیمات معماری اولیه (#۱ تا #۴)

### 🛠️ اسکریپت‌های تولیدشده
| # | نام | شرح |
|---|---|---|
| 01 | `01_create_structure.py` | ساخت ساختار پوشه و فایل‌های خالی |
| 02 | `02_initial_docs.py` | اسناد پایه اولیه |

> توجه: قانون #۲۲ (تست همراه) هنوز در این چت وجود نداشت.

### 📁 فایل‌های جدید
- `README.md` (اولیه)
- `CHANGELOG.md`
- `.gitignore`
- `docs/PROJECT_CONTEXT.md`
- `docs/SESSION_STATUS.md`
- ساختار پوشه‌های `backend/`, `frontend/`, `scripts/`

### 🏛️ تصمیمات معماری
- **Decision #1:** Stack نهایی — FastAPI + SQLAlchemy + React + Vite + zustand
- **Decision #2:** Repository Pattern برای DB access
- **Decision #3:** DataSource Abstraction لایه infrastructure
- **Decision #4:** Layered Architecture (routes → services → repositories → models)

### 📜 قوانین جدید
- قوانین #۱ تا #۱۴ ابتدایی (basics: ساختار، DRY، typing، …)

### 🔗 ارتباطات
- ادامه چت قبل: ─ (اولین چت)
- پیشنهاد چت بعد: backend pipeline core

---

## چت ۲ — phase0-part02-backend-core

**نام چت (با اصلاحیه v2.7):** `TRADING-phase0-part02-backend-core`  
**تاریخ تقریبی:** 2026-05-14  
**فاز شروع:** فاز ۰ — ~۱۵٪  
**فاز پایان:** فاز ۰ — ~۳۵٪

### 📌 موضوع کلی
ساخت Backend Core: FastAPI scaffold + venv + dependencies + Core Layer (Logger، Exceptions، Handlers، Response).

### 🎯 گام‌های انجام‌شده
1. ساخت venv و نصب FastAPI + uvicorn + pydantic + sqlalchemy
2. ساخت `backend/main.py` و route پایه `/health`
3. تنظیمات از `.env` با Pydantic Settings
4. Logger با Loguru (با fix رنگ ANSI و emoji برای Windows CMD)
5. Custom Exceptions hierarchy
6. Exception Handlers (سراسری)
7. Standard Response model
8. ۱۳ تصمیم معماری ثبت شد

### 🛠️ اسکریپت‌های تولیدشده
- `03_*.py` تا `~10_*.py` (تخمینی) — backend setup

### 📁 فایل‌های جدید
- `backend/venv/` (نصب)
- `backend/requirements.txt`
- `backend/.env` و `.env.example`
- `backend/app/main.py`
- `backend/app/config/settings.py`
- `backend/app/core/logger.py`
- `backend/app/core/exceptions.py`
- `backend/app/core/handlers.py`
- `backend/app/core/response.py`

### 🐛 Bug ها رفع‌شده
- **Bug #1-#10 (تقریبی):** عمدتاً encoding/path issues در Windows
- مهم‌ترین: رنگ ANSI و emoji در Windows CMD

### 🏛️ تصمیمات معماری
- ادامه Decisions تا #۱۳
- استفاده از Loguru به جای logging stdlib
- Pydantic v2 Settings برای config
- Exception hierarchy: BaseException → DomainException → SpecificException

### 🔗 ارتباطات
- پیشنهاد چت بعد: database + models

---

## چت ۳ — phase0-part03-db-and-data

**نام چت (با اصلاحیه v2.7):** `TRADING-phase0-part03-db-and-data`  
**تاریخ تقریبی:** 2026-05-15  
**فاز شروع:** فاز ۰ — ~۳۵٪  
**فاز پایان:** فاز ۰ — ~۶۰٪

### 📌 موضوع کلی
لایه داده: Database، Models، Repositories، Alembic migrations، Seeding، DataSource، Excel Reader.

### 🎯 گام‌های انجام‌شده
1. تنظیمات SQLAlchemy async + SQLite
2. Models: User، Exchange، Symbol، Timeframe، Market، OhlcvData
3. Repositories: یک repo per model + base CRUD
4. Alembic setup + اولین migration
5. Seeding: کاربر admin/1 + exchange Excel
6. DataSource implementation: ExcelDataSource
7. Excel Reader برای فایل‌های .xlsx

### 🛠️ اسکریپت‌های تولیدشده
- `~11_*.py` تا `~20_*.py` (تخمینی)

### 📁 فایل‌های جدید
- `backend/app/database/connection.py`
- `backend/app/database/base.py`
- `backend/app/models/*.py` (۶ مدل)
- `backend/app/repositories/*.py`
- `backend/alembic/`
- `backend/app/infrastructure/data_sources/excel_data_source.py`
- `backend/trading.db` (۴۲۱KB)

### 🏛️ تصمیمات معماری
- async SQLAlchemy
- SQLite برای phase 0 (با احتمال PostgreSQL در فاز ۲+)
- Alembic برای migrations
- bcrypt برای password hashing

### ⚠️ نکات مهم برای آینده
- `trading.db` در .gitignore است
- بازسازی DB با `scripts/00b_post_unzip_setup.py`

### 🔗 ارتباطات
- پیشنهاد چت بعد: Auth + اولین API + Frontend scaffold

---

## چت ۴ — phase0-part04-auth-and-frontend

**نام چت (با اصلاحیه v2.7):** `TRADING-phase0-part04-auth-and-frontend`  
**تاریخ تقریبی:** 2026-05-16  
**فاز شروع:** فاز ۰ — ~۶۰٪  
**فاز پایان:** فاز ۰ — ~۸۵٪

### 📌 موضوع کلی
Authentication کامل با JWT + OAuth2، اولین API endpoint برای OHLCV، Frontend scaffold با Vite، Login واقعی، ChartPage با lightweight-charts.

### 🎯 گام‌های انجام‌شده
1. JWT setup با python-jose
2. OAuth2 password flow
3. bcrypt مستقیم (نه passlib، به دلیل مشکل Windows)
4. Auth dependencies: `current_user`, `current_admin`
5. اولین endpoint محافظت‌شده: `GET /ohlcv/{symbol_id}`
6. Frontend scaffold: Vite + React + react-router-dom + axios + zustand + lightweight-charts
7. LoginPage با فرم
8. ProtectedRoute component
9. authStore + apiClient با interceptor
10. HomePage ساده
11. ChartPage با OHLCV واقعی + lightweight-charts

### 🛠️ اسکریپت‌های تولیدشده
- `~21_*.py` تا `~26_*.py` (تخمینی)
- شامل `24_frontend_scaffold.py`، `25_frontend_login.py`، `26_chart_page.py`

### 📁 فایل‌های جدید
- `backend/app/auth/*.py` (JWT, dependencies, schemas)
- `backend/app/api/v1/routes/auth.py`
- `backend/app/api/v1/routes/ohlcv.py`
- `frontend/` — کامل Vite project
- `frontend/src/services/api.js`
- `frontend/src/stores/authStore.js`
- `frontend/src/components/common/ProtectedRoute.jsx`
- `frontend/src/pages/LoginPage.jsx`
- `frontend/src/pages/HomePage.jsx`
- `frontend/src/pages/ChartPage.jsx`

### 🐛 Bug ها رفع‌شده
- **Bug #15-#25 (تقریبی):**
  - passlib در Windows مشکل داشت → bcrypt مستقیم
  - CORS برای localhost:5173
  - timestamp تبدیل به Unix در lightweight-charts
- **Bug #42 (احتمالاً):** قبل از Theme Engine، رنگ‌های نمودار hardcoded بودند

### 🏛️ تصمیمات معماری
- bcrypt مستقیم (Decision)
- JWT با expire 7 روز
- localStorage برای token (نه cookie — برای فاز ۰ ساده‌تر)
- lightweight-charts برای نمودار (نه ApexCharts/Plotly)

### 🔗 ارتباطات
- پیشنهاد چت بعد: Theme Engine

---

## چت ۵.الف — phase0-part04-theme-engine

> ⚠️ **توجه:** نام چت ۴ و ۵ هر دو `part04` بودند به دلیل اصلاحیه نام چت در سند v2.7. در v2.7+ نام صحیح این چت `part05` خواهد بود — ولی در زمان شروعش `part04` نوشته شد.

**نام چت (در زمان شروع):** `TRADING-phase01-part01-theme-engine` → اصلاح‌شده در پایان به `TRADING-phase0-part04-theme-engine`  
**نام صحیح طبق pattern نهایی:** `TRADING-phase0-part04-theme-engine`  
**تاریخ:** 2026-05-17 (صبح)  
**فاز شروع:** فاز ۰ — ~۸۵٪  
**فاز پایان:** فاز ۰ — ~۹۷٪

### 📌 موضوع کلی
زیرگام ۸.۱ Theme Engine + زیرگام ۸.۲ Toast Notifications + ساخت اسکریپت `00b_post_unzip_setup.py` + ثبت قوانین #۲۱ و #۲۲.

### 🎯 گام‌های انجام‌شده
1. ساخت Theme Engine با ۵ تم: `binance-dark`, `light-minimal`, `dark-modern`, `pastel`, `sky-blue`
2. ThemeProvider که CSS variables را به `:root` تزریق می‌کند
3. themeStore با Zustand persist (تم + fontSize + customColors + resetAll)
4. Bug #43: Binance Color Accuracy — رنگ‌های دقیق بایننس
5. Bug #44: Interactive States — hover/active/focus-visible/disabled
6. Toast Notifications: ToastContainer + Toast + toastStore
7. Bug #45: Toast Theme Consistency — Variant Indicator Pattern (سند ۸.۸.۱)
8. اسکریپت `00b_post_unzip_setup.py` — راه‌اندازی خودکار با fallback به mirrors ایران
9. قانون #۲۱: هر چیز قابل تست با کد، با کد تست شود
10. قانون #۲۲: هر `{N}_*.py` باید `{N}b_test_*.py` همراه داشته باشد

### 🛠️ اسکریپت‌های تولیدشده
- `27_theme_engine.py` + `27b_test_theme_engine.py`
- `27c_fix_binance_colors.py` (Bug #43)
- `27e_fix_interactive_states.py` (Bug #44)
- `28_toast_notifications.py` + `28b_test_toast_notifications.py`
- `28c_fix_toast_theme.py` (Bug #45)
- `00b_post_unzip_setup.py`

### 📁 فایل‌های جدید
- `frontend/src/themes/themes.js` — ۵ تم
- `frontend/src/stores/themeStore.js`
- `frontend/src/components/common/ThemeProvider.jsx`
- `frontend/src/components/common/Toast.jsx`
- `frontend/src/components/common/ToastContainer.jsx`
- `frontend/src/stores/toastStore.js`
- `scripts/00b_post_unzip_setup.py`

### 🐛 Bug ها رفع‌شده
- **Bug #43:** Binance Color Accuracy
- **Bug #44:** Interactive States missing
- **Bug #45:** Toast Theme Inconsistency (kicked off Variant Indicator Pattern در سند ۸.۸.۱)

### 🎨 Feature ها افزوده‌شده
- ۵ تم کامل با switcher
- Toast notifications (success/error/info/warning)
- Variant Indicator Pattern — مفهوم بنیادی برای تمام variant ها

### 📜 قوانین جدید
- **#۲۱:** هر چیز قابل تست با کد، با کد تست شود (نه Swagger UI)
- **#۲۲:** هر اسکریپت `{N}_*.py` باید `{N}b_test_*.py` همراه داشته باشد

### ⚠️ نکات مهم برای آینده
- Variant Indicator Pattern (۸.۸.۱) همیشه باید رعایت شود
- اسکریپت 00b بازسازی‌کننده ۳ چیز است: venv, trading.db, node_modules

### 🔗 ارتباطات
- پیشنهاد چت بعد: skeleton + confirm

---

## چت ۵.ب — phase0-part05-ui-polish-and-governance

**نام چت (در زمان شروع):** `TRADING-phase0-part05-skeleton-confirm`  
**نام نهایی (بر اساس موضوعات):** `TRADING-phase0-part05-ui-polish-and-governance`  
**تاریخ:** 2026-05-17  
**Claude version:** Claude Opus 4.7  
**فاز شروع:** فاز ۰ — ~۹۷٪  
**فاز پایان:** فاز ۰ — **۱۰۰٪** + اضافه: زیرساخت Governance

### 📌 موضوع کلی
این چت قرار بود فقط زیرگام ۸.۳ (Skeleton + ConfirmDialog) را انجام دهد، ولی به دلیل سبک بودن context و درخواست کاربر، گسترش یافت به:
1. تکمیل کامل ۸.۳، ۸.۴، ۸.۵ (پایان فاز ۰)
2. رفع ۴ Bug (Font scaling، tooltip تاریخ، عدد ۱۷۱۴ بدون کاما، ESM URL در ویندوز)
3. افزودن feature انتخاب فرمت تاریخ میلادی
4. **ساخت زیرساخت Governance کامل** — ۱۲ سند جدید/به‌روز برای handoff و کیفیت بلندمدت

### 📦 ورودی‌های چت
- سند جامع v2.6 (پیوست)
- trading-system.zip (شامل کار چت ۵)
- اصلاحیه ابتدای چت: نام `phase{NN}` → `phase{N}` تک‌رقم

### 🎯 گام‌های انجام‌شده

#### بخش الف — ۳ زیرگام UI (۸.۳، ۸.۴، ۸.۵)

**زیرگام ۸.۳ — Skeleton + ConfirmDialog:**
1. SkeletonBlock با ۴ variant + shimmer animation
2. confirmStore (Zustand) Promise-based با `await askConfirm({...})`
3. ConfirmDialog با Variant Indicator Pattern + focus trap + Escape + backdrop click
4. ادغام: Skeleton در ChartPage loading + ConfirmDialog در HomePage logout

**زیرگام ۸.۴ — Settings Page:**
1. SettingsPage در `/settings` با ۳ بخش
2. ThemeCard کامپوننت با preview ۵ رنگ از theme.vars
3. FontSizeControl با ۴ preset (12/14/16/18px)
4. حذف dropdown موقت از HomePage، افزودن لینک ⚙️
5. دکمه «بازگشت به پیش‌فرض» با ConfirmDialog + Toast

**زیرگام ۸.۵ — Numeric + Persian Calendar:**
1. `formatNumber()` با `Intl.NumberFormat`
2. `formatDate()` با `Intl.DateTimeFormat("fa-IR-u-ca-persian", ...)` — بدون کتابخانه خارجی
3. preferencesStore جدا برای calendar (بعد گسترش به gregorianFormat)
4. CalendarToggle با radiogroup
5. ChartPage: متن "1,714 کندل" + tooltip تاریخ شمسی (بعد timeFormatter)
6. SettingsPage: بخش "زبان و تقویم"

#### بخش ب — رفع ۴ Bug

7. **Bug #46:** `Path.as_posix()` → `Path.as_uri()` در اسکریپت تست (ویندوز ESM URL)
8. **Bug #47:** Font Size scaling — `html { font-size: var(--font-size-base) }` + همه inline `fontSize: N` → `'X.XXrem'` در ۹ فایل
9. **Bug #48:** lightweight-charts `localization.dateFormat` (function نمی‌پذیرد) → `timeFormatter`
10. **Bug #49:** HomePage `1714 کندل` hardcoded → `{formatNumber(1714)}`

#### بخش ج — Feature

11. انتخاب فرمت تاریخ میلادی: ISO، آمریکایی (`MM/DD/YYYY`)، اروپایی (`DD/MM/YYYY`)، کامل (`January 15, 2024`)
12. ذخیره در `preferencesStore.gregorianFormat`
13. UI: `<select>` در CalendarToggle (نمایش فقط هنگام انتخاب میلادی)

#### بخش د — Governance (سرمایه‌گذاری بلندمدت)

14. PROJECT_GOVERNANCE.md — سند راهبردی فرایند
15. CLAUDE_CHECKLIST.md — چک‌لیست explicit ۳ فاز
16. TASK_BACKLOG.md — ۶۳ task با ۴ Tier
17. CHAT_LOG.md — این سند (بازسازی ۶ چت)
18. GLOSSARY.md — واژه‌نامه
19. TROUBLESHOOTING.md — FAQ + Bug solutions
20. DECISIONS_LOG.md — ADR
21. REUSABLE_SKELETON.md — راهنمای استفاده مجدد
22. ONBOARDING_GUIDE.md — روز اول برنامه‌نویس
23. STYLE_GUIDE.md — code style + patterns
24. README.md — بازنویسی صفحه اول
25. CHANGELOG.md — به‌روز از v0.1.1
26. سند جامع v2.7 — بخش‌های جدید ۱۶، ۱۷ + قوانین #۲۳-۲۶ + Bug #46-49 + اصلاحیه ۱۳.۶
27. SESSION_STATUS.md به‌روز
28. PROJECT_CONTEXT.md به‌روز

### 🛠️ اسکریپت‌های تولیدشده

| # | نام | شرح | تست همراه |
|---|---|---|---|
| 29 | `29_skeleton_confirm.py` | SkeletonBlock + ConfirmDialog + confirmStore | `29b_test_skeleton_confirm.py` |
| 30 | `30_settings_page.py` | SettingsPage + ThemeCard + FontSizeControl | `30b_test_settings_page.py` |
| 31 | `31_numeric_calendar.py` | formatNumber + formatDate + CalendarToggle + preferencesStore | `31b_test_numeric_calendar.py` |
| 32 | `32_phase0_polish.py` | رفع ۳ Bug + افزودن فرمت میلادی | `32b_test_fixes.py` |

### 📁 فایل‌های جدید/به‌روز

**Frontend جدید:**
- `frontend/src/components/common/SkeletonBlock.jsx`
- `frontend/src/components/common/ConfirmDialog.jsx`
- `frontend/src/stores/confirmStore.js`
- `frontend/src/pages/SettingsPage.jsx`
- `frontend/src/components/settings/ThemeCard.jsx`
- `frontend/src/components/settings/FontSizeControl.jsx`
- `frontend/src/components/settings/CalendarToggle.jsx`
- `frontend/src/utils/numberFormat.js`
- `frontend/src/utils/dateFormat.js`
- `frontend/src/stores/preferencesStore.js`

**Frontend به‌روز:**
- `frontend/src/App.jsx` (mount ConfirmDialog + route /settings)
- `frontend/src/index.css` (keyframes + html font-size + بقیه animations)
- `frontend/src/pages/HomePage.jsx` (askConfirm + Link به /settings + formatNumber + rem)
- `frontend/src/pages/ChartPage.jsx` (Skeleton + timeFormatter + formatNumber + rem)
- `frontend/src/pages/LoginPage.jsx` (rem)
- `frontend/src/components/common/Toast.jsx` (rem)

**Docs جدید (Governance):**
- `docs/PROJECT_GOVERNANCE.md`
- `docs/CLAUDE_CHECKLIST.md`
- `docs/TASK_BACKLOG.md`
- `docs/CHAT_LOG.md`
- `docs/GLOSSARY.md`
- `docs/TROUBLESHOOTING.md`
- `docs/DECISIONS_LOG.md`
- `docs/REUSABLE_SKELETON.md`
- `docs/ONBOARDING_GUIDE.md`
- `docs/STYLE_GUIDE.md`

**Docs به‌روز:**
- `README.md` (بازنویسی)
- `CHANGELOG.md` (همه نسخه‌ها)
- `docs/PROJECT_CONTEXT.md`
- `docs/SESSION_STATUS.md`
- سند جامع v2.7

### 🐛 Bug ها رفع‌شده
- **#46:** ESM URL scheme ویندوز (Path.as_uri)
- **#47:** Font Size scaling (px → rem + html font-size)
- **#48:** tooltip تاریخ نمودار (timeFormatter)
- **#49:** عدد بدون کاما در HomePage (formatNumber)

### 🎨 Feature ها افزوده‌شده
- SkeletonBlock عمومی با ۴ variant
- ConfirmDialog سراسری با variant indicator
- Settings Page با ۳ بخش (theme/font/calendar)
- formatNumber + formatDate utilities
- تقویم شمسی + ۴ فرمت میلادی
- زیرساخت Governance (۱۰ سند جدید)

### 🏛️ تصمیمات معماری
- **Decision #50:** preferencesStore جدا از themeStore (calendar به theme ربط ندارد)
- **Decision #51:** Variant Indicator Pattern برای ConfirmDialog (تأیید مجدد ۸.۸.۱)
- **Decision #52:** `Intl` built-in به جای کتابخانه (moment-jalaali، dayjs، etc)
- **Decision #53:** rem به جای px برای تمام fontSize های inline
- **Decision #54:** زیرساخت Governance ۱۲-سندی (تغییر فلسفه از "Claude به یاد می‌آورد" به "اسناد بیرونی هستند")

### 📜 قوانین جدید
- **#۲۳:** هر چت، CHAT_LOG با بخش جدید آپدیت شود
- **#۲۴:** سند جامع فقط افزوده/اصلاح می‌شود، **هرگز حذف نمی‌شود** (No-Deletion principle)
- **#۲۵:** Claude در شروع چت چک‌لیست ۸ مرحله را انجام دهد
- **#۲۶:** هر تغییر در یک سند، اگر روی سایر اسناد تأثیر دارد، به‌صورت **اتمیک** اعمال شود

### ⚠️ نکات مهم برای آینده
- اصلاحیه نام چت بحرانی است: `phase{N}` تک‌رقم (نه `phase{NN}`)
- `Intl.DateTimeFormat("fa-IR-u-ca-persian", ...)` در همه مرورگرهای modern کار می‌کند — بدون نیاز به polyfill
- در lightweight-charts v4.x: برای time formatting، `timeFormatter` استفاده شود نه `dateFormat`
- در ویندوز، برای ESM imports، از `Path.as_uri()` استفاده شود نه `Path.as_posix()`
- اگر فقط `fontSize: 14` در inline داشتید و html را تغییر دادید، scaling کار نمی‌کند — همه باید rem باشند

### 📊 آمار
- اسکریپت‌های جدید: ۴ (29, 30, 31, 32)
- اسکریپت‌های تست همراه: ۴
- چک‌های استاتیک کل: ~۳۰۰ (76+72+80+76)
- چک‌های runtime: ۲۲ (15+15 از 31b, 32b)
- npm build زمان: ~۵۴۰-۹۷۶ms
- Bundle size: ~۴۴۰KB (143KB gzip)

### 🔗 ارتباطات
- ادامه چت قبل: `TRADING-phase0-part04-theme-engine`
- **نام چت بعد پیشنهادی:** `TRADING-phase0-part06-quality-hardening` (شروع Tier 2)
- یا اگر کاربر می‌خواهد فاز ۱ را شروع کند: `TRADING-phase1-part01-ccxt-websocket-setup`

### TASK های DONE شده در این چت
- T1.01 — PROJECT_GOVERNANCE.md
- T1.02 — CLAUDE_CHECKLIST.md
- T1.03 — TASK_BACKLOG.md
- T1.04 — CHAT_LOG.md (همین سند)
- T1.05 تا T1.16 — در پیام‌های بعدی این چت
- زیرگام‌های ۸.۳، ۸.۴، ۸.۵ (از Backlog قبلی)

### TASK های جدید کشف‌شده
- بازنویسی README که قبلاً TASK نبود
- اضافه شدن CHANGELOG (از v0.1.1 معطل بود)
- شناسایی Tier 2 task ها برای چت بعد

---

## چت ۶ — phase0-part06-quality-hardening

**نام چت (در زمان شروع):** `TRADING-phase0-part06-quality-hardening`  
**نام نهایی:** `TRADING-phase0-part06-quality-hardening` (بدون تغییر)  
**تاریخ:** 2026-05-17  
**Claude version:** Claude Opus 4.7  
**فاز شروع:** فاز ۰ کامل (۱۰۰٪) — شروع Tier 2  
**فاز پایان:** Tier 2 — **۴/۹ تکمیل (~۴۴٪)**

### 📌 موضوع کلی

اولین چت اختصاصی برای Tier 2 (Quality Hardening). هدف: ارتقای کیفیت حرفه‌ای codebase بعد از تکمیل فاز ۰.

طبق پیشنهاد کاربر («از گزینه‌ای که فکر می‌کنی درست‌تر و بهتره شروع کن»)، چهار task به ترتیب پیچیدگی صعودی انجام شدند:
1. **T2.03 — `.env.example` audit** (XS — warm-up)
2. **T2.01 — Error Boundaries** (M — مقاومت UI)
3. **T2.02 — vitest setup + ۵ smoke test** (L — پایه تست frontend)
4. **T2.04 — ARCHITECTURE.md با ۶ دیاگرام Mermaid** (M — مستندسازی معماری)

### 📦 ورودی‌های چت

- `trading-system05.zip` (state پایان چت ۶)
- سند جامع v2.7 (پیوست جداگانه برای دسترسی سریع)
- پیام کاربر: «از گزینه ای که فکر میکنی درستر و بهتره شروع کن»

### 🎯 گام‌های انجام‌شده

#### بخش الف — T2.03: env.example audit (XS)

**اسکریپت:** `34_env_examples_audit.py` + `34b_test_env_examples.py`

1. **`backend/.env.example` به‌روز شد:**
   - `APP_VERSION` از `0.1.1` (stale) به `0.4.0`
   - افزودن `API_PREFIX=/api/v1` (در `config.py` بود ولی در `.env.example` نبود)
   - افزودن دستورالعمل تولید `SECRET_KEY` (با `secrets.token_urlsafe`) و `ENCRYPTION_KEY` (با `Fernet.generate_key`) در کامنت‌ها
   - افزودن کامنت برای هر کلید
2. **`frontend/.env.example` از صفر ساخته شد:**
   - `VITE_API_URL=http://localhost:8000/api/v1`
   - هشدار امنیتی Vite (prefix `VITE_` به مرورگر expose می‌شود — برای SECRETها استفاده نشود)
3. **تست:** ۲۰/۲۰ pass — شامل drift detection (AST parse `config.py` و مقایسه با کلیدهای `.env.example`)

**فایل `backend/.env` کاربر دست‌نخورده باقی ماند** — فقط فایل قابل-commit `.env.example` به‌روز شد.

#### بخش ب — T2.01: Error Boundaries (M)

**اسکریپت:** `35_error_boundaries.py` + `35b_test_error_boundaries.py`

1. **`frontend/src/components/common/ErrorBoundary.jsx` ساخته شد:**
   - کلاس‌-کامپوننت (تنها روش React برای catch render-time errors)
   - `static getDerivedStateFromError` + `componentDidCatch`
   - **Variant Indicator Pattern** (سند ۸.۸.۱): accent ۴px رنگ danger + icon ⚠
   - بدون hex hardcoded — همه از CSS variables
   - **dev gating:** stack trace فقط در `import.meta.env.DEV` در `<details>` collapsible
   - دکمه‌ها: «تلاش مجدد» (reset state) + «بارگذاری مجدد» (`window.location.reload()`)
   - **dev-only:** «کپی جزئیات» (با `navigator.clipboard`)
   - Accessibility: `role="alert"` + `aria-live="assertive"`
   - Props اختیاری: `fallback: (info) => ReactNode` و `onReset: () => void` و `label: string`
   - متن RTL فارسی: «خطایی رخ داد»، «تلاش مجدد»، «بارگذاری مجدد»

2. **`frontend/src/App.jsx` با defense-in-depth به‌روز شد:**
   - **مرز سراسری:** `<ErrorBoundary label="root">` کل `Routes` را در بر می‌گیرد
   - **مرز per-route:** هر ۴ صفحه (`route:login`, `route:home`, `route:chart`, `route:settings`) ErrorBoundary اختصاصی دارند
   - دلیل: کاربر در صورت crash در یک صفحه، می‌تواند با navigate به مسیر دیگر فرار کند

3. **تست:** ۳۱/۳۱ pass — شامل بررسی:
   - وجود lifecycle methodها (`getDerivedStateFromError`، `componentDidCatch`)
   - بدون hex hardcoded
   - بدون `fontSize: <عدد>` inline (همه با rem)
   - متن‌های فارسی موجود
   - integration: ۵ ErrorBoundary در App.jsx (۱ root + ۴ inner)

#### بخش ج — T2.02: vitest setup + smoke tests (L)

**اسکریپت:** `36_vitest_setup.py` + `36b_test_vitest_setup.py`

1. **`frontend/package.json` به‌روز شد:**
   - افزودن devDependencies: `vitest ^3.0.0`، `@vitest/coverage-v8 ^3.0.0`، `jsdom ^25.0.1`، `@testing-library/{react ^16.1.0, jest-dom ^6.6.3, user-event ^14.5.2}`
   - افزودن npm scripts: `test`, `test:watch`, `test:coverage`, `test:ui`
   - dependencies و scripts قبلی همگی حفظ شدند

2. **`frontend/vite.config.js` به‌روز شد** — افزودن بلوک `test`:
   - `environment: 'jsdom'`
   - `globals: true` (بدون نیاز به import `describe`/`it`/`expect`)
   - `setupFiles: ['./src/test/setup.js']`
   - coverage با provider `v8` و include/exclude patterns

3. **`frontend/src/test/setup.js`** — فقط `import '@testing-library/jest-dom/vitest'`

4. **۵ فایل smoke test ساخته شد:**

   | فایل | پوشش |
   |---|---|
   | `utils/numberFormat.test.js` | `formatNumber()` + `parseFormattedNumber()` — ۸ test cases شامل edge cases (null/Infinity/NaN/negative) |
   | `utils/dateFormat.test.js` | ۴ فرمت میلادی + jalali + validators + constants |
   | `stores/confirmStore.test.js` | Promise resolve/reject، replacing previous dialog، beforeEach reset |
   | `components/common/ErrorBoundary.test.jsx` | ⭐ Critical: Bomb component، fallback UI، role='alert'، custom fallback، onReset callback |
   | `pages/LoginPage.test.jsx` | render with MemoryRouter، labels «نام کاربری»/«رمز عبور»، disabled submit |

5. **تست:** ۴۵/۴۵ pass (static) — runtime `npm test` به دلیل غیبت `node_modules` در container skip شد. کاربر باید `cd frontend && npm install` را روی ماشین خود اجرا کند.

#### بخش د — T2.04: ARCHITECTURE.md (M)

**اسکریپت:** `37_architecture_doc.py` + `37b_test_architecture_doc.py`

ساخت `docs/ARCHITECTURE.md` (~۲۵۰ خط) با ۹ بخش و **۶ دیاگرام Mermaid**:

1. **System overview** — flowchart: User → Frontend → Backend → DB + DataSource آینده
2. **Backend layers** — flowchart 5-لایه: API → Service → Repository → Models → DB + Infrastructure
3. **Frontend hierarchy** — flowchart: main.jsx → StrictMode → ThemeProvider → BrowserRouter → App → (ErrorBoundary root + per-route)
4. **Theme system flow** — sequenceDiagram: کاربر کلیک تم → themeStore.setTheme → ThemeProvider effect → `:root` vars
5. **DataSource abstraction** — classDiagram: BaseDataSource ← ExcelDataSource (فعلی) + CCXTDataSource (آینده)
6. **Auth flow** — sequenceDiagram: کاربر → LoginPage → API → AuthService → bcrypt → JWT

+ جدول ۵ Zustand store + درخت فایل کامل + cross-references به سند جامع، PROJECT_CONTEXT، TASK_BACKLOG، DECISIONS_LOG.

**تست:** ۳۶/۳۶ pass — شامل شمارش دیاگرام‌های Mermaid (۳ flowchart + ۲ sequenceDiagram + ۱ classDiagram = ۶) و وجود همه ۹ بخش.

### 📁 فایل‌های ساخته‌شده/به‌روز در این چت

#### Frontend جدید
- `frontend/src/components/common/ErrorBoundary.jsx` ⭐
- `frontend/src/components/common/ErrorBoundary.test.jsx`
- `frontend/src/test/setup.js`
- `frontend/src/utils/numberFormat.test.js`
- `frontend/src/utils/dateFormat.test.js`
- `frontend/src/stores/confirmStore.test.js`
- `frontend/src/pages/LoginPage.test.jsx`
- `frontend/.env.example`

#### Frontend به‌روز
- `frontend/src/App.jsx` (defense-in-depth ErrorBoundary)
- `frontend/package.json` (devDependencies + scripts test)
- `frontend/vite.config.js` (بلوک test)

#### Backend به‌روز
- `backend/.env.example` (audit کامل + API_PREFIX + دستورالعمل کلیدها)

#### Scripts جدید
- `scripts/34_env_examples_audit.py` + `34b_test_env_examples.py`
- `scripts/35_error_boundaries.py` + `35b_test_error_boundaries.py`
- `scripts/36_vitest_setup.py` + `36b_test_vitest_setup.py`
- `scripts/37_architecture_doc.py` + `37b_test_architecture_doc.py`

#### Docs جدید
- `docs/ARCHITECTURE.md` ⭐ (با ۶ دیاگرام Mermaid)

#### Docs به‌روز
- `docs/TASK_BACKLOG.md` (T2.01-T2.04 → DONE، آمار جدید)
- `docs/CHAT_LOG.md` (این چت)
- `docs/SESSION_STATUS.md` (وضعیت جدید)
- `docs/DECISIONS_LOG.md` (افزودن ۳ تصمیم جدید #۵۵، #۵۶، #۵۷)
- `docs/PROJECT_CONTEXT.md` (افزودن لینک ARCHITECTURE.md)
- `CHANGELOG.md` (v0.5.0)

### ⚠️ نکات مهم برای آینده

- **`npm install` لازم است:** بعد از pull این تغییرات، کاربر باید `cd frontend && npm install` را اجرا کند تا dev deps جدید (vitest و testing libraries) نصب شوند.
- **اولین اجرای `npm test`:** انتظار pass شدن همه ۵ فایل تست. اگر fail شد، اولین جای بررسی: نسخه `react` در `package.json` (باید ^19.x باشد چون `@testing-library/react ^16.x` فقط با React 19 سازگار است).
- **ErrorBoundary فقط render-time errors را catch می‌کند** — خطاهای event handler و async (setTimeout، Promise unhandled) نیاز به `try/catch` دستی دارند (مستندسازی شده در docstring).
- **Mermaid در GitHub native رندر می‌شود** — در VS Code نیاز به افزونه «Markdown Preview Mermaid Support».
- **سند جامع v2.7 ارتقا نیافت** — تغییرات این چت اضافه‌ای به constitution نبودند (Error Boundary و vitest در سند ۸ و ۱۰ پوشش داده شده). در صورت نیاز در چت‌های آینده v2.8 ساخته خواهد شد.

### 📊 آمار این چت

| متریک | مقدار |
|---|---|
| اسکریپت‌های اصلی | ۴ (`34_`، `35_`، `36_`، `37_`) |
| اسکریپت‌های تست همراه | ۴ |
| چک‌های استاتیک کل | ۱۳۲ (20 + 31 + 45 + 36) |
| چک‌های runtime | ۰ (skip شد — node_modules غایب در container) |
| فایل‌های frontend جدید | ۸ (۱ component، ۵ تست، ۱ setup، ۱ env.example) |
| دیاگرام‌های Mermaid | ۶ (3 flowchart + 2 sequence + 1 class) |
| Bug رفع‌شده | ۰ |
| Decision ثبت‌شده | ۳ (#۵۵، #۵۶، #۵۷) |
| قوانین جدید | ۰ |

### 🔗 ارتباطات

- ادامه چت قبل: `TRADING-phase0-part05-ui-polish-and-governance`
- **نام چت بعد پیشنهادی:** `TRADING-phase0-part07-quality-hardening-continued` (ادامه T2.05-T2.09)
- یا اگر کاربر می‌خواهد به فاز ۱ بپرد: `TRADING-phase1-part01-ccxt-websocket-setup`

### TASK های DONE شده در این چت

- T2.01 — Error Boundaries
- T2.02 — vitest setup + smoke tests
- T2.03 — `.env.example` audit
- T2.04 — ARCHITECTURE.md

### TASK های جدید کشف‌شده

- (هیچ task جدیدی کشف نشد — کل کار طبق Backlog قبلی پیش رفت)

---


## چت ۷ — phase0-part07-quality-hardening-continued

**نام چت:** `TRADING-phase0-part07-quality-hardening-continued`  
**تاریخ:** 2026-05-18  
**Claude version:** Claude Opus 4.7  
**فاز شروع:** فاز ۰ — ۱۰۰٪ + Tier 2 — ۴/۹  
**فاز پایان:** Tier 2 — **۹/۹ DONE** ✅ + قوانین #۳۳-۴۷ + درس‌نامه M1-M21 + زیرساخت Claude Desktop

> ⚠️ **یادداشت بحرانی از چت ۸:** این بخش در چت ۸ (Atomic Update T2.19) **بازنویسی شد** چون در پایان چت ۷ به‌صورت stub باقی ماند. این **مهم‌ترین درس کل پروژه (M23)** است: «اعتماد به حافظه فعال در پایان چت، نه چک‌لیست فعال سند ۱۷.۵». راه‌حل ریشه‌ای: **قانون #۶۰** + `PENDING_FOR_NEXT_VERSION.md` که در چت ۸ معرفی شد.

### 📌 موضوع کلی

ادامه Tier 2 (Quality Hardening). سه فاز اصلی:

1. **مرحله A:** Atomic Update قوانین #۲۷-۳۲ (T2.11) — v2.7 → v2.8
2. **مرحله B:** اتمام T2.05 تا T2.09 (Git + Pre-commit + Anti-Patterns + pytest + API_DOCS) + سند v2.8 → v2.9
3. **مرحله C:** نصب Filesystem MCP + Claude Desktop config + claude_workspace structure (Tier 2 افزوده‌شده)

### 🎯 گام‌های انجام‌شده

#### مرحله A — Atomic Update قوانین #۲۷-۳۲ (T2.11)

- سند جامع: v2.7 → v2.8 با ۶ قانون جدید
- CLAUDE_CHECKLIST: v1.1 → v1.2
- PROJECT_GOVERNANCE: v1.1 → v1.2 (C21-C25)
- CHAT_LOG: یکپارچه‌سازی شمارش چت‌ها (چت ۵→۵.الف، ۶→۵.ب، ۷→۶)

#### مرحله B — Tier 2 Quality Hardening (T2.05-T2.09)

- **T2.05 — Git workflow + GIT_WORKFLOW.md:** سند جدید + اصلاح .gitignore + retroactive commits
- **T2.06 — Pre-commit hooks (Hybrid mode):** critical اجباری + minor warning + black/isort/ruff + custom hooks A1/A4/A8/A10
- **T2.07 — Anti-pattern catalog:** ANTI_PATTERNS.md با ۱۰ نمونه concrete A1-A10
- **T2.08 — Backend pytest + coverage:** pyproject.toml + conftest + ۲۵ test → **۲۵/۲۵ pass**
- **T2.09 — API_DOCS.md:** markdown alternative به Swagger با OpenAPI examples

در پایان مرحله B، سند جامع به v2.9 ارتقا یافت (+۱۵ قانون #۳۳-۴۷ + درس‌نامه M1-M21).

#### مرحله C — Infrastructure زیرساخت Claude Desktop

- **T2.14 — Filesystem MCP integration:** نصب + configure (read-only Always Allow، write Needs Approval)
- **T2.15 — Memory + Project Knowledge + Custom Instructions:** Memory toggles ON، PROJECT_KNOWLEDGE.md ساخت
- **T2.16 — `claude_workspace/` structure:** ۵ subfolder با gitignore policy

### 🛠️ اسکریپت‌های تولیدشده

| # | نام | شرح |
|---|---|---|
| 38 | `38_atomic_update_v2_8.py` | Atomic Update قوانین #۲۷-۳۲ |
| 39 | `39_git_workflow.py` | GIT_WORKFLOW.md + .gitignore audit |
| 40 | `40_pre_commit_hooks.py` | Pre-commit Hybrid mode |
| 41 | `41_anti_patterns.py` | ANTI_PATTERNS.md |
| 42 | `42_pytest_setup.py` | pyproject.toml + conftest + ۲۵ test |
| 43 | `43_sync_from_zip.py` | sync helper (single-root) |
| 44 | `44_api_docs.py` | API_DOCS.md |
| 45 | `45_fix_react_imports.py` | Bug #50 موقت (15 .jsx) |
| 46-54 | `46_*` تا `54_*` | فایل‌های auxiliary + fix scripts + atomic update v2.9 |

> توجه: قوانین #۳۳-۴۷ + درس‌نامه M1-M21 از تجربه این چت استخراج شدند (همگی در سند v2.9 ثبت).

### 📁 فایل‌های جدید

- `docs/GIT_WORKFLOW.md` + `ANTI_PATTERNS.md` + `BACKEND_TESTING.md` + `API_DOCS.md` + `PRECOMMIT.md`
- `backend/pyproject.toml` + `backend/tests/conftest.py` + ۲۵ test file
- `.pre-commit-config.yaml` + custom hook scripts
- `PROJECT_KNOWLEDGE.md` (برای Project Knowledge آپلود)
- `claude_workspace/` با ۵ subfolder + `.gitkeep` ها

### 🐛 Bug ها رفع‌شده

- (هیچ Bug جدید بحرانی — فقط fix scripts مربوط به pre-commit + tests)

### 🏛️ تصمیمات معماری

- **Hybrid Pre-commit Mode:** critical اجباری + minor warning (سند ۲۰)
- **`.gitattributes` به‌جای hook برای CRLF:** اجتناب از cp1252 crash
- **pre-commit entry: `python wrapper.py`:** cross-platform

### 📜 قوانین جدید

**#۳۳-۴۷ (۱۵ قانون):** Backup، zip placement، pip vs npm flags، read-back verify، .py vs zip routing، multi-root zip، argparse verify، .get() در or، --no-verify، Hybrid mode، .gitattributes، wrapper.py، ASCII-only، test hook قبل از deploy

### 📜 درس‌نامه‌های جدید

**M1-M21 (۲۱ درس):** درس‌نامه اشتباهات از تجربه این چت (در سند v2.9 بخش ۱۸ ثبت)

### ⚠️ نکات بحرانی برای آینده — یادداشت چت ۸

این بخش در چت ۸ اضافه شد:

1. **M23 (مهم‌ترین درس کل پروژه):** Claude در پایان چت ۷ پیام handoff تولید **نکرد** با وجود ثبت قانون در همان چت. علت: اعتماد به حافظه فعال نه چک‌لیست فعال. راه‌حل ریشه‌ای: قانون #۶۰ (PENDING-EOC در لحظه ثبت).
2. **اعداد تناقض‌دار در پایان چت ۷:** کاربر گفت +۲۷ قانون (#۳۳-۵۹) و M1-M52، ولی واقعیت سند v2.9: فقط #۳۳-۴۷ و M1-M21. این تناقض در چت ۸ کشف و حل شد (سیاست conservative numbering).
3. **CHAT_LOG چت ۷ stub باقی ماند** — همین بخش که در چت ۸ بازنویسی شد (تست عملی M23).

### 📊 آمار این چت

| متریک | مقدار |
|---|---|
| اسکریپت‌های اصلی | ~۱۷ (`38_` تا `54_`) |
| pytest tests | ۲۵/۲۵ pass |
| vitest tests | ۳۰/۳۰ pass (carry forward از چت ۶) |
| اسناد جدید | ۵ (GIT_WORKFLOW + ANTI_PATTERNS + BACKEND_TESTING + API_DOCS + PRECOMMIT) |
| قوانین جدید | ۱۵ (#۳۳-۴۷) |
| درس‌نامه جدید | ۲۱ (M1-M21) |
| Git commits | `91704ca` → `d6bc75c` |

### 🔗 ارتباطات

- ادامه چت قبل: `TRADING-phase0-part06-quality-hardening`
- **نام چت بعد:** `TRADING-phase0-part08-pre-phase1-setup` (چت ۸)
- **پیام handoff:** فراموش شد (درس M23 — در چت ۸ بازسازی شد)

### TASK های DONE شده در این چت

- T2.05 — Git Workflow + GIT_WORKFLOW.md
- T2.06 — Pre-commit hooks Hybrid mode
- T2.07 — Anti-pattern catalog
- T2.08 — Backend pytest (۲۵/۲۵)
- T2.09 — API_DOCS.md
- T2.11 — Atomic Update قوانین #۲۷-۳۲
- T2.14 — Filesystem MCP integration
- T2.15 — Claude Desktop Memory + Project Knowledge
- T2.16 — claude_workspace structure

### TASK های جدید کشف‌شده

- T2.17 تا T2.21 (در چت ۸ ثبت و برنامه‌ریزی شدند)

---

## چت ۸ — phase0-part08-pre-phase1-setup

> 🚧 **در حال انجام — این چت.** ۴ بلوک کاری قبل از فاز ۱.

**نام چت:** `TRADING-phase0-part08-pre-phase1-setup`  
**تاریخ:** 2026-05-19  
**Claude version:** Claude Opus 4.7 + Adaptive Thinking + Filesystem MCP + Project Knowledge + Memory  
**فاز شروع:** فاز ۰ — ۱۰۰٪ + Tier 2 — ۹/۹ + قوانین #۳۳-۴۷  
**فاز پایان (در حال):** آماده فاز ۱ + قوانین #۴۸-۶۱ + سند v2.10 + درس‌نامه M22-M62

### 📌 موضوع کلی

اولین چت با **Filesystem MCP + Project Knowledge + Memory + قانون #۶۰**. ۴ بلوک کاری:

1. **بلوک A — Documentation Backlog:** ادغام PENDING → v2.10 + Atomic Updates Governance + تکمیل CHAT_LOG چت ۷ + Infrastructure audit (A1-A7 + B1-B5)
2. **بلوک B — تعاملی:** GitHub setup + Settings audit (۸ tab) — نیاز به screenshot
3. **بلوک C — Tier 2 پایانی + Phase 1 readiness:** T2.10 ARCHITECTURE.md + T2.13 Bug #50 + Model Selection Guide
4. **بلوک D — پایان چت:** ادغام نهایی PENDING + CHAT8_FINALIZE + handoff + commit + push

### 📦 ورودی‌های چت

- سند جامع v2.9 (پیوست)
- Project Knowledge فعال با PROJECT_KNOWLEDGE.md
- Memory toggles ON (Search past chats + Generate memory)
- Filesystem MCP با permissions تنظیم‌شده

### 🎯 گام‌های انجام‌شده (تا این لحظه)

#### بلوک A — Documentation Backlog

- **A1 ✅:** ادغام PENDING → سند جامع v2.10 (171KB → 200.8KB، +۱۴ قانون + ۲۱ ردیف درس‌نامه + ۴ بخش جدید)
- **A2 ✅:** Atomic Update CLAUDE_CHECKLIST v1.2 → v1.3
- **A3 ✅:** Atomic Update PROJECT_GOVERNANCE v1.2 → v1.3 (C26-C30 + A11 + G8)
- **A4 ✅:** Atomic Update TASK_BACKLOG v1.4 → v1.5 (+۸ task زیرساخت Claude Desktop)
- **A5 ✅ (همین لحظه):** تکمیل CHAT_LOG چت ۷ (T2.19 — تست عملی M23) + افزودن بخش چت ۸ + اصلاح آمار
- **A6 ✅:** اصلاح آمار کلی CHAT_LOG (۲۶ → ۶۱ قانون)
- **A7 ⏳:** SESSION_STATUS برای پایان چت ۸ (در پایان چت)
- **B1-B5 ⏳:** Infrastructure audit

#### بلوک B — تعاملی (پس از بلوک A)

- **D1 ⏳:** GitHub setup
- **C1-C8 ⏳:** Settings audit (نیاز به ۸ screenshot)

### 🆕 فایل‌های جدید در این چت

- `docs/PENDING_FOR_NEXT_VERSION.md` ⭐⭐⭐ (بنیادی — قانون #۶۰)
- `docs/سند_جامع_v2_10.md` (جایگزین v2.9 — No-Deletion)

### 🆙 فایل‌های به‌روز (Atomic Update)

- `docs/CLAUDE_CHECKLIST.md` v1.2 → v1.3
- `docs/PROJECT_GOVERNANCE.md` v1.2 → v1.3
- `docs/TASK_BACKLOG.md` v1.4 → v1.5
- `docs/CHAT_LOG.md` v1.2 → v1.3 (همین فایل!)

### 🎓 درس‌های جدید کشف‌شده (M22-M62)

**کشف‌شده (۱۵ درس):**
- **M23** ⭐⭐⭐ (از چت ۷ بازیافت): عدم تولید handoff در پایان چت ۷
- **M25-M28، M30، M31، M44:** درس‌های چت ۷ که در Memory پیدا شد
- **M56-M62:** درس‌های جدید چت ۸ (Memory ≠ ثبت دقیق، self-binding، preview قبل از write، read-back verify، پیشنهاد گزینه مطلوب، ...)

**Reserved (۲۵ درس):**
- M22، M24، M29، M32-M43، M45-M55 — سیاست conservative numbering

### 📜 قوانین جدید (#۴۸-۶۱)

- **#۴۸:** پروتکل اجباری شروع چت — بخش ۱۸ + PENDING
- **#۴۹-۵۱:** Filesystem MCP permissions و workflow
- **#۵۲-۵۳:** Reserved
- **#۵۴-۵۸:** sandbox، Project Knowledge، screenshots، snapshots، تحویل فایل
- **#۵۹** ⭐: بلااستثنا اعلام مسیر دانلود
- **#۶۰** ⭐⭐⭐: PENDING-EOC در لحظه با MCP
- **#۶۱** ⭐: پیشنهاد گزینه مطلوب در چندگزینه‌ای

### 🆕 بخش‌های جدید سند جامع v2.10

- سند ۲۲: Filesystem MCP Integration
- سند ۲۳: Claude Desktop Configuration
- سند ۲۴: claude_workspace Structure
- سند ۲۵: Skills اختصاصی پروژه (placeholder)

### 🔗 ارتباطات (چت ۸)

- ادامه چت قبل: `TRADING-phase0-part07-quality-hardening-continued`
- **چت بعد:** چت ۹ — `TRADING-phase0-part09-v2_11-atomic-update-and-bug50-cleanup` (فاز A: ادغام + Bug #50 cleanup)

---

## چت ۹ (Session 9) — `TRADING-phase0-part09-v2_11-atomic-update-and-bug50-cleanup`

**تاریخ:** 2026-05-20  
**مدت:** ~۵ ساعت  
**وضعیت:** ✅ فاز A کامل (فاز B به چت ۱۰ موکول شد)  
**Git HEAD شروع:** `cae4b0b` (push شده به GitHub)  
**Tier:** Tier 2 در حال تکمیل

### دستاوردهای کلیدی

- **Atomic Update v2.10 → v2.11:** ادغام ۱۰ آیتم PENDING + ۴ قانون UX جدید + ۱ درس (M63)
- **Bug #50 cleanup:** حذف ۱۷ خط `import React` + تنظیم `jsxRuntime: 'automatic'` + تبدیل `React.StrictMode` → named `StrictMode`
- **کشف درس M64:** vitest تنظیم `esbuild.jsx` جداگانه از plugin-react لازم دارد — راه‌حل اعمال شد، ثبت در PENDING برای v2.12
- **Bug #52 مستند شد:** pre-commit `end-of-file-fixer` با فایل فارسی Windows (TROUBLESHOOTING v1.1)
- **اصلاحات مستندات:** سند ۲۳.۱ (Capabilities → Memory)، ۲۳.۴ (Settings audit)، `.gitignore` (فرمت پوشه + .gitkeep)
- **Governance docs v1.4:** هر ۴ سند governance (CLAUDE_CHECKLIST، PROJECT_GOVERNANCE، TASK_BACKLOG، CHAT_LOG)
- **تست:** 30/30 vitest pass پس از cleanup

### تصمیمات کلیدی

- **DECISION:** فاز B (CCXT skeleton) به چت ۱۰ موکول شد — context محدود بعد از کشف M64 + planning تازه برای CCXT لازم است
- **DECISION:** سبک تعامل Claude-کاربر با ۴ قانون UX (#۶۲-۶۵) تثبیت شد
- **DECISION:** فرمت Atomic Update v2.10 → v2.11 با ۷ string-based edit اسکریپت Python (idempotent + read-back verify)

### Bug های جدید

- **Bug #52:** pre-commit `end-of-file-fixer` با نام فایل فارسی روی Windows کرش می‌کند. Workaround: `$env:PYTHONIOENCODING="utf-8"`. راه‌حل دائمی: env var محیطی User-level.
- **Bug #50 (رفع شد):** `import React from 'react'` اضافه از ۱۵ .jsx حذف شد با تنظیم صریح JSX runtime. در حین حل آن، Bug جدید (M64) کشف شد.

### درس‌های جدید

- **M63** ⭐ (در v2.11 ادغام شد): فرض نکردن وضعیت کارهای infrastructure در handoff — status صریح لازم است (✅/📋/⚠️/💡)
- **M64** (در PENDING برای v2.12): plugin-react `jsxRuntime` به vitest منتقل نمی‌شود — `esbuild.jsx` top-level لازم است

### قوانین جدید (#۶۲-۶۵)

- **#۶۲** ⭐: فایل handoff دائمی در `claude_workspace/incoming_permanent/CHAT{N+1}_HANDOFF.txt` با prefix صریح
- **#۶۳** ⭐: Convention بصری برای گام‌های اجرایی (🟢 ▶️ EXECUTE)
- **#۶۴** ⭐: عدم نمایش جزئیات تصحیح خطای کد
- **#۶۵** ⭐: ثبت درس از اشتباهات با نمایش به کاربر

### اسناد تغییریافته

- `docs/سند_جامع_v2_11.md` — ایجاد شد (152,438 chars، +5,035 نسبت به v2.10)
- `docs/TROUBLESHOOTING.md` — v1.0 → v1.1 (Bug #52 افزوده شد)
- `docs/PENDING_FOR_NEXT_VERSION.md` — v0.1 → v0.2 (پاک‌سازی آیتم‌های ادغام شده + نگه داشتن Z2.1/M64)
- هر ۴ سند governance v1.3 → v1.4 (CLAUDE_CHECKLIST، PROJECT_GOVERNANCE، TASK_BACKLOG، همین CHAT_LOG)
- `frontend/vite.config.js` — +`jsxRuntime: 'automatic'` + `esbuild.jsx`
- `frontend/src/main.jsx` — `React.StrictMode` → named `StrictMode`
- `frontend/src/**/*.jsx` (۱۷ فایل) — حذف `import React from 'react';`
- `.gitignore` — فرمت `claude_workspace/{screenshots,zip_temp}/*` + `!.gitkeep`
- 4 اسکریپت جدید: `scripts/55`، `55b`، `56`، `56b`

### 🔗 ارتباطات

- ادامه چت قبل: `TRADING-phase0-part08-pre-phase1-setup`
- **چت بعد پیشنهادی:** `TRADING-phase1-part01-ccxt-websocket-setup` (شروع رسمی فاز ۱ — CCXTDataSource skeleton + WebSocket subscriber)
- **handoff فایل:** `claude_workspace/incoming_permanent/CHAT10_HANDOFF.txt`

---

## چت ۱۰ (Session 10) — `TRADING-phase1-part01-ccxt-websocket-setup`

**تاریخ:** 2026-05-20  
**Claude version:** Claude Opus 4.7 (با Filesystem MCP + قوانین #۶۲-۶۵)  
**Git HEAD شروع:** `88debb7`  
**Git HEAD پایان:** `5cfc7e0`  
**فاز شروع:** فاز ۰ کامل (۱۰۰٪) + فاز ۱ آماده شروع  
**فاز پایان:** **فاز ۱ — CCXTDataSource Skeleton آماده** 🎉

### 📌 موضوع کلی

اولین چت رسمی **فاز ۱** (Market Data). سه گام بنیادی:

1. **G1 — Dependencies** (~۹۰ دقیقه با ۴ iteration رفع bug):
   - افزودن `ccxt`, `websockets` به requirements.txt
   - رفع Bug #53 (BOM برای pip روی Windows)
   - pin ccxt به نسخه موجود در PyPI (4.3.98 به‌جای 4.3.0)
   - نصب موفق در venv فعال + verification با import

2. **G2 — Architecture Q&A** (~۲۰ دقیقه):
   - مرور `base.py` + `excel_source.py` + `binance_mappings.py`
   - ۴ تصمیم معماری (Decisions #۶۱-۶۴)

3. **G3 — CCXTDataSource Skeleton** (~۶۰ دقیقه):
   - بلوک ۱: gradient interface در `base.py` (read_ohlcv_async با default impl)
   - بلوک ۲: ساخت `ccxt_source.py` با ~۲۰۰ خط + ۵ تست AsyncMock

### 🎯 گام‌های انجام‌شده

#### G1 — Dependencies

**اسکریپت‌ها:** `58_*`, `59_*`, `60_*` (و تست‌های همراه)

- **58:** افزودن `ccxt==4.3.0` و `websockets==12.0` به requirements.txt + comment update — ۶/۶ pass
- **59:** افزودن BOM (utf-8-sig) برای رفع Bug #53 — ۴/۴ pass
- **60:** تغییر ccxt به `4.3.98` (آخرین stable در 4.3.x) — ۵/۵ pass
- **pip install:** 14 package جدید (شامل ccxt 4.3.98، websockets 12.0، aiohttp، yarl، multidict، …)
- **verification:** `import ccxt, websockets, ccxt.async_support` → OK

**نکته جانبی:** pip بطور خودکار `websockets-16.0` موجود را به `12.0` downgrade کرد (Pinning موفق).

#### G2 — Architecture Decisions (Decisions #۶۱-۶۴)

| # | تصمیم | مزیت |
|---|---|---|
| **#۶۱** | Gradient interface: `DataSource.read_ohlcv_async` با default impl = `asyncio.to_thread(self.read_ohlcv, ...)` | backwards compat با ExcelDataSource، async-first در FastAPI |
| **#۶۲** | Mock strategy: `AsyncMock` در fixtures (نه VCR، نه live) | سریع، deterministic، بدون شبکه |
| **#۶۳** | WS ↔ repository: `asyncio.Queue` واسطه (نه direct write) | decoupling، batch write، multi-consumer در آینده |
| **#۶۴** | Rate limiting: ccxt built-in `enableRateLimit=True` | ساده، کار می‌کند، YAGNI برای custom |

#### G3 — CCXTDataSource Skeleton

**اسکریپت‌ها:** `61_*`, `62_*` (و تست‌های همراه)

- **61:** Atomic edit روی `base.py` — افزودن `import asyncio` + متد `read_ohlcv_async` با default impl. Backwards compat ExcelDataSource تأیید شد (۵/۵ pass)
- **62:** ساخت `backend/app/infrastructure/data_sources/ccxt_source.py` (7993 bytes)
  - کلاس `CCXTDataSource(DataSource)` با `__init__`, `name`, `_get_exchange`, `close`, `read_ohlcv_async`, `read_ohlcv` (sync wrapper)
  - Error mapping: `BadSymbol` → `ValidationError(CCXT_BAD_SYMBOL)`، بقیه → `BusinessLogicError(CCXT_FETCH_ERROR)`
  - Documentation کامل با docstring فارسی
- **62b:** ۵ تست با AsyncMock — همه pass در اولین تلاش (exception signatures و schema fields صحیح بود)

### 📁 فایل‌های جدید/تغییریافته

#### Backend جدید
- `backend/app/infrastructure/data_sources/ccxt_source.py` ⭐ (7993 bytes)

#### Backend به‌روز
- `backend/requirements.txt` (+ccxt==4.3.98, +websockets==12.0, +BOM)
- `backend/app/infrastructure/data_sources/base.py` (+import asyncio, +read_ohlcv_async)

#### Scripts جدید (۱۰)
- `scripts/58_add_phase1_deps.py` + `58b_test_phase1_deps.py`
- `scripts/59_fix_requirements_encoding.py` + `59b_test_requirements_encoding.py`
- `scripts/60_pin_ccxt_to_4_3_98.py` + `60b_test_ccxt_pin.py`
- `scripts/61_add_async_to_base_datasource.py` + `61b_test_async_base.py`
- `scripts/62_create_ccxt_source.py` + `62b_test_ccxt_source.py`

#### Docs به‌روز (پایان چت)
- `docs/PENDING_FOR_NEXT_VERSION.md` (v0.3 → v0.4)
- `docs/CHAT_LOG.md` (این بخش)
- `docs/TROUBLESHOOTING.md` (افزودن Bug #53)
- `docs/SESSION_STATUS.md` (rewrite برای شروع چت ۱۱)

### 🐛 Bug های جدید

- **Bug #53:** pip روی Windows فارسی-locale فایل UTF-8 بدون BOM با متن غیر-ASCII را crash می‌کند با `UnicodeDecodeError: 'charmap' codec can't decode byte 0x81`. راه‌حل: utf-8-sig (با BOM). در TROUBLESHOOTING ثبت شد.

### 🎓 درس‌های جدید کشف‌شده (M66-M69)

| ID | شرح | وضعیت |
|---|---|---|
| **M66** | Filesystem MCP و فایل‌های >200KB (hang کل session) | در PENDING برای v2.12 |
| **M67** | BOM لازم برای فایل UTF-8 + غیر-ASCII روی Windows pip | در PENDING (همراه Bug #53 در TROUBLESHOOTING) |
| **M68** | نسخه‌های pinned باید با PyPI verify شوند هنگام مستندسازی | در PENDING |
| **M69** | `asyncio.run()` در FastAPI handler crash می‌کند (در docstring CCXTDataSource ذکر شد) | در PENDING |

### 🏛️ تصمیمات معماری (Decisions #۶۱-۶۴)

به DECISIONS_LOG ادغام می‌شود در ابتدای چت ۱۱ یا v2.12. متن کامل در بخش G2 بالا.

### 📜 قوانین جدید

**هیچ قانون جدیدی در چت ۱۰ ساخته نشد.** ۴ قانون UX (#۶۲-۶۵) که در v2.11 ادغام شده بودند، در عمل تست شدند و کار کردند:

- **#۶۲** (handoff دائمی): فایل CHAT10_HANDOFF خوانده شد ✅
- **#۶۳** (🟢 ▶️ EXECUTE): در ۱۰+ گام استفاده شد ✅
- **#۶۴** (عدم نمایش جزئیات تصحیح): در حل Bug #53 رعایت شد ✅
- **#۶۵** (نمایش درس): M66-M69 به کاربر نمایش داده شدند ✅

### ⚠️ نکات مهم برای آینده (چت ۱۱+)

- **`ccxt_source.py` skeleton است** — هنوز با Binance واقعی تست نشده. در چت ۱۱ یا ۱۲ یک integration test با اتصال واقعی انجام شود (احتیاج: VPN در ایران)
- **`binance_client.py` و `binance_ws.py` هنوز ساخته نشده‌اند** — در `backend/app/infrastructure/exchange/` (فقط `__init__.py` موجود)
- **`exchange_repository.py` هنوز نیست** — برای مدیریت `Exchange` و `ExchangeApiKey` در DB
- **WebSocket endpoint API برای frontend هنوز ساخته نشده**
- **Bug #53 fix در `requirements.txt` BOM دارد** — اگر کاربر فایل را با editor بدون BOM-aware باز و save کند، BOM از دست می‌رود و pip دوباره crash می‌کند. نگه‌داری مهم است.

### 📊 آمار این چت

| متریک | مقدار |
|---|---|
| اسکریپت‌های اصلی (تعداد ID مستقل) | ۵ (`58`, `59`, `60`, `61`, `62`) |
| اسکریپت‌های تست همراه | ۵ (`58b`, `59b`, `60b`, `61b`, `62b`) |
| **مجموع اسکریپت‌ها** | **۱۰** |
| تست‌های static + integration | ۲۵ (۶+۴+۵+۵+۵) |
| فایل‌های جدید Backend | ۱ (`ccxt_source.py`) |
| فایل‌های تغییریافته Backend | ۲ (`requirements.txt`, `base.py`) |
| Bug رفع‌شده | ۱ (Bug #53 — BOM) |
| Decision جدید | ۴ (#۶۱-۶۴) |
| درس جدید | ۴ (M66-M69) |
| قوانین جدید | ۰ (۴ قانون UX چت ۹ در عمل تست شدند) |
| فایل‌های دیگر تغییریافته | ۴ (PENDING، CHAT_LOG، TROUBLESHOOTING، SESSION_STATUS) |

### 🔗 ارتباطات

- ادامه چت قبل: `TRADING-phase0-part09-v2_11-atomic-update-and-bug50-cleanup`
- **چت بعد پیشنهادی:** `TRADING-phase1to2-transition-discovery` (Discovery Chat — جمع‌بندی فنی فازهای ۲-۸ قبل از ورود به فاز ۲)
- **تصمیمات استراتژیک پایان چت:**
  - **Decision #65:** اتصال زنده Binance/Telegram تا فاز ۵+ موکول می‌شود. CCXTDataSource skeleton روی Shelf می‌ماند.
  - **Decision #66 + قانون #۶۶:** Backup اجباری در پایان هر چت — فرمت `trading-system-chatNN-YYYY-MM-DD.zip` در `claude_workspace/backups/`. پیاده‌سازی اولیه: scripts/63_*.
  - **Discovery Chat:** چت ۱۱ به discovery اختصاص می‌یابد برای بحث جامع انتظارات + roadmap فاز‌های ۲-۸.
- **handoff فایل:** `claude_workspace/incoming_permanent/CHAT11_HANDOFF.txt`

### TASK های DONE شده در این چت

- T3.01 (پیشنهادی) — CCXTDataSource skeleton + ۵ test mock
- T3.02 (پیشنهادی) — DataSource async extension (gradient interface)

### TASK های جدید کشف‌شده برای چت ۱۱+

- T3.03 — binance_client.py (REST wrapper)
- T3.04 — binance_ws.py (WebSocket subscriber با asyncio.Queue)
- T3.05 — exchange_repository.py (Exchange + ExchangeApiKey)
- T3.06 — WebSocket endpoint برای frontend
- T3.07 — integration test با Binance واقعی (نیاز به VPN در ایران)
- T3.08 — انتشار Endpoint REST برای fetch OHLCV (تبدیل CCXTDataSource به HTTP endpoint)

---

## آمار کلی پروژه

| دسته | تعداد |
|---|---|
| چت‌های انجام‌شده | ۱۰ |
| اسکریپت‌های تولید‌شده | ~۶۴ (~۶۰ تا چت ۸ + ۴ جدید در چت ۹: 55، 55b، 56، 56b) |
| Bug های ثبت‌شده | ۵۳ (+Bug #53 در چت ۱۰ — BOM در requirements.txt) |
| Decisions ثبت‌شده | ~۶۴ (+۴ در چت ۱۰: #۶۱-۶۴ معماری CCXT) |
| قوانین قفل‌شده | **۶۵** (با ۲ Reserved: #۵۲، #۵۳) |
| درس‌نامه ثبت‌شده | **۶۷ ردیف** (۴۲ کشف‌شده تا M69 + ۲۵ Reserved) |
| فاز پایان‌یافته | فاز ۰ (۱۰۰٪) + Tier 2 (۱۶/۲۱ ✅) + فاز ۱ skeleton |
| فاز در حال انجام | فاز ۱ — binance_client.py + binance_ws.py (چت ۱۱+) |
| نسخه سند جامع | **v2.11** (در چت ۹ ایجاد شد) |

---

## 📌 پایان CHAT_LOG

**نسخه:** v1.5 (2026-05-20 — چت ۱۰: افزودن بخش چت ۱۰ — CCXTDataSource skeleton + ۴ Decision + ۴ درس)  
**به‌روز شده در:** چت `TRADING-phase1-part01-ccxt-websocket-setup`  
**به‌روز توسط:** Claude طبق قانون #۲۳ + #۲۶ + #۶۰ — CLAUDE_CHECKLIST v1.4 فاز ۳
