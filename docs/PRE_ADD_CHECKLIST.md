# PRE_ADD_CHECKLIST — چک‌لیست قبل از افزودن Artifact جدید

> **هدف:** Gate قبل از reaching trigger در `REVIEW_PROTOCOL.md`. این چک‌لیست تشخیصی است: قبل از اینکه چیز جدیدی به scope حاکمیتی پروژه اضافه شود، ۱۰ check تشخیصی انجام شود.
> **مرتبط:** `docs/REVIEW_PROTOCOL.md` (post-trigger procedure)، `docs/REVIEW_LOG.md` (index)، `docs/CLAUDE_CHECKLIST.md` (per-chat workflow)
> **نسخه:** v1.0 (S2 D7 از MDRS v2)

---

## ۱. Purpose — چرا این چک‌لیست لازم است

### ۱.۱ تفاوت با CLAUDE_CHECKLIST.md
- `CLAUDE_CHECKLIST.md` = **per-chat** workflow checklist (boot، phase transitions، chat-end protocol)
- `PRE_ADD_CHECKLIST.md` = **per-artifact** decision gate (هر زمان که چیز جدید می‌خواهد add شود)

### ۱.۲ تفاوت با REVIEW_PROTOCOL.md
- `REVIEW_PROTOCOL.md` = **post-trigger** procedure (وقتی Review لازم شد، چه کاری بکنیم؟)
- `PRE_ADD_CHECKLIST.md` = **pre-trigger** gate (آیا Review لازم است؟ چه چیز را قبل از add باید چک کنیم؟)

### ۱.۳ Function اصلی
این چک‌لیست **prevention layer** است:
- Missed steps (e.g., فراموش‌کردن companion test برای script جدید)
- Mismatched tiers (e.g., T3 code که اشتباهاً در docs/ گذاشته شد)
- Missing artifacts (e.g., new script بدون SESSION_STATUS update)
- Skipped Reviews (e.g., new T2 doc بدون REVIEW_LOG entry)

---

## ۲. When to Use — چه زمانی این چک‌لیست اجرا شود

### ۲.۱ Trigger phrases (شناسایی لحظه‌ی استفاده)

این چک‌لیست در لحظه‌ای استفاده می‌شود که یکی از این عبارات در discussion ظاهر شود:
- "بیاید X اضافه کنیم"
- "نیاز به Y جدید است"
- "regression test برای Z"
- "script جدید برای ..."
- "این rule را به constitution اضافه کنیم"
- "این فایل را create کنیم"
- "این directory را اضافه کنیم"

### ۲.۲ Trigger negatives (لحظه‌هایی که این چک‌لیست لازم نیست)
- "این bug را fix می‌کنیم" (typo، edge case — refer به `REVIEW_PROTOCOL.md` §3.2)
- "این comment را اضافه می‌کنیم"
- "black auto-reformat کرد، re-stage" (M94 pattern)

---

## ۳. Pre-Trigger Checks — ۱۰ تشخیصی

این ۱۰ check باید **به ترتیب** انجام شوند. پاسخ هر check decision دارد:

### Check ۱ — Tier Classification 🏷️
**سؤال:** این artifact به کدام Tier تعلق دارد؟
- **T1** (Constitution + State) — `docs/constitution/`, `docs/SESSION_STATUS.md`, `docs/PROJECT_MANIFEST.md`, ...
- **T2** (Reference Docs) — `docs/ARCHITECTURE.md`, `docs/REVIEW_PROTOCOL.md`, ...
- **T3** (Code) — `backend/`, `frontend/`, `scripts/`, ...
- **T4.1** (Config) — `pyproject.toml`, `.gitignore`, `.pre-commit-config.yaml`, ...
- **T4.2** (Assets) — `data/excel_imports/`, `claude_workspace/snapshots/`, ...
- **T5** (Excluded) — temp files, build artifacts, vendored dependencies

**Conditional:**
- اگر T1 → also Check ۷ (Constitution impact)
- اگر T2 → also Check ۵ (Reference doc impact)
- اگر T3 → also Check ۴ (Companion test)
- اگر T4.* → also Check ۶ (Manifest impact)
- اگر T5 → STOP — این artifact tracked نمی‌شود (نگاه به `REVIEW_PROTOCOL.md` §3.6)

