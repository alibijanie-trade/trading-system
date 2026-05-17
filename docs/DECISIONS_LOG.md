# 🏛️ DECISIONS_LOG — تاریخچه تصمیمات معماری

> **هدف یک‌خطی:** ثبت "چرا"ی هر تصمیم معماری در پروژه — برای جلوگیری از بازکردن همان سؤالات در آینده.

> **محل قرارگیری:** `docs/DECISIONS_LOG.md`  
> **به‌روز توسط:** Claude در پایان چت اگر تصمیم جدید گرفته شد (CLAUDE_CHECKLIST فاز ۳ مرحله ۴)  
> **نسخه:** v1.0 (2026-05-17)

---

## 📑 فهرست

- [راهنما](#راهنما)
- [دسته‌بندی موضوعی](#دستهبندی-موضوعی)
- [Decision Catalog](#decision-catalog)

---

## راهنما

این سند بر اساس **ADR pattern** (Architecture Decision Record) است. هر تصمیم:

```markdown
## Decision #N — {عنوان}

**ثبت‌شده در:** چت {نام چت}  
**تاریخ:** YYYY-MM-DD  
**Status:** [Accepted / Superseded by #M / Rejected / Pending]  
**دسته:** [Backend / Frontend / Infrastructure / Process / Tooling]

### Context (زمینه)
چرا این سؤال مطرح شد؟

### Options Considered (گزینه‌های بررسی‌شده)
1. **Option A:** ...  پیامد: ...
2. **Option B:** ...  پیامد: ...

### Decision (تصمیم نهایی)
✅ Option {X} انتخاب شد.

### Rationale (دلیل)
- مزیت ۱
- مزیت ۲
- (پذیرفته‌شده trade-off ها)

### Consequences (پیامدها)
- 👍 مثبت: ...
- 👎 منفی: ...

### Reference
- سند مرتبط
- اسکریپت/فایل
```

---

## دسته‌بندی موضوعی

| دسته | Decision IDs |
|---|---|
| **Stack & Tooling** | #1, #5, #7, #14, #15 |
| **Backend Architecture** | #2, #3, #4, #6, #8, #9, #10 |
| **Auth & Security** | #11, #12, #13 |
| **Frontend Architecture** | #20-#29 |
| **Theme & UI Design** | #30-#48 |
| **Process & Governance** | #50-#54 |

---

## Decision Catalog

### Decision #1 — Stack نهایی پروژه

**ثبت‌شده در:** چت ۱ (setup)  
**تاریخ:** 2026-05-13  
**Status:** ✅ Accepted  
**دسته:** Stack & Tooling

#### Context
نیاز به انتخاب stack برای پروژه ترید. ملاحظات: قابلیت توسعه، performance، ecosystem ایرانی.

#### Options Considered
1. **Django + Vue:** ecosystem بزرگ، اما Django سنگین‌تر از نیاز.
2. **Express + React:** سبک، اما TypeScript پایه نیست.
3. **FastAPI + React:** ✅ هر دو modern، async-first، type-hinted.
4. **Go + Svelte:** عالی برای performance، اما learning curve بالا.

#### Decision
✅ **FastAPI + React + Vite + zustand + SQLAlchemy**

#### Rationale
- FastAPI: async، Pydantic، OpenAPI خودکار، کارایی نزدیک Go
- React: ecosystem بزرگ، lightweight-charts compatible
- Vite: HMR سریع، dev experience عالی
- zustand: state management ساده‌تر از Redux

#### Consequences
- 👍 dev experience سریع، typing عالی، docs خودکار
- 👎 یادگیری async در Python برای کاربر جدید

---

### Decision #2 — Repository Pattern

**ثبت‌شده در:** چت ۱  
**Status:** ✅ Accepted

#### Context
چگونه query های DB سازماندهی شوند؟

#### Decision
✅ هر مدل یک Repository class. Routes/Services هرگز مستقیماً به DB query نمی‌زنند.

#### Rationale
- Testability (mock کردن Repository ساده‌تر)
- جلوگیری از تکرار query
- یک محل برای optimization

---

### Decision #3 — DataSource Abstraction

**ثبت‌شده در:** چت ۱  
**Status:** ✅ Accepted

#### Context
در فاز ۰ از Excel استفاده می‌کنیم، در فاز ۱ CCXT، در فاز ۲ احتمالاً DB. چگونه یک interface واحد بدهیم؟

#### Decision
✅ `BaseDataSource` abstract در `app/infrastructure/data_sources/`. Implementations: `ExcelDataSource`, آینده: `CcxtDataSource`.

#### Rationale
- وقتی منبع داده تغییر کند، فقط implementation عوض می‌شود نه caller
- Tests می‌توانند Mock DataSource بسازند

---

### Decision #4 — Layered Architecture

**ثبت‌شده در:** چت ۱  
**Status:** ✅ Accepted

#### Context
سازماندهی Backend.

#### Decision
✅ ۴ لایه: **routes → services → repositories → models**.

#### Rationale
- routes: HTTP concerns فقط
- services: business logic
- repositories: DB access فقط
- models: schema تعریف

---

### Decision #5 — Pydantic v2 Settings

**ثبت‌شده در:** چت ۲  
**Status:** ✅ Accepted

#### Decision
✅ استفاده از `pydantic_settings.BaseSettings` برای خواندن `.env`.

#### Rationale
- type validation
- env‌های اشتباه را در startup catch می‌کند نه runtime
- سازگار با FastAPI

---

### Decision #6 — Async SQLAlchemy

**ثبت‌شده در:** چت ۳  
**Status:** ✅ Accepted

#### Decision
✅ SQLAlchemy async (`AsyncSession`).

#### Rationale
- Match با FastAPI async
- در آینده با PostgreSQL بهتر scale می‌کند
- در فاز ۰ overhead کمی دارد ولی future-proof است

---

### Decision #7 — SQLite برای فاز ۰

**ثبت‌شده در:** چت ۳  
**Status:** ✅ Accepted (با احتمال upgrade)

#### Decision
✅ SQLite در فاز ۰. PostgreSQL در فاز ۲+.

#### Rationale
- Zero config برای dev
- یک فایل واحد (راحت backup/share)
- async support موجود

#### Consequences
- 👎 محدودیت concurrent writes — در فاز ۲ با کاربران زیاد نیاز به PG

---

### Decision #8 — Alembic برای Migrations

**ثبت‌شده در:** چت ۳  
**Status:** ✅ Accepted

#### Decision
✅ Alembic (نه Tortoise migrations، نه manual SQL).

#### Rationale
- استاندارد SQLAlchemy
- async support

---

### Decision #9 — Loguru به جای logging stdlib

**ثبت‌شده در:** چت ۲  
**Status:** ✅ Accepted

#### Decision
✅ Loguru.

#### Rationale
- syntax ساده‌تر
- color خودکار
- rotation راحت

---

### Decision #10 — Exception Hierarchy

**ثبت‌شده در:** چت ۲  
**Status:** ✅ Accepted

#### Decision
✅ `BaseException → DomainException → SpecificException`. Handlers سراسری در main.

---

### Decision #11 — JWT (نه session cookie)

**ثبت‌شده در:** چت ۴  
**Status:** ✅ Accepted

#### Decision
✅ JWT با expire ۷ روز.

#### Rationale
- API stateless
- frontend می‌تواند مستقل از backend deploy شود
- mobile app آینده هم همین endpoint را استفاده کند

#### Consequences
- 👎 invalidation سخت (نیاز به blacklist در آینده)

---

### Decision #12 — localStorage برای Token

**ثبت‌شده در:** چت ۴  
**Status:** ✅ Accepted (با ملاحظه)

#### Decision
✅ token در `localStorage`.

#### Rationale
- ساده‌تر از httpOnly cookie
- برای فاز ۰ ریسک XSS قابل قبول

#### Consequences
- 👎 XSS attack می‌تواند token را بدزدد
- در آینده ممکن است به httpOnly cookie migrate شود (Decision آینده)

---

### Decision #13 — bcrypt مستقیم (نه passlib)

**ثبت‌شده در:** چت ۴  
**Status:** ✅ Accepted

#### Context
passlib در Windows مشکل داشت.

#### Decision
✅ `bcrypt` package به‌صورت مستقیم.

#### Rationale
- یک کتابخانه کمتر
- مشکل compat با Windows حل شد

---

### Decision #14 — Node.js 22 LTS

**ثبت‌شده در:** چت ۱  
**Status:** ✅ Accepted (Pinned)

#### Decision
✅ Node.js **22.x LTS** برای frontend.

#### Rationale
- LTS = پایداری
- ESM support کامل
- Vite 7+ نیاز دارد

---

### Decision #15 — Vite (نه Webpack/Next.js)

**ثبت‌شده در:** چت ۱  
**Status:** ✅ Accepted

#### Decision
✅ Vite.

#### Rationale
- HMR فوق‌العاده سریع
- bundle size کوچک
- config ساده
- Next.js overkill برای SPA

---

### Decision #20-#29 — Frontend Architecture (تجمیعی)

این تصمیمات در چت‌های ۴ و ۵ گرفته شدند:

| # | تصمیم | دلیل |
|---|---|---|
| #20 | react-router-dom (نه TanStack Router) | پایداری، ecosystem |
| #21 | axios (نه fetch) | interceptors، error handling |
| #22 | zustand (نه Redux/Jotai) | سادگی + persist plugin |
| #23 | lightweight-charts (نه ApexCharts/Plotly) | سبک، حرفه‌ای |
| #24 | Vazirmatn فونت | RTL/فارسی |
| #25 | Inline styles + CSS variables (نه Tailwind/styled-components) | با تم engine سازگار |
| #26 | ProtectedRoute pattern | RBAC ساده |
| #27 | Functional components only (نه class) | hooks-first |
| #28 | `.jsx` (نه `.tsx`) در فاز ۰ | سادگی، TS بعداً |
| #29 | localStorage برای theme/preferences | persist بدون backend |

---

### Decision #30-#48 — Theme & UI Design (تجمیعی)

این تصمیمات در چت‌های ۵ و ۶ گرفته شدند:

| # | تصمیم | دلیل |
|---|---|---|
| #30 | ۵ تم پیش‌فرض | پوشش سلیقه‌های متنوع |
| #31 | CSS variables (نه prop-based) | کارایی + سازگاری |
| #32 | ThemeProvider به‌جای Context API | سادگی |
| #33 | تم پیش‌فرض: binance-dark | شناخت قبلی کاربر |
| #34 | Variant Indicator Pattern | یکپارچگی بصری |
| #35 | Interactive States الزامی | UX حرفه‌ای |
| #36 | Toast top-end (RTL = راست-بالا) | استاندارد + RTL |
| #37 | ConfirmDialog مرکز صفحه | focus کاربر |
| #38 | SkeletonBlock shimmer (نه dots/spinner) | حس "بارگذاری در حال انجام" |
| #39 | preferencesStore جدا از themeStore | concerns متفاوت |
| #40 | `Intl` built-in (نه moment-jalaali) | bundle size + standard |
| #41 | تقویم پیش‌فرض: میلادی | تصمیم Session 1 |
| #42 | ۴ فرمت میلادی (ISO/US/EU/Long) | انعطاف کاربر |
| #43 | rem به جای px برای fontSize | scaling سراسری |
| #44 | timeFormatter (نه dateFormat) در lightweight-charts | API نسخه ۴.x |
| #45 | همه CSS variables بدون hex hardcoded | maintainability |
| #46 | فونت Vazirmatn از CDN | تجربه فارسی |
| #47 | shimmer شفاف هنگام reduced-motion | accessibility |
| #48 | reset به ۲ store (theme + preferences) | یکپارچگی |

---

### Decision #50 — Governance Infrastructure

**ثبت‌شده در:** چت ۶  
**تاریخ:** 2026-05-17  
**Status:** ✅ Accepted ⭐  
**دسته:** Process & Governance

#### Context
پروژه به نقطه‌ای رسیده که اگر هر چت یک جزیره مستقل باشد، دانش گم می‌شود. کاربر متوجه شد که Claude در شروع چت ابتدا "همه‌جانبه فکر نمی‌کند".

#### Options Considered
1. **Status Quo:** فقط سند جامع + SESSION_STATUS. ⚠️ تجربه نشان داد ناکافی است.
2. **چند سند کوچک‌تر:** پراکنده، سخت پیدا کردن. ❌
3. **یک سند خیلی بزرگ:** قابلیت جستجو دارد ولی performance Claude افت می‌کند. ❌
4. **✅ ۱۲ سند تخصصی با cross-reference:** هر سند یک نقش، با مرز روشن.

#### Decision
✅ زیرساخت Governance ۱۲ سندی:
1. سند جامع (Constitution)
2. PROJECT_GOVERNANCE (راهبردی)
3. CLAUDE_CHECKLIST (operational)
4. CHAT_LOG (history)
5. TASK_BACKLOG (TODO/DONE)
6. DECISIONS_LOG (این سند — ADR)
7. GLOSSARY
8. TROUBLESHOOTING
9. STYLE_GUIDE
10. REUSABLE_SKELETON
11. ONBOARDING_GUIDE
12. README + CHANGELOG + SESSION_STATUS + PROJECT_CONTEXT (پشتیبان)

#### Rationale
- هر سند یک "تک مسئولیت" دارد (مثل اصل Single Responsibility در کد)
- جستجوپذیر (هر سند معمولاً < ۱۰۰۰ خط)
- handoff به برنامه‌نویس بعدی در ۱ روز
- Claude بعدی می‌تواند explicitly چک کند که "خواندم"

#### Consequences
- 👍 پروژه scalable برای چت‌های آینده
- 👍 reusable برای پروژه‌های بعدی
- 👎 سربار اولیه بزرگ (همین چت)
- 👎 نیاز به انضباط در به‌روزرسانی (هر چت)

#### Reference
- `PROJECT_GOVERNANCE.md` بخش ۲ (معماری اسناد)
- قوانین جدید #۲۳, #۲۴, #۲۵, #۲۶

---

### Decision #51 — Variant Indicator Pattern مجدداً تأیید

**ثبت‌شده در:** چت ۶  
**Status:** ✅ Accepted (تأیید مجدد در ConfirmDialog)

#### Decision
✅ ConfirmDialog همان الگو را رعایت کرد: کانتینر از `--color-card` + accent باریک ۴px در سمت start.

#### Rationale
ثبات بصری در تمام variant ها (Toast، Dialog، Badge آینده).

---

### Decision #52 — `Intl` به‌جای کتابخانه خارجی

**ثبت‌شده در:** چت ۶  
**Status:** ✅ Accepted

#### Context
نیاز به نمایش تاریخ شمسی و فرمت اعداد. گزینه‌ها:
- `moment-jalaali` (~۱۰۰KB)
- `dayjs` + plugin (~۲۰KB)
- `Intl` built-in (~۰KB)

#### Decision
✅ **`Intl.DateTimeFormat("fa-IR-u-ca-persian", ...)`** + **`Intl.NumberFormat`**.

#### Rationale
- bundle size 0
- standard W3C
- در همه browser های modern موجود
- نسخه‌بندی نیاز ندارد

#### Consequences
- 👍 سبک‌ترین راه‌حل
- 👎 ممکن است در browser های قدیمی غایب باشد (در پروژه ما target مدرن)

---

### Decision #53 — rem برای fontSize های inline

**ثبت‌شده در:** چت ۶  
**Status:** ✅ Accepted (الزامی)

#### Context
Bug #47 (Font scaling شکسته).

#### Decision
✅ همه `fontSize` در inline style ها باید **rem** باشند، نه px.

#### Implementation
- `html { font-size: var(--font-size-base) }` (مقدار 14px پیش‌فرض)
- در JSX: `fontSize: "1rem"` (= 14px در پیش‌فرض)
- baseline = 14px → جدول تبدیل در `32_phase0_polish.py`

#### Rationale
- اجازه می‌دهد ThemeProvider با تغییر `--font-size-base` سراسری scale کند

---

### Decision #54 — Path.as_uri() نه as_posix()

**ثبت‌شده در:** چت ۶  
**Status:** ✅ Accepted

#### Context
Bug #46 (ESM URL scheme در ویندوز).

#### Decision
✅ برای ESM dynamic import در Node از Python، از `Path.as_uri()` استفاده شود.

---

### Decision #55 — ErrorBoundary با defense-in-depth (root + per-route)

**ثبت‌شده در:** چت ۷  
**Status:** ✅ Accepted

#### Context
React 19 برای catch کردن render-time errors نیاز به class-component ErrorBoundary دارد. سؤال: یک مرز سراسری کافی است یا per-route بهتر است؟

#### گزینه‌ها
- **A** فقط مرز سراسری (root) — ساده‌تر، یک خطا کل اپ را به fallback می‌برد.
- **B** فقط per-route — granular‌تر، ولی اگر خود `App.jsx` یا `ToastContainer` خراب شود، defense ندارد.
- **C** هر دو لایه (defense-in-depth) — کمی verbosity بیشتر، ولی مقاوم‌تر.

#### Decision
✅ **C: defense-in-depth** — `<ErrorBoundary label="root">` بیرونی + `<ErrorBoundary label="route:{name}">` به ازای هر صفحه.

#### Rationale
- خطای یک صفحه نباید navigation را از کار بیندازد — کاربر می‌تواند به مسیر دیگر برود.
- root ErrorBoundary به عنوان safety-net برای خطاهای App.jsx یا global components.
- prop `label` به logging کمک می‌کند (`[route:chart] ErrorBoundary caught:`).
- هزینه: ~۲۰ خط extra در `App.jsx`. منفعت: tolerance بسیار بالاتر.

#### پیامد
- ۵ ErrorBoundary در درخت اپ (۱ root + ۴ inner)
- props اختیاری `fallback: (info) => ReactNode` و `onReset: () => void` برای customization
- جزئیات فنی فقط در `import.meta.env.DEV` نمایش داده می‌شود (نه در production)

---

### Decision #56 — Vitest به‌جای Jest برای frontend tests

**ثبت‌شده در:** چت ۷  
**Status:** ✅ Accepted

#### Context
T2.02 نیاز به test runner برای frontend دارد. دو گزینه اصلی: Jest (sponsor: Meta) یا Vitest (همراه با Vite).

#### گزینه‌ها
- **A** Jest — پیش‌فرض صنعتی، حجم community بزرگ‌تر، ولی config پیچیده در Vite/ESM.
- **B** Vitest — هم‌خانواده با Vite، config از همان `vite.config.js`، ESM-native، API سازگار با Jest.

#### Decision
✅ **B: Vitest**

#### Rationale
- پروژه روی Vite 8 است؛ Vitest aliasها، plugins و env را خودکار share می‌کند.
- ESM-native — بدون نیاز به Babel transform برای `import.meta.env`.
- API سازگار با Jest — `describe`/`it`/`expect`/`vi.fn` همان نام‌ها هستند، migration trivial است.
- اجرای سریع‌تر (parallel + در حافظه).
- Coverage built-in با v8 provider — بدون نیاز به Istanbul.

#### پیامد
- devDeps جدید: `vitest ^3.0.0`، `@vitest/coverage-v8 ^3.0.0`، `jsdom ^25.0.1`، `@testing-library/{react ^16.1.0, jest-dom ^6.6.3, user-event ^14.5.2}`
- پیکربندی در `vite.config.js` field `test` (نه `vitest.config.js` جدا — کم‌تر duplication)
- ۴ npm script: `test`, `test:watch`, `test:coverage`, `test:ui`
- setup file: `src/test/setup.js` با import از `@testing-library/jest-dom/vitest`

---

### Decision #57 — ARCHITECTURE.md به‌جای multiple architecture/ files

**ثبت‌شده در:** چت ۷  
**Status:** ✅ Accepted

#### Context
T2.04 نیاز به سند معماری دارد. پوشه `docs/architecture/` خالی از قبل وجود داشت — می‌توان چند فایل کوچک در آن قرار داد یا یک فایل بزرگ.

#### گزینه‌ها
- **A** چند فایل (مثلاً `architecture/backend.md`, `architecture/frontend.md`, `architecture/data_flow.md`) — تفکیک منطقی، ولی navigation سخت‌تر.
- **B** یک فایل `docs/ARCHITECTURE.md` — یک نقطه‌ی reference، scrollable، linkable.
- **C** بخش جدید در سند جامع — همخوان با constitution، ولی سند جامع را بزرگ‌تر می‌کند.

#### Decision
✅ **B: یک فایل `docs/ARCHITECTURE.md`**

#### Rationale
- در onboarding، یک فایل قابل‌خواندن از ابتدا تا انتها بهتر از چند فایل پراکنده است.
- لینک از `PROJECT_CONTEXT.md`، `README.md` و سند جامع به یک URL آسان‌تر است.
- محتوای فعلی (~۲۵۰ خط) برای یک فایل مناسب است؛ اگر در آینده > ۶۰۰ خط شد، می‌توان split کرد.
- فاصله concern: سند جامع = constitution (immutable rules)؛ ARCHITECTURE.md = نمای high-level فنی (mutable، با پروژه تغییر می‌کند).

#### پیامد
- ۶ دیاگرام Mermaid در یک فایل (3 flowchart + 2 sequenceDiagram + 1 classDiagram)
- پوشه `docs/architecture/` خالی باقی ماند (آینده: می‌توان diagram-as-code جدا برای auto-render نگهداری کرد)
- اسکریپت `37_architecture_doc.py` به‌صورت idempotent سند را regenerate می‌کند — اگر معماری تغییر کند، فقط محتوا در اسکریپت ویرایش می‌شود

---

## آمار

| Status | تعداد |
|---|---|
| ✅ Accepted | ۵۷ |
| ⚠️ Superseded | ۰ |
| ❌ Rejected | ۰ |
| ⏳ Pending | ۰ |

---

## 📌 پایان DECISIONS_LOG

**نسخه:** v1.1 (2026-05-17 — پایان چت ۷)  
**تصمیمات ثبت‌شده:** ۵۷  
**Status کلی:** همه Accepted
