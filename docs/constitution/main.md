# Constitution سامانه هوشمند ترید — v2.17 (Modular)

> **Intelligent Trading System — Modular Constitution**
> در بازارهای مالی | ارز دیجیتال و فارکس
>
> **نسخه:** 2.17 (atomic amendment از v2.16 — Governance Self-Sync + Authoring: Rule #۸۷ + Rule #۸۸)
> **تاریخ شروع split:** اردیبهشت ۱۴۰۵ (May 2026)
> **تاریخ v2.13:** خرداد ۱۴۰۵ (May 2026)
> **تاریخ v2.14:** خرداد ۱۴۰۵ (May 2026)
> **تاریخ v2.15:** خرداد ۱۴۰۵ (May 2026)
> **تاریخ v2.16:** خرداد ۱۴۰۵ (May 2026)
> **تاریخ v2.17:** خرداد ۱۴۰۵ (May 2026)
> **چت مسئول:** ۱۱.۰.ج (`TRADING-infra-governance-finalize-and-merge`)
> **چت مسئول v2.14:** part04-part08 (`TRADING-phase1-part04..part08-mdrs-v2-*`)
> **Branch:** `infra/v2.14-source-of-truth`
> **Created in commit:** `<git log --diff-filter=A --oneline -- docs/constitution/main.md>` (scaffold modular constitution v2.12، commit 1/8؛ هش از git مشتق شود — نه hardcode در ماژول، per #۸۶/check_5)

---

## 🎯 چرا این Constitution Modular است؟

نسخه v2.11 یک فایل ~۲۲۰KB بود که با Filesystem MCP در فایل‌های بزرگ کند می‌شد (M66). split به ۶ ماژول + main این مشکل را حل می‌کند:

- هر ماژول < ۵۰KB → MCP-safe
- ویرایش هدفمند بدون لمس کل سند
- cross-refs صریح به‌جای جستجوی متنی
- precedent برای پروژه‌های آینده

---

## 📚 ساختار ماژول‌ها

| ماژول | محتوا | برآورد اندازه |
|---|---|---|
| **[main.md](./main.md)** | این فایل — index + cross-refs + Vision + Quick-start | ~8KB |
| **[01_rules.md](./01_rules.md)** | قوانین Locked #۱-N (با شرح کامل، نمونه، استثناها) | ~45KB |
| **[02_lessons.md](./02_lessons.md)** | درس‌نامه اشتباهات Claude (M1-M105) با علت ریشه‌ای و راه‌حل | ~50KB |
| **[03_bugs.md](./03_bugs.md)** | کاتالوگ Bug ها (#1-#54+) با علائم، علت، fix | ~30KB |
| **[04_principles.md](./04_principles.md)** | ۸ اصل بنیادی + سطح‌بندی 🔒/🎯/💡 + No-Deletion + Atomic Updates | ~12KB |
| **[05_architecture.md](./05_architecture.md)** | Stack + DB Schema + Backend + Frontend + UI/UX + Security + Roadmap | ~40KB |
| **[06_meta.md](./06_meta.md)** | Session/Context + Templates + MCP + Claude Desktop + claude_workspace + Skills | ~35KB |

---

## 🗝️ راهنمای نمادها (سراسری در همه ماژول‌ها)

| نماد | معنا |
|---|---|
| 🔒 | **قفل‌شده** — قابل تغییر نیست مگر با توافق صریح صاحب پروژه |
| 🎯 | **تصمیم‌شده** — با پیشنهاد مستدل Claude + تأیید صاحب پروژه قابل تغییر است |
| 💡 | **پیشنهادی** — Claude می‌تواند بهبود بدهد، باید دلیل و مزیت را توضیح دهد و منتظر تأیید بماند |
| 🆕 v2.X | تغییر اضافه‌شده در نسخه v2.X |
| ⭐ | بخش حیاتی — توجه ویژه |
| ⚠️ | هشدار/توجه |

---

## 🧭 Quick-start برای Claude در شروع هر چت جدید

طبق قانون #۴۸ (پروتکل اجباری شروع چت)، Claude باید این مسیر را طی کند:

1. **`main.md`** (همین فایل) — برای آشنایی با ساختار modular
2. **`04_principles.md`** — برای فهم سطح‌بندی و فلسفه پروژه
3. **`01a_rules_core.md`** — قوانین کامل Locked (جدول #۱-۸۸ + بخش‌های پایه) ⭐
   - `01b_rules_detail.md` — شرح مفصل قوانین — **on-demand** (فقط وقتی شرح خاص قانونی لازم است)
4. **`claude_workspace/LOCKED_RULES_INBOX.md`** — قوانین Locked فعال (۶ قانون binding که هنوز در 01_rules.md ادغام نشده‌اند) ⭐
5. **`02_lessons.md`** — درس‌نامه برای جلوگیری از تکرار اشتباهات
6. **`docs/PENDING_FOR_NEXT_VERSION.md`** — PENDING آیتم‌های ادغام نشده
7. **`docs/SESSION_STATUS.md`** — وضعیت فعلی پروژه
8. **`docs/DECISIONS_LOG.md`** — تصمیمات معماری ثبت‌شده
9. **`docs/CHAT_LOG.md`** بخش چت قبل
10. **اجرای M73 audit** — Cross-Document Consistency Check

سایر ماژول‌ها (`03_bugs.md`, `05_architecture.md`, `06_meta.md`) **on-demand** خوانده می‌شوند — وقتی موضوع مرتبط مطرح شد.

---

## 🔗 Cross-references اصلی

### قوانین مهم در `01_rules.md`

- **#۴۸** پروتکل اجباری شروع چت → `01_rules.md#قانون-48`
- **#۶۰** PENDING-EOC در لحظه ثبت → `01_rules.md#قانون-60`
- **#۶۲** فایل handoff دائمی → `01_rules.md#قانون-62`
- **#۶۳** Convention `🟢 ▶️ EXECUTE` → `01_rules.md#قانون-63`
- **#۶۴** عدم نمایش جزئیات تصحیح خطا → `01_rules.md#قانون-64`
- **#۶۵** ثبت درس از اشتباهات با نمایش → `01_rules.md#قانون-65`
- **#۶۶** Push اجباری در پایان هر چت (Locked در v2.12) → `01_rules.md#قانون-66`
- **#۶۷** Cross-shell EXECUTE blocks اجباری (Locked در v2.13) → `01_rules.md#قانون-67`
- **#۶۸-#۷۷** 🆕 v2.14 — MDRS v2 framework: Tier classification، Review Trigger، Path Validator، VERSION SSoT، Manifest Self-Awareness، Triple-Rule Atomic Boundary، Z-ID Permanence، Review Scope Closure، Pre-Action Checklist Visibility، Continuous Discovery Logging → `01_rules.md#قانون-68` تا `قانون-77`
- **#۷۸-#۸۵** 🆕 v2.15 — Trust & Anti-Sycophancy Rules: SCM، QHP، NSISN، RDEM، MPTC، HAT، APMM، Self-Activation Lock → `01_rules.md` بخش «شرح کامل قوانین Trust & Anti-Sycophancy»
- **#۸۶** 🆕 v2.16 — Escape-Aware Sequence Derivation → `01_rules.md` بخش «شرح کامل قانون Mechanical-Claim Verification»
- **#۸۷-#۸۸** 🆕 v2.17 — Settings/Instructions/Project-Asset Sync Reminder + AI-Optimized Prompt/Artifact Authoring → `01_rules.md` بخش «شرح کامل قوانین Sync & Authoring»

### درس‌های مهم در `02_lessons.md`

- **M23** ⭐⭐⭐ عدم تولید handoff → `02_lessons.md#m23`
- **M66** Filesystem MCP و فایل‌های بزرگ → `02_lessons.md#m66`
- **M71-M73** Documentation Drift + Verification + Audit → `02_lessons.md#m71-m73`
- **M74-M79** درس‌های cleanup round 2 → `02_lessons.md#m74-m79`
- **M82** Verification Claim Must Be Verified → `02_lessons.md#m82`
- **M83** Retry First, Restructure Last → `02_lessons.md#m83`
- **M87** Active-Writing Self-Binding Failure (v2.13) → `02_lessons.md#m87`
- **M88** 🆕 v2.14 Hidden Regeneration Hazard → `02_lessons.md#m88`
- **M93** 🆕 v2.14 Triple-Rule Atomic Boundary → `02_lessons.md#m93`
- **M98** 🆕 v2.14 Review Scope Closure → `02_lessons.md#m98`
- **M99** 🆕 v2.14 CMD Long-Command + -F Flag Standard → `02_lessons.md#m99`
- **M100** 🆕 v2.14 Hidden-Checklist Completion → `02_lessons.md#m100`
- **M102** 🆕 v2.14 Rule-Implementation Decoupling → `02_lessons.md#m102`
- **HM-1 to HM-7** 🆕 v2.14 Helper Consultation Lessons → `02_lessons.md#§2-9`
- **M103** 🆕 v2.15 Audit Over-Promise Pattern → `02_lessons.md` §۲.۸
- **M104** 🆕 v2.16 Mechanical-Claim Verification before Persisting → `02_lessons.md` §۲.۸
- **M105** 🆕 v2.17 EXECUTE Command Paste-Integrity (`&`-chain) → `02_lessons.md` §۲.۸

### اصول بنیادی در `04_principles.md`

- اصل ۸ مشاوره: کاربردی، مهندسی، صادقانه، بدون تعارف، همه‌جانبه
- اصل طلایی: «امروز ساده، فردا قابل‌توسعه»
- No-Deletion (قانون #۲۴): سند جامع هرگز حذف نمی‌شود
- Atomic Updates (قانون #۲۶): تغییر در یک سند → اعمال هم‌زمان در همه اسناد مرتبط
- M82: Verification Claim Must Be Verified Itself

### معماری در `05_architecture.md`

- Stack: FastAPI + SQLAlchemy + React + Vite + SQLite
- DB Schema: ۱۲ جدول اصلی + AuditLog
- Backend: Layered Architecture (Presentation/Application/Domain/Infrastructure)
- Frontend: BrowserRouter + Zustand + axios interceptor
- UI/UX: RTL + Theme Engine + Design System بایننس
- Security: bcrypt + JWT + Fernet + RBAC + AuditLog
- Roadmap: ۱۵ فاز

### Meta در `06_meta.md`

- Session Management + Context handoff
- Templates پاسخ Claude (۱۰ Template)
- Filesystem MCP Integration
- Claude Desktop Configuration (Memory + Project Knowledge + Custom Instructions + Settings)
- `claude_workspace/` structure
- Skills اختصاصی پروژه (placeholder)

### Helper Consultation در `docs/HELPER_PROTOCOL.md` 🆕 v2.14

- **§۱** Helper Role Definition + Authority Hierarchy (advisory only، نه approval gate)
- **§۲** 8-Layer Review Framework (Conceptual, Self-Aware, Boundary, Convention, Decision, MDRS, Drift, Process)
- **§۳** Bounded Bootstrap Pattern + Escalation Criteria + Modified Round-1.5 edge case
- **§۴** Helper Output Format (Discoveries Log per Rule #۷۷)
- **§۵** HM-namespace design
- **§۶** Helper-User Approval Boundary
- **§۷** Constraint Checklist pattern (مجری Rule #۷۶)
- **§۸** Helper-side anti-patterns (HM-1 to HM-7 origin)

**Cross-refs:** Rule #۷۷ (Continuous Discovery Logging)، HM-series در `02_lessons.md` §۲.۹، Review #۰۰۳ (D24 decision record).

---

## 📊 آمار Constitution v2.17

| دسته | تعداد |
|---|---|
| قوانین Locked | ۸۸ ثبت‌شده (#۱-۸۸) + ۲ Reserved (#۵۲, #۵۳) — 🆕 ۲ قانون v2.17 (#۸۷-۸۸) + ۱ قانون v2.16 (#۸۶) + ۸ قانون Trust v2.15 (#۷۸-۸۵) + ۱۰ قانون v2.14 (#۶۸-#۷۷) |
| درس‌نامه M-series | M1-M105 (۷۳ ثبت + ۳۲ Reserved) — 🆕 M105 v2.17 (EXECUTE Paste-Integrity) + M104 v2.16 (Mechanical-Claim Verification) + M103 v2.15 (Audit Over-Promise) + ۱۱ درس v2.14 (M88+M93-M102) + ۴ Reserved جدید (M89-M92) |
| درس‌نامه HM-series 🆕 v2.14 | HM-1 to HM-7 در `02_lessons.md` §۲.۹ |
| Bug ها | ۱۶ ثبت‌شده در `03_bugs.md` + ۳۰+ در `docs/TROUBLESHOOTING.md` |
| ماژول‌ها | ۷ (شامل main.md) + archive |
| اندازه کل واقعی | ~۲۰۰KB توزیع‌شده (پس از S3.1) |
| بزرگترین ماژول | `02_lessons.md` (~۵۰KB پس از §۲.۹ HM-series) |

---

## ✅ وضعیت Migration (چت ۱۱.۰.الف — کامل)

- [x] Skeleton (commit 1) ✅
- [x] Migrate سند ۱ → `01_rules.md` (commit 2) ✅
- [x] Migrate سند ۱۸ → `02_lessons.md` (commit 3) ✅
- [x] Migrate Bug catalog → `03_bugs.md` (commit 4) ✅
- [x] Migrate principles → `04_principles.md` (commit 5) ✅
- [x] Migrate سند ۲-۸+۱۲ → `05_architecture.md` (commit 6) ✅
- [x] Migrate سند ۱۳-۱۷+۱۹-۲۵ → `06_meta.md` (commit 7) ✅
- [x] Archive سند قدیمی + Atomic Update v2.12 (commit 8) ✅

**Branch:** `infra/governance-overhaul` (آماده merge به `main` در پایان چت ۱۱.۰.ج) — ⚠️ توجه (drift اصلاح‌شده part17): merge به main انجام نشد؛ کار حاکمیتی روی `infra/v2.14-source-of-truth` ادامه یافت.

---

## 📜 تاریخچه نسخه‌ها

| نسخه | تاریخ | چت(ها) | تغییرات اصلی |
|---|---|---|---|
| v2.17 | May 2026 | part18 | **Governance Self-Sync + Authoring** — قانون #۸۷ (Settings/Instructions/Project-Asset Sync Reminder با Materiality Threshold) + قانون #۸۸ (AI-Optimized Prompt/Artifact Authoring) + Reviews #۰۱۰+#۰۱۱ + Decisions #۶۹+#۷۰ |
| v2.16 | May 2026 | part16 | **Mechanical-Claim Verification** — قانون #۸۶ (Escape-Aware Sequence Derivation) + درس M104 + Review #۰۰۸ |
| v2.15 | May 2026 | part11 | **Trust & Anti-Sycophancy Rules** — قوانین #۷۸-۸۵ (SCM/QHP/NSISN/RDEM/MPTC/HAT/APMM/Self-Activation Lock) + M103 (Audit Over-Promise، part10 origin) + Review #۰۰۵ |
| v2.14 | May 2026 | part04-part08 | MDRS v2 + Helper Infrastructure — Rules #۶۸-۷۷، Lessons M88+M93-M102، HM-1 to HM-7، Golden Rule، Templates 11-12، HELPER_PROTOCOL.md، Reviews #۰۰۲+#۰۰۳ |
| v2.13 | May 2026 | ۱۱.۰.ج | **Cross-shell mandatory** — قانون #۶۷ + M87 (Active-Writing Self-Binding Failure) + Pre-EXECUTE verification template |
| v2.12 | May 2026 | ۱۱.۰.الف+ب+ج | **Modular split** — تقسیم به ۶ ماژول + atomic update با ادغام PENDING |
| v2.11 | May 2026 | ۸+۹ | UX hardening — قوانین #۶۲-۶۵ |
| v2.10 | May 2026 | ۷+۸ | Filesystem MCP + claude_workspace |
| v2.9 | May 2026 | ۷ | Tier 2 Quality Hardening |
| v2.8 | May 2026 | ۶ | Atomic Update چت ۶ + قوانین #۲۷-۳۲ |
| v2.7 | May 2026 | ۵.ب | Governance ۱۲-سندی + قوانین #۲۳-۲۶ |
| v2.6 | May 2026 | ۵.الف | Theme Engine + Variant Pattern |
| v2.5 | May 2026 | ۴ | Auth + Frontend scaffold + قوانین #۱۹-۲۰ |
| v2.4 | May 2026 | ۳ | DB Infrastructure + DataSource Layer + قوانین #۱۶-۱۸ |
| v2.3 | May 2026 | ۲ | Chat Handoff Protocol |
| v2.2 | May 2026 | ۲ | اولین versioning رسمی |
| v2.1 | May 2026 | ۱ | Stack hardening + Fernet + AuditLog |
| v2.0 | May 2026 | ۱ | بنیاد اولیه |

---

**📌 پایان main.md**

برای جزئیات هر بخش، به ماژول مربوطه مراجعه کنید. این فایل صرفاً index و navigation است.
