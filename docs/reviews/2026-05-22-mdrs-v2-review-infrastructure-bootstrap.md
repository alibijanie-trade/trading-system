# Review #001 — MDRS v2 Review Infrastructure Bootstrap

> **تاریخ:** 2026-05-22  
> **Trigger:** REVIEW_PROTOCOL §2.2 (T1/T2 doc creation) + §2.3 (Infrastructure governance) + §2.4 (Major Refactor — MDRS v2)  
> **Related artifacts:** Decision #۶۵، MDRS v2 D1-D23 plan، commits `c71edd4`، `f5c5004`، `4726b38`، `d9747b5`  
> **Status:** Implemented

---

## ۱. Context — چرا الان؟

### ۱.۱ Trigger primary
**Decision #۶۵** در پایان چت deep-audit (`TRADING-phase1-part02-mdrs-v2-deep-audit`) ثبت شد: "implementation of MDRS v2 framework before continuing to binance_client phase".

این decision خود triggered شده توسط:
- شناسایی چندین drift در deep-audit (مرتبط با governance + state-of-record)
- نیاز به یک Manifest-Driven Repository Source-of-Truth framework
- درس‌های critical از چت ۱۱.۰.ج خصوصاً **Triple-Rule violation** (Atomic + PENDING + Push chain)

### ۱.۲ Why a review infrastructure?
MDRS v2 خود ۲۳ deliverable دارد (D1-D23) که چند تای آن‌ها constitution changes هستند. بدون trail رسمی برای ثبت reasoning این تصمیمات، در آینده:
- "چرا Tier rules این‌گونه طراحی شدند؟" بدون پاسخ می‌ماند
- "چرا Black retry pattern positive lesson است نه anti-pattern؟" گم می‌شود
- decisions reconstructable نخواهند بود

این Review #001 خود **first instance** از این framework است — **self-aware proof** که سیستم از روز اول کار می‌کند.

### ۱.۳ Connection با existing systems
- **Constitution v2.13:** قوانین #۲۶ (Atomic Updates) + #۶۰ (Continuous PENDING) + #۶۶ (Push) — این Review framework یک companion mechanism است برای lifecycle decisions
- **MDRS v2 D1 (PROJECT_MANIFEST.md):** Manifest scan آینده می‌تواند detect کند هر T1/T2 doc جدید بدون REVIEW_LOG row → audit FAIL
- **Decision Records در `DECISIONS_LOG.md`:** Decision Records کوتاه‌اند (یک پاراگراف). Reviews ساختاریافته‌ترند (Options Considered explicit، Impact، Lessons Applied)

---

## ۲. Options Considered

### Option A — Notion external knowledge base
**شرح:** ساخت یک Notion workspace با Database برای reviews.

**مزایا:**
- Rich UI، relations، tags، automations
- Mobile/web accessibility
- Templates آماده

**معایب:**
- ❌ **Outside repo** — git history و reviews از هم جدا می‌شوند
- ❌ **Context loss** — کسی که `git log` می‌خواند، نمی‌بیند چرا تصمیم گرفته شد
- ❌ Subscription cost برای team features (آینده)
- ❌ Vendor lock-in
- ❌ Search و grep از CLI ممکن نیست
- ❌ ⚠️ **Critical:** Claude در Project Settings نمی‌تواند Notion را دائماً access کند

### Option B — GitHub Issues only
**شرح:** هر تصمیم → یک GitHub Issue با labels (decision، architecture، governance).

**مزایا:**
- In-repo (issues + code در یک place)
- Free for private repos
- Searchable از CLI با `gh issue list`
- Built-in templates (planned در D15-D18)

**معایب:**
- ❌ **Free-form** — هر issue ساختار خاص خود را دارد
- ❌ **No structured trail** — Options Considered/Decision/Impact نمی‌توان enforce کرد
- ❌ Issues primarily reactive ابزارند (problem tracking) نه proactive decision-record
- ❌ Closed issues کمتر discoverable هستند

### Option C — Jira یا Linear
**شرح:** Enterprise PM platform.

**مزایا:**
- Workflow automations
- Comprehensive integrations

**معایب:**
- ❌ **Overhead برای solo project** — این پروژه single-developer است
- ❌ Subscription cost
- ❌ Outside repo (مثل Option A)
- ❌ Context-switching cost

