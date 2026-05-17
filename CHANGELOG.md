# 📝 CHANGELOG

تمام تغییرات قابل توجه پروژه در این فایل ثبت می‌شوند.

فرمت: [Keep a Changelog](https://keepachangelog.com/) با Semantic Versioning.

---

## [Unreleased]

### Planned
- ادامه Tier 2: T2.05 (Git workflow audit), T2.06 (Pre-commit hooks), T2.07-T2.09
- یا فاز ۱: CCXT + WebSocket

---

## [0.5.0] — 2026-05-17

> 🛡️ **Tier 2 (Quality Hardening) — ۴/۹ تکمیل** — پایه‌گذاری مقاومت UI و تست frontend

### Added (افزوده شد)

#### Frontend Components
- `ErrorBoundary.jsx` ⭐ — class component با Variant Indicator Pattern، defense-in-depth (root + per-route)، dev-only stack trace در `<details>`، fallback prop سفارشی، onReset callback، accessibility کامل (`role="alert"` + `aria-live="assertive"`)

#### Frontend Tests (پنج smoke test)
- `utils/numberFormat.test.js` — ۸ test case برای `formatNumber()` و `parseFormattedNumber()`
- `utils/dateFormat.test.js` — ۴ فرمت میلادی + jalali + validators + constants
- `stores/confirmStore.test.js` — Promise resolve/reject، replacing previous dialog
- `components/common/ErrorBoundary.test.jsx` — ⭐ Bomb component برای trigger خطا، تست fallback UI، custom fallback، onReset
- `pages/LoginPage.test.jsx` — render with MemoryRouter، labels فارسی، disabled submit

#### Test Infrastructure
- vitest ^3.0.0 با coverage v8 — اضافه به `frontend/package.json`
- `frontend/vite.config.js` — افزودن بلوک `test` با `environment: 'jsdom'`, `globals: true`, `setupFiles`
- `frontend/src/test/setup.js` — import از `@testing-library/jest-dom/vitest`
- ۴ npm script: `test`, `test:watch`, `test:coverage`, `test:ui`

#### Environment Files
- `frontend/.env.example` — ساخت از صفر با هشدار امنیتی Vite (prefix VITE_)

#### Documentation
- `docs/ARCHITECTURE.md` ⭐ — سند معماری با ۶ دیاگرام Mermaid:
  - System overview (flowchart)
  - Backend layers (flowchart 5-لایه)
  - Frontend hierarchy (flowchart با ErrorBoundary defense-in-depth)
  - Theme system flow (sequenceDiagram)
  - DataSource abstraction (classDiagram)
  - Auth flow (sequenceDiagram)
  + جدول ۵ Zustand store + درخت فایل کامل + cross-references

### Changed (تغییر کرد)

#### Frontend
- `frontend/src/App.jsx` — wrap کل Routes با `<ErrorBoundary label="root">` و هر صفحه با `<ErrorBoundary label="route:{name}">` جداگانه
- `backend/.env.example` — به‌روزرسانی `APP_VERSION` به `0.4.0`، افزودن `API_PREFIX=/api/v1`، افزودن دستورالعمل تولید `SECRET_KEY` (`secrets.token_urlsafe`) و `ENCRYPTION_KEY` (`Fernet.generate_key`) در کامنت‌ها
- `frontend/package.json` — افزودن ۶ devDep جدید + ۴ npm script test

### Scripts (جدید — ۴ اسکریپت اصلی + ۴ تست همراه)
- `scripts/34_env_examples_audit.py` + `34b_test_env_examples.py` (20/20 ✅)
- `scripts/35_error_boundaries.py` + `35b_test_error_boundaries.py` (31/31 ✅)
- `scripts/36_vitest_setup.py` + `36b_test_vitest_setup.py` (45/45 ✅)
- `scripts/37_architecture_doc.py` + `37b_test_architecture_doc.py` (36/36 ✅)

### Decisions Logged
- #۵۵ — ErrorBoundary defense-in-depth (root + per-route) — به جای فقط یک مرز سراسری
- #۵۶ — Vitest به‌جای Jest برای frontend tests
- #۵۷ — ARCHITECTURE.md به‌صورت یک فایل واحد (نه چند فایل در `architecture/`)

### Migration Notes (برای کاربر)

⚠️ **بعد از pull این تغییرات، اجرای `npm install` لازم است:**
```bash
cd frontend
npm install
```

نصب ~۶ devDependency جدید (vitest + testing libraries + jsdom) لازم است. حجم اضافه: ~۵۰MB در `node_modules`.

سپس می‌توان تست‌ها را اجرا کرد:
```bash
npm test               # یک‌بار، quiet
npm run test:watch     # حالت تعاملی (re-run هنگام تغییر)
npm run test:coverage  # با گزارش پوشش (HTML در coverage/)
```

### نکات فنی

- **ErrorBoundary محدودیت‌ها:** فقط render-time errors را catch می‌کند. خطاهای event handler و async (setTimeout، Promise unhandled) نیاز به `try/catch` دستی دارند. این محدودیت ذاتی React است.
- **Mermaid rendering:** GitHub native رندر می‌کند. در VS Code افزونه‌ی «Markdown Preview Mermaid Support» نصب کنید.
- **سند جامع v2.7 ارتقا نیافت:** تغییرات این چت اضافه‌ای به constitution نبودند. در صورت تغییرات معماری بنیادی در آینده، v2.8 ساخته خواهد شد.

---

## [0.4.0] — 2026-05-17

> 🎉 **فاز ۰ تکمیل ۱۰۰٪** + ساخت Governance Infrastructure

### Added (افزوده شد)

#### Frontend Components
- `SkeletonBlock.jsx` — placeholder متحرک با ۴ variant (rect/text/circle/line)
- `ConfirmDialog.jsx` — مودال تأیید با Variant Indicator Pattern + focus trap
- `SettingsPage.jsx` — صفحه `/settings` با ۳ بخش
- `ThemeCard.jsx` — کارت preview تم با ۵ نوار رنگ
- `FontSizeControl.jsx` — ۴ preset (12/14/16/18px)
- `CalendarToggle.jsx` — انتخاب تقویم + ۴ فرمت میلادی

#### Frontend Utilities
- `utils/numberFormat.js` — `formatNumber()` با `Intl.NumberFormat`
- `utils/dateFormat.js` — `formatDate()` با شمسی/میلادی + ۴ فرمت

#### Frontend Stores
- `confirmStore.js` — Zustand store برای ConfirmDialog (Promise-based)
- `preferencesStore.js` — calendar + gregorianFormat با persist v2

#### Governance Infrastructure (۱۰ سند جدید + ۱ ارتقا)
- `docs/PROJECT_GOVERNANCE.md` ⭐ — سند راهبردی فرایند
- `docs/CLAUDE_CHECKLIST.md` ⭐ — چک‌لیست explicit ۳ فاز
- `docs/TASK_BACKLOG.md` ⭐ — ۶۳ task در ۴ Tier
- `docs/CHAT_LOG.md` ⭐ — تاریخچه ۶ چت با Template
- `docs/GLOSSARY.md` — ~۷۰ اصطلاح در ۷ بخش
- `docs/TROUBLESHOOTING.md` — ۴۹ Bug + ۱۰ FAQ + ۷ مشکل محیطی
- `docs/DECISIONS_LOG.md` — ۵۴ ADR
- `docs/REUSABLE_SKELETON.md` — راهنمای استفاده مجدد + Vision template
- `docs/ONBOARDING_GUIDE.md` — راهنمای ۴-۶ ساعته برنامه‌نویس جدید
- `docs/STYLE_GUIDE.md` — code style + Anti-Patterns + Patterns
- `docs/سند_جامع_v2_7.md` — ارتقا از v2.6 + سند ۱۶ و ۱۷ جدید
- `README.md` — بازنویسی کامل

#### Scripts
- `scripts/29_skeleton_confirm.py` + `29b_test_skeleton_confirm.py`
- `scripts/30_settings_page.py` + `30b_test_settings_page.py`
- `scripts/31_numeric_calendar.py` + `31b_test_numeric_calendar.py`
- `scripts/32_phase0_polish.py` + `32b_test_fixes.py`
- `scripts/33_upgrade_doc_to_v27.py`

### Changed (تغییر کرد)

- `frontend/src/index.css`:
  - افزودن `html { font-size: var(--font-size-base) }`
  - افزودن `@keyframes skeleton-shimmer`
  - افزودن `@keyframes dialog-fade-in` و `dialog-slide-in`
  - افزودن `@media (prefers-reduced-motion: reduce)`
- `frontend/src/App.jsx` — mount ConfirmDialog + route `/settings`
- `frontend/src/pages/HomePage.jsx` — `askConfirm` برای logout + لینک ⚙️ به `/settings` + `formatNumber(1714)` + همه fontSize به rem
- `frontend/src/pages/ChartPage.jsx` — SkeletonBlock در loading + `timeFormatter` به جای `dateFormat` + `formatNumber` در متادیتا + همه fontSize به rem
- `frontend/src/pages/LoginPage.jsx` — همه fontSize به rem
- `frontend/src/components/common/Toast.jsx` — همه fontSize به rem

### Fixed (رفع شد)

- **Bug #46:** ESM URL scheme در ویندوز در اسکریپت‌های تست — `Path.as_posix()` → `Path.as_uri()`
- **Bug #47:** Font Size scaling شکسته — body با var ست بود ولی همه inline px ثابت override می‌کردند. راه‌حل: `html { font-size: var(...) }` + تبدیل همه inline `fontSize: N` به rem
- **Bug #48:** tooltip تاریخ نمودار نمایش داده نمی‌شد — lightweight-charts v4.x فقط string می‌پذیرد در `dateFormat`. راه‌حل: استفاده از `timeFormatter` (function)
- **Bug #49:** عدد 1714 کندل در HomePage بدون کاما — hardcoded string بود. راه‌حل: `{formatNumber(1714)}`

### Decided (تصمیم گرفته شد)

- **#50:** `preferencesStore` جدا از `themeStore` (concerns متفاوت)
- **#51:** Variant Indicator Pattern مجدداً برای ConfirmDialog تأیید
- **#52:** `Intl` built-in به جای کتابخانه شمسی (moment-jalaali، dayjs)
- **#53:** rem به جای px برای fontSize های inline
- **#54:** Governance Infrastructure ۱۲-سندی — تغییر فلسفه از "Claude به یاد می‌آورد" به "اسناد بیرونی"

### New Rules (قوانین جدید)

- **#۲۳:** هر چت، CHAT_LOG با بخش جدید آپدیت شود
- **#۲۴:** سند جامع فقط افزوده/اصلاح می‌شود — هرگز حذف نمی‌شود (No-Deletion)
- **#۲۵:** Claude در شروع چت چک‌لیست ۸ مرحله را اجرا کند
- **#۲۶:** تغییرات اسناد به‌صورت اتمیک اعمال شوند

---

## [0.3.0] — 2026-05-17 (صبح)

> Theme Engine + Toast Notifications

### Added
- Theme Engine با ۵ تم (binance-dark، light-minimal، dark-modern، pastel، sky-blue)
- `ThemeProvider` که CSS variables را به `:root` تزریق می‌کند
- `themeStore` با Zustand persist
- Toast Notifications سراسری
- `Toast`, `ToastContainer`, `toastStore`
- اسکریپت `scripts/00b_post_unzip_setup.py` برای راه‌اندازی خودکار

### Fixed
- **Bug #43:** Binance Color Accuracy — استخراج رنگ‌های دقیق از سایت بایننس
- **Bug #44:** Interactive States Missing — افزودن hover/active/focus-visible/disabled برای همه buttons و inputs
- **Bug #45:** Toast Theme Inconsistency — معرفی Variant Indicator Pattern

### New Rules
- **#۲۱:** هر چیز قابل تست با کد، با کد تست شود
- **#۲۲:** هر اسکریپت `{N}_*.py` باید `{N}b_test_*.py` همراه داشته باشد

### Documentation
- **سند جامع v2.6:** افزودن بخش ۸.۷.۱ (Interactive States) و ۸.۸.۱ (Variant Indicator Pattern)
- اصلاحیه ۱۳.۶: قالب نام چت

---

## [0.2.0] — 2026-05-16 (تخمینی)

> Auth + اولین API + Frontend Foundation

### Added
- JWT authentication با python-jose
- bcrypt direct (به جای passlib)
- OAuth2 password flow
- Auth dependencies: `current_user`, `current_admin`
- اولین endpoint محافظت‌شده: `GET /ohlcv/{symbol_id}`
- Frontend scaffold با Vite + React 18 + react-router-dom + axios + zustand
- LoginPage + ProtectedRoute
- HomePage ساده
- ChartPage با lightweight-charts و OHLCV واقعی

### Fixed
- ~Bug #15-#25 (تقریبی): passlib، CORS، timestamp، ProtectedRoute، ...

---

## [0.1.5] — 2026-05-15 (تخمینی)

> Database Layer + Models + Repositories + DataSource

### Added
- Async SQLAlchemy setup با SQLite
- Models: User، Exchange، Symbol، Timeframe، Market، OhlcvData
- Repositories: یک per model + BaseRepository
- Alembic + اولین migration
- Seeding: admin user + Excel exchange
- DataSource Abstraction: `BaseDataSource` + `ExcelDataSource`

---

## [0.1.1] — 2026-05-14 (تخمینی)

> Backend Core Layer

### Added
- FastAPI scaffold + venv + dependencies
- `backend/main.py` با endpoint `/health`
- Pydantic Settings برای `.env`
- Loguru logger (با fix رنگ ANSI و emoji برای Windows CMD)
- Custom Exceptions hierarchy
- Exception Handlers سراسری
- Standard Response model
- ۱۳ تصمیم معماری ثبت شد

### Fixed
- ~Bug #1-#10 (تقریبی): encoding، paths، venv در Windows، emoji

---

## [0.1.0] — 2026-05-13 (تخمینی)

> Project Setup — اولین نسخه

### Added
- ساختار پوشه پروژه (backend, frontend, scripts, docs)
- `.gitignore` حرفه‌ای Python + Node
- اسناد پایه: README، CHANGELOG، SESSION_STATUS، PROJECT_CONTEXT
- DataSource Abstraction در `app/infrastructure/`
- ۴ تصمیم معماری اولیه (#1-#4)
- قوانین #۱ تا #۱۴ ابتدایی

---

## فرمت نسخه‌گذاری

این پروژه از Semantic Versioning استفاده می‌کند:
- **MAJOR.MINOR.PATCH**
- `MAJOR`: تغییر breaking در API یا معماری
- `MINOR`: feature جدید بدون breaking
- `PATCH`: bug fix

نسخه‌گذاری فاز:
- `0.x.x`: فاز ۰ (در حال توسعه)
- `0.4.0`: تکمیل فاز ۰
- `1.0.0`: تکمیل فاز ۱ (CCXT + WebSocket) — اولین نسخه قابل استفاده

---

**به‌روز:** 2026-05-17  
**نسخه فعلی:** v0.4.0
