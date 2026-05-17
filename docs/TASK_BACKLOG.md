# 📋 TASK_BACKLOG — لیست کامل task های پروژه

> **هدف یک‌خطی:** فهرست همه task های پروژه با وضعیت آن‌ها، گروه‌بندی به Tier، با اولویت و تخمین.

> **محل قرارگیری:** `docs/TASK_BACKLOG.md`  
> **به‌روز توسط:** Claude در پایان هر چت (فاز ۳ مرحله ۳ چک‌لیست)  
> **نسخه این Backlog:** v1.0 (2026-05-17)

---

## 📑 فهرست

- [راهنمای استفاده](#راهنمای-استفاده)
- [Tier 1 — In Progress (این چت)](#tier-1--in-progress-این-چت)
- [Tier 2 — برای چت بعدی (quality-hardening)](#tier-2--برای-چت-بعدی-quality-hardening)
- [Tier 3 — موازی با فاز ۱+](#tier-3--موازی-با-فاز-۱)
- [Tier 4 — آینده دور (production-readiness)](#tier-4--آینده-دور-production-readiness)
- [DONE History](#done-history)

---

## راهنمای استفاده

### وضعیت‌ها

| Status | معنی |
|---|---|
| 📋 **TODO** | شروع نشده |
| 🚧 **IN-PROGRESS** | در حال انجام در این چت |
| ⏸️ **BLOCKED** | منتظر prerequisite |
| ✅ **DONE** | تمام شده + در DONE History منتقل شد |
| 🔄 **REVIEW** | نیاز به بازبینی کاربر |
| ❌ **CANCELLED** | لغو شد (با دلیل) |

### اولویت

| اولویت | معنی |
|---|---|
| 🔴 **CRITICAL** | تا تکمیل پروژه باید انجام شود |
| 🟠 **HIGH** | برای کیفیت حرفه‌ای لازم |
| 🟡 **MEDIUM** | بهبود قابل توجه |
| 🟢 **LOW** | nice-to-have |

### تخمین تلاش

- **XS:** < 1 ساعت
- **S:** 1-3 ساعت
- **M:** 0.5-1 روز
- **L:** 1-2 روز
- **XL:** > 2 روز

---

## Tier 1 — In Progress (این چت)

> **این چت:** `TRADING-phase0-part05-ui-polish-and-governance` (نام نهایی در پایان چت)  
> **Tier 1 = اسناد بنیادی + اصلاحات این چت**

| ID | Task | Status | اولویت | تلاش | Notes |
|---|---|---|---|---|---|
| T1.01 | PROJECT_GOVERNANCE.md ساخت | ✅ DONE | 🔴 | M | قلب سیستم |
| T1.02 | CLAUDE_CHECKLIST.md ساخت | ✅ DONE | 🔴 | M | چک‌لیست explicit |
| T1.03 | TASK_BACKLOG.md ساخت | 🚧 IN-PROGRESS | 🔴 | S | این سند |
| T1.04 | CHAT_LOG.md بازسازی ۶ چت | 📋 TODO | 🔴 | M | پیام بعدی |
| T1.05 | GLOSSARY.md ساخت | 📋 TODO | 🟠 | S | پیام بعدی |
| T1.06 | TROUBLESHOOTING.md ساخت | 📋 TODO | 🟠 | M | از Bug list سند جامع |
| T1.07 | DECISIONS_LOG.md ساخت | 📋 TODO | 🟠 | M | از Decisions سند جامع |
| T1.08 | REUSABLE_SKELETON.md ساخت | 📋 TODO | 🟠 | M | پیام ۳ |
| T1.09 | ONBOARDING_GUIDE.md ساخت | 📋 TODO | 🟠 | M | روز اول برنامه‌نویس |
| T1.10 | STYLE_GUIDE.md ساخت | 📋 TODO | 🟡 | S | code style + patterns |
| T1.11 | README.md بازنویسی | 📋 TODO | 🟠 | S | صفحه اول مخزن |
| T1.12 | CHANGELOG.md به‌روز (از v0.1.1) | 📋 TODO | 🔴 | M | تاریخ کامل نسخه‌ها |
| T1.13 | سند جامع v2.7 — بخش‌های جدید | 📋 TODO | 🔴 | XL | بخش ۱۶، ۱۷ + قوانین + Bug #46-49 |
| T1.14 | SESSION_STATUS.md به‌روز | 📋 TODO | 🔴 | XS | پایان چت |
| T1.15 | PROJECT_CONTEXT.md به‌روز | 📋 TODO | 🔴 | XS | پایان چت |
| T1.16 | zip نهایی این چت | 📋 TODO | 🔴 | S | پایان چت |

### Bug Fix ها انجام‌شده در این چت

- ✅ Bug #46: `Path.as_posix()` ESM URL در ویندوز
- ✅ Bug #47: Font Size scaling (px → rem)
- ✅ Bug #48: lightweight-charts `dateFormat` → `timeFormatter`
- ✅ Bug #49: HomePage `1714 کندل` بدون formatNumber

### Feature ها انجام‌شده در این چت

- ✅ SkeletonBlock کامپوننت (۸.۳)
- ✅ ConfirmDialog با Variant Indicator Pattern (۸.۳)
- ✅ Settings Page با ۳ بخش (۸.۴)
- ✅ ThemeCard preview (۸.۴)
- ✅ FontSizeControl با ۴ preset (۸.۴)
- ✅ formatNumber + formatDate utilities (۸.۵)
- ✅ preferencesStore با calendar + gregorianFormat (۸.۵)
- ✅ CalendarToggle با انتخاب فرمت میلادی (۸.۵ + اصلاحیه)

---

## Tier 2 — Quality Hardening (در حال انجام — ۴/۹ DONE)

> **چت ۷ بسته شد:** `TRADING-phase0-part06-quality-hardening` — T2.01/T2.02/T2.03/T2.04  
> **چت بعدی پیشنهادی:** `TRADING-phase0-part07-quality-hardening-continued` (T2.05-T2.09)  
> **Tier 2 = ارتقاء کیفیت حرفه‌ای**

| ID | Task | Status | اولویت | تلاش | Prerequisites |
|---|---|---|---|---|---|
| T2.01 | Error Boundaries در React | ✅ DONE | 🟠 | M | چت ۷ — `35_error_boundaries.py` |
| T2.02 | Frontend tests (vitest setup + smoke tests) | ✅ DONE | 🟠 | L | چت ۷ — `36_vitest_setup.py` |
| T2.03 | بررسی `.env.example` و تکمیل اگر ناقص | ✅ DONE | 🟠 | XS | چت ۷ — `34_env_examples_audit.py` |
| T2.04 | ARCHITECTURE.md ساخت (با دیاگرام layered) | ✅ DONE | 🟠 | M | چت ۷ — `37_architecture_doc.py` |
| T2.05 | Git workflow audit (آیا commit history واقعی هست؟) | 📋 TODO | 🟠 | S | - |
| T2.06 | Pre-commit hooks (husky + lint-staged) | 📋 TODO | 🟡 | M | - |
| T2.07 | Anti-pattern catalog (نمونه concrete از A1-A10) | 📋 TODO | 🟡 | M | STYLE_GUIDE |
| T2.08 | Backend test coverage گزارش | 📋 TODO | 🟡 | M | - |
| T2.09 | API_DOCS.md (markdown alternative به Swagger) | 📋 TODO | 🟡 | M | - |

### Prerequisites برای Tier 2

- ✅ همه اسناد Tier 1 آماده
- ✅ کاربر backend و frontend را تأیید کرده

---

## Tier 3 — موازی با فاز ۱+

> **Tier 3 = بهبودهای بزرگ‌تر، می‌تواند به فاز خاصی attach شود**

### بهبود Performance

| ID | Task | Status | اولویت | تلاش |
|---|---|---|---|---|
| T3.01 | Code splitting (React.lazy برای routes) | 📋 TODO | 🟡 | S |
| T3.02 | Image optimization (hero.png) | 📋 TODO | 🟢 | XS |
| T3.03 | Bundle analysis (vite-bundle-visualizer) | 📋 TODO | 🟡 | S |
| T3.04 | API response caching (frontend با SWR یا TanStack Query) | 📋 TODO | 🟡 | M |
| T3.05 | Database indexes review | 📋 TODO | 🟡 | M |

### Type Safety

| ID | Task | Status | اولویت | تلاش |
|---|---|---|---|---|
| T3.06 | TypeScript migration (gradual با allowJs) | 📋 TODO | 🟡 | XL |
| T3.07 | API client types (از OpenAPI schema) | 📋 TODO | 🟡 | M |
| T3.08 | Runtime validation با Zod | 📋 TODO | 🟡 | M |

### UX بهبود

| ID | Task | Status | اولویت | تلاش |
|---|---|---|---|---|
| T3.09 | Network status indicator (offline detection) | 📋 TODO | 🟡 | S |
| T3.10 | Custom 404 page | 📋 TODO | 🟢 | S |
| T3.11 | Toast spam prevention (debounce + collapse) | 📋 TODO | 🟢 | S |
| T3.12 | Keyboard shortcuts سراسری (Cmd+K، g+s، ...) | 📋 TODO | 🟡 | M |
| T3.13 | Loading spinner سراسری (page transitions) | 📋 TODO | 🟢 | S |

### i18n (انگلیسی)

| ID | Task | Status | اولویت | تلاش |
|---|---|---|---|---|
| T3.14 | react-i18next setup | 📋 TODO | 🟢 | M |
| T3.15 | استخراج متن‌های فارسی به فایل locale | 📋 TODO | 🟢 | L |
| T3.16 | RTL/LTR switching | 📋 TODO | 🟢 | M |
| T3.17 | Number locale switching (fa-IR vs en-US) | 📋 TODO | 🟢 | S |

### Backend بهبود

| ID | Task | Status | اولویت | تلاش |
|---|---|---|---|---|
| T3.18 | Rate limiting middleware | 📋 TODO | 🟡 | S |
| T3.19 | Request/Response logging middleware | 📋 TODO | 🟡 | S |
| T3.20 | Health check جامع‌تر (DB، DiskSpace، ...) | 📋 TODO | 🟡 | XS |

---

## Tier 4 — آینده دور (production-readiness)

> **Tier 4 = آماده‌سازی برای deploy production**

### CI/CD

| ID | Task | Status | اولویت | تلاش |
|---|---|---|---|---|
| T4.01 | GitHub Actions workflow (test + build) | 📋 TODO | 🟡 | M |
| T4.02 | Docker containerization (backend + frontend) | 📋 TODO | 🟡 | L |
| T4.03 | Docker Compose برای dev environment | 📋 TODO | 🟢 | M |

### Deployment

| ID | Task | Status | اولویت | تلاش |
|---|---|---|---|---|
| T4.04 | Production deploy guide (DigitalOcean/Hetzner) | 📋 TODO | 🟡 | M |
| T4.05 | Nginx config + SSL (Let's Encrypt) | 📋 TODO | 🟡 | M |
| T4.06 | Process manager (systemd یا pm2) | 📋 TODO | 🟡 | S |
| T4.07 | Backup automation (trading.db daily) | 📋 TODO | 🟠 | S |
| T4.08 | Monitoring (Sentry برای frontend، Loguru برای backend) | 📋 TODO | 🟡 | M |

### Security

| ID | Task | Status | اولویت | تلاش |
|---|---|---|---|---|
| T4.09 | Security audit (npm audit + safety) | 📋 TODO | 🟠 | S |
| T4.10 | HTTPS enforcement | 📋 TODO | 🟠 | XS |
| T4.11 | CSP headers | 📋 TODO | 🟡 | S |
| T4.12 | CORS سختگیرانه‌تر برای production | 📋 TODO | 🟠 | XS |

### PWA / Mobile

| ID | Task | Status | اولویت | تلاش |
|---|---|---|---|---|
| T4.13 | PWA manifest | 📋 TODO | 🟢 | S |
| T4.14 | Service worker (offline access) | 📋 TODO | 🟢 | L |
| T4.15 | Mobile responsive audit | 📋 TODO | 🟡 | M |

### Migration & Data

| ID | Task | Status | اولویت | تلاش |
|---|---|---|---|---|
| T4.16 | Migration rollback testing | 📋 TODO | 🟠 | S |
| T4.17 | DB backup/restore scripts | 📋 TODO | 🟠 | M |
| T4.18 | Data archiving strategy (برای OHLCV قدیمی) | 📋 TODO | 🟢 | M |

---

## DONE History

این بخش **پیوسته** افزوده می‌شود — به ترتیب تاریخ تکمیل.

### چت ۱ (Session 1) — 2026-05-13

| Task | Status |
|---|---|
| ساختار پوشه پروژه | ✅ DONE |
| اسناد پایه (README، CHANGELOG، SESSION_STATUS، PROJECT_CONTEXT) | ✅ DONE |
| .gitignore حرفه‌ای | ✅ DONE |
| DataSource Abstraction در infrastructure/ | ✅ DONE |
| تصمیم: Node.js 22 LTS | ✅ DONE |
| قانون قفل‌شده #۱۴ | ✅ DONE |

### چت ۲ (Session 2) — 2026-05-14

| Task | Status |
|---|---|
| Backend پایه (venv + requirements + main.py + .env + config + health) | ✅ DONE |
| Core Layer (Logger + Exceptions + Handlers + Response) | ✅ DONE |
| Fix رنگ ANSI و emoji در Windows CMD | ✅ DONE |
| ثبت ۱۳ تصمیم معماری | ✅ DONE |

### چت ۳ (Session 3) — 2026-05-15 (تخمینی)

| Task | Status |
|---|---|
| Database + Models + Repositories | ✅ DONE |
| Alembic + اولین Migration | ✅ DONE |
| Seeding (admin + Excel exchange) | ✅ DONE |
| DataSource + Excel Reader | ✅ DONE |

### چت ۴ (Session 4 - part04) — 2026-05-16 (تخمینی)

| Task | Status |
|---|---|
| Auth + JWT + OAuth2 + bcrypt مستقیم | ✅ DONE |
| اولین API endpoint (`GET /ohlcv/{symbol_id}`) | ✅ DONE |
| Frontend scaffold (Vite + dependencies) | ✅ DONE |
| Login واقعی + JWT در localStorage | ✅ DONE |
| ChartPage با lightweight-charts | ✅ DONE |

### چت ۵ (Session 5 - part04 با اصلاح نام) — 2026-05-17 (theme-engine)

| Task | Status |
|---|---|
| Theme Engine Foundation (۵ تم) | ✅ DONE |
| Bug #43: Binance Color Accuracy | ✅ DONE |
| Bug #44: Interactive States | ✅ DONE |
| Toast Notifications | ✅ DONE |
| Bug #45: Toast Theme Consistency (Variant Pattern) | ✅ DONE |
| اسکریپت 00b_post_unzip_setup.py | ✅ DONE |
| قانون #۲۱ و #۲۲ | ✅ DONE |

### چت ۶ (Session 6 - part05) — 2026-05-17 (ui-polish + governance)

| Task | Status |
|---|---|
| ۸.۳ Skeleton + ConfirmDialog | ✅ DONE |
| ۸.۴ Settings Page | ✅ DONE |
| ۸.۵ Numeric + Persian Calendar | ✅ DONE |
| Bug #46: ESM URL در ویندوز (Path.as_uri) | ✅ DONE |
| Bug #47: Font Size scaling (px → rem) | ✅ DONE |
| Bug #48: lightweight-charts timeFormatter | ✅ DONE |
| Bug #49: HomePage formatNumber | ✅ DONE |
| Feature: انتخاب فرمت میلادی | ✅ DONE |
| Tier 1 (Governance Infrastructure) | ✅ DONE |

### چت ۷ (Session 7 - part06) — 2026-05-17 (quality-hardening)

| Task | Status |
|---|---|
| T2.03 — `.env.example` audit (backend + frontend) | ✅ DONE |
| T2.01 — Error Boundaries (defense-in-depth: ۱ root + ۴ per-route) | ✅ DONE |
| T2.02 — vitest setup + ۵ smoke test (numberFormat، dateFormat، confirmStore، ErrorBoundary، LoginPage) | ✅ DONE |
| T2.04 — ARCHITECTURE.md با ۶ دیاگرام Mermaid | ✅ DONE |

---

## آمار

| سطح | تعداد Tasks | DONE | باقیمانده |
|---|---|---|---|
| Tier 1 | 16 | 16 | 0 (همگی در چت ۶ تکمیل شد) |
| Tier 2 | 9 | 4 | 5 (T2.05-T2.09) |
| Tier 3 | 20 | 0 | 20 |
| Tier 4 | 18 | 0 | 18 |
| **مجموع** | **63** | **20** | **43** |

> 💡 این آمار **حدوداً** است و در طول پروژه تغییر می‌کند. هدف یک "نقشه راه زنده" است، نه contract.

---

## 📌 پایان TASK_BACKLOG

**نسخه:** v1.1 (2026-05-17 — پایان چت ۷)  
**به‌روز شده در:** پایان چت `TRADING-phase0-part06-quality-hardening`  
**به‌روز توسط:** Claude (طبق قانون #۲۳ و CLAUDE_CHECKLIST فاز ۳ مرحله ۳)
