# 📒 PHASE_LEDGER — دفترچهٔ تجمعی همیشه‌زندهٔ پروژه

> **هدف:** یک source-of-truth واحد و **append-only** که قصهٔ کل پروژه را از یک فایل قابل‌خواندن نگه می‌دارد — مستقل از کامل‌بودن حلقه‌های میانی HANDOFF.
> **سیاست:** append-only (Rule #۲۴ No-Deletion). هیچ ردیف حذف نمی‌شود؛ فقط افزوده/به‌روزرسانی state.
> **ساخته‌شده:** part12 (2026-05-30) — per دستور کاربر (ارتقای قانون تداوم تک‌حلقه → دوحلقه).
> **Branch:** `infra/v2.14-source-of-truth`

---

## ⭐ قانون تداوم دوحلقه‌ای (canonical — جایگزین نسخهٔ تک‌حلقه)

هر چت در chat-end، **به این ترتیب**:

1. **حلقهٔ ۱ (Ledger) — اول:** چند خط به جدول «خلاصهٔ هر چت» این فایل append کن (بدون حذف) + وضعیت زندهٔ ۳ Objective + HEAD/hashهای مهم + DEADLINEها را به‌روز کن.
2. **حلقهٔ ۲ (Handoff) — بعد:** فایل `PHASE1_PART{N+1}_HANDOFF.txt` دلتای خود را بساز (اهداف کامل + اصل حاکم «جامعیت > یک‌چت» + شرط escape + همین قانون تداوم دوحلقه‌ای).
3. هر دو را در **یک commit** ثبت کن (read-back M82) + push (Rule #۶۶) + متن paste بده.

**چرا دوحلقه:** زنجیرهٔ تک‌حلقه شکننده است — اگر یک چت forward نکند، بعدی‌ها کور می‌شوند. **مدرک:** `PART10` و `PART11` handoff اصلاً ساخته نشدند (زنجیره یک‌بار شکست). این Ledger تجمعی شکست را جبران می‌کند: چت N+k با خواندن همین یک فایل کل قصه را می‌بیند.

**Enforcement مکانیکی:** ✅ `check_12_continuity` در `scripts/63_pre_commit_audit.py` — **پیاده‌سازی شد در part13** (file-based، invariant H==L+1؛ Review #۰۰۶؛ audit ۱۲/۱۲ runtime-verified). از این پس قانون دوحلقه مکانیکی enforce می‌شود، نه صرفاً دستورالعمل.

---

## 📊 خلاصهٔ هر چت (append-only)

| چت | خلاصه (۲-۳ خط) | commitهای مهم |
|---|---|---|
| part01–08 | بنیاد (FastAPI+React) + Auth + Frontend + Governance ۱۲-سندی + Tier2 + Constitution modular + MDRS v2 تا **Stage S3 COMPLETE** | tag `v0.6.0`=`5730173` · S3.3=`35ea822` |
| part09 | S4 (D12 Audit Checks #۸–۱۱) + Z3.15/16/17/25 RESOLVED. chat-end Triple-Rule **defer** شد (HM-2 escape) | `234ba2f` |
| part10 | Infrastructure Sprint + audit session؛ کشف الگوی over-promise (**M103 genesis**). boot دوبار escape (HM-9 #9/#10). **PART10 handoff ساخته نشد** | HEAD `90db89f` (بدون تغییر) |
| part11 | codify ۸ Trust Rule **#۷۸–۸۵** + درس **M103** → Constitution **v2.15**. audit 11/11 PASS. **PART11 handoff ساخته نشد** (مستقیم PART12) | codify=`59c075a` · handoff part12=`bb964cf` |
| part12 | boot کامل + verify ۴/۴ فایل غول فاز ۲ (۷ یافته، همه Phase 3) + backfill `59c075a` در REVIEW_LOG #۰۰۵ و review#005 §۴/§۶ + **Phase 2 CLOSED** + پایه‌گذاری این Ledger + قانون تداوم دوحلقه‌ای | chat-end part12 = `5173e6f` |
| part13 | boot کامل + M101 backfill part12=`5173e6f` (Ledger/CHAT_LOG) · **#۰ check_12_continuity ساخته شد** (file-based، invariant H==L+1، chicken-and-egg-safe) + test_12/13 · **F-A** DECISIONS_LOG→v1.4 · **F-B** check_1 سخت‌سازی (Latin→Persian anchor؛ true-PASS ۸۵/۸۵/۸۵) + test_14 · **F-C** backfill #۰۰۲=`3fd2405`/#۰۰۴=`234ba2f` · Review #۰۰۶/#۰۰۷. audit ۱۲/۱۲ + tests ۱۴/۱۴ PASS | chat-end part13 = `3eae91e` |
| part14-15 | full-refresh اتمیک + reconcile: M101 backfill part13 (`3eae91e`) + بازنویسی SESSION_STATUS (part08→part13) + CHAT_LOG part09-13 + PENDING reconcile part09-13 + آشتی count + Z3.15/16/17/25 RESOLVED-mark + manifest D2 (Total=282، T1=28) + بستن Triple-Rule معوق part09 + P-candidate M104/#۸۶ (escape↔check_12 off-by-one). part14=full-refresh، part15=reconcile+manifest+commit+chat-end | chat-end part14-15 = `c30dbe5` |
| part16 | boot کامل (M101 backfill part14-15=`c30dbe5` ✅) + **codify v2.16**: درس **M104** + قانون **#۸۶** (Escape-Aware Sequence Derivation) در ۱۱ فایل اتمیک + Review #۰۰۸ + Decision #۶۸ + PENDING P-candidate→CODIFIED. audit ۱۲/۱۲ + companion ۱۴/۱۴ PASS (دستی + هوک pre-commit) | codify=`8c9c6a7` · chat-end=`81a3562` |
| part17 | boot کامل (M101 backfill part16=`81a3562` ✅) + **Phase 3 — ۴ Batch**: B4 stale/cosmetic (main.md branch+created-commit `5285fb6`+خط۱۷۷، test_2 «11»→«12»، boot-template ref→modular) · B1 deprecate ۱۰ سند legacy + **Review #۰۰۹** · B2 بازسازی PROJECT_KNOWLEDGE→v2.16 (#۵۵) · B3 catch-up README/CHANGELOG/TASK_BACKLOG (scoped) · P17-candidate (#۶۱ elicitation drop). **B5 + موارد موکول → PART18.** | chat-end part17 = `55f4f66` |
| part18 | boot کامل (M101 backfill part17=`55f4f66` ✅) + **codify v2.17**: ۲ قانون Locked **#۸۷** (Settings/Instructions/Project-Asset Sync Reminder + Materiality Threshold + Full-Text Delivery) + **#۸۸** (AI-Optimized Authoring) در batch اتمیک (۱۰ فایل) + Review #۰۱۰/#۰۱۱ + Decision #۶۹/#۷۰ + main bump v2.17 (۸۸ قانون، M1-M105، ۱۱ Review) + audit CURRENT_VERSION→v2.17 + .pre-commit label. **پلاس درس M105** (EXECUTE `&`-chain Paste-Integrity) + **B5 drift-backfill ۷/۷** (Created-in-commit non-literal · REVIEW resolution #۰۰۱=`35a634f`/#۰۰۳=`3bf66bf`/#۰۰۸=`8c9c6a7` · DECISIONS drift=۰ · PERSIST TASKS main-side✓ helper-side DEFER · workspace Tier verify · CHANGELOG [0.6.0]=2026-05-22 · TASK_BACKLOG SUPERSEDED). audit ۱۲/۱۲ + companion ۱۴/۱۴ PASS (دستی، با self-catch check_2 M75). | chat-end part18 = `a6e7625` |
| part19 | boot کامل (تأیید STEP 2/3) + M101 backfill part18 frontier=`a6e7625` (نه `041b80e` stale، از git زنده). **کشف drift REVIEW_LOG↔file** (#۰۱۰/#۰۱۱ بدون فایل؛ علت: check_10 فقط numbering) → ساخت ۲ فایل review + **check_13** (دوطرفه row↔file + slug + heading) + test_15/16 + **Review #۰۱۲** (commit `dcb5c20`). · **CHAT_LOG catch-up** part14→part18 (commit `104abf0`). · **بازیابی Project Instructions** پس از overwrite سهوی + **Quick-Lock** (LOCKED_RULES_INBOX: QL-0 مکانیزم / QL-1 Manual-Box Full-Text / QL-2 per-task write) + boot template (commit `a6300ce`). audit **۱۳/۱۳** + tests **۱۶/۱۶** PASS. | chat-end part19 = `5de05e0` |
| part20 | boot کامل (M101 backfill part19=`5de05e0` در چت 20 انجام شد) + **governance repair Batch 1**: header v2.14→v2.17 در ۶ ماژول + LOCKED_RULES_INBOX در Quick-start main.md + PHASE_LEDGER در STEP 1 boot template + SESSION_STATUS rewrite از part13→part19. **Batch 2**: split 01_rules.md→01a_rules_core.md (boot-critical ~25KB) + shell standard CMD→PowerShell در بخش ۱.۷. در این چت متن چت 20 (docx) نیز خوانده شد و با کارها تطبیق داده شد (QL-6 ثبت، Scope Contract v2.18 آماده). | chat-end part20 = `17bb60a` ✅ |

> 🔎 **شکاف زنجیره (یک‌خطی، per دستور کاربر — نه بازسازی کامل):** part10 = escape (هیچ handoff) · part11 = codify (هیچ handoff، مستقیم به PART12). تاریخچهٔ ۱۱→۱۲ از همین Ledger خوانده می‌شود.

---

## 🎯 وضعیت زندهٔ سه Objective

### Objective 1 — Phase 2 (Trust Rules codify → v2.15)
✅ **CLOSED در part12.** codify `59c075a` (audit 11/11) + verify ۴/۴ فایل غول کامل + backfill #۰۰۵ (`59c075a`) اعمال و read-back شد. صحت محتوای #۷۸–۸۵/M103/#۶۷ تأیید شد، آسیب جانبی ۰.

### Objective 2 — Phase 3 (Remediation + full refresh)
⏳ IN PROGRESS — part13 یک batch بست؛ full-refresh سنگین → part14.
- ✅ **#۰ check_12_continuity — DONE part13** (file-based، H==L+1، chicken-and-egg-safe؛ test_12/13؛ Review #۰۰۶؛ audit ۱۲/۱۲ runtime-verified)
- ✅ **F-A** DECISIONS_LOG header+footer → v1.4 (2026-05-30، بازتاب #۶۷)
- ✅ **F-B** check_1 سخت‌سازی (Latin→Persian/structural anchor؛ true-PASS ۸۵/۸۵/۸۵؛ test_14؛ Review #۰۰۷)
- ✅ **F-C** backfill M101: #۰۰۲=`3fd2405` (S3.4 part08) · #۰۰۴=`234ba2f` (S4)
- ✅ **DONE part14-15** (full-refresh اتمیک): بازنویسی SESSION_STATUS (part08→part13) + CHAT_LOG (part09-13) + PENDING reconcile (part09-13 + آشتی count + Z3.15/16/17/25) + PROJECT_MANIFEST D2 (Total=282) + بستن Triple-Rule معوق part09 (M93/#۷۳) + P-candidate M104/#۸۶ ثبت‌شد (codify v2.16 در part16)
- ✅ **DONE part16** (codify v2.16): M104 + #۸۶ Locked + main bump (۸۶ قانون، M1-M104، ۸ Review) + Review #۰۰۸ + Decision #۶۸ + audit CURRENT_VERSION→v2.16 (ACCEPTABLE v2.14/15/16) + .pre-commit label + PENDING P-candidate→CODIFIED. codify=`8c9c6a7`، audit ۱۲/۱۲ + companion ۱۴/۱۴ (دستی + هوک)
- ✅ **DONE part17** (Phase 3، ۴ Batch): B4 (stale/cosmetic: main.md branch/created-commit `5285fb6`/خط۱۷۷، test_2، boot-template ref) · B1 (deprecate ۱۰ legacy + Review #۰۰۹) · B2 (PROJECT_KNOWLEDGE→v2.16، #۵۵) · B3 (catch-up README/CHANGELOG/TASK_BACKLOG، scoped)
- ✅ **DONE part18** (codify v2.17 + B5): قوانین **#۸۷/#۸۸** Locked + درس **M105** + Review #۰۱۰/#۰۱۱ + Decision #۶۹/#۷۰ + main bump v2.17 + audit→v2.17. **B5 drift-backfill ۷/۷ بسته شد**: REVIEW resolution #۰۰۱=`35a634f`/#۰۰۳=`3bf66bf`/#۰۰۸=`8c9c6a7` (همه git-verified) · Created-in-commit non-literal · DECISIONS drift=۰ · PERSIST TASKS main-side✓ helper-side DEFER · workspace Tier verify · CHANGELOG [0.6.0] · TASK_BACKLOG SUPERSEDED. audit ۱۲/۱۲ + companion ۱۴/۱۴
- 🔮 معلق (helper-side، خارج دسترس): HM-META-H/I/J/K + W4-W5 (منبع helper chat part09 — fabricate نمی‌شود) · تصمیمات Settings/connector (موکول) · CHAT_LOG.md sections part15-18 (boot observation، خارج B5 scope)
- ارتقای تداوم دوحلقه‌ای: ✅ پایه part12 + ✅ enforcement مکانیکی (check_12) part13

### Objective 3 — Phase 4 (اسکن ۱۰۰٪ ۲۷۸ فایل classified)
🔮 TODO — part13+. با Scope Contract (Rule #۷۸) + گزارش N/M (Rule #۷۹) + بدون pattern-matching (Rule #۸۴).

---

## 🔑 HEAD و hashهای مهم
- Branch فعال: `infra/v2.14-source-of-truth`
- `59c075a` = Phase 2 codify (part11، push شده)
- `bb964cf` = PHASE1_PART12_HANDOFF (part11 chat-end، push شده)
- **`5173e6f`** = chat-end part12 (backfill #۰۰۵ + این Ledger + PART13 handoff + commit_msg) — M101 backfill ثبت‌شده در boot part13 (per user git)
- **`3eae91e`** = chat-end part13 (check_12 + F-A/B/C + Review #۰۰۶/#۰۰۷ + این به‌روزرسانی Ledger + PART14 handoff)
- **`c30dbe5`** = chat-end part14-15 (full-refresh + reconcile + manifest D2=282 + این ردیف + PART16 handoff + P-candidate M104/#۸۶) — backfill در part16 boot (M101) ✅ انجام شد
- **`8c9c6a7`** = codify v2.16 part16 (M104 + #۸۶ + Review #۰۰۸ + Decision #۶۸ + M101 backfill c30dbe5 folded؛ push شد)
- **`81a3562`** = chat-end part16 (این ردیف Ledger + PART17 handoff + SESSION_STATUS pointer) — backfill در part17 boot (M101) ✅ انجام شد
- **`55f4f66`** = chat-end part17 (B4+B1+B2+B3 + Review #۰۰۹ + این ردیف Ledger + PART18 handoff + SESSION_STATUS) — backfill در PART18 boot (M101) ✅ انجام شد
- **`a6e7625`** = chat-end part18 frontier (codify v2.17 [#۸۷/#۸۸ + M105 + B5 ۷/۷] در `29b2b56` ← زنجیره: `5876f20` → `7199739` → sweep `041b80e` → `a6e7625` (handoff/reliability-audit note)) — backfilled در boot part19 (M101، از git زنده)
- **`5de05e0`** = part19 chat-end (ردیف Ledger part19 + PART20 handoff + backfill #۰۱۲=`dcb5c20`) — backfill هش در boot part20 (M101، از git ref زنده). زنجیرهٔ commitهای part19: `dcb5c20` (check_13/Review #۰۱۲) → `104abf0` (CHAT_LOG catch-up) → `a6300ce` (Quick-Lock + بازیابی کادر) → chat-end (این commit).
- مرجع تاریخی: `234ba2f` (S4 part09) · `3fd2405` (S3.4 chat-end part08) · `35ea822` (S3.3 part08) · `5730173` (tag v0.6.0 main)

---

## 🔴 DEADLINEهای فعال
- ✅ **check_12_continuity — DONE part13** (DEADLINE رعایت شد؛ Review #۰۰۶؛ audit ۱۲/۱۲ runtime-verified). از این پس دوحلقه مکانیکی enforce می‌شود.
- ✅ **full-refresh وضعیت‌نامه — DONE part14-15** (SESSION_STATUS/CHAT_LOG/PENDING/MANIFEST atomic در commit اتمیک part14-15؛ Triple-Rule معوق part09 بسته شد).

- **`17bb60a`** = chat-end part20 (governance repair Batch 1+2 — 12 files changed, 493 insertions) — backfill انجام شد ✅

---
**📌 پایان PHASE_LEDGER.md — append-only؛ هر چت در chat-end حلقهٔ ۱ را اینجا می‌زند.**
