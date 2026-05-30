# Review #008 — Escape-Aware Sequence Derivation (v2.16)

> **تاریخ:** 2026-05-30
> **Trigger:** §۲.۱ (Constitution change — ۱ Locked rule جدید #۸۶ + ۱ lesson M104)
> **Related artifacts:** docs/constitution/01_rules.md, docs/constitution/02_lessons.md, docs/constitution/main.md, scripts/63_pre_commit_audit.py, .pre-commit-config.yaml, docs/DECISIONS_LOG.md, docs/SESSION_STATUS.md
> **Status:** **Implemented**

## ۱. Context — چرا الان؟

در چت `TRADING-phase1-part14-phase3-fullrefresh` (هنگام ساخت escape-note)، شمارهٔ handoff به‌صورت literal «PART16» hard-code شد — از روی الگو/نام انسانی، نه اشتقاق مکانیکی. چون part14 **escape** بود (budget)، frontier جلو نرفت و مقدار درستِ مکانیکی **PART15** بود. این تعارض با invariant `check_12` (H==L+1) در part15 کشف و حل شد (گزینهٔ C: ردیف بازه‌ای part14-15 + handoff PART16).

ریشه: نقض #۸۴ (APMM — extrapolation از الگوی دنباله) + cross-check نکردن تعامل escape↔check_12. درس **M104** + قانون **#۸۶** این الگو را codify می‌کنند (Objective 2 / Phase 3، چت part16).

## ۲. Options Considered — گزینه‌ها

۱. **Option A — atomic batch (M104 + #۸۶ + version bump + audit + Decision + Review) در یک commit** (selected)
   - Pros: M93 atomic، governance trail کامل، یک snapshot
   - Cons: payload چندفایلی (split per Z3.20)

۲. **Option B — فقط درس M104 بدون قانون #۸۶**
   - Cons: M87 spirit — «درس بدون positive constraint» کافی نیست؛ #۸۶ enforcement رفتاری می‌دهد

۳. **Option C — defer به v2.17**
   - Cons: P-candidate از part15 معلق می‌ماند؛ هرچه دیرتر، drift بیشتر

## ۳. Decision — تصمیم

**Selected:** Option A (atomic batch، codify در part16)

**Rationale:**
- M104 (درس) + #۸۶ (قانون) یک concept واحد (M98 scope closure) → atomic
- positive constraint > negative reminder (#۴۶/#۶۷ precedent، M87)
- #۸۶ مکمل #۸۴ (APMM) است و check_12 را به‌عنوان invariant مرجع تثبیت می‌کند

## ۴. Impact — اثر

### Files changed
- `docs/constitution/02_lessons.md` — M104 (جدول §۲.۳ + heading + index §۲.۷ + شرح §۲.۸ + count ۷۱→۷۲)
- `docs/constitution/01_rules.md` — قانون #۸۶ (جدول ۱.۹ + بخش شرح کامل + footer #۱-۸۶)
- `docs/constitution/main.md` — frontmatter v2.15→v2.16 + H1 + آمار (۸۵→۸۶، M1-M103→M1-M104) + version history + cross-refs (#۸۶/M104)
- `docs/SESSION_STATUS.md` — surgical (rule ۸۵→۸۶، lesson M1-M103→M1-M104، Reviews ۷→۸، Constitution v2.16) — برای سبز ماندن check_1/check_2
- `scripts/63_pre_commit_audit.py` — CURRENT_VERSION v2.15→v2.16 + ACCEPTABLE_VERSIONS ["v2.14","v2.15"]→["v2.14","v2.15","v2.16"] (transitional، M102 — v2.14 نگه داشته شد چون module headers هنوز v2.14) + label/docstring
- `.pre-commit-config.yaml` — hook name (v2.15)→(v2.16)
- `docs/DECISIONS_LOG.md` — Decision #۶۸ + آمار (Max ۶۸، Recorded ۶۳)
- `claude_workspace/PHASE_LEDGER.md` — M101 backfill part14-15 (`c30dbe5`) [fold در همین commit]
- `docs/PENDING_FOR_NEXT_VERSION.md` — P-candidate part15 → CODIFIED v2.16
- `docs/reviews/2026-05-30-escape-aware-sequence-derivation.md` — این فایل

### Commits
- این part16 codify atomic commit (hash: M101 backfill در boot بعد)

### Constitution impact
- ۱ rule جدید Locked (#۸۶)، ۱ lesson جدید (M104)
- version: v2.15 → v2.16 (minor bump)

### Audit coupling (verify finding، part16)
- check_2 (lesson counts) با «M1-M» match می‌شود → main.md (**۲ نمونه**) و SESSION_STATUS باید M1-M104 شوند (الزامی)
- check_1 (rule counts) با anchor «Locked|N» (main) + «قفل…**N**» (SESSION) match می‌شود → هر سه منبع باید ۸۶ شوند (الزامی، per F-B hardening part13)
- check_6 (version) → ACCEPTABLE_VERSIONS باید v2.16 را شامل شود، atomic با main.md bump (M102/#۷۱)
- check_10 (review numbering) → #۰۰۸ متوالی پس از #۰۰۷
- check_12 (continuity) → دست‌نخورده (L=part15، H=PART16، 16==15+1)

### Backward compatibility
- safe: قواعد #۱-۸۵ unchanged؛ #۸۶ additive؛ module headers روی v2.14 (در ACCEPTABLE_VERSIONS، check_6 سبز)

## ۵. Lessons Applied — درس‌های کاربردی

- **M104 (dogfood)**: hash chat-end part14-15 از `git rev-parse` گرفته شد (`c30dbe5`)، نه حافظه؛ شماره‌های Review/Decision/Rule از REVIEW_LOG/DECISIONS_LOG/main استخراج شدند نه فرض ✅
- **M82**: read-back per edit (edit_file diff) + audit واقعی قبل از commit ✅
- **M93 Triple-Rule**: codification atomic؛ state-of-record full refresh به chat-end ✅
- **M95+M97+M99**: commit message ASCII-only + -F flag (در EXECUTE block) ✅
- **M98 Scope Closure**: فقط codify v2.16؛ بقیهٔ Phase 3 (deprecate/PROJECT_KNOWLEDGE) defer ✅
- **M101/M77**: Resolution بدون hash hardcode (placeholder + backfill boot بعد) ✅
- **M102**: قانون #۸۶ با Normative + Implementation Notes جدا؛ ACCEPTABLE_VERSIONS transitional ✅
- **Rule #۷۸/#۸۲/#۸۳ (dogfood)**: scope contract + pre-task checkpoint + Honesty Audit در همین چت ✅
- **Rule #۸۴ (dogfood)**: main.md کامل scan شد و **۲** نمونهٔ «M1-M103» پیدا شد (نه فرض یک نمونه) ✅

## ۶. Signatures

- Claude: confirmed in part16 commit message + this Review file
- User: explicit approval (scope contract اصلاح‌شدهٔ ۱۱ فایل + standing approval فایل‌به‌فایل)
- Commit boundary: این part16 codify atomic commit (hash backfill در boot بعد)
