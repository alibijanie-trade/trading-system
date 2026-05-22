# REVIEW_PROTOCOL — پروتکل بازنگری Artifacts جدید

> **هدف:** فرآیند ساخت‌یافته برای ارزیابی، مستندسازی، و تأیید قبل از افزودن artifact جدید به scope حاکمیتی پروژه.
> **مرتبط:** MDRS v2 (Manifest-Driven Repository Source-of-Truth)، Decision #۶۵، قوانین #۲۶ + #۶۰ + #۶۶
> **نسخه:** v1.0 (S2 D4 از MDRS v2)
> **مرتبط با:** `docs/REVIEW_LOG.md`, `docs/PRE_ADD_CHECKLIST.md`, `docs/reviews/`

---

## ۱. Purpose — چرا review لازم است

افزودن artifact جدید (قانون، درس، script، doc، architecture component) به scope حاکمیتی پروژه یک تصمیم **irreversible-by-default** است (طبق قانون #۲۴ No-Deletion). بدون trail مستند:
- "چرا این تصمیم گرفته شد؟" گم می‌شود
- alternatives بررسی‌شده reconstructable نیست
- impact غیرواضح است
- یادگرفتن از تصمیم برای آینده ناممکن می‌شود

این protocol یک trail کوچک ولی صریح ایجاد می‌کند: هر artifact غیرروتین → یک Review Report → entry در REVIEW_LOG → file در `docs/reviews/`.

---

## ۲. Triggers — چه چیزی review می‌خواهد

⚠️ **Review Report لازم است** برای موارد زیر:

### ۲.۱ Constitution Changes
- افزودن قانون جدید (#X)
- افزودن یا تغییر substantive یک درس (M-Y)
- افزودن یا تغییر یک principle در `04_principles.md`
- افزودن یا تغییر یک architecture decision در `05_architecture.md`
- atomic update version bump (e.g., v2.13 → v2.14)
- bug catalog entry جدید با implication معماری

### ۲.۲ T1/T2 Documents
- ساخت یک T1 (Constitution+State) جدید
- ساخت یک T2 (Reference Doc) جدید
- بازنویسی عمده یک T2 document (>۳۰٪ تغییر محتوا)
- حذف از scope (rename + redirect-stub، چون deletion ممنوع)

### ۲.۳ Infrastructure
- ساخت script جدید در `scripts/` با تأثیر governance/audit/automation (نه one-shot)
- تغییر `.pre-commit-config.yaml` (افزودن hook، تغییر behavior)
- تغییر `pyproject.toml`، `package.json` با dependency جدید implication‌دار
- ساخت یا تغییر CI workflow

### ۲.۴ Major Refactor
- modular split (مثل v2.12 → modular constitution)
- moving files بین tier ها (مثل Z3.13 — legacy sand-docs به archive)
- پاک‌سازی یا consolidation در سطح پروژه

### ۲.۵ Cross-cutting Decisions
- جابه‌جایی architecture (e.g., تغییر data source از X به Y)
- security model change
- license change

---

## ۳. Anti-patterns of Review — چه چیزی review نمی‌خواهد

⚠️ **اگر هر تغییری review نیاز داشته باشد، سیستم به overhead تبدیل می‌شود.** این لیست explicit از non-triggers اجتناب از این failure mode است:

### ۳.۱ Routine Code Edits (T3)
- backend function implementation طبق pattern موجود
- React component update داخل routine pattern
- pytest case افزوده
- import statement reorganization

### ۳.۲ Bug Fix (تا زمانی که architectural نباشد)
- error message clarification
- edge case handling
- typo در exception text
- one-line logic fix

🚨 **Exception:** اگر bug fix یک architectural change را reveal می‌کند (e.g., "این bug نشان داد Tier classification الگو ندارد") → review لازم است.

### ۳.۳ Cosmetic Changes
- typo correction در هر document
- punctuation fix
- whitespace normalization
- markdown formatting (heading hierarchy، list indentation)

### ۳.۴ Automated/Tool-driven Changes
- black/isort auto-format
- pre-commit `fix-end-of-files` modifications
- **pre-commit re-stage pattern (M94 candidate)** — expected workflow
- npm/pip lock-file regenerations (when versions unchanged)

### ۳.۵ Stage-end State Refresh
- `SESSION_STATUS.md` update per Triple-Rule (#۲۶+#۶۰+#۶۶)
- `CHAT_LOG.md` per-chat section append
- آمار refresh per-stage
- این‌ها **template-driven** هستند، content از stage emergent است

### ۳.۶ MDRS Manifest Regeneration
- اجرای `scripts/64_generate_manifest.py` (D2) per stage-end
- این idempotent و scan-based است — output reproducible از scope (و Z3.15 برای first-run gap)

### ۳.۷ Documentation Refresh Per Stage
- بروز `CHANGELOG.md` با entry جدید
- بروز `README.md` stats
- این‌ها follow-up template-driven از تصمیمات قبلی هستند

---

## ۴. Review Report — Structure

هر Review Report فایل `.md` در `docs/reviews/YYYY-MM-DD-{slug}.md` با ساختار زیر:

```markdown
# Review #{N} — {Subject}

> **تاریخ:** YYYY-MM-DD  
> **Trigger:** {۲.۱-۲.۵ از REVIEW_PROTOCOL}  
> **Related artifacts:** {commits، files، Z-items، lessons}  
> **Status:** Proposed | Approved | Rejected | Deferred | Implemented

## ۱. Context — چرا الان؟
{چه چیزی این review را trigger کرد؟ چه مشاهده‌ای؟ چه conversation chain؟}

## ۲. Options Considered — گزینه‌ها
1. **Option A — {نام}:** {شرح، pros، cons}
2. **Option B — {نام}:** {شرح، pros، cons}
3. **Option C — {نام}:** {شرح، pros، cons}
...
(حداقل ۲ option، توصیه ۳-۵)

## ۳. Decision — تصمیم
**Selected:** Option {X}  
**Rationale:** {چرا این انتخاب شد؟ یک یا دو پاراگراف}

## ۴. Impact — اثر
- **Files changed:** {list}
- **Commits:** {hashes}
- **Constitution impact:** {rules/lessons/principles added/changed}
- **Manifest impact:** {Z-items resolved یا added}
- **Backward compatibility:** {breaking | safe | migration needed}

## ۵. Lessons Applied — درس‌های کاربردی
- {M-X از constitution که در این تصمیم اعمال شد}

## ۶. Signatures
- Claude: {confirmation در commit message}
- User: {confirmation در commit approval}
- Commit boundary: {hash of resolving commit}
```

### ۴.۱ Status States — معنای هر state

| State | معنی | وقتی استفاده می‌شود |
|---|---|---|
| **Proposed** | Draft نوشته شده، در انتظار discussion | بعد از Step 2 (Draft) |
| **Approved** | تصمیم گرفته شده، در انتظار implementation | بعد از Step 4 (Decision) |
| **Rejected** | به‌جایی نخواهد رفت — هیچ option انتخاب نمی‌شود | جای‌گزین Approved اگر همه options رد شدند |
| **Deferred** | تصمیم به موکول شدن — نیاز به feedback انسان دوم، یا منتظر phase بعدی، یا blocker خارجی | جای‌گزین Approved اگر زمان مناسب نیست |
| **Implemented** | تغییرات commit شده و push شده، اثرات تأیید شده | بعد از Step 7 (Log Entry) |

⚠️ **Deferred ≠ Rejected.** Deferred یک halfway-state معتبر است: تصمیم در حال جریان، پایان نگرفته. باید reason explicit ذکر شود (e.g., "Deferred — منتظر T2.20 GitHub setup در S6").

---

## ۵. Filing Convention — قرارداد نام‌گذاری

### ۵.۱ Path
```
docs/reviews/YYYY-MM-DD-{slug}.md
```

- `YYYY-MM-DD`: تاریخ ISO 8601 (UTC) از زمان initiation
- `{slug}`: kebab-case، ۱-۵ کلمه، descriptive
  - مثال: `mdrs-v2-bootstrap`, `tier-rules-revision`, `legacy-sand-docs-archival`

### ۵.۲ Numbering
- IDs از `#001` شروع می‌شوند، incrementing
- Numbering در `REVIEW_LOG.md` انجام می‌شود (tracking authority)
- Reports خود ID را در heading reference می‌کنند: `# Review #042 — ...`

---

## ۶. Workflow — جریان کار

```
[Trigger detected]
       ↓
[Draft Report]  --  در claude_workspace/ یا direct در docs/reviews/
       ↓
[Discuss with User]  --  iterate options
       ↓
[Decision]  --  selected option (approval per قانون #۵۱)
       ↓
[Implement]  --  commits applying decision
       ↓
[File Report]  --  docs/reviews/YYYY-MM-DD-{slug}.md
       ↓
[Log Entry]  --  append row to REVIEW_LOG.md
       ↓
[Commit + Push]  --  per قانون #۲۶ + #۶۶
       ↓
[Status: Implemented]
```

### مرحله‌های detail:
1. **Trigger detected:** Claude یا user یک تغییر که triggers (بخش ۲) را match می‌کند تشخیص می‌دهد
2. **Draft Report:** Claude پیشنهاد می‌نویسد، شامل Options Considered substantive. Status: **Proposed**
3. **Discuss:** user و Claude در chat options را بررسی می‌کنند، refinement
4. **Decision:** option انتخاب می‌شود (با approval صریح user طبق قانون #۵۱). Status: **Approved** یا **Rejected** یا **Deferred**
5. **Implement:** commits به branch (granular sub-commits توصیه می‌شود)
6. **File Report:** Report نهایی به `docs/reviews/`
7. **Log Entry:** row جدید در `REVIEW_LOG.md`. Status: **Implemented**
8. **Commit + Push:** atomic per Triple-Rule

### ۶.۱ Iteration — Step 4 ↔ Step 5 طبیعی است

⚠️ این workflow **خطی نیست**. در عمل، **Step 4 (Decision) ممکن است در Step 5 (Implement) issue کشف کند** — مثلاً:
- "این option pre-commit hook را fail می‌کند"
- "این architecture با backend موجود سازگار نیست"
- "این naming convention با existing pattern conflict می‌کند"

در این مواقع، **return to Step 3 (Discuss) برای refinement** طبیعی است، نه failure. workflow allows این loop را:

```
Step 3 (Discuss) → Step 4 (Decision) → Step 5 (Implement) 
                                            │
                                            ├─ if smooth → Step 6 (File)
                                            └─ if issue detected → loop back to Step 3
```

این iteration باید در Report's "Decision" section explicit ذکر شود (e.g., "اولین decision در Step 4 یک issue revealed در Step 5، refined در iteration دوم").

---

## ۷. Connection با MDRS v2 Framework

این protocol بخشی از MDRS v2 (D4) است. ارتباطات:

| MDRS Artifact | Relation |
|---|---|
| `docs/PROJECT_MANIFEST.md` (D1) | Manifest scan detects new artifacts → reviewer cross-checks against REVIEW_LOG |
| `scripts/64_generate_manifest.py` (D2) | Future audit (D12 Check #?): "هر T1/T2 doc جدید باید REVIEW_LOG entry داشته باشد" |
| `docs/PRE_ADD_CHECKLIST.md` (D7) | Pre-step به این workflow — checklist قبل از reaching trigger |
| `docs/REVIEW_LOG.md` (D5) | Companion tracking log |
| `docs/reviews/` (D6) | Storage location |
| GitHub Issue Templates (D15-D18) | Complementary — issues برای discussion، reviews برای decisions |

---

## ۸. Examples

### Example 1: ✅ Review needed
**Scenario:** "می‌خواهیم rule #۶۸ جدید اضافه کنیم برای MDRS v2 enforcement."  
**Type:** Constitution Change (بخش ۲.۱)  
**Report:** Yes — `docs/reviews/2026-XX-XX-rule-68-mdrs-enforcement.md`  
**Options:** خود rule wording، sub-clauses، severity، enforcement mechanism

### Example 2: ❌ Review NOT needed
**Scenario:** "این comment در `backend/api/orders.py` typo داشت، fix کردم."  
**Type:** Cosmetic Change (بخش ۳.۳)  
**Report:** No — direct commit با clear message

### Example 3: ✅ Review needed
**Scenario:** "می‌خواهیم `scripts/65_doc_path_validator.py` جدید بسازیم برای D19."  
**Type:** Infrastructure (بخش ۲.۳) — این governance/audit script است  
**Report:** Yes — `docs/reviews/2026-XX-XX-doc-path-validator.md`

### Example 4: ❌ Review NOT needed
**Scenario:** "black فایل جدید را auto-reformat کرد، re-stage کردم."  
**Type:** Automated Change (بخش ۳.۴) — M94 pattern  
**Report:** No — این یک expected operational workflow است

---

## ۹. Anti-flooding Safeguards

برای جلوگیری از abuse و review fatigue:

### ۹.۱ Conceptual Cohesion — اصل batch‌سازی

⚠️ **Batch when (conceptual cohesion):**
- ۲+ trigger در یک stage که **همگی به یک concept واحد مربوط می‌شوند**
- مثال: `S3 Constitutional Updates` که D8-D11 + D13 با هم atomic هستند، یک Review جامع می‌خواهد، نه ۵ مستقل

⚠️ **Don't batch when (independent triggers):**
- triggers مستقل هستند، حتی اگر تعداد زیاد باشد
- batch کردن آن‌ها = مخفی‌سازی reasoning (anti-pattern Z3.8 reversal — اطلاعات critical در template تک جا hide نمی‌شود)
- مثال: `S8 cleanup` که Z3.2, Z3.6, Z3.7, Z3.8, Z3.10 شامل تصمیمات مستقل هستند، هر کدام Review خودش را می‌خواهد

🚨 **اصل کلیدی:** این **conceptual cohesion** است، نه **numeric threshold**. تعداد review مهم نیست؛ مهم coupling مفهومی triggers است.

### ۹.۲ Bootstrap Exception
Review #001 خود این protocol را اعتبارسنجی می‌کند (self-aware proof — protocol خودش از روز اول اعمال می‌شود). این یک exception معتبر است چون نمی‌توان protocol را برای ساختن خودش از قبل وجود داشته فرض کرد.

### ۹.۳ Stage-end Consolidation Reports
Review reports از یک stage **اگر conceptual cohesion داشته باشند** می‌توانند در یک "Stage Closure Review" جمع‌بندی شوند. اگر نه (per ۹.۱)، باید مستقل بمانند.

---

## ۱۰. Lessons Codified در این Protocol

این protocol درس‌های پروژه را encode می‌کند:
- **Z3.11 / M93 candidate (Triple-Rule):** workflow بخش ۶ atomic boundary تضمین می‌کند
- **Z3.8 / M88 candidate (Hidden Regeneration Hazard):** Anti-patterns بخش ۳.۶ MDRS regeneration را explicit non-trigger می‌کند (anti-pattern reversal). همچنین Anti-flooding ۹.۱ این principle را اعمال می‌کند: hiding multiple decisions در یک batch generic = همان anti-pattern reversal لازم.
- **Golden Rule:** Triggers based on role، نه git tracking
- **M94 candidate (Black retry):** Anti-patterns بخش ۳.۴ explicit recognition
- **قانون #۲۴ (No-Deletion):** Filing convention permanent record
- **قانون #۵۱ (Explicit approval):** Workflow بخش ۶ مرحله ۴

---

**نسخه:** v1.0 (S2 D4 از MDRS v2)
**ساخته توسط:** Claude در `TRADING-phase1-part03-mdrs-v2-implementation`
**Review Record:** این document خود subject Review #001 است (bootstrap self-reference) — مراجعه به `docs/REVIEW_LOG.md` و `docs/reviews/2026-05-22-mdrs-v2-review-infrastructure-bootstrap.md`
