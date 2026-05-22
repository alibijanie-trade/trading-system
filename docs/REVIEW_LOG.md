# REVIEW_LOG — لاگ بازنگری‌ها

> **هدف:** Master index از همه Review Reports (decision-records) پروژه.
> **مرتبط:** `docs/REVIEW_PROTOCOL.md` (procedure)، `docs/reviews/` (full files)
> **نسخه:** v1.0 (S2 D5 از MDRS v2)

---

## ۱. ساختار

هر Review Report یک row در جدول زیر دارد. ID متوالی است (no gaps allowed — توسط audit check آینده enforce می‌شود).

| ID | Date | Slug | Subject | Trigger | Status | Resolution |
|---|---|---|---|---|---|---|
| 001 | 2026-05-22 | mdrs-v2-review-infrastructure-bootstrap | Bootstrap of MDRS v2 review workflow per Decision #65. Selected internal markdown + REVIEW_LOG over Notion external, GitHub Issues only, or Jira/Linear. | §2.2 + §2.3 + §2.4 | **Implemented** | `4726b38` (D4) → `d9747b5` (D5) → this S2.3 atomic commit (D6) |

---

## ۲. Column Definitions

- **ID:** Sequential integer (1-based، zero-padded به 3 رقم). Audit check (آینده) enforces continuity.
- **Date:** YYYY-MM-DD UTC at initiation (نه completion).
- **Slug:** kebab-case، 1-5 words، matches filename suffix در `docs/reviews/YYYY-MM-DD-{slug}.md`.
- **Subject:** 1-3 sentence substantive summary of what was decided. **این نباید placeholder باشد** — حتی اگر Status=Proposed، subject باید reflect substantive content.
- **Trigger:** Reference به REVIEW_PROTOCOL section (e.g., `§2.2`). Multi-trigger با `+` (e.g., `§2.2 + §2.3 + §2.4`). شرح کامل هر trigger در `REVIEW_PROTOCOL.md`.
- **Status:** Proposed / Approved / Rejected / Deferred / Implemented (per `REVIEW_PROTOCOL.md` §4.1).
- **Resolution:** یکی از:
  - Commit chain: `f5c5004 → 4726b38 → ...` (وقتی Implemented)
  - Placeholder صریح: `<pending {stage}>` (وقتی Proposed/Approved/Deferred)
  - Rejection reason: `<rejected: {reason}>` (وقتی Rejected)
  - **هرگز:** `TBD`, `?`, خالی — این dangling reference است (anti-pattern از Triple-Rule lesson)

---

## ۳. Status Lifecycle (cross-ref REVIEW_PROTOCOL.md §4.1)

```
[Trigger]
   ↓
Proposed (Draft written, in discussion)
   ↓
   ├─→ Approved (Decision selected, implementation pending)
   │      ↓
   │   Implemented (Commits applied + pushed, full chain in Resolution)
   │
   ├─→ Rejected (No option selected — row stays for history, never deleted)
   │
   └─→ Deferred (Decision moved — explicit reason required in Resolution)
```

**نکات مهم:**
- **Deferred ≠ Rejected**: Deferred یک halfway-state معتبر است (e.g., "Deferred — منتظر T2.20 GitHub setup در S6")
- **Rejected رفته‌شده‌ها هم در LOG می‌مانند** (طبق قانون #۲۴ No-Deletion).
- **هر transition status نیاز به commit جداگانه دارد** برای traceability (شاید نه برای minor batch updates، طبق conceptual cohesion در REVIEW_PROTOCOL §9.1).

---

## ۴. Future Audit Reference

این LOG توسط future audit check بررسی می‌شود:
- هر file در `docs/reviews/*.md` باید row اینجا داشته باشد (و برعکس)
- ID numbering متوالی (001, 002, 003 — no gaps)
- File ID در heading با LOG row ID match کند
- Slug در filename با LOG slug column match کند

این check در D12 (extend `63_pre_commit_audit.py` با Check جدید) یا D21 (`scripts/65_doc_path_validator.py`) implemented خواهد شد. جزئیات implementation در `docs/PENDING_FOR_NEXT_VERSION.md` پس از atomic transfer در پایان چت ثبت می‌شود.

---

## ۵. Anti-patterns در LOG management

⚠️ **این الگوها از Triple-Rule pattern (قوانین #۲۶ + #۶۰ + #۶۶ chain) درس گرفته‌اند:**

1. **Dangling Reference:**
   - ❌ Row با Resolution=`TBD` → ambiguous، چه چیزی pending است؟
   - ✅ Row با Resolution=`<pending S2.3-S2.4>` → explicit، scope-bounded.

2. **Silent Status Drift:**
   - ❌ Status=Approved بدون commit chain → "claimed but not implemented"
   - ✅ Status transition باید با commit واقعی همراه باشد (قانون #۲۶ Atomic)

3. **Out-of-band Updates:**
   - ❌ Review file ساخته شد بدون LOG row update
   - ✅ Atomic update: LOG row + file در یک commit (قانون #۲۶)

4. **Forward-only Updates:**
   - ❌ Update row بدون اشاره به state قبلی (history loss)
   - ✅ Commit message ذکر کند چه چیزی تغییر کرد ("Status: Proposed → Implemented")

5. **Temporary-Reference Pollution:**
   - ❌ Subject یا Resolution شامل ID‌های موقت (tracker IDs که در آینده evaporate می‌شوند)
   - ✅ فقط permanent IDs (Rule #، M-lesson، Decision #) استفاده شود — این LOG خود permanent doc است

---

**نسخه:** v1.0 (S2 D5 از MDRS v2)
**ساخته توسط:** Claude در `TRADING-phase1-part03-mdrs-v2-implementation`
**Initial entry:** Review #001 با Status=Implemented در S2.3 atomic commit (همراه با ساخت `docs/reviews/README.md` و `docs/reviews/2026-05-22-mdrs-v2-review-infrastructure-bootstrap.md`). Triple-Rule prevention pattern موفق applied — هیچ dangling reference. Scope-closed طبق M98 candidate principle — D7 (PRE_ADD_CHECKLIST) در scope این Review نیست.
