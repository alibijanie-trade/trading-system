# Review #007 — check_1 Persian Hardening (F-B)

> **تاریخ:** 2026-05-30
> **Trigger:** §۲.۳ (Infrastructure — audit-logic change in scripts/63_pre_commit_audit.py)
> **Related artifacts:** part13 commit (this), scripts/63_pre_commit_audit.py, scripts/63b_test_pre_commit_audit.py
> **Status:** **Implemented**

## ۱. Context — چرا الان؟

F-B (یافتهٔ Phase 3): `check_1_rule_counts` برای main.md و SESSION_STATUS به regexهای ترانسلیتراسیون لاتین («sabt»، «qoflshode») تکیه داشت. ولی `to_ascii_digits` فقط **ارقام** فارسی را به ASCII تبدیل می‌کند، نه حروف — پس آن regexها هرگز با متن واقعی فارسی («ثبت‌شده»، «قفل‌شده») match نمی‌کردند. نتیجه: `main_count=None` و `session_count=None` → هیچ discrepancy → **false-PASS**. یعنی drift شمارش قوانین بین سه سند بی‌صدا رد می‌شد.

## ۲. Options Considered — گزینه‌ها

۱. **Real-Persian/structural anchors (selected):** main.md از Latin «Locked» + pipe + عدد؛ SESSION از ریشهٔ فارسی «قفل» + اولین عدد bold.
   - Pros: با متن واقعی match می‌کند؛ check_1 واقعاً مقایسه می‌کند؛ همان دام transliteration تکرار نمی‌شود.
   - Cons: literal فارسی در source (قابل‌قبول — Rule #۴۶ فقط print()/commit-message را ASCII می‌خواهد، نه string literal).
۲. **افزودن transliteration بیشتر (rejected):** هم‌خانوادهٔ ریشه‌ای bug؛ شکننده.
۳. **حذف مقایسهٔ main/session (rejected):** check_1 را بی‌اثر می‌کرد.

## ۳. Decision — تصمیم

**Selected:** Option 1.

- main.md: `re.search(r"Locked\s*\|\s*(\d+)", main_text)` → ۸۵.
- SESSION_STATUS: `re.search(r"قفل[^\n]*?\*\*(\d+)\*\*", session_text)` → ۸۵.
- «قفل» عمداً انتخاب شد چون داخلش ZWNJ ندارد (برخلاف «قفل‌شده») → match پایدار.
- **حفاظت در برابر بازگشت:** test_14 جدید assert می‌کند هم سبزبودن check_1 و هم استخراج واقعی هر دو count (نه None).

## ۴. Impact — اثر

### Files changed
- `scripts/63_pre_commit_audit.py` — بازنویسی بدنهٔ استخراج counts در `check_1_rule_counts` + docstring.
- `scripts/63b_test_pre_commit_audit.py` — افزودن `test_14_check_1_logic` (F-B regression guard) + ALL_TESTS + docstring.
- `docs/reviews/2026-05-30-check1-persian-hardening.md` — این فایل.
- `docs/REVIEW_LOG.md` — ردیف #۰۰۷.

### Behavior change
- قبل: check_1 با main/session=None، فقط count_in_rules را داشت → false-PASS.
- بعد: ۸۵ (rules) == ۸۵ (main) == ۸۵ (SESSION) → **true PASS**. اگر در آینده هر کدام drift کند → واقعاً FAIL.

### Backward compatibility
- safe: امضای تابع و registry بدون تغییر؛ فقط منطق داخلی استخراج دقیق‌تر شد.

## ۵. Lessons Applied — درس‌های کاربردی

- **M22**: companion test (test_14) mandatory.
- **M82**: read-back per edit + re-run full audit برای تأیید سبزماندن (نه false-FAIL).
- **M88 spirit / eat-your-own-dogfood:** audit خودش نباید دام transliteration داشته باشد؛ anchor واقعی استفاده شد.
- **M102 decoupling:** normative (Rule #۱ شمارش consistent) ثابت ماند؛ فقط implementation (regex) اصلاح شد.

## ۶. Signatures

- Claude: confirmed in part13 commit message + this Review file.
- User: explicit approval (F-B, part13) + درخواست re-run full audit جهت تأیید سبزماندن check_1.
- Commit boundary: part13 chat-end commit (hash recorded post-push; backfilled in part14 boot per M101).
