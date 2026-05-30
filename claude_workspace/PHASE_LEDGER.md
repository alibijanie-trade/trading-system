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
| part17 | boot کامل (M101 backfill part16=`81a3562` ✅) + **Phase 3 — ۴ Batch**: B4 stale/cosmetic (main.md branch+created-commit `5285fb6`+خط۱۷۷، test_2 «11»→«12»، boot-template ref→modular) · B1 deprecate ۱۰ سند legacy + **Review #۰۰۹** · B2 بازسازی PROJECT_KNOWLEDGE→v2.16 (#۵۵) · B3 catch-up README/CHANGELOG/TASK_BACKLOG (scoped) · P17-candidate (#۶۱ elicitation drop). **B5 + موارد موکول → PART18.** | chat-end part17 = `<backfill در PART18 boot، M101>` |

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
- ⏳ معلق (→PART18، عمدتاً B5): DECISIONS_LOG drift backfill · resolution REVIEW_LOG #۰۰۱/#۰۰۳/#۰۰۹ با hash (git) · PERSIST TASKS A-G verify · workspace Tier · `Created in commit` سایر ماژول‌ها (01/02/06) · CHANGELOG [0.6.0] (تاریخ git) · TASK_BACKLOG Tier reconcile · تصمیمات Settings (موکول)
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
- **`<chat-end part17>`** = chat-end part17 (B4+B1+B2+B3 + Review #۰۰۹ + این ردیف Ledger + PART18 handoff + SESSION_STATUS) — backfill در PART18 boot (M101)
- مرجع تاریخی: `234ba2f` (S4 part09) · `3fd2405` (S3.4 chat-end part08) · `35ea822` (S3.3 part08) · `5730173` (tag v0.6.0 main)

---

## 🔴 DEADLINEهای فعال
- ✅ **check_12_continuity — DONE part13** (DEADLINE رعایت شد؛ Review #۰۰۶؛ audit ۱۲/۱۲ runtime-verified). از این پس دوحلقه مکانیکی enforce می‌شود.
- ✅ **full-refresh وضعیت‌نامه — DONE part14-15** (SESSION_STATUS/CHAT_LOG/PENDING/MANIFEST atomic در commit اتمیک part14-15؛ Triple-Rule معوق part09 بسته شد).

---
**📌 پایان PHASE_LEDGER.md — append-only؛ هر چت در chat-end حلقهٔ ۱ را اینجا می‌زند.**
