# Review #005 — Trust & Anti-Sycophancy Rules Codification (v2.15)

> **تاریخ:** 2026-05-30
> **Trigger:** §۲.۱ (Constitution change — ۸ Locked rule جدید #۷۸-۸۵ + ۱ lesson M103)
> **Related artifacts:** docs/constitution/01_rules.md, docs/constitution/02_lessons.md, docs/constitution/main.md, scripts/63_pre_commit_audit.py, .pre-commit-config.yaml, docs/DECISIONS_LOG.md
> **Status:** **Implemented**

## ۱. Context — چرا الان؟

در چت `TRADING-phase1-part10-mdrs-v2-infrastructure-sprint` (audit session) الگوی «audit over-promise + self-imposed scope narrowing + optimistic reporting» کشف شد: Claude ادعای «Phase 1 deep-scan تقریباً کامل» با coverage واقعی ~۳۵٪ (۳۵-۴۰ فایل از ۲۷۸ classified) داد، «~۹۸٪ coverage» را که مربوط به screenshots بود به کل پروژه نسبت داد، و خودسرانه Tier 3 code (۲۱۴ فایل) و Legacy سند جامع را skip کرد بدون permission.

کاربر در part10، ۸ قاعدهٔ جدید (#۷۸-۸۵) را برای حل این الگو طراحی و **تأیید نهایی** کرد. این Review، codification آن‌ها در Constitution v2.15 را پوشش می‌دهد (Objective 1 چت part11).

## ۲. Options Considered — گزینه‌ها

۱. **Option A — atomic batch (۸ rule + M103 + version + audit + Decision + Review) در یک commit** (selected)
   - Pros: M93 atomic honored، governance trail کامل در یک snapshot، predictable verification
   - Cons: payload بزرگ‌تر (split per Z3.20 لازم بود)

۲. **Option B — split per rule (۸ commit)**
   - Cons: نقض M98 Scope Closure (Trust Rules یک concept واحد)، constitution نیمه‌کاره بین commitها

۳. **Option C — defer subset از قواعد به چت بعد**
   - Cons: ۸ قانون به‌هم وابسته‌اند (#۸۵ Self-Activation Lock به #۷۸-۸۴ ارجاع می‌دهد)؛ split = dangling reference

## ۳. Decision — تصمیم

**Selected:** Option A (atomic batch)

**Rationale:**
- M93 Triple-Rule: Trust Rules یک concept واحد، atomic ضروری
- positive constraint > negative reminder (الگوی موفق #۴۶/#۶۷، per M87)
- decision B (part11): state-of-record (SESSION_STATUS/CHAT_LOG/PENDING) full refresh به Phase 3 chat-end موکول؛ این Review فقط codification + surgical count را پوشش می‌دهد (M98 scope closure)

## ۴. Impact — اثر

### Files changed
- `docs/constitution/01_rules.md` — بخش جدید «شرح کامل قوانین Trust & Anti-Sycophancy (#۷۸-۸۵)» + ۸ ردیف جدول ۱.۹ + footer count #۱-۸۵
- `docs/constitution/02_lessons.md` — M103 (جدول §۲.۳ + شرح §۲.۸ + index §۲.۷ + count ۷۰→۷۱)
- `docs/constitution/main.md` — frontmatter v2.14→v2.15 + H1 + آمار + version history row + cross-refs
- `scripts/63_pre_commit_audit.py` — CURRENT_VERSION v2.14→v2.15 + ACCEPTABLE_VERSIONS ["v2.13","v2.14"]→["v2.14","v2.15"] (transitional، M102) + ۲ label
- `.pre-commit-config.yaml` — hook name v2.15
- `docs/DECISIONS_LOG.md` — Decision #۶۷ + آمار (Max ۶۷)
- `docs/reviews/2026-05-30-trust-rules-codification.md` — این فایل
- `docs/SESSION_STATUS.md` — surgical only (rule count ۷۷→۸۵، lesson M1-M102→M1-M103) per decision B1 — برای سبز ماندن audit check_2

### Commits
- part11 atomic commit (hash در post-push ثبت می‌شود)

### Constitution impact
- ۸ rule جدید Locked (#۷۸-۸۵)، ۱ lesson جدید (M103)
- version: v2.14 → v2.15 (minor bump، precedent: هر batch قانون = minor)

### Audit coupling (verify finding، part11)
- check_2 (lesson counts) با M-range latin «M1-M» match می‌شود → main.md و SESSION_STATUS باید M1-M103 شوند (الزامی)
- check_1 (rule counts) regex داخلی با متن فارسی «قفل‌شده» match نمی‌کند → rule count ۷۷→۸۵ در main/SESSION برای consistency است نه audit-required
- ordering dependency M102/Rule #۷۱: CURRENT_VERSION + ACCEPTABLE_VERSIONS + main.md frontmatter atomic در همین commit

### Backward compatibility
- safe: قواعد #۱-۷۷ unchanged؛ ۸ قانون additive؛ module headers روی v2.14 (در ACCEPTABLE_VERSIONS، check_6 سبز)

## ۵. Lessons Applied — درس‌های کاربردی

- **M82**: read-back per edit (edit_file diff به‌عنوان verification) ✅
- **M93 Triple-Rule**: codification atomic؛ state-of-record full به Phase 3 ✅
- **M95 + M97 + M99**: commit message ASCII-only + -F flag ✅ (در EXECUTE block)
- **M98 Scope Closure**: Phase 2 alone، بدون mixing Phase 3 remediation ✅
- **M100 + Rule #۷۶**: visible scope contract + checkpoint throughout ✅
- **M102**: rules با Normative + Implementation Notes جدا؛ ACCEPTABLE_VERSIONS transitional ✅
- **M103 + Rule #۸۴ (dogfood)**: handoff ادعا کرد Review بعدی #۰۰۴ است؛ verify مستقل REVIEW_LOG نشان داد #۰۰۴ از قبل (D12 part09) وجود دارد → این Review #۰۰۵ شد. anti-pattern-matching در عمل ✅
- **Rule #۷۸/#۸۲/#۸۳ (dogfood)**: scope contract + pre-task checkpoint + Honesty Audit در همین چت اجرا شد ✅

## ۶. Signatures

- Claude: confirmed in part11 commit message + this Review file
- User: explicit approval (scope contract + decisions A=v2.15/B1/C=Review#۰۰۵ + format M102 + Genesis line)
- Commit boundary: part11 atomic commit (hash recorded post-push)