### Option D — Internal Markdown + REVIEW_LOG ⭐ (Selected)
**شرح:** سه فایل markdown داخل repo:
- `docs/REVIEW_PROTOCOL.md` — procedure (D4)
- `docs/REVIEW_LOG.md` — master index/log (D5)
- `docs/reviews/YYYY-MM-DD-{slug}.md` — هر review یک فایل (D6)

**مزایا:**
- ✅ **In-repo** — `git log` + reviews + decisions همه با هم
- ✅ **Structured** — REVIEW_PROTOCOL §4 enforces Options Considered/Decision/Impact/Lessons
- ✅ **Free** — هیچ external dependency
- ✅ **Greppable** — `grep "Triple-Rule" docs/reviews/*.md`
- ✅ **Auditable** — future audit (D12/D21) می‌تواند consistency check کند
- ✅ **Forward-compat** — می‌تواند با D15-D18 GitHub Issue Templates pair شود (issues برای discussion، reviews برای decisions)
- ✅ **Project Knowledge friendly** — Claude desktop می‌تواند کل review trail را در context داشته باشد

**معایب:**
- ⚠️ Manual workflow — automation کم
- ⚠️ Discipline-dependent — اگر فراموش شد، silent gap (mitigated با future audit check)

---

## ۳. Decision

**Selected:** Option D — Internal Markdown + REVIEW_LOG.

### Rationale
**خلاصه:** in-repo + structured + free + greppable + auditable. این anchor همه دسترسی Claude است؛ Notion/Jira outside-repo بزرگ‌ترین weakness در workflow ما هستند، چون trail decision را از history کد جدا می‌کنند.

این تصمیم با **MDRS v2 framework** کاملاً سازگار است: Manifest scope منشأ truth برای governance است؛ reviews next-level evidence برای **چرا** governance این‌گونه طراحی شد. Both در یک repo، both auditable.

GitHub Issues (Option B) به‌عنوان **complement** نگه داشته می‌شود (D15-D18) — issues برای **bug tracking و discussion**، reviews برای **decision-records ساختاریافته**. این division of labor طبیعی است.

---

## ۴. Impact

### ۴.۱ Bootstrap Scope
این Review **scope محدود** به **Review Infrastructure Bootstrap** دارد: ساخت اولیه D4 (Protocol) + D5 (Log) + D6 (reviews/ directory + first review file).

D7 (PRE_ADD_CHECKLIST) یک deliverable مجزا با scope مستقل است؛ اگر نیاز به Review جداگانه داشت، Review #002 می‌شود — نه افزایش scope #001.

### ۴.۲ Commits برای این Review

| Commit | عمل | Stage |
|---|---|---|
| `4726b38` | Create `docs/REVIEW_PROTOCOL.md` (310 خط) | S2.1 (D4) |
| `d9747b5` | Create `docs/REVIEW_LOG.md` (98 خط) | S2.2 (D5) |
| این commit (atomic) | Create `docs/reviews/README.md` + Create این فایل + Update `docs/REVIEW_LOG.md` Row #001 (Status: Proposed → Implemented) | S2.3 (D6) |

### ۴.۳ Constitution Impact
**در S3 (atomic update v2.13 → v2.14) ادغام خواهد شد:**
- Rule جدید #۶۸+: MDRS v2 enforcement (manifest + review workflow)
- M-lessons formalized: M88 (Hidden Regeneration Hazard)، M93 (Triple-Rule Atomic Boundary)، M94 (Black Re-Stage)، M95 (CMD metachars)، M96 (Z-ID Permanence)، M97 (CMD em-dash side-effect)، M98 (Review Scope Closure)
- Principle: Golden Rule (Tier rules ≠ git tracking) → `04_principles.md`
- Templates ۱۱-۱۲ (D8-D11 پروژه)

### ۴.۴ Manifest Impact
- 4 جدید T2 doc اضافه شده/می‌شود (REVIEW_PROTOCOL ✅، REVIEW_LOG ✅، این فایل ✅، PRE_ADD_CHECKLIST در D7)
- 1 جدید directory (`docs/reviews/`) با README + Review files

