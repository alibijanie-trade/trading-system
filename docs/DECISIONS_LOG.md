# 🏛️ DECISIONS_LOG — تاریخچه تصمیمات معماری

> **هدف یک‌خطی:** ثبت "چرا"ی هر تصمیم معماری در پروژه — برای جلوگیری از بازکردن همان سؤالات در آینده.

> **محل قرارگیری:** `docs/DECISIONS_LOG.md`  
> **به‌روز توسط:** Claude در پایان چت اگر تصمیم جدید گرفته شد (CLAUDE_CHECKLIST فاز ۳ مرحله ۴)  
> **نسخه:** v1.4 (2026-05-30)

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
| **Process & Governance** | #50-#57, #67 |
| **Quality Hardening (Tier 2)** | #55, #56, #57 |
| **Pre-commit & Git** | #58, #59, #60 |
| **CCXT & Architecture (Phase 1)** | #61, #62, #63, #64 |
| **Strategic (End of Chat 10)** | #65, #66 |
| **Reserved (غیر-ثبت‌شده)** | #16, #17, #18, #19, #49 — برای renumbering آینده یا backfill تصمیمات تاریخی گم‌شده (درس M79) |

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

### Decision #58 — Pre-commit Hybrid Mode (critical اجباری + minor warning)

**ثبت‌شده در:** چت ۷ (Atomic Update v2.9) — backfilled در چت ۱۰  
**Status:** ✅ Accepted

#### Context
T2.06 نیاز به pre-commit hook دارد. دو گزینه: strict (همه چیز اجباری) vs lenient (فقط warning).

#### Decision
✅ **Hybrid Mode** — critical hooks (black, isort, ruff, trailing-whitespace) اجباری؛ minor (line length warnings) فقط warning.

#### Rationale
- strict باعث friction در commit های سریع می‌شود
- lenient کیفیت را تضمین نمی‌کند
- Hybrid: ضروریات اجباری، توصیه‌ها optional

---

### Decision #59 — `.gitattributes` به‌جای hook برای CRLF normalization

**ثبت‌شده در:** چت ۷ — backfilled در چت ۱۰  
**Status:** ✅ Accepted

#### Context
Windows-Linux interop باعث CRLF/LF conflicts می‌شود. Bug #51 cp1252 crash از همین مسیر آمد.

#### Decision
✅ استفاده از `.gitattributes` با `* text=auto eol=lf` به‌جای pre-commit hook.

#### Rationale
- .gitattributes در همه ابزارها (VS Code, git CLI, GitHub) اعمال می‌شود
- hook فقط در زمان commit عمل می‌کند
- جلوگیری از cp1252 fallback روی Windows

---

### Decision #60 — Pre-commit entry: `python wrapper.py` (cross-platform)

**ثبت‌شده در:** چت ۷ — backfilled در چت ۱۰  
**Status:** ✅ Accepted

#### Context
pre-commit hook ها روی Windows با shell scripts کار نمی‌کنند.

#### Decision
✅ هر custom hook با `python wrapper.py` (نه bash) فراخوانی شود.

#### Rationale
- cross-platform (Windows/Linux/macOS)
- venv activation در Python سازگارتر
- error handling consistent

---

### Decision #61 — Gradient Interface برای DataSource async extension

**ثبت‌شده در:** چت ۱۰ (G2 — Architecture Q&A)  
**Status:** ✅ Accepted

#### Context
DataSource(ABC) فعلی sync است. CCXTDataSource نیاز به async دارد. چطور بدون breaking change اضافه کنیم؟

#### گزینه‌ها
- **A** — تغییر `read_ohlcv` به async (breaking ExcelDataSource)
- **B** — کلاس جدید `AsyncDataSource` جدا (duplication)
- **C** — `read_ohlcv_async` اضافی با default impl `asyncio.to_thread(self.read_ohlcv, ...)` (gradient interface)

#### Decision
✅ **C — Gradient interface**

