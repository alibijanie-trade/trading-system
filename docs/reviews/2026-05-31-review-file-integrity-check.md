# Review #012 — Review LOG<->file Integrity Check (check_13)

> **تاریخ:** 2026-05-31
> **Trigger:** §۲.۳ (audit script change — افزودن check_13 + companion test، هم‌کلاس Review #۰۰۶/#۰۰۷)
> **Related artifacts:** scripts/63_pre_commit_audit.py, scripts/63b_test_pre_commit_audit.py, docs/REVIEW_LOG.md, docs/reviews/2026-05-30-settings-instructions-sync-reminder.md, docs/reviews/2026-05-30-ai-optimized-authoring-standard.md
> **Status:** **Implemented**

## ۱. Context — چرا الان؟

در boot part19، هنگام M101 backfill هش part18 (طبق handoff §۲)، کشف شد ردیف‌های Review **#۰۱۰** و **#۰۱۱** در `REVIEW_LOG.md` وجود دارند (Status=Implemented) ولی فایل‌های متناظرشان در `docs/reviews/` **ساخته نشده بودند**. part18 هنگام codify فقط rowها را ساخت.

علت ریشه‌ای (تأیید‌شده از خواندن کد): `check_10_review_numbering` فقط **پیوستگی شماره‌ها** را در جدول LOG چک می‌کند، نه **وجود فایل**. چون #۰۱۰/#۰۱۱ متوالی بودند، check_10 PASS داد و شکاف silent ماند. این دقیقاً همان چیزی است که `REVIEW_LOG §۴` آرزو کرده («هر file یک row و برعکس») ولی در کد پیاده نشده بود.

این Review اقدام **مکانیکی** را مستند می‌کند — هم‌راستا meta-deliverable «reliability-audit» (part18): تبدیل یک تضمین رفتاری/آرزویی به یک check مکانیکی.

## ۲. Options Considered — گزینه‌ها

۱. **Option A — check_13 جدا (Review LOG↔file integrity)** (selected)
   - Pros: single-responsibility (SOLID)؛ منطق تست‌شدهٔ check_10 (numbering) دست‌نخورده؛ عین الگوی افزودن check_12 (part13)
   - Cons: یک check بیشتر (۱۲→۱۳)
۲. **Option B — گسترش check_10 به numbering + file existence**
   - Cons: تغییر منطق تست‌شدهٔ موجود؛ نام/مسئولیت check_10 مبهم می‌شود
۳. **Option C — صرفاً یادآوری رفتاری (بدون check)**
   - Cons: رفتاری، نامطمئن — همان شکست اولیه را تکرار می‌کند (M87/M103 spirit: نوشتن قانون ≠ رعایت)

## ۳. Decision — تصمیم

**Selected:** Option A (check_13 جدا).

**Rationale:**
- single-responsibility: check_10 = numbering، check_13 = LOG↔file existence — دو مسئولیت متمایز
- کم‌ریسک‌تر: منطق check_10 (که تست‌های test_10/regression دارد) تغییر نمی‌کند
- precedent: check_12 هم به‌جای overload یک check موجود، جدا اضافه شد (part13)
- اقدام مکانیکی (نه رفتاری) — مستقیماً recurrence را می‌بندد

## ۴. Impact — اثر

### Files changed (در commit part19)
- `scripts/63_pre_commit_audit.py` — افزودن `check_13_review_file_integrity` (دوطرفه row↔file + slug match via filename + heading-ID match) + ثبت در `ALL_CHECKS` + constant `REVIEWS_DIR` + docstring + help text (1-12→1-13)
- `scripts/63b_test_pre_commit_audit.py` — test_15 (check_13 runs) + test_16 (check_13 logic PASS) + به‌روزرسانی test_2 (12→13) + docstring/comment
- `docs/reviews/2026-05-30-settings-instructions-sync-reminder.md` — backfill (Review #۰۱۰، A1)
- `docs/reviews/2026-05-30-ai-optimized-authoring-standard.md` — backfill (Review #۰۱۱، A1)
- `docs/REVIEW_LOG.md` — backfill resolution #۰۱۰/#۰۱۱ (`29b2b56`) + ردیف جدید #۰۱۲ (این Review)
- `claude_workspace/PHASE_LEDGER.md` — backfill هش frontier part18 (`a6e7625`) + ردیف part19 (chat-end)
- `docs/PENDING_FOR_NEXT_VERSION.md` — Discovery part19-1 + P19-candidate-3
- `docs/reviews/2026-05-31-review-file-integrity-check.md` — این فایل

### Audit/test coupling
- audit checks: ۱۲ → **۱۳** (افزودن check_13)
- companion tests: ۱۴ → **۱۶** (test_15 + test_16)
- check_13 پس از A1 باید PASS دهد (۱۲ row ↔ ۱۲ file؛ README مستثنا)
- check_10 (numbering) → ۰۰۱-۰۱۲ متوالی، بدون gap

### Constitution impact
- هیچ — این تغییر T3 (code) + governance trail است، نه قانون/درس جدید. version بدون تغییر (v2.17).

### Backward compatibility
- safe: check_1..12 دست‌نخورده؛ check_13 additive

## ۵. Lessons Applied — درس‌های کاربردی

- **M82/#۸۴ (verify نه فرض)**: علت ریشه‌ای از **خواندن کد واقعی** check_10 استخراج شد، نه فرض؛ شکاف با list_directory تأیید شد ✅
- **#۸۶/M104 (منبع زنده)**: هش‌های backfill از `git log` زنده گرفته شدند (`a6e7625` frontier، `29b2b56` codify)، نه از عدد ثابت handoff (`041b80e` که stale بود) ✅
- **meta-deliverable reliability-audit (part18)**: تبدیل تضمین رفتاری → مکانیکی (check) ✅
- **SOLID (single-responsibility)**: check_13 جدا به‌جای overload check_10 ✅
- **#۲۲ (companion test)**: test_15 + test_16 همراه ✅
- **M101/M77**: Resolution این Review بدون hash literal (placeholder + backfill چت بعد) ✅
- **dogfood**: ساخت فایل review #۰۱۲ خودش نمونهٔ بستن شکاف است (row + file اتمیک، نه فقط row) ✅

## ۶. Signatures

- Claude: confirmed (part19 commit + این فایل)
- User: explicit approval (scope A1-A6 + check_13 جدا + دستور «ثبت + اقدام جلوگیری» part19)
- Commit boundary: `dcb5c20` (part19 — commit افزودن check_13 + companion tests)
