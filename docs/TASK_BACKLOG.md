# 📋 TASK_BACKLOG — لیست کامل task های پروژه

> **هدف یک‌خطی:** فهرست همه task های پروژه با وضعیت آن‌ها، گروه‌بندی به Tier، با اولویت و تخمین.

> **محل قرارگیری:** `docs/TASK_BACKLOG.md`  
> **به‌روز توسط:** Claude در پایان هر چت (فاز ۳ مرحله ۳ چک‌لیست)  
> **نسخه این Backlog:** v1.5 (2026-05-19 — چت ۸: ادغام Tier 2 + ۸ task جدید زیرساخت Claude Desktop)

---

## 📑 فهرست

- [راهنمای استفاده](#راهنمای-استفاده)
- [Tier 1 — DONE (در چت ۵)](#tier-1)
- [Tier 2 — Quality Hardening + Infrastructure (۱۴/۲۱ ✅)](#tier-2--quality-hardening)
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
| T2.05 | Git workflow audit + GIT_WORKFLOW.md | ✅ DONE | 🟠 | S | چت ۷ |
| T2.06 | Pre-commit hooks (Hybrid mode: critical اجباری + minor warning) | ✅ DONE | 🟡 | M | چت ۷ |
| T2.07 | Anti-pattern catalog (A1-A10) | ✅ DONE | 🟡 | M | چت ۷ |
| T2.08 | Backend pytest + coverage + pyproject.toml (**۲۵/۲۵ pass**) | ✅ DONE | 🟡 | M | چت ۷ |
| T2.09 | API_DOCS.md (markdown alternative به Swagger) | ✅ DONE | 🟡 | M | چت ۷ |

### Tasks اضافی کشف‌شده در چت ۶

| ID | Task | Status | شرح |
|---|---|---|---|
| T2.10 | توسعه ARCHITECTURE.md (بخش‌های فاز ۱) | 📋 TODO | minimal expansion — افزودن Repository Layer + CCXT connector sections. در چت ۸ بلوک ۳. Tier 2، 🟡 MEDIUM، S. |
| T2.11 | ادغام قوانین #۲۷-#۳۲ در سند جامع | ✅ DONE | atomic update در آغاز چت ۷ (سند v2.7→v2.8 + CLAUDE_CHECKLIST + PROJECT_GOVERNANCE + CHAT_LOG) |
| T2.12 | ارزیابی و مهاجرت به Claude Code / GitHub MCP workflow | 📋 TODO | Tier 3، 🟢 LOW، XL — بررسی در چت ۸ بلوک ۳ (ارزیابی دو connector برای فاز ۱+). |
| T2.13 | علت‌یابی ریشه‌ای Bug #50 (import React اضافی) | 📋 TODO | timebox 30min در چت ۸ بلوک ۳. اگر در زمان رفع نشد، open issue باقی. Tier 2، 🟡 MEDIUM، S. |
| T2.14 🆕 | Filesystem MCP integration + permissions | ✅ DONE | چت ۷ — نصب + configure. در v2.10 سند ۲۲ مستند شد. |
| T2.15 🆕 | Claude Desktop: Memory + Project Knowledge + Custom Instructions | ✅ DONE | چت ۷ — Memory toggles ON. در v2.10 سند ۲۳ مستند شد. |
| T2.16 🆕 | `claude_workspace/` structure (۵ subfolder + gitignore) | ✅ DONE | چت ۷. در v2.10 سند ۲۴ مستند شد. |
| T2.17 🆕 | PENDING_FOR_NEXT_VERSION.md system (قانون #۶۰) | ✅ DONE | چت ۸ — فایل ساخت + پروتکل. **حل ریشه‌ای M23**. |
| T2.18 🆕 | ادغام PENDING → سند جامع v2.10 + Atomic Updates Governance | 🚧 IN-PROGRESS | چت ۸ بلوک ۱ — A1-A7. |
| T2.19 🆕 | تکمیل CHAT_LOG.md چت ۷ (stub بود — نتیجه M23) | 🚧 IN-PROGRESS | چت ۸ بلوک ۱ — A5. |
| T2.20 🆕 | GitHub setup طبق سند ۲۱ | 📋 TODO | چت ۸ بلوک ۲ (تعاملی، نیاز به کاربر). |
| T2.21 🆕 | Audit Settings Claude Desktop (سند ۲۳) | 📋 TODO | چت ۸ بلوک ۲ — نیاز به ۸ screenshot از کاربر. |

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

### چت ۷ (Session 7 - part07) — 2026-05-18 (quality-hardening-continued)

| Task | Status |
|---|---|
| T2.05 — Git workflow audit + GIT_WORKFLOW.md | ✅ DONE |
| T2.06 — Pre-commit hooks (Hybrid mode) | ✅ DONE |
| T2.07 — Anti-pattern catalog (A1-A10) | ✅ DONE |
| T2.08 — Backend pytest + coverage + pyproject.toml | ✅ DONE — ۲۵/۲۵ pass |
| T2.09 — API_DOCS.md | ✅ DONE |
| T2.11 — ادغام قوانین #۲۷-۳۲ (Atomic Update v2.7→v2.8→v2.9) | ✅ DONE |
| T2.14 — Filesystem MCP integration | ✅ DONE |
| T2.15 — Claude Desktop: Memory + Project Knowledge + Custom Instructions | ✅ DONE |
| T2.16 — `claude_workspace/` structure | ✅ DONE |
| قوانین #۳۳-۴۷ + درس‌نامه M1-M21 ثبت | ✅ DONE — در سند v2.9 |
| ۵ سند جانبی جدید (GIT_WORKFLOW + API_DOCS + ANTI_PATTERNS + BACKEND_TESTING + PRECOMMIT) | ✅ DONE |
| Git: تکمیل تاریخچه چت ۷ (91704ca → d6bc75c) | ✅ DONE |

> ⚠️ **نکته از چت ۸:** CHAT_LOG.md چت ۷ در پایان آن چت stub باقی ماند (درس M23 — مهم‌ترین درس پروژه). در چت ۸ تکمیل خواهد شد (T2.19).

### چت ۸ (Session 8 - part08) — 2026-05-19 (pre-phase1-setup) — 🚧 IN-PROGRESS

| Task | Status |
|---|---|
| T2.17 — PENDING_FOR_NEXT_VERSION.md system (قانون #۶۰) | ✅ DONE |
| T2.18 — Atomic Update Governance docs (A1-A7) | 🚧 IN-PROGRESS |
| قوانین جدید #۴۸-۶۱ + درس‌های M22-M62 | ✅ DONE — در v2.10 |
| ۴ بخش جدید سند جامع (۲۲-۲۵) | ✅ DONE |
| Atomic Update CLAUDE_CHECKLIST v1.2→v1.3 | ✅ DONE |
| Atomic Update PROJECT_GOVERNANCE v1.2→v1.3 | ✅ DONE |
| Atomic Update TASK_BACKLOG v1.4→v1.5 | 🚧 IN-PROGRESS (همین لحظه!) |

> این بخش در پایان چت ۸ تکمیل می‌شود.

---

## آمار

| سطح | تعداد Tasks | DONE | باقیمانده |
|---|---|---|---|
| Tier 1 | 16 | 16 | 0 |
| Tier 2 | 21 | 14 | 7 (T2.10، T2.12، T2.13، T2.18، T2.19، T2.20، T2.21) |
| Tier 3 | 21 | 0 | 21 |
| Tier 4 | 18 | 0 | 18 |
| **مجموع** | **76** | **30** | **46** |

> 💡 این آمار **حدوداً** است و در طول پروژه تغییر می‌کند.

---

## 📌 پایان TASK_BACKLOG

**نسخه:** v1.5 (2026-05-19 — چت ۸: ادغام Tier 2 + ۸ task جدید زیرساخت Claude Desktop)  
**به‌روز شده در:** چت `TRADING-phase0-part08-pre-phase1-setup`  
**به‌روز توسط:** Claude (طبق قانون #۲۳ و CLAUDE_CHECKLIST v1.3 فاز ۳)