### ۴.۵ Backward Compatibility
**Safe** — این features additive هستند. هیچ existing artifact رفتارش تغییر نمی‌کند. Future audit checks (D12, D21) که ممکن است هشدار دهند، اضافه‌بر هستند نه breaking.

### ۴.۶ Forward Compatibility
GitHub Issue Templates (S6 D15-D18) به این Review framework reference خواهد کرد. این Bootstrap layer برای entire workflow است.

---

## ۵. Lessons Applied

این تصمیم directly از این درس‌های اخیر استفاده کرد:

### ۵.۱ Triple-Rule Atomic Boundary (M93 candidate)
**از:** کشف drift در Phase 3 این چت — SESSION_STATUS uncommitted در 11.0.ج.  
**اعمال:** Workflow §6 از REVIEW_PROTOCOL.md mandates که LOG row update + Review file create در همان commit (نه دو commit جداگانه که می‌تواند dangling reference بسازد). این Review #001 خودش این pattern را اعمال می‌کند: ۳ فایل در یک atomic commit (README + این فایل + LOG row update).

### ۵.۲ Golden Rule (Principle)
**از:** D2 design discovery (کاربر) در S1.  
**اعمال:** Triggers (REVIEW_PROTOCOL §2) based on **role** (T1/T2/Infrastructure/Major Refactor) هستند، نه git status. Reviews با هیچ git stage یا branch tied نیستند.

### ۵.۳ Hidden Regeneration Hazard reversal (M88 candidate)
**از:** درس از scan-based vs hardcoded template generators.  
**اعمال:** REVIEW_PROTOCOL §3.6 explicit non-trigger می‌سازد برای MDRS manifest regeneration. این **anti-pattern reversal** است: scan-based generation OK، hardcoded template NOT.

### ۵.۴ Z-ID Permanence (M96 candidate)
**از:** Q4 catch کاربر در S2.2 review design.  
**اعمال:** این Review #001 file (permanent doc) **هیچ Z-ref ندارد** — فقط permanent refs (Rule #، M-candidate، Decision #). M-candidate IDs (M88, M93, M98, etc.) stable هستند حتی قبل از atomic update.

### ۵.۵ Black Re-Stage Pattern (M94 candidate)
**از:** S1 sub-commits 2 و 3.  
**اعمال:** REVIEW_PROTOCOL §3.4 این expected workflow را explicit non-trigger می‌سازد. هیچ Review نمی‌خواهد برای retry-after-formatter.

### ۵.۶ Conceptual Cohesion (Anti-flooding)
**از:** Q1 refinement کاربر در S2.1.  
**اعمال:** REVIEW_PROTOCOL §9.1 پرنسیپ "batch when conceptual cohesion، don't batch when independent triggers". این یک upgrade مفهومی از numeric threshold بود.

### ۵.۷ Review Scope Closure (M98 candidate)
**از:** سری Q3 + Q4 + اضافی catches کاربر در S2.3 design.  
**اعمال:** این Review file خود scope-bounded است: §۴.۱ صراحتاً declare می‌کند که scope محدود به D4+D5+D6 bootstrap است. §۴.۲ Commits list فقط شامل commits این scope. §۶ Signatures هیچ "Commit boundary: TBD" placeholder ندارد چون `git log` source of truth است. این self-aware proof از M98 پرنسیپ است — first case study.

---

## ۶. Signatures

- **Claude:** confirmation در commit message این sub-commit (S2.3)
- **User:** approval در S2 sign-off چت با ۵ Q + ۲ critical refinements (substantive Review #001 + bootstrap-self-reference) + ۲ refinement S2.3 (scope clarity در §۴.۲ + Commit boundary field حذف) + ۱ catch اضافی (Commits list scope-bounded)

(Commit history در `git log` خود source of truth است — هیچ commit boundary field در سرفصل به‌خاطر redundancy و dangling potential ذکر نمی‌شود.)

---

**نسخه:** v1.0 (S2 D6 از MDRS v2 — first Review Report در پروژه)
**ساخته توسط:** Claude در `TRADING-phase1-part03-mdrs-v2-implementation`
**Self-aware proof:** این فایل خود instance اول از framework است که خود توصیف می‌کند، و scope-closed طبق M98 principle.