#### Rationale
- backwards compat کامل با ExcelDataSource (هیچ تغییری در sync code نیاز نیست)
- async-first در FastAPI handlers
- swap بین Excel و CCXT بدون درد در فاز ۵+ (تأیید در Decision #65)

#### پیامد
- `read_ohlcv` (sync) باقی می‌ماند برای backwards compat
- `read_ohlcv_async` با default `asyncio.to_thread(self.read_ohlcv, ...)`
- ExcelDataSource بدون تغییر کار می‌کند
- CCXTDataSource `read_ohlcv_async` را override می‌کند و `read_ohlcv` (sync wrapper) از `asyncio.run` استفاده می‌کند (با warning M69 درباره FastAPI handler)

---

### Decision #62 — Mock Strategy: AsyncMock در pytest fixtures

**ثبت‌شده در:** چت ۱۰ (G2)  
**Status:** ✅ Accepted

#### Context
تست CCXTDataSource بدون اتصال به Binance واقعی.

#### گزینه‌ها
- **A** — VCR.py (record/replay HTTP)
- **B** — Live testnet Binance
- **C** — AsyncMock در fixtures

#### Decision
✅ **C — AsyncMock**

#### Rationale
- سریع، deterministic، بدون شبکه
- کنترل کامل روی scenarios (BadSymbol، rate limit، …)
- exception signatures و schema fields در اولین تلاش match می‌شوند (تجربه چت ۱۰: ۵/۵ test pass)

---

### Decision #63 — WebSocket → Repository: asyncio.Queue واسطه

**ثبت‌شده در:** چت ۱۰ (G2)  
**Status:** ✅ Accepted (پیاده‌سازی موکول به فاز ۵+)

#### Context
وقتی WebSocket subscriber در فاز ۵ ساخته شود، چطور به DB write کند؟

#### گزینه‌ها
- **A** — Direct DB write از WS handler
- **B** — asyncio.Queue واسطه + consumer worker

#### Decision
✅ **B — asyncio.Queue**

#### Rationale
- decoupling از DB latency
- batch write برای performance
- multi-consumer در آینده (DB + Cache + WebSocket broadcast)

---

### Decision #64 — Rate Limiting: ccxt built-in `enableRateLimit=True`

**ثبت‌شده در:** چت ۱۰ (G2)  
**Status:** ✅ Accepted

#### Context
Binance API rate limits دارد. آیا custom token bucket بسازیم؟

#### Decision
✅ **ccxt built-in `enableRateLimit=True`**

#### Rationale
- ساده، کار می‌کند، YAGNI برای custom
- اگر در فاز ۵+ نیاز به throttling پیشرفته‌تر شد، می‌توان جایگزین کرد

---

### Decision #65 — موکول‌کردن اتصال زنده Binance/Telegram به فاز ۵+

**ثبت‌شده در:** چت ۱۰ (پایان چت — تصمیم استراتژیک)  
**Status:** ✅ Accepted

#### Context
در چت ۱۰، CCXTDataSource skeleton ساخته شد. آیا فاز ۲ روی اتصال زنده تمرکز کند یا روی اندیکاتورها؟

#### گزینه‌ها
- **A** — فاز ۲ = binance_client + binance_ws (ادامه اتصال زنده)
- **B** — فاز ۲ = اندیکاتورها با ExcelDataSource (اتصال زنده موکول به فاز ۵+)

#### Decision
✅ **B — موکول‌کردن اتصال زنده تا فاز ۵+**

#### Rationale
- gradient interface (Decision #61) swap را بدون درد می‌کند
- ExcelDataSource دارای ۱۷۱۴ کندل BTC/USDT 1d است — کافی برای backtest
- backtest با Excel data static reproducibility بالاتری دارد (بدون look-ahead bias)
- value-delivery سریع‌تر: اندیکاتورها روی نمودار قابل-نمایش بدون نیاز به live
- CCXTDataSource skeleton روی Shelf می‌ماند برای فاز ۵+

#### پیامد
- فاز ۲ (اندیکاتورها)، ۳ (استراتژی)، ۴ (بک‌تست) با ExcelDataSource
- فاز ۵+ شروع: binance_client.py، binance_ws.py، integration test واقعی
- در چت ۱۱ scope به Discovery / Master Architecture تغییر یافت

---

### Decision #66 — Push اجباری در پایان هر چت (GitHub-only backup)

**ثبت‌شده در:** چت ۱۰ (پایان چت — پس از بحث با کاربر)  
**Status:** ✅ Accepted

#### Context
نیاز به استراتژی backup در پایان هر چت.

#### گزینه‌ها
- **A** — local zip + GitHub (دو لایه)
- **B** — فقط GitHub (یک لایه، استاندارد صنعتی)

#### Decision
✅ **B — GitHub-only با اسکریپت optional برای کاربرانی که DB/.env هم می‌خواهند**

#### Rationale
- سادگی workflow بهتر از لایه‌بندی پیچیده
- GitHub خودش backup primary است — کاربر می‌تواند با git clone backup داشته باشد
- .env هرگز در git نباشد (امنیتی) — فقط .env.example
- DB در .gitignore می‌ماند (*.db)
- Recovery time در disaster: ~۴۵-۶۰ دقیقه (ماشین آماده) — قابل قبول
- اسکریپت scripts/63_backup_project.py optional برای کاربری که می‌خواهد backup شامل DB+.env داشته باشد

#### قانون مرتبط
قانون #۶۶ (پیشنهادی — برای ادغام در v2.12): در پایان هر چت، Claude باید مطمئن شود همه تغییرات commit و push شده‌اند.

#### پیامد
- پروتکل پایان چت: git add . → git commit → git push origin main
- پس از هر commit بزرگ، یک HEAD backfill commit جداگانه (به‌خاطر M71 self-reference paradox)
- در PENDING Z2.9 ثبت شد برای ادغام در v2.12

---

### Decision #67 — Trust & Anti-Sycophancy Rules (#۷۸-۸۵) adoption

**ثبت‌شده در:** چت part11 (`TRADING-phase1-part11-trust-rules-and-remediation`)
**تاریخ:** 2026-05-30
**Status:** ✅ Accepted
**دسته:** Process & Governance

#### Context
در part10 audit session، الگوی «audit over-promise + self-imposed scope narrowing + optimistic reporting» کشف شد (Claude ادعای «deep-scan تقریباً کامل» با ~۳۵٪ coverage واقعی داد). نیاز به قواعد ساختاری anti-sycophancy.

#### Options Considered
1. **Option A — ۸ قانون Locked جدید (#۷۸-۸۵) + M103** ✅ — ساختاری، self-enforcing per #۸۵
2. **Option B — یک درس (M103) بدون قانون** — ضعیف‌تر؛ M87 نشان داد «درس بدون positive constraint» کافی نیست
3. **Option C — Custom Instructions only** — خارج از constitution، traceable نیست

#### Decision
✅ **Option A** — ۸ Trust Rule (#۷۸-۸۵) در 01_rules.md + M103 در 02_lessons.md + v2.15 bump.

#### Rationale
- positive constraint > negative reminder (الگوی موفق #۴۶/#۶۷)
- Self-Activation Lock (#۸۵) خودکارسازی per-turn را تضمین می‌کند (per F36)
- Genesis traceable به part10

#### Consequences
- 👍 honesty/anti-sycophancy ساختاری، self-enforcing
- 👎 سربار per-turn self-check (پذیرفته‌شده)

#### Reference
- `01_rules.md` بخش «شرح کامل قوانین Trust & Anti-Sycophancy (#۷۸-۸۵)»
- `02_lessons.md` M103
- Review #۰۰۵ (`docs/reviews/2026-05-30-trust-rules-codification.md`)

---

## آمار

| Status | تعداد |
|---|---|
| ✅ Accepted (Recorded) | ۶۲ |
| ⬜ Reserved (غیر-ثبت‌شده) | ۵ (#۱۶-۱۹، #۴۹) |
| ⚠️ Superseded | ۰ |
| ❌ Rejected | ۰ |
| ⏳ Pending | ۰ |

**Max Decision ID:** ۶۷  
**Total Recorded:** ۶۲  
**Reserved Slots:** ۵ (در دسته‌بندی موضوعی بالا مستند شد)

**تصمیم برای Reserved IDs (پایان چت ۱۰ round 2):**  
دسته "ج" از Z2.19 (PENDING) → backfill تصمیمات واقعی تاریخی در v2.12 اگر در CHAT_LOG چت‌های ۲-۵ پیدا شدند. در غیر این صورت، "Reserved" دائمی شوند و فقط برای تست‌پذیری تاریخی نگه داشته می‌شوند.

---

## 📌 پایان DECISIONS_LOG

**نسخه:** v1.4 (2026-05-30 — part13/Phase 3 F-A: bump نسخه برای بازتاب Decision #۶۷ (Trust Rules #۷۸-۸۵، Review #۰۰۵) + sync نسخهٔ header از v1.0 به v1.4)  
**تصمیمات ثبت‌شده:** ۶۲ (Max ID ۶۷ — ۵ اسلات Reserved)  
**Status کلی:** همه Accepted
