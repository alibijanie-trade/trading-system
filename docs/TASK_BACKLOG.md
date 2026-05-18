# 📋 TASK_BACKLOG — لیست کامل task های پروژه

> **هدف یک‌خطی:** فهرست همه task های پروژه با وضعیت آن‌ها، گروه‌بندی به Tier، با اولویت و تخمین.

> **محل قرارگیری:** `docs/TASK_BACKLOG.md`  
> **به‌روز توسط:** Claude در پایان هر چت (فاز ۳ مرحله ۳ چک‌لیست)  
> **نسخه این Backlog:** v1.2 (2026-05-17 — پایان چت ۶)

---

## 📑 فهرست

- [راهنمای استفاده](#راهنمای-استفاده)
- [Tier 1 — DONE (در چت ۵)](#tier-1)
- [Tier 2 — Quality Hardening (در حال انجام — ۴/۹)](#tier-2--quality-hardening)
- [Tier 3 — موازی با فاز ۱+](#tier-3)
- [Tier 4 — آینده دور](#tier-4)
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

## Tier 1

> **Tier 1 = اسناد بنیادی Governance**  
> **وضعیت:** ✅ ۱۶/۱۶ DONE — در چت ۵ تکمیل شد

| ID | Task | Status |
|---|---|---|
| T1.01-T1.16 | همه اسناد Governance Infrastructure | ✅ DONE |

جزئیات: `docs/CHAT_LOG.md` بخش چت ۵.

---

## Tier 2 — Quality Hardening

> **این Tier در چت ۶ شروع شد و در چت ۶ به‌صورت جزئی (۴/۹) تکمیل شد.**  
> **چت بعدی پیشنهادی:** `TRADING-phase0-part07-quality-hardening-continued`

| ID | Task | Status | اولویت | تلاش | چت |
|---|---|---|---|---|---|
| T2.01 | Error Boundaries در React | ✅ DONE | 🟠 | M | چت ۶ — verified runtime ✅ |
| T2.02 | Frontend tests (vitest setup + smoke tests) | ✅ DONE | 🟠 | L | چت ۶ — **۳۰/۳۰ pass** ✅ |
| T2.03 | بررسی `.env.example` و تکمیل اگر ناقص | ✅ DONE | 🟠 | XS | چت ۶ |
| T2.04 | ARCHITECTURE.md ساخت (با دیاگرام layered) | ✅ DONE | 🟠 | M | چت ۶ |
| T2.05 | Git workflow audit + GIT_WORKFLOW.md | 📋 TODO | 🟠 | S | چت ۷ |
| T2.06 | Pre-commit hooks (pre-commit framework + ruff + eslint) | 📋 TODO | 🟡 | M | چت ۷ |
| T2.07 | Anti-pattern catalog (نمونه concrete از A1-A10) | 📋 TODO | 🟡 | M | چت ۷ |
| T2.08 | Backend pytest + coverage + pyproject.toml | 📋 TODO | 🟡 | M | چت ۷ |
| T2.09 | API_DOCS.md (markdown alternative به Swagger) | 📋 TODO | 🟡 | M | چت ۷ |

### Tasks اضافی کشف‌شده در چت ۶

| ID | Task | Status | شرح |
|---|---|---|---|
| T2.10 | رفع ریشه‌ای Bug #50 (import React) | 📋 TODO | علت‌یابی چرا React 19 + vitest نیاز به import React صریح دارد |
| T2.11 | ادغام قوانین #۲۷-#۳۲ در سند جامع | 📋 TODO | atomic update لازم در ابتدای چت ۷ |

---

## Tier 3 — موازی با فاز ۱+

> **Tier 3 = بهبودهای بزرگ‌تر، می‌تواند به فاز خاصی attach شود**

(جزئیات در نسخه قبلی این سند — ۲۰ task)

---

## Tier 4 — آینده دور (production-readiness)

(جزئیات در نسخه قبلی این سند — ۱۸ task)

---

## DONE History

### چت ۱ (Session 1) — 2026-05-13

| Task | Status |
|---|---|
| ساختار اولیه پروژه (Phase 0 - Step 1) | ✅ DONE |
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

### چت ۳ (Session 3) — 2026-05-15

| Task | Status |
|---|---|
| Database + Models + Repositories | ✅ DONE |
| Alembic + اولین Migration | ✅ DONE |
| Seeding (admin + Excel exchange) | ✅ DONE |
| DataSource + Excel Reader | ✅ DONE |

### چت ۴ (Session 4 - part04) — 2026-05-16

| Task | Status |
|---|---|
| Auth + JWT + OAuth2 + bcrypt مستقیم | ✅ DONE |
| اولین API endpoint (`GET /ohlcv/{symbol_id}`) | ✅ DONE |
| Frontend scaffold (Vite + dependencies) | ✅ DONE |
| Login واقعی + JWT در localStorage | ✅ DONE |
| ChartPage با lightweight-charts | ✅ DONE |

### چت ۵ (Session 5 - part04 + part05) — 2026-05-17

دو زیربخش:

**۵.الف — theme-engine:**

| Task | Status |
|---|---|
| Theme Engine Foundation (۵ تم) | ✅ DONE |
| Bug #43: Binance Color Accuracy | ✅ DONE |
| Bug #44: Interactive States | ✅ DONE |
| Toast Notifications | ✅ DONE |
| Bug #45: Toast Theme Consistency (Variant Pattern) | ✅ DONE |
| اسکریپت 00b_post_unzip_setup.py | ✅ DONE |
| قانون #۲۱ و #۲۲ | ✅ DONE |

**۵.ب — ui-polish-and-governance:**

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
| Tier 1 (Governance Infrastructure ۱۶ task) | ✅ DONE |

### چت ۶ (Session 6 - part06) — 2026-05-17 (quality-hardening)

| Task | Status |
|---|---|
| T2.03 — `.env.example` audit (backend + frontend) | ✅ DONE |
| T2.01 — Error Boundaries (defense-in-depth) | ✅ DONE |
| T2.02 — vitest setup + ۵ smoke test | ✅ DONE — **۳۰/۳۰ pass on user machine** |
| T2.04 — ARCHITECTURE.md با ۶ دیاگرام Mermaid | ✅ DONE |
| Git Infrastructure (12 commits, retroactive sync) | ✅ DONE |
| Sync Infrastructure (script 43) | ✅ DONE |
| Bug #50 موقت rفع شد (import React در 15 .jsx) | ✅ DONE (TEMP) |
| Bug #51 درس آموخته (python -c escape) | ✅ DONE |
| قوانین #۲۷-#۳۲ کشف شد | ✅ DONE — ⏳ ادغام در چت ۷ |

---

## آمار

| سطح | تعداد Tasks | DONE | باقیمانده |
|---|---|---|---|
| Tier 1 | 16 | 16 | 0 |
| Tier 2 | 11 | 4 | 7 (T2.05-T2.09 + T2.10 + T2.11) |
| Tier 3 | 20 | 0 | 20 |
| Tier 4 | 18 | 0 | 18 |
| **مجموع** | **65** | **20** | **45** |

> 💡 این آمار **حدوداً** است و در طول پروژه تغییر می‌کند.

---

## 📌 پایان TASK_BACKLOG

**نسخه:** v1.2 (2026-05-17 — پایان چت ۶)  
**به‌روز شده در:** پایان چت `TRADING-phase0-part06-quality-hardening`  
**به‌روز توسط:** Claude (طبق قانون #۲۳ و CLAUDE_CHECKLIST فاز ۳ مرحله ۳)