### Check ۲ — Path Validity 📁
**سؤال:** location صحیح است؟
- آیا path با Tier matching الگو دارد؟ (T1 docs در `docs/constitution/` نه `docs/`)
- آیا parent directory موجود است؟
- آیا فایل قبلاً وجود ندارد؟ (collision check)

**اگر مشکل:** Refer به `docs/PROJECT_MANIFEST.md` برای patterns موجود.

### Check ۳ — Naming Convention 📝
**سؤال:** نام artifact با existing patterns همخوان است؟
- **Scripts:** `{N}_descriptive_name.py` (مثل `64_generate_manifest.py`)
- **Tests:** `{N}b_test_descriptive_name.py` (مثل `64b_test_manifest.py`)
- **Docs:** `UPPER_SNAKE.md` (مثل `REVIEW_PROTOCOL.md`)
- **Reviews:** `YYYY-MM-DD-{slug}.md` در `docs/reviews/`

**اگر T3 script:** Check ۴ نیز.

### Check ۴ — Companion Test (Rule #۲۲) 🧪
**سؤال:** اگر T3 script ساخته می‌شود، test همراه plan شده؟
- هر `scripts/{N}_*.py` نیاز به `scripts/{N}b_test_*.py` دارد (طبق قانون #۲۲)
- آیا test plan شده در همان sub-commit یا next؟
- آیا test همان stage commit می‌شود (atomic) یا later؟

**اگر T3 + companion test missing:** STOP — companion test را اضافه به scope.

### Check ۵ — Reference Doc Impact 📚
**سؤال:** کدام T2 doc(s) باید update شود؟
- آیا `docs/ARCHITECTURE.md` نیاز به entry جدید دارد؟
- آیا `docs/STYLE_GUIDE.md` نیاز به example دارد؟
- آیا `docs/API_DOCS.md` نیاز به update دارد؟

**اگر update lookup‌ها:** plan آن‌ها در همان sub-commit یا stage-end.

### Check ۶ — Manifest Impact 🗂️
**سؤال:** آیا D2 re-run لازم است؟
- آیا artifact جدید pattern موجود T1-T4 را match می‌کند؟
- اگر بله → manifest خودش در commit بعدی regenerate می‌شود (تنها در stage-end)
- اگر artifact pattern جدید است → tier rules در `scripts/64_generate_manifest.py` نیاز به update دارد (این خود triggers Review!)

### Check ۷ — Constitution Impact 📜
**سؤال:** آیا constitution change نیاز است؟
- آیا rule جدید (#X)?
- آیا lesson جدید (M-Y)?
- آیا principle update?
- آیا architecture decision (`05_architecture.md`)?

**اگر بله:** This is REVIEW TRIGGER — به Decision در §۴ مراجعه.

### Check ۸ — State-of-Record Plan 📊
**سؤال:** Stage-end refresh چگونه این تغییر را reflect می‌کند؟
- آیا `SESSION_STATUS.md` نیاز به update دارد؟ (مثلاً stats، آخرین deliverable، lesson candidates)
- آیا `CHAT_LOG.md` نیاز به section/sub-section دارد؟
- آیا tracker (`MDRS_V2_PENDING_DRAFT.md`) نیاز به entry جدید دارد؟

**Critical (Triple-Rule pattern):** plan این updates **در همان stage-end commit boundary** — نه later به‌عنوان "I'll update SESSION_STATUS in next commit".

### Check ۹ — Audit-Ready ✅
**سؤال:** existing pre-commit hooks pass خواهند کرد؟
- اگر T3 Python: black, isort, anti-patterns — likely OK
- اگر T1/T2 Markdown: trim whitespace, fix end-of-files
- اگر Layer 1 Audit در `scripts/63_pre_commit_audit.py`: rule count consistency، lesson count consistency

**اگر مشکوک:** قبل از commit attempt dry-run با `pre-commit run --files {path}`.

### Check ۱۰ — Review Scope Check 🎯
**سؤال:** این تغییر بخشی از یک Review در حال Implementation (در `REVIEW_LOG.md`) است، یا Review جدید trigger می‌کند؟

- **اگر بخشی از موجود است:**
  - Scope آن Review را closed نگه‌دار
  - هیچ forward-reference به upcoming sub-stage نباشد در Review file
  - اگر scope صرفاً extend شد (نه coherent)، split به Review #N+1

- **اگر Review جدید trigger می‌کند:**
  - Refer به `REVIEW_PROTOCOL.md` §2 (Triggers) و §6 (Workflow)
  - Draft Review در `docs/reviews/YYYY-MM-DD-{slug}.md`
  - Row جدید در `docs/REVIEW_LOG.md`
  - این هر دو atomic در همان commit (Triple-Rule)

- **اگر هیچ‌کدام:** این تغییر یا cosmetic است یا T3 routine — بدون Review proceed (refer به `REVIEW_PROTOCOL.md` §3 Anti-patterns).

---

## ۴. Decision Output — Routing

```
[Pre-Add Checklist 1-10 complete]
       ↓
   Decision?
       │
       ├─→ ✅ Proceed with Add
       │       ↓
       │   No Review needed (routine/cosmetic per §3 of REVIEW_PROTOCOL)
       │       ↓
       │   Commit + push با existing pattern
       │
       ├─→ 📋 Trigger Review #N
       │       ↓
       │   Go to REVIEW_PROTOCOL §6 Workflow Step 2 (Draft Report)
       │       ↓
       │   Pre-Add complete، Review process begins
       │
       └─→ ⏸️ Defer / Reject
               ↓
           Reason explicit:
             - "Defer — منتظر S6 GitHub setup"
             - "Reject — این تغییر contradicts Tier rules"
             - "Defer — نیاز به consultation انسان دوم"
               ↓
           اگر Defer: Issue در tracker یا backlog
           اگر Reject: discussion پایان، scope abandoned
```

---

## ۵. Examples — ۳ Case Study

### Example 1 — Proceed (T3 routine) ✅
**Scenario:** "می‌خواهیم function `calculate_pnl()` به `backend/services/portfolio.py` اضافه کنیم."

**Pre-Add Checklist:**
1. Tier: T3 ✓
2. Path: `backend/services/portfolio.py` (existing file, append) ✓
3. Naming: snake_case function ✓
4. Companion test: `tests/services/test_portfolio.py` existing — append test case
5. Reference doc impact: hiç (T3 routine، not architectural)
6. Manifest impact: none (existing file)
7. Constitution impact: none
8. State-of-record: no special entry (T3 routine)
9. Audit-ready: pytest pass plan شده
10. Review Scope: بخشی از فاز ۱ ongoing scope، no new Review

**Decision:** ✅ Proceed with Add — direct commit (e.g., `feat(portfolio): add calculate_pnl function`).

### Example 2 — Trigger Review (new T2 doc) 📋
**Scenario:** "می‌خواهیم `docs/BACKTESTING_GUIDE.md` جدید بسازیم."

**Pre-Add Checklist:**
1. Tier: T2 ✓
2. Path: `docs/BACKTESTING_GUIDE.md` (parent exists) ✓
3. Naming: UPPER_SNAKE.md ✓
4. Companion test: N/A (T2 doc)
5. Reference doc impact: یک T2 جدید است، خودش impact است
6. Manifest impact: D2 re-run خودکار در stage-end
7. Constitution impact: none (یک reference doc، نه rule)
8. State-of-record: SESSION_STATUS اضافه شدن این T2 ذکر شود
9. Audit-ready: trim/end-of-files hooks مشکل ندارد
10. **Review Scope: 🚨 جدید T2 doc per REVIEW_PROTOCOL §2.2 → Review TRIGGER**

**Decision:** 📋 Trigger Review #N — draft `docs/reviews/YYYY-MM-DD-backtesting-guide-creation.md` با Options Considered (e.g., guide format، scope، examples scope) → workflow REVIEW_PROTOCOL §6.

⚠️ **Critical (Triple-Rule prevention):** Review file create + REVIEW_LOG row insert باید **atomic در یک commit** باشد. نه دو commit مجزا — این Z-drift pattern است که خود Review #001 آن را در S2.3 اعمال کرد (یک‌جا: README + Review file + LOG row update).

### Example 3 — Defer (complex refactor) ⏸️
**Scenario:** "می‌خواهیم `backend/data_sources/` را کاملاً refactor کنیم تا data source plugin system شود."

**Pre-Add Checklist:**
1. Tier: T3 (code) + T2 impact (ARCHITECTURE.md)
2. Path: existing directory restructure
3. Naming: TBD based on plugin pattern
4. Companion test: substantial test rewrites
5. Reference doc impact: ARCHITECTURE.md نیاز به section مجزا
6. Manifest impact: significant (T3 file relocations)
7. Constitution impact: ⚠️ architecture decision در `05_architecture.md`
8. State-of-record: multiple updates لازم
9. Audit-ready: تست‌های موجود ممکن است fail شوند
10. **Review Scope: 🚨 Major Refactor per REVIEW_PROTOCOL §2.4 → Review TRIGGER**

**Decision:** 📋 Trigger Review #N — ولی scope بزرگ است. Options:
- (الف) Defer — تا فاز ۱ کامل شود (binance_client اول)
- (ب) Single Review جامع
- (ج) Split به ۳ Reviews (interface design + migration + testing)

**Recommended:** ⏸️ **Defer** — این refactor outside scope MDRS v2 است. Backlog entry برای فاز بعدی.

---

## ۶. Connection — Cross-references

| Topic | Reference |
|---|---|
| Post-trigger workflow | `docs/REVIEW_PROTOCOL.md` §6 |
| Review file template | `docs/REVIEW_PROTOCOL.md` §4 |
| Anti-patterns (non-triggers) | `docs/REVIEW_PROTOCOL.md` §3 |
| LOG structure | `docs/REVIEW_LOG.md` §2 |
| Tier definitions | `docs/PROJECT_MANIFEST.md` (Summary Statistics) |
| Tier rules implementation | `scripts/64_generate_manifest.py` TIER_RULES |
| Atomic Update rule | Rule #۲۶ + Triple-Rule chain (Rules #۲۶ + #۶۰ + #۶۶) |
| Companion test rule | Rule #۲۲ |
| No-Deletion rule | Rule #۲۴ |
| Explicit approval rule | Rule #۵۱ |

---

## ۷. Anti-patterns در این Checklist

⚠️ **این پیشگیری‌ها مهم‌اند:**

1. **Skip-the-checklist:** "این تغییر کوچکی است، چک‌لیست لازم نیست." — اگر شک دارید، چک‌لیست را اجرا کنید. ۲-۳ دقیقه time ولی نگه‌داری از drift آینده.

2. **Checklist-as-bureaucracy:** اجرای mechanical بدون درک هر check. Each check دلیلی دارد — اگر دلیلش معلوم نیست، refer به `REVIEW_PROTOCOL` یا constitution rules.

3. **Selective-checks:** فقط برخی checks اجرا کردن. ۱۰ check به ترتیب — همه یا هیچ.

4. **Forward-reference:** "Check ۱۰ بعد از write انجام می‌دهم." — نه. Check‌ها قبل از write انجام می‌شوند. این gate است، نه post-hoc audit.

5. **Hidden-checklist-completion:** "Check‌ها را در ذهن انجام دادم، نتیجه را preview نوشتم." — این مخفی است. partner (انسان یا future audit) check‌ها را نمی‌بیند. **هر check باید explicit ذکر شود** با Yes/No و reasoning کوتاه (مثل Examples §۵)، حتی اگر mental.
   
   **چرا این مهم است:**
   - Mental checking = invisible to partner
   - Partner نمی‌تواند ۱-۲ check missed را catch کند
   - Future Audit (D12/D21) impossible — audit script در metadata file چیزی برای verification نمی‌یابد
   - تجربه S2.1-S2.4: catches کاربر (Q3, Q4, Catch) نشان دادند که explicit visibility = higher catch quality

---

**نسخه:** v1.0 (S2 D7 از MDRS v2 — final D-deliverable در S2)
**ساخته توسط:** Claude در `TRADING-phase1-part03-mdrs-v2-implementation`
**Status:** Active gate برای همه pre-add decisions از این لحظه به بعد.
