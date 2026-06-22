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
| QL-3 | 2026-05-31 | **Next-Chat-Name Declaration (chat-end):** در هر chat-end، Claude باید **صریحاً نام چت بعد** را طبق الگوی HM-3 (`TRADING-phase{N}-part{NN}-{topic-slug}`) به کاربر اعلام کند — علاوه بر ثبت در handoff §۸. شمارهٔ phase/part مکانیکی (#۸۶)؛ topic-slug پیشنهادی و قابل تغییر توسط کاربر. فراموشیِ اعلام = نقض پروتکل chat-end. Genesis: فراموشیِ تکرارشونده در part18/part19. | HM-3 · #۶۲ (handoff) · process | ACTIVE |
| QL-4 | 2026-05-31 | **Chat-End Hash from Live HEAD Only:** هش frontier/chat-end فقط از `git rev-parse --short HEAD` زنده گرفته شود؛ هیچ هش میانی یا ثابت از handoff/Ledger/حافظه کپی نشود. در artifactهای تداوم هیچ عدد هشِ ثابتی که وسوسهٔ کپی ایجاد کند نوشته نشود. Genesis: part19 — افزودن commit بعد از ساخت handoff → frontier جابه‌جا شد. | #۸۶/M104 · M101 | ACTIVE |
| QL-5 | 2026-05-31 | **No Reliance on Human Memory/Attention (اصل بنیادین):** Claude هرگز نباید برای جلوگیری از خطا به حافظه، توجه، یا یادآوریِ انسان (کاربر یا خودِ Claude) متکی باشد. هر نیازمندیِ تکرارشونده باید با **گارد مکانیکی** (check خودکار / invariant / منبع زندهٔ مشتق‌شده / قاعدهٔ enforceable) تضمین شود، نه با «تذکر». اگر برای چیزی فقط می‌توان یادآوری کرد، آن خودِ یک نقص است که باید مکانیکی شود. Genesis: part19 — دو بار اتکا به یادآوری به‌جای گارد (next-chat-name، frontier hash). | اصل reliability-audit (رفتاری→مکانیکی) · #۸۴/#۸۵ · check_* | ACTIVE |
| QL-6 | 2026-06-21 | **Helper Model Change:** مدل helper تغییر کرد — چت‌های قبلی در نقش کمکی نیستند و HELPER_PROTOCOL.md = مرجع تاریخی منجمد (نه پروتکل فعال). محتوای HELPER_PROTOCOL.md بدون لمس حفظ می‌شود (#۲۴). تصمیم در part20 گرفته شد. | QL-6 · #۲۴ · HELPER_PROTOCOL | ACTIVE — pending codify v2.18 |

---

## 📌 یادداشت

- این فایل source-of-truth برای قوانین Quick-Lockشده است؛ محتوای آن هرگز در حافظهٔ چت بازسازی نشود — همیشه از disk خوانده شود (هم‌راستا #۸۶).
- هنگام codify رسمی، ردیف‌ها به‌جای حذف، `CODIFIED → #N/MN` می‌گیرند (#۲۴).

**آخرین به‌روزرسانی:** part21 (2026-06-21) — افزودن QL-6 (Helper Model Change).
