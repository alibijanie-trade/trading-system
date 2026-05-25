# Review #004 — D12 Audit Checks Extension (v2.14 S4)

> **تاریخ:** 2026-05-25
> **Trigger:** §۲.۳ (Infrastructure — extension of scripts/63_pre_commit_audit.py)
> **Related artifacts:** S4 commit (this), scripts/63_pre_commit_audit.py, scripts/63b_test_pre_commit_audit.py, docs/constitution/01_rules.md
> **Status:** **Implemented**

## ۱. Context — چرا الان؟

S4 از MDRS v2 atomic plan: deliverable D12 (Audit Checks #۸-۱۱). part09 boot per HANDOFF priority اول.

scope بسته per HANDOFF + PENDING:
- Check #۸: Detect uncommitted state files (M93 enforcement)
- Check #۹: Manifest self-row existence + first-run gap (Z3.15)
- Check #۱۰: Review numbering integrity (Z3.16)
- Check #۱۱: Z-ID Permanence anti-pattern scanner (Rule #۷۴ + M96)

این Review **lightweight LOG-only** است (per DECISION 2 part09) — بدون separate Draft phase، چون scope pre-spec شده در 24-deliverable plan بود و Review #۰۰۲ کلیات را endorse کرد.

## ۲. Options Considered — گزینه‌ها

از آن‌جا که scope pre-spec شده بود، option-tree محدود بود:

۱. **Option A — All 4 checks در یک atomic commit + companion test** (selected)
   - Pros: M93 atomic honored، single commit برای کل D12، predictable verification
   - Cons: payload commit بزرگ‌تر (~۲۶ edit شامل round 1 + cleanup)

۲. **Option B — Split per check (4 commits)**
   - Pros: granular history
   - Cons: نقض M98 Scope Closure (D12 یک concept واحد است)، multiple commits برای deliverable واحد

۳. **Option C — Defer check_8 + check_11 به part10 (only static checks 9 + 10 الان)**
   - Pros: لaze باز کم‌تر در S4
   - Cons: D12 یک deliverable است، split = scope creep خفته

## ۳. Decision — تصمیم

**Selected:** Option A

**Rationale:**

- M93 Triple-Rule: D12 یک concept واحد است، atomic ضروری
- Companion test atomic per Rule #۲۲
- precedent: S3.1 + S3.3 با scope جامع موفق بودند
- Z3.25 (test_6 drift از S3.3) همراه fix شد (Rule #۲۲ retroactive)
- Rule #۷۴ self-violation در round 1 check_11 caught و در round 2 + 3 cleanup → M96 evidence working

## ۴. Impact — اثر

### Files changed
- `scripts/63_pre_commit_audit.py` — افزوده ۴ check function + ۵ constants + extended ALL_CHECKS + argparse update + docstring M-mappings
- `scripts/63b_test_pre_commit_audit.py` — افزوده ۴ test function + helper `_run_specific_check` + extended ALL_TESTS + test_2 update + test_6 Z3.25 fix
- `docs/constitution/01_rules.md` — surgical Z-ID cleanup (13 edits، Rule #۷۴ eat-your-own-dogfood resolved)
- `docs/reviews/2026-05-25-d12-audit-checks-extension.md` — این فایل
- `docs/REVIEW_LOG.md` — Row #۰۰۴ افزوده

### Commits
- این S4 commit: hash در post-commit ثبت می‌شود

### Constitution impact
- هیچ rule جدید/تغییر
- هیچ lesson جدید (M-list unchanged: M1-M102)
- Rule #۷۴ کلمات پاکسازی شدند ولی content semantic حفظ شد

### Manifest impact
- D2 re-run در chat-end (per Z3.21 policy)
- 2 T3 file content hash changed + 1 T1 file content hash changed

### Backward compatibility
- safe: existing 7 checks unchanged، 4 جدید additive
- companion test ALL_TESTS sequential — no breaking

## ۵. Lessons Applied — درس‌های کاربردی

- **M22**: companion test mandatory ✅
- **M82**: read-back per edit ✅ (verified post-batch)
- **M88 reversal**: ALL_CHECKS list = single source، derived counts dynamic via `len()` ✅
- **M93 Triple-Rule**: audit + test در یک commit ✅
- **M95 + M97**: ASCII-only commit message ✅
- **M96**: Z-ID Permanence operational + Rule #۷۴ self-violation resolved ✅
- **M98 Scope Closure**: S4 alone، no S5 mixed ✅
- **M99 -F flag**: commit_msg_s4.txt استاندارد ✅
- **M100**: visible Pre-Action Checklist throughout ✅
- **M102**: Check #۸ implements Rule #۷۳ normative; Check #۱۱ implements Rule #۷۴ normative — decoupling honored ✅

## ۶. Signatures

- Claude: confirmed in S4 commit message + this Review file
- User: explicit approval per DECISION 1-7 (part09 turns 5, 7, 9, 11, 13, 15)
- Commit boundary: S4 atomic commit (hash recorded post-push)
