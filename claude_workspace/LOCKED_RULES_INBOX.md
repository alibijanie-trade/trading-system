# LOCKED RULES — Quick-Lock Inbox

> **نقش:** ثبتگاه سبک و فوری برای قوانینی که کاربر «اجباری و قفل‌شده» اعلام می‌کند.
> **اصل کلیدی (Quick-Lock):** قفل‌کردن یک تصمیم سادهٔ کاربر است و **فوراً لازم‌الاجرا** می‌شود — بدون نیاز به version bump، Decision، Review یا batch چندفایلی. نسخه‌بندی رسمیِ constitution (تبدیل به #/M + bump) به‌صورت **ادواری/دسته‌ای** و در زمان دلخواه کاربر انجام می‌شود.

---

## 🔒 مکانیزم Quick-Lock (پروتکل)

1. وقتی کاربر گفت «این را قفل/اجباری کن» (یا معادلش)، Claude **فقط یک ردیف** به جدول زیر append می‌کند (#۲۴ append-only): شناسهٔ موقت QL-N، تاریخ، متن کامل و صریح قانون (#۸۸)، قانون/درس مرتبط، وضعیت.
2. از همان لحظه برای Claude **binding** است (هم‌سطح قواعد Locked؛ در تعارض، آخرین دستور صریح کاربر مرجع است).
3. **هیچ** version bump / Decision / Review در زمان قفل لازم نیست. این تفکیکِ صریحِ «قفل‌کردن (ارزان، فوری)» از «codify رسمی (ادواری، دسته‌ای)» است.
4. این فایل در **هر boot** خوانده می‌شود (در STEP 1 mandatory reads ثبت شده) تا قوانین قفل‌شده فعال بمانند.
5. codify رسمی (افزودن به 01_rules/02_lessons + bump + Decision + Review) **ادواری** انجام می‌شود؛ پس از codify، ردیف اینجا با وضعیت `CODIFIED → #/M` علامت می‌خورد (حذف نمی‌شود، #۲۴).
6. خود این مکانیزم هم یک قانون قفل‌شده است (QL-0).

---

## 📋 جدول قوانین قفل‌شده (binding، فعال)

| QL | تاریخ | متن قانون (binding) | مرتبط | وضعیت |
|----|-------|----------------------|-------|--------|
| QL-0 | 2026-05-31 | **مکانیزم Quick-Lock:** قفل‌کردن = append یک‌خطی اینجا + binding فوری، بدون batch/bump/Decision؛ codify رسمی ادواری و به‌خواست کاربر. این فایل هر boot خوانده شود. Genesis: اصطکاکِ part19 (هر قفل ساده به batch ۱۰فایلی تبدیل می‌شد). | process · #۸۷/#۸۸ | ACTIVE — pending periodic codify |
| QL-1 | 2026-05-31 | **Manual-Box Full-Text Protocol:** پیش از هر به‌روزرسانی هر یک از سه کادر دستی (Settings→General / Project Instructions / Project Knowledge)، Claude باید (۱) **اول** متن کامل فعلی کادر را ببیند (از آینهٔ `claude_workspace/manual_boxes/` با verify last-sync؛ یا اگر آینه مطمئن نیست از کاربر paste بخواهد)، سپس (۲) **کل متن نهایی** را یک‌جا (select-all→paste) تحویل دهد. تحویل قطعه‌ای/partial با «اضافه/کم کن» **ممنوع مطلق**. آینه پس از هر تحویل به‌روز و read-back شود. Genesis: overwrite سهوی part19. | تشدید #۸۷ (Full-Text Delivery) | ACTIVE — pending codify (P19-candidate-4) |
| QL-2 | 2026-05-31 | **Per-Task Write Approval Granularity:** پس از تأیید یک task توسط کاربر و شروع تهیهٔ کد/فایل، write/edit بعدیِ همان task نیاز به اجازهٔ مجدد per-file ندارد (تأیید در سطح task/Scope-Contract، نه per-write)؛ مشروط بر dryRun/preview + read-back (M60/M82) و مکث فقط هنگام «تصمیم جدید»؛ گاردهای #۵۱ پابرجا (هرگز .env / خارج از مسیر / حذف دائمی؛ تأیید untracked ناشناخته قبل از add -A). | تبصرهٔ #۵۱ | ACTIVE — در Project Instructions هم هست (P19-candidate-3) |

---

## 📌 یادداشت

- این فایل source-of-truth برای قوانین Quick-Lockشده است؛ محتوای آن هرگز در حافظهٔ چت بازسازی نشود — همیشه از disk خوانده شود (هم‌راستا #۸۶).
- هنگام codify رسمی، ردیف‌ها به‌جای حذف، `CODIFIED → #N/MN` می‌گیرند (#۲۴).

**آخرین به‌روزرسانی:** part19 (2026-05-31) — ایجاد inbox + ثبت QL-0/QL-1/QL-2.
