# Review #006 — Continuity Audit Check (check_12, two-loop chain)

> **تاریخ:** 2026-05-30
> **Trigger:** §۲.۳ (Infrastructure — extension of scripts/63_pre_commit_audit.py)
> **Related artifacts:** part13 commit (this), scripts/63_pre_commit_audit.py, scripts/63b_test_pre_commit_audit.py, claude_workspace/PHASE_LEDGER.md, claude_workspace/incoming_permanent/PHASE1_PART{N}_HANDOFF.txt
> **Status:** **Implemented**

## ۱. Context — چرا الان؟

قانون تداوم دوحلقه‌ای (در `PHASE_LEDGER.md` + PHASE1_PART13_HANDOFF) تا اینجا فقط دستورالعمل بود و به پایبندی هر چت متکی. شکست تک‌حلقه دوبار رخ داد: handoff های part10 و part11 اصلاً ساخته نشدند (زنجیره کور شد). آیتم #۰ Phase 3 با DEADLINE قطعی پایان part13: enforcement مکانیکی این قانون به‌صورت یک audit check.

scope بسته per HANDOFF بند #۰:
- `check_12_continuity` در `scripts/63_pre_commit_audit.py`
- companion test (Rule #۲۲)
- ردیف REVIEW_LOG #۰۰۶ + همین فایل

## ۲. Options Considered — گزینه‌ها

### محور ۱ — منبع تشخیص «چت جاری»
۱. **Option 1-A — file-based (selected):** L = آخرین ردیف part در جدول خلاصهٔ `PHASE_LEDGER.md`؛ H = بزرگ‌ترین N در `PHASE1_PART{N}_HANDOFF.txt`. بدون git در hook.
   - Pros: deterministic، بدون وابستگی به git/branch روی Windows، مطابق روح check (همان فایل‌هایی که دو حلقه تولید می‌کنند).
   - Cons: به نام canonical handoff وابسته است.
۲. **Option 1-B — git-parse (rejected):** شمارهٔ چت از branch/commit message. شکننده روی CMD/Windows، خلاف الگوی file-based بقیهٔ checkها.

### محور ۲ — سطح Review
۱. **Option 2-A — فایل کامل + ردیف LOG، atomic (selected):** مطابق Rule #۶۹/#۷۵ و precedent #۰۰۴.
۲. **Option 2-B — فقط ردیف LOG (rejected):** سبک‌تر ولی trail ناقص برای یک governance-enforcement جدید.

## ۳. Decision — تصمیم

**Selected:** Option 1-A + Option 2-A (تأیید صریح کاربر در part13).

**Invariant:** `H == L + 1`.

- **chicken-and-egg fix (نکتهٔ کلیدی کاربر):** «چت جاری = آخرین HANDOFF موجود (H)»، نه «چت در حال انجام». ردیف part خودِ چت و handoff بعدی فقط در chat-end همان چت ساخته می‌شوند؛ پس حین اجرای چت H، مقدار L روی H-1 می‌ماند و check **سبز** است (اکنون: L=۱۲، H=۱۳ → ۱۳==۱۲+۱ → PASS). در chat-end، هر دو با هم جلو می‌روند (L→H، H→H+1) و invariant حفظ می‌شود.
- **FAIL ها:** `H==L` → handoff بعدی غایب (نقض حلقهٔ ۲)؛ `H>=L+2` → ردیف ledger غایب (نقض حلقهٔ ۱، M23/M101)؛ `H<L` → ناسازگار.
- **تحمل عمدی gap زیر frontier:** نبود PART10/PART11 (تاریخی، مستند در ledger) check را نمی‌شکند؛ فقط frontier (آخرین مرز) محافظت می‌شود.

## ۴. Impact — اثر

### Files changed
- `scripts/63_pre_commit_audit.py` — افزوده: تابع `check_12_continuity` + ۴ constant (PHASE_LEDGER_MD، INCOMING_PERMANENT، HANDOFF_PATTERN، LEDGER_PART_ROW_PATTERN) + ثبت در `ALL_CHECKS` + docstring coverage + argparse help (۱-۱۱ → ۱-۱۲).
- `scripts/63b_test_pre_commit_audit.py` — افزوده: test_12 (runs) + test_13 (logic) + به‌روزرسانی test_2 (۱۱ → ۱۲) + ALL_TESTS + docstring.
- `docs/reviews/2026-05-30-continuity-audit-check.md` — این فایل.
- `docs/REVIEW_LOG.md` — ردیف #۰۰۶.

### Constitution impact
- هیچ rule جدید/تغییر، هیچ lesson جدید (M-list unchanged M1-M103). این صرفاً enforcement مکانیکی Rule #۶۲ موجود است.

### Backward compatibility
- safe: ۱۱ check موجود بدون تغییر، check_12 additive. runner از `len(ALL_CHECKS)` پویا استفاده می‌کند؛ `--check` range خودکار ۱-۱۲ شد.

### Manifest impact
- D2 re-run در full-refresh chat-end (per Z3.21): ۲ T3 file content hash changed.

## ۵. Lessons Applied — درس‌های کاربردی

- **M22**: companion test mandatory (test_12 + test_13).
- **M82**: read-back per edit.
- **M88 reversal:** بدون hardcoded list؛ منبع authoritative = خودِ فایل‌های ledger/handoff؛ شمارش پویا via `len()`.
- **F-B avoidance (eat-your-own-dogfood):** برخلاف `check_1` که به برچسب لاتین «sabt» تکیه دارد (که `to_ascii_digits` تولیدش نمی‌کند)، check_12 از anchor ساختاری زبان‌مستقل (`^| partNN`) استفاده می‌کند؛ همان دام F-B تکرار نشد.
- **M77/M101/HM-5 (chicken-and-egg):** invariant frontier طوری طراحی شد که self-reference چت جاری را درست هندل کند.
- **M98 Scope Closure:** فقط #۰؛ F-A/F-B/F-C و full-refresh جدا.
- **M102 decoupling:** check_12 enforcement مکانیکی Rule #۶۲ normative است (interface/implementation جدا).
- **M99 + M95/M97:** commit با `-F` و ASCII در chat-end.

## ۶. Signatures

- Claude: confirmed in part13 commit message + this Review file.
- User: explicit approval — Option 1-A + 2-A (part13).
- Commit boundary: part13 chat-end commit (hash recorded post-push; backfilled in part14 boot per M101).
