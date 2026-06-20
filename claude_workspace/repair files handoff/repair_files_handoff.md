# HANDOFF — بررسی جامع
---------------------
⚠️⚠️⚠️ این فایل، نه حافظه چت، منبع وضعیت زنده (Living Source of Truth) است ⚠️⚠️⚠️

مسیر این فایل: D:\Projects\trading-system\claude_workspace\repair files handoff\repair_files_handoff.md

قوانین اجباری برای هر چتی که این فایل را می‌خواند:

۱. این فایل باید قبل از هر اقدام دیگری، کامل و خط‌به‌خط خوانده شود — حتی اگر این فایل از یک پیام/چت قبلی به نظر برسد. هیچ بخشی (از جمله بخش ضمیمه/Addendum در انتها) را نباید رد کرد یا فرض گرفت قبلاً دیده شده.

۲. این فایل جایگزین boot sequence رسمی پروژه (main.md, CHAT_BOOT_TRIGGER_TEMPLATE.md, LOCKED_RULES_INBOX.md, و غیره) نیست — مکمل آن است و باید کنار آن خوانده شود، نه به‌جای آن.

۳. هر کشف جدید (یافته، تناقض، drift)، هر اقدام انجام‌شده، هر اصلاح اعمال‌شده، و هر تصمیم گرفته‌شده در طول این چت یا هر چت آینده‌ای که از این فایل استفاده می‌کند، باید مستقیماً در همین فایل (نه در یک سند جدید جدا) ثبت/آپدیت شود.

۴. هیچ‌گاه به‌جای آپدیت این فایل، یک فایل handoff جدید و مستقل ساخته نشود. این فایل باید تنها مرجع تجمیعی بماند — وگرنه دوباره همان مشکل پراکندگی/drift که این فایل برای حلش ساخته شده، تکرار می‌شود.

۵. هر آپدیت روی این فایل باید:
   الف) موارد قبلی این فایل را حذف نکند (طبق اصل No-Deletion پروژه) — موارد حل‌شده باید با وضعیت «✅ حل‌شده در part/تاریخ X» علامت بخورند، نه پاک شوند.
   ب) پیش از نوشتن، چک شود آیا تغییر جدید با بخش‌های دیگر همین فایل (یا با فایل‌های دیگر پروژه که در این فایل ارجاع شده‌اند) تناقض ایجاد می‌کند؛ اگر بله، پیش از اعمال، به کاربر اعلام و منتظر تصمیم بماند.
   ج) به‌صورت atomic (یکجا، نه نیمه‌کاره) ذخیره شود.

۶. اگر حجم این فایل با گذشت زمان بیش‌از‌حد بزرگ شد (مشابه مشکلی که خود این فایل برای 01_rules.md کشف کرد)، باید این موضوع به‌صراحت به کاربر اعلام شود تا درباره تقسیم/خلاصه‌سازی آن تصمیم مشترک گرفته شود — نه این‌که خودسرانه چیزی از آن حذف یا خلاصه شود.

هدف این فایل: تضمین این‌که دانش، کشفیات، و کارهای باقی‌مانده این پروژه هرگز فقط در حافظه یک چت موقت نباشند، بلکه همیشه در یک نقطه واحد و قابل‌پیگیری روی دیسک نگهداری شوند.

--------------

⚠️ این سند یک ضمیمه (Addendum) در انتهای خود دارد (بعد از بخش ۹) با ۱۲ یافته تکمیلی. هرکدام به بخش/مشکل مرتبط ارجاع می‌دهد. **قبل از اجرای هر اقدام، ابتدا کل سند تا انتهای ضمیمه خوانده شود.**
----------------------


----------------------
Governance + اصلاحات لازم (پیش از اجرا)
**نوشته‌شده توسط:** Claude، در یک چت مستقل خارج از چرخه عادی part
**تاریخ نوشتن:** 2026-06-18 (خارج از تاریخ‌گذاری داخلی پروژه — این چت جزو part-sequence رسمی نیست)
**هدف این سند:** انتقال کامل دانش یک بررسی بسیار عمیق و خط‌به‌خط از ۱۵ فایل متنی پروژه به چت بعدی، به‌گونه‌ای که چت بعدی نیازی به تکرار این بررسی نداشته باشد و مستقیماً بتواند اصلاحات را با تأیید کاربر اجرا کند.

---

## ⚠️ نکته حیاتی پیش از هر چیز — وضعیت این سند

این یک **پیشنهاد بررسی‌شده** است، نه یک handoff رسمی در چرخه part. این چت:
- بخشی از یک «جلسه ممیزی کیفیت اسناد governance» بوده که خود پروژه (در part18، در PENDING) به‌صراحت چنین جلسه‌ای را پیش‌بینی و DEFER کرده بود.
- **هیچ فایلی هنوز در دیسک پروژه تغییر نکرده.** تمام این بررسی صرفاً خواندن (read-only) بوده.
- چت بعدی باید این سند را به‌عنوان **ورودی تکمیلی** کنار boot sequence رسمی پروژه (CHAT_BOOT_TRIGGER_TEMPLATE.md) بخواند — نه جایگزین آن.

---

## بخش ۱ — فهرست کامل فایل‌های خوانده‌شده در این بررسی (۱۵ فایل، همگی خط‌به‌خط و کامل)

### دسته A — فایل‌های Constitution اصلی (۶ فایل، از `docs/constitution/`)
| # | فایل | حجم | نسخه ذکرشده در header | وضعیت خوانده‌شدن |
|---|---|---|---|---|
| 1 | `main.md` | ~۲۰۲ خط | "v2.14" (در header — outdated) | ✅ کامل |
| 2 | `01_rules.md` | 74,785 بایت | "v2.14" / "#1-65 تا v2.11" (header — شدیداً outdated) | ✅ کامل (در ۲ بخش پیوسته) |
| 3 | `02_lessons.md` | 73,310 بایت | "v2.14" / "M1-M63 از v2.11" (header — شدیداً outdated) | ✅ کامل (در ۲ بخش پیوسته) |
| 4 | `04_principles.md` | ~۲۴۸ خط | "v2.14" (header — outdated) | ✅ کامل |
| 5 | `05_architecture.md` | 33,959 بایت | "v2.14" (header — outdated) | ✅ کامل |
| 6 | `03_bugs.md` | 16,917 بایت | "v2.14" (header — outdated) | ✅ کامل |

> توجه: `06_meta.md` در همین چت **قبلاً** (در یک نقطه زودتر از بررسی سیستماتیک ۱۲-فایلی) کامل خوانده شده بود؛ به دستور کاربر دوباره خوانده نشد، اما یافته‌هایش (به‌خصوص بخش ۶.۴ Custom Instructions با ارجاع نسخه v2.14) در حافظه این چت ثبت است.

### دسته B — فایل‌های وضعیت/تاریخچه (۴ فایل، از `docs/` و `claude_workspace/`)
| # | فایل | حجم | یافته کلیدی |
|---|---|---|---|
| 7 | `docs/SESSION_STATUS.md` | 6,021 بایت | متوقف در «پس از part17» در header، بدنه تا part17 — **۲ part عقب از واقعیت (part19)** |
| 8 | `docs/DECISIONS_LOG.md` | 36,617 بایت | تنها فایلی که **drift نداشت** — تا Decision #۷۰ (part18) به‌روز بود |
| 9 | `docs/CHAT_LOG.md` | 144,226 بایت | کامل‌ترین تاریخچه، تا part19 catch-up — شامل روایت دقیق همه مشکلات ساختاری تاریخی پروژه |
| 10 | `claude_workspace/PHASE_LEDGER.md` | 12,717 بایت | **منبع authoritative نهایی** — تا part19، HEAD=`5de05e0` |

### دسته C — فایل عملیاتی منسوخ (۱ فایل)
| # | فایل | حجم | یافته کلیدی |
|---|---|---|---|
| 11 | `docs/CLAUDE_CHECKLIST.md` | 25,352 بایت | **خودش را DEPRECATED اعلام کرده** (part17، v2.16) — بر مبنای zip-workflow قدیمی، نه MCP. در boot sequence فعلی استفاده نمی‌شود. |

### دسته D — فایل‌های Boot/Enforcement خارج از ۱۲ فایل اولیه (۴ فایل، کشف‌شده در ادامه بررسی)
| # | فایل | حجم | یافته کلیدی |
|---|---|---|---|
| 12 | `claude_workspace/LOCKED_RULES_INBOX.md` | کوچک | **۶ قانون Binding فعال (QL-0 تا QL-5)** از part19 که هنوز در 01_rules.md رسمی codify نشده‌اند |
| 13 | `claude_workspace/manual_boxes/PROJECT_INSTRUCTIONS.md` | 6,056 بایت | آینه کادر واقعی Project Instructions در Claude.ai — وضعیتش نسبت به کادر واقعی «منتظر تأیید کاربر» مانده (از part19) |
| 14 | `claude_workspace/manual_boxes/SETTINGS_GENERAL_INSTRUCTIONS.md` | کوچک | آینه کادر Settings — عمداً مینیمال، فقط نقطه ورود به CHAT_BOOT_TRIGGER_TEMPLATE.md |
| 15 | `claude_workspace/CHAT_BOOT_TRIGGER_TEMPLATE.md` | متوسط | **مرجع enforcement واقعی boot** — از part09، ساخته‌شده برای حل مشکل «constitution bypass despite boot files read» |

### دسته E — فایل‌های اضافی خوانده‌شده در ادامه (بعد از دستور صریح کاربر، طبق آخرین درخواست‌ها)
| # | فایل | حجم | یافته کلیدی |
|---|---|---|---|
| 16 | `docs/HELPER_PROTOCOL.md` | 31,806 بایت | تعریف زیرساخت Helper Consultation (D24) — شامل 8-Layer Review Framework، Bounded Bootstrap Pattern، HM-namespace |
| 17 | `claude_workspace/incoming_permanent/PHASE1_PART20_HANDOFF.txt` | کوچک | **آخرین دستورالعمل رسمی موجود** برای ادامه پروژه (نوشته‌شده در پایان part19) |
| 18 | `claude_workspace/CHAT_HANDOFF_MDRS_V2.md` | 29,769 بایت | Handoff بسیار قدیمی (part02→part03) — اکثر یافته‌هایش با وضعیت فعلی چک متقابل شد (جدول کامل در بخش ۴ همین سند) |

**جمع کل چت قبلی (بررسی اولیه): ۱۸ فایل متنی خوانده‌شده، همگی خط‌به‌خط.**

---

### دسته F — فایل‌های خوانده‌شده در این چت (بررسی تکمیلی — چت دوم، 2026-06-18)

| # | فایل | حجم | یافته کلیدی |
|---|---|---|---|
| 19 | `claude_workspace/CHAT_BOOT_TRIGGER_TEMPLATE.md` | متوسط | تأیید مستقیم: STEP 1 ۱۲ آیتم دارد، PHASE_LEDGER.md در آن غایب است (مشکل ۷) |
| 20 | `claude_workspace/LOCKED_RULES_INBOX.md` | کوچک | تأیید کامل: QL-0 تا QL-5 همگی ACTIVE، آخرین به‌روزرسانی part19 |
| 21 | `docs/constitution/main.md` | ~۲۰۲ خط | تأیید header v2.14 (مشکل ۱۰)؛ LOCKED_RULES_INBOX در Quick-start غایب (مشکل ۶) |
| 22 | `docs/constitution/01_rules.md` | 74,785 بایت | تأیید header v2.14؛ محتوا تا #۸۸ کامل — شرح «وضعیت این ماژول» می‌گوید migration کامل تا #۸۶ ولی #۸۷-۸۸ هم در متن هستند (ناهماهنگی جزئی داخلی) |
| 23 | `docs/constitution/02_lessons.md` | 73,310 بایت | تأیید header v2.14؛ M-series تا M105 + HM-1 تا HM-7 کامل — شمارش مستقل با جدول match کرد (مشکل ۱۲ تأیید سالم) |
| 24 | `docs/constitution/06_meta.md` | 36,820 بایت | تأیید header v2.14؛ §۶.۸ Custom Instructions نسخه «v2.14» را در متن پیشنهادی دارد؛ **تکمیلی ۱ به‌صورت جزئی بسته شد:** §۶.۸ به‌صراحت به Rule #۸۷ و Materiality Threshold ارجاع می‌دهد — پل ارتباطی با manual_boxes در خودِ فایل نوشته شده |
| 25 | `docs/constitution/04_principles.md` | ~۲۴۸ خط | تأیید header v2.14؛ بدون یافته جدید قابل توجه |
| 26 | `docs/constitution/05_architecture.md` | 33,959 بایت | تأیید header v2.14؛ React:18 در §۵.۳ تأیید (مشکل ۹)؛ TODO منسوخ shell در «وضعیت این ماژول» تأیید (مشکل ۱۱)؛ **یافته جدید: footer می‌گوید «commit 6 — migration completed» نه S3.1/S3.2 → این فایل از آخرین Atomic Update جا مانده (مشکل ۱۳ — جدید)** |
| 27 | `docs/constitution/03_bugs.md` | 16,917 بایت | تأیید header v2.14؛ ۱۶ Bug ثبت‌شده همگی Resolved؛ بدون یافته جدید |

### دسته G — فایل‌های خوانده‌شده در این چت (مرحله دوم — فایل‌های اولویت‌دار نخوانده)

| # | فایل | یافته کلیدی |
|---|---|---|
| 28 | `docs/SESSION_STATUS.md` | تأیید مشکل ۱ (header part13، بدنه part17، واقعیت part19)؛ **یافته جدید:** محیط فعال «React 19.2» ذکر می‌کند — تأیید سوم مشکل ۹ |
| 29 | `docs/PHASE_LEDGER.md` | تأیید قطعی: آخرین چت = part19، HEAD = `5de05e0`، Constitution = v2.17 |
| 30 | `docs/PROJECT_CONSTITUTION.md` | فقط یک redirect stub است (v2.12) — بی‌خطر اما آمارهایش شدیداً outdated («قوانین #۱-۶۶» و «M1-M86» — مشکل ۱۴) |
| 31 | `docs/PENDING_FOR_NEXT_VERSION.md` | ارشیو تاریخی کامل PENDINGها از part03 تا part19 — همه در constitution codify شده‌اند؛ فایل خود دیگر PENDING فعالی ندارد (تأیید از SESSION_STATUS که می‌گوید فایل بعد از Part20 ادامه خواهد داشت) |
| 32 | `claude_workspace/snapshots/CUSTOM_INSTRUCTIONS.md` | **⚠️ مشکل ۱۵ (NEW):** این فایل بسیار قدیمی است — ارجاع به `docs/سند_جامع_v2_9.md` و `docs/CLAUDE_CHECKLIST.md` و شماره‌های قانون قدیمی |
| 33 | `claude_workspace/snapshots/PROJECT_KNOWLEDGE.md` | تا part18 به‌روز است — Constitution v2.17، ۸۸ قانون، React 19.2 (تأیید مشکل ۹) |
| 34 | `frontend/package.json` | **✅ تأیید نهایی مشکل ۹:** `"react": "^19.2.6"` — چهار منبع مستقل هم‌داستان |

**جمع این مرحله: ۸ فایل جدید (28-34) + scan کامل دایرکتوری.**
**جمع تجمیعی کل: ۳۴ فایل خوانده‌شده + scan کامل.**

---

## بخش ۲ — فایل‌های متنی شناسایی‌شده که هنوز خوانده نشده‌اند

> **وضعیت:** این فهرست بر اساس **scan کامل بازگشتی** `docs/` و `claude_workspace/` در چت دوم (2026-06-18) تهیه شده — نه از ارجاعات تصادفی. این فهرست جایگزین نسخه تخمینی قبلی است.

### دسته ۱ — `docs/` (فایل‌های خوانده‌نشده)

| فایل | اولویت | توضیح |
|---|---|---|
| `docs/PROJECT_MANIFEST.md` | ⭐ بالا | منبع authoritative Tier classification؛ در HELPER_PROTOCOL cross-reference شده |
| `docs/PROJECT_CONSTITUTION.md` | ⭐ بالا | **⚠️ کشف جدید از scan** — در فهرست قبلی نبود؛ نام آن نگران‌کننده است (آیا با constitution/ تداخل دارد؟) |
| `docs/PENDING_FOR_NEXT_VERSION.md` | ⭐ بالا | PENDING فعلی پروژه؛ باید با SESSION_STATUS مقابله شود |
| `docs/PROJECT_GOVERNANCE.md` | بالا | governance framework کلی |
| `docs/REVIEW_PROTOCOL.md` | بالا | پروتکل Review؛ در HELPER_PROTOCOL cross-reference شده |
| `docs/PRE_ADD_CHECKLIST.md` | بالا | checklist قبل از Add؛ در 06_meta.md Template 11 cross-reference شده |
| `docs/TASK_BACKLOG.md` | متوسط | آمار inconsistency احتمالی (از فهرست تاریخی) |
| `docs/REVIEW_LOG.md` | متوسط | وضعیت Reviews |
| `docs/PROJECT_CONTEXT.md` | متوسط | context کلی پروژه |
| `docs/TROUBLESHOOTING.md` | متوسط | Bug #۱-۳۰ که در 03_bugs.md cross-ref شده |
| `docs/HANDOFF_TEMPLATE.md` | متوسط | template رسمی handoff |
| `docs/PRECOMMIT.md` | متوسط | ⚠️ مرتبط با تکمیلی ۴: پیش از نوشتن Check جدید خوانده شود |
| `docs/DECISIONS_LOG.md` | پایین | در بررسی اول خوانده شد ✅ — فقط اگر آپدیت‌های بعد از part18 نیاز به verify داشت |
| `docs/CHAT_LOG.md` | پایین | در بررسی اول خوانده شد ✅ |
| `docs/ANTI_PATTERNS.md` | پایین | |
| `docs/ARCHITECTURE.md` | پایین | |
| `docs/API_DOCS.md` | پایین | |
| `docs/BACKEND_TESTING.md` | پایین | |
| `docs/GIT_WORKFLOW.md` | پایین | |
| `docs/GLOSSARY.md` | پایین | |
| `docs/ONBOARDING_GUIDE.md` | پایین | |
| `docs/REUSABLE_SKELETON.md` | پایین | |
| `docs/STYLE_GUIDE.md` | پایین | |
| `docs/CHAT6_FINALIZE.md` | پایین | تاریخی |
| `docs/CHAT7_FINALIZE.md` | پایین | تاریخی |
| `docs/HANDOFF_TEMPLATE.md` | پایین | |
| `docs/constitution/archive/v2_11_legacy.md` | خیلی پایین | legacy |
| `docs/reviews/*.md` (۱۳ فایل) | پایین | همه Reviews — `README.md` هم وجود دارد |
| `docs/سند_جامع_v2_*.md` (۶ فایل: v2.6-v2.11) | خیلی پایین | legacy monolithic — طبق Z3.13 باید آرشیو می‌شدند |

### دسته ۲ — `claude_workspace/` (فایل‌های خوانده‌نشده)

| فایل | اولویت | توضیح |
|---|---|---|
| `claude_workspace/snapshots/PROJECT_KNOWLEDGE.md` | ⭐ بالا | **⚠️ کشف جدید از scan** — آخرین نسخه Project Knowledge؛ محتوای آن ممکن است با وضعیت فعلی governance همخوانی نداشته باشد |
| `claude_workspace/snapshots/CUSTOM_INSTRUCTIONS.md` | ⭐ بالا | **⚠️ کشف جدید از scan** — آینه Custom Instructions؛ مرتبط با مشکل ۷ و تکمیلی ۱ |
| `claude_workspace/snapshots/2026-05-30-PROJECT_KNOWLEDGE-v2.16.md` | متوسط | snapshot تاریخی v2.16 |
| `claude_workspace/snapshots/PROJECT_README.md` | پایین | snapshot README |
| `claude_workspace/HELPER_SESSION_TODO_part09_final.md` | متوسط | helper-side؛ طبق هشدار PHASE_LEDGER fabricate نشود |
| `claude_workspace/HELPER_SANDBOX_HANDOFF_PART09.txt` | پایین | helper-side تاریخی |
| `claude_workspace/HELPER_SANDBOX_HANDOFF_PART09_FINAL.txt` | پایین | helper-side تاریخی |
| `claude_workspace/PART16_BOOT_TRIGGER.txt` | پایین | تاریخی |
| `claude_workspace/inventory.txt` | پایین | |
| `claude_workspace/inventory_filtered.txt` | پایین | |
| `claude_workspace/commit_msg_*.txt` (۲۱ فایل) | خیلی پایین | آرشیو commit messages — محتوا احتمالاً در CHAT_LOG خلاصه شده |
| `claude_workspace/incoming_permanent/` (۲۳ فایل) | پایین | فقط PHASE1_PART20_HANDOFF.txt خوانده شد ✅؛ بقیه تاریخی |
| `claude_workspace/live_inbox/` | — | ✅ **scan شد: همه پوشه‌ها خالی هستند** — نیازی به بررسی محتوا ندارند |

### یافته مهم از scan — `docs/PROJECT_CONSTITUTION.md`
⚠️ این فایل در هیچ فهرست قبلی این سند نبود. نام آن (PROJECT_CONSTITUTION) با پوشه `docs/constitution/` (که ۶ ماژول دارد) احتمالاً ارتباط دارد. باید اولین فایلی باشد که در بررسی بعدی خوانده می‌شود — ممکن است یک legacy monolithic، یا یک ورودی/index برای constitution modules باشد.

### تغییرات نسبت به فهرست تخمینی قبلی
- ✅ `live_inbox/` همه پوشه‌هایش خالی هستند (نیازی به بررسی محتوا ندارند)
- ✅ `docs/constitution/archive/` فقط یک فایل دارد: `v2_11_legacy.md`
- ➕ `docs/PROJECT_CONSTITUTION.md` اضافه شد (کشف جدید از scan)
- ➕ `claude_workspace/snapshots/PROJECT_KNOWLEDGE.md` و `CUSTOM_INSTRUCTIONS.md` اضافه شدند (کشف جدید از scan)
- ➕ `docs/reviews/README.md` به فهرست reviews اضافه شد
- `frontend/package.json` باید هم خوانده شود (برای تأیید نهایی React version — مشکل ۹)

---

## بخش ۳ — یافته‌های قطعی (مشکلات تأیید‌شده، با جزئیات کامل برای اصلاح)

> این بخش، نسخه نهایی و تجمیع‌شده تمام یافته‌هایی است که در طول این بررسی به‌صراحت تأیید شدند. هر کدام شامل: محل دقیق، شرح مشکل، شواهد از حداقل دو فایل مستقل (cross-verified)، و پیشنهاد اصلاح اولیه است (نه اصلاح نهایی — اصلاح نهایی نیاز به تأیید کاربر و رعایت Upfront Constraint Checklist دارد، طبق HELPER_PROTOCOL §۷).

### مشکل ۱ — SESSION_STATUS.md به‌شدت Drift دارد (۲ part عقب)
**محل:** `docs/SESSION_STATUS.md`
**شرح:** Header می‌گوید «وضعیت پس از part13»، بدنه می‌گوید «پس از part17»، اما PHASE_LEDGER.md (منبع authoritative) تأیید می‌کند آخرین چت **part19** با HEAD=`5de05e0` است.
**شواهد متقابل:** فایل ۹ (PHASE_LEDGER) ردیف part19 + فایل ۸ (CHAT_LOG) بخش part19.
**تشخیص ریشه‌ای:** این دقیقاً همان «full-refresh» است که خود پروژه به‌صورت دوره‌ای انجام می‌دهد (مثل part14-15) — یعنی این یک الگوی شناخته‌شده و قابل‌انتظار است، نه یک خطای غیرمنتظره.
**اصلاح پیشنهادی:** بازنویسی کامل SESSION_STATUS.md با اطلاعات part18+part19 از PHASE_LEDGER (نه از حافظه).

### مشکل ۲ — حجم 01_rules.md از حد هشدار شده عبور کرده (مشکل تاریخی رشدیافته)
**محل:** `docs/constitution/01_rules.md`
**شرح:** اندازه فعلی ۷۴,۷۸۵ بایت (~۷۵KB). در `CHAT_HANDOFF_MDRS_V2.md` (فایل تاریخی part02) صراحتاً هشدار داده شده بود این فایل «نزدیک به حد ۵۰KB» است — یعنی الان **۵۰٪ بیشتر** از حد هشدارشده است.
**شواهد متقابل:** فایل ۱۸ (CHAT_HANDOFF_MDRS_V2، بخش ۴.ب) + اندازه واقعی فایل که در فایل ۳ گرفتم.
**تأثیر عملی:** boot sequence هر چت باید این فایل کامل را بخواند — حجم بالا یعنی مصرف زیاد context window فقط برای یک فایل.
**اصلاح پیشنهادی (دو گزینه که باید با کاربر مطرح شود):**
- گزینه الف: ساخت یک فایل خلاصه (نه با لیست hardcoded طبق هشدار M88 genus در HELPER_PROTOCOL، بلکه با ارجاع اصولی) که فقط قوانین پراستفاده را نشان دهد و به جزئیات کامل لینک دهد.
- گزینه ب: تقسیم 01_rules.md به دو فایل (مثلاً قوانین پایه‌ای/همیشگی در یک فایل، Trust Rules/قوانین تخصصی در فایل دیگر) — مشابه الگویی که قبلاً برای سند جامع به ۶ ماژول انجام شد.
**هشدار مهم:** هرگونه فایل خلاصه/راهنما **باید** اصل M88 genus prevention را رعایت کند — یعنی محتوایش نباید لیست hardcoded از قوانین فعلی باشد (که خودش منبع drift آینده می‌شود)، بلکه باید به PROJECT_MANIFEST.md یا 01_rules.md اصلی ارجاع اصولی بدهد.

### مشکل ۳ — تناقض فعال و حل‌نشده بین دو فایل درباره شل پیش‌فرض (CMD vs PowerShell)
**محل:** `docs/constitution/01_rules.md` بخش ۱.۷ **در تناقض با** `docs/constitution/05_architecture.md` بخش ۵.۱.۲
**شرح دقیق:**
- در `01_rules.md` بخش ۱.۷: متن قدیمی هنوز می‌گوید CMD باید default باشد، با یک یادداشت داخلی که می‌گوید «این تناقض ۹ بود که کشف شد» ولی هرگز اصلاح رسمی نشده.
- در `05_architecture.md` بخش ۵.۱.۲: عنوان صریح «Shell Configuration — اصلاحیه v2.12 ✅» و متن می‌گوید «این تناقض... در v2.12 رسماً رفع شد» و PowerShell را default اعلام می‌کند.
- **اما** آخرین Handoff عملیاتی واقعی (`PHASE1_PART20_HANDOFF.txt`، بخش ۶ GUARDS) دستورالعمل‌های عملی را به سبک **CMD با `&`-chaining** (طبق M105) می‌دهد، نه PowerShell.
**شواهد متقابل سه‌گانه:** فایل ۳ (01_rules.md) + فایل ۱۱ (05_architecture.md) + فایل ۱۷ (PHASE1_PART20_HANDOFF.txt).
**تشخیص ریشه‌ای:** این یک تناقض **سه‌طرفه** است، نه دوطرفه همان‌طور که در ابتدای این بررسی فکر می‌کردم: (۱) قانون رسمی قدیمی، (۲) اصلاح در فایل architecture، (۳) واقعیت عملی روزمره (CMD با `&`-chain طبق M105). این سه باید با هم sync شوند، نه فقط ۲ مورد اول.
**درس‌های مرتبط (باید در اصلاح نهایی cite شوند):** M84 (multi-line `-m` در CMD)، M85 (Terminal Type Awareness)، M87 (Active-Writing Self-Binding Failure — این قانون نوشته شد و در همان چت نقض شد)، Rule #۶۷ (Cross-shell mandatory)، M105 (EXECUTE چندتایی = یک خط `&`-chain).
**اصلاح پیشنهادی:** بازنویسی بخش ۱.۷ در 01_rules.md به‌گونه‌ای که (۱) با ۵.۱.۲ در 05_architecture.md کاملاً هم‌خوان باشد، (۲) صراحتاً الگوی M105 (`&`-chain برای چند دستور) را به‌عنوان روش عملی فعلی ثبت کند، (۳) بخش قدیمی منسوخ را با برچسب `[منسوخ — vX.Y]` نگه دارد نه حذف کند (طبق Rule #۲۴ No-Deletion).

### مشکل ۴ — CLAUDE_CHECKLIST.md منسوخ است، اما این کم‌خطرتر از تخمین اولیه است
**محل:** `docs/CLAUDE_CHECKLIST.md`
**شرح:** خودش از خط اول DEPRECATED اعلام شده (part17، v2.16). اما **بررسی تکمیلی نشان داد** که هیچ‌کدام از فایل‌های boot واقعی (نه main.md، نه CHAT_BOOT_TRIGGER_TEMPLATE.md، نه Project Instructions) به این فایل ارجاع نمی‌دهند.
**تجدید نظر نسبت به ارزیابی اولیه:** در ابتدای این بررسی (پیش از خواندن کامل)، این مشکل با اولویت بالا (🟡 مهم) ارزیابی شده بود. پس از بررسی کامل، این مشکل باید **پایین‌اولویت** ارزیابی شود، چون به‌درستی منسوخ شده و در عمل بازدید نمی‌شود.
**اصلاح پیشنهادی:** هیچ اقدام فوری لازم نیست. اگر زمانی خواستیم، فقط می‌توان تناقض داخلی نسخه (v1.3 در بالا / v1.4 در پایین فایل) را اصلاح کرد — اما این هم چون فایل deprecated است، اولویت ندارد.

### مشکل ۵ — main.md و آمارهای آن (M-series count) outdated است
**محل:** `docs/constitution/main.md`
**شرح:** آمار «بزرگترین ماژول 02_lessons با ~۵۰KB» را نشان می‌دهد در حالی که اندازه واقعی ۷۳KB است. این جدا از header version drift (که در همه ۶ فایل constitution مشترک است) است.
**شواهد متقابل:** اندازه واقعی از `get_file_info` در فایل ۴ + ادعای main.md در فایل ۱.
**اصلاح پیشنهادی:** بازنویسی بخش آمار در main.md بر اساس اندازه‌های واقعی فعلی (نیاز به `get_file_info` تازه در زمان اجرا، نه از این سند کپی شود — طبق Rule #۸۶/M104 اعداد مکانیکی باید از منبع زنده گرفته شوند).

### مشکل ۶ (حیاتی‌ترین یافته جدید) — LOCKED_RULES_INBOX.md از boot sequence اصلی (main.md) غایب است
**محل:** `claude_workspace/LOCKED_RULES_INBOX.md` **در تناقض با** `docs/constitution/main.md`
**شرح:** این فایل ۶ قانون Binding فعال (QL-0 تا QL-5، از part19) دارد. خودِ QL-0 می‌گوید: «این فایل در هر boot خوانده می‌شود». اما در `main.md` (که Quick-start را تعریف می‌کند) هیچ ارجاعی به این فایل نیست.
**شواهد متقابل:** فایل ۱ (main.md، که این فایل را در ۹ آیتم Quick-start نداشت) + فایل ۱۲ (LOCKED_RULES_INBOX.md) + فایل ۱۵ (CHAT_BOOT_TRIGGER_TEMPLATE.md، که این فایل را در STEP 1 آیتم ۲ **دارد**) + فایل ۱۷ (PHASE1_PART20_HANDOFF.txt، که این فایل را در بخش ۱ آیتم ۴ **دارد**).
**تحلیل دقیق:** پس این فایل (LOCKED_RULES_INBOX) در ۲ مرجع boot (CHAT_BOOT_TRIGGER_TEMPLATE و آخرین Handoff) **هست**، اما در ۱ مرجع (main.md که جزو Constitution رسمی است) **نیست**. یعنی اگر کسی فقط از main.md پیروی کند (بدون خواندن CHAT_BOOT_TRIGGER_TEMPLATE)، این ۶ قانون فعال را نمی‌بیند.
**اصلاح پیشنهادی:** افزودن یک ارجاع صریح در Quick-start بخش main.md به `claude_workspace/LOCKED_RULES_INBOX.md`، با توضیح که این فایل قوانین binding فوری (خارج از چرخه version bump رسمی) را نگه می‌دارد.
**نکته فرعی مهم:** این ۶ قانون (QL-0 تا QL-5) هنوز «codify رسمی» نشده‌اند (طبق تأیید خودشان و PHASE1_PART20_HANDOFF بخش ۵). یعنی این یک TODO شناخته‌شده و **به‌عمد معلق نگه‌داشته‌شده** پروژه است، نه یک خطای کشف‌نشده. باید این تفاوت در گزارش نهایی لحاظ شود: مشکل واقعی فقط «main.md به این فایل ارجاع نمی‌دهد»، نه «این قوانین codify نشده‌اند» (که عمدی است).

### مشکل ۷ (حیاتی) — تناقض ترتیب Boot Sequence بین سه منبع
**محل:** `claude_workspace/manual_boxes/PROJECT_INSTRUCTIONS.md` در تناقض با `claude_workspace/CHAT_BOOT_TRIGGER_TEMPLATE.md`
**شرح دقیق:** Project Instructions (آینه کادر واقعی) می‌گوید: «۱) اول CHAT_BOOT_TRIGGER_TEMPLATE.md را بخوان ۲) **اول از همه** PHASE_LEDGER.md را بخوان» — این خودش یک تناقض داخلی است («اول» دوبار با دو معنی متفاوت استفاده شده).
از طرف دیگر، CHAT_BOOT_TRIGGER_TEMPLATE.md (STEP 1) ترتیب را این‌گونه می‌دهد: main.md → 01_rules.md+LOCKED_RULES_INBOX → 02_lessons.md → 06_meta.md → 04_principles.md+05_architecture.md → HELPER_PROTOCOL.md → SESSION_STATUS.md → PENDING.md → ... و **PHASE_LEDGER.md را در این لیست اصلاً ندارد!**
اما آخرین Handoff واقعی (`PHASE1_PART20_HANDOFF.txt`) ترتیب نهایی و به‌نظر صحیح‌ترین را می‌دهد: CHAT_BOOT_TRIGGER_TEMPLATE.md → **PHASE_LEDGER.md** (دوم) → main.md → 01_rules.md+LOCKED_RULES_INBOX → ...
**شواهد متقابل سه‌گانه:** فایل ۱۳ (Project Instructions) + فایل ۱۵ (CHAT_BOOT_TRIGGER_TEMPLATE) + فایل ۱۷ (PHASE1_PART20_HANDOFF).
**نتیجه‌گیری:** سه منبع، سه ترتیب نسبتاً متفاوت. آخرین Handoff (فایل ۱۷) محتمل‌ترین و به‌روزترین نسخه واقعی است، اما **CHAT_BOOT_TRIGGER_TEMPLATE.md** (که سند رسمی‌تر و پایدارتر است) باید به‌روزرسانی شود تا PHASE_LEDGER.md را در جای درست (بعد از STEP 0، قبل از main.md) داشته باشد.
**اصلاح پیشنهادی:** به‌روزرسانی STEP 1 در `CHAT_BOOT_TRIGGER_TEMPLATE.md` برای افزودن `PHASE_LEDGER.md` به‌عنوان آیتم اول (یا دوم، بعد از Pre-Flight)، و رفع ابهام «اول از همه» در Project Instructions.

### مشکل ۸ — Rule #۷۷ در HELPER_PROTOCOL.md به‌عنوان «candidate» ذکر شده، در حالی که در 01_rules.md به‌صورت Locked کامل تأیید شده
**محل:** `docs/HELPER_PROTOCOL.md` بخش ۶.۱ **در تناقض با** `docs/constitution/01_rules.md`
**شرح:** HELPER_PROTOCOL.md (نوشته‌شده در D24/part06) می‌گوید: «per Rule #77 **(candidate)** Hybrid C — pending locking در part07 S3.1». اما در بررسی کامل 01_rules.md (فایل ۳ این بررسی)، Rule #۷۷ به‌عنوان قانون کاملاً Locked با شرح کامل دیده شد.
**شواهد متقابل:** فایل ۳ (01_rules.md، شرح کامل #۷۷) + فایل ۱۶ (HELPER_PROTOCOL.md، بخش ۶.۱).
**تشخیص:** این یک «بخش جزئی فراموش‌شده پس از تغییر بیرونی» است — وقتی Rule #۷۷ در part07 رسماً Locked شد، کسی برنگشت تا این یک خط در HELPER_PROTOCOL.md (که در part06 نوشته شده بود) را به‌روزرسانی کند.
**اصلاح پیشنهادی:** اصلاح این یک خط در HELPER_PROTOCOL.md §۶.۱ — حذف کلمه «(candidate)» و «pending locking» و افزودن ارجاع به وضعیت Locked نهایی.

### مشکل ۹ — Roadmap نسخه‌های Stack در 05_architecture.md با شواهد مستقل (CHAT_LOG، DECISIONS_LOG) ناهم‌خوان است
**محل:** `docs/constitution/05_architecture.md` بخش ۵.۳ (Frontend Stack)
**شرح:** این بخش می‌گوید «React: 18» — اما در `CHAT_LOG.md` (چت ۶ و part07) و `DECISIONS_LOG.md` (Decision #۵۶) صراحتاً «React 19» ذکر شده (و حتی دلیل فنی دارد: «`@testing-library/react ^16.x` فقط با React 19 سازگار است»).
**تأیید سوم از SESSION_STATUS (2026-06-18):** بخش «محیط فعال» در SESSION_STATUS.md صراحتاً «React 19.2» ذکر می‌کند — سطح اطمینان این مشکل به «بالا» ارتقا یافت (سه منبع مستقل هم‌داستان).
**شواهد متقابل:** 05_architecture.md («React: 18») + CHAT_LOG (چت ۶) + DECISIONS_LOG (#۵۶) + SESSION_STATUS («React 19.2»).
**سطح اطمینان:** ✅ بالا — سه منبع مستقل همگی React 19 را تأیید می‌کنند. تأیید نهایی با `frontend/package.json` کمافی است ولی برای کامل‌بودن به‌روزرسانی در 05_architecture.md مناسب است.
**اصلاح پیشنهادی:** بخش ۵.۳ در 05_architecture.md به‌روزرسانی شود — «React: 18» → «React: 19.2» (مشتق از SESSION_STATUS یا package.json زنده، نه از این سند).

### مشکل ۱۰ — Header تمام ۶ فایل Constitution یکسان outdated است (الگوی سیستماتیک، نه تصادفی)
**محل:** `main.md`، `01_rules.md`، `02_lessons.md`، `04_principles.md`، `05_architecture.md`، `03_bugs.md` — همگی در خط ۳ خودشان
**شرح:** همگی می‌گویند «بخشی از Constitution v2.14» — در حالی که نسخه فعلی واقعی v2.17 است (تأیید قطعی از CHAT_LOG part18 + PHASE_LEDGER).
**علت ریشه‌ای (یافته مهم):** این ۶ فایل در یک عملیات «migration» واحد (commit‌های اولیه part11.0.الف) از سند جامع monolithic به حالت modular منتقل شدند، با عنوان مشترک «v2.14» (نسخه‌ای که modular split در آن انجام شد). از آن زمان، نسخه‌های بعدی (v2.15 تا v2.17) محتوای داخلی هر فایل را به‌روز کرده‌اند (که در فایل ۳ و ۹ تأیید شد — مثلاً 01_rules.md شرح کامل #۸۸ را دارد) ولی **هیچ‌کس خط هدر بالای فایل را به‌روزرسانی نکرده**.
**این الگو دقیقاً نمونه عملی از M87 (Active-Writing Self-Binding Failure) در سطح سیستماتیک‌تر است:** Rule #۲۶ (Atomic Updates) و #۸۸ (AI-Optimized Authoring) صراحتاً می‌گویند تغییرات باید atomic و کامل باشند، اما در عمل، شش بار پشت سر هم، این یک خط فراموش شده.
**اصلاح پیشنهادی:** اصلاح هر ۶ خط header به «v2.17» (یا نسخه فعلی در زمان اجرای اصلاح، که باید از main.md زنده گرفته شود نه فرض شود) — این باید یک batch اتمیک باشد، شبیه به آنچه قبلاً در part08 (S3.3) برای همین مشکل (اما در نسخه‌های قبلی) انجام شده بود.

### مشکل ۱۱ — main.md بخش «وضعیت این ماژول» در 05_architecture.md TODO منسوخ دارد که در عمل قبلاً انجام شده
**محل:** `docs/constitution/05_architecture.md` بخش پایانی «وضعیت این ماژول»
**شرح:** این بخش می‌گوید «افزوده‌های آینده: تبدیل توجه v2.12 به اصلاحیه رسمی (Shell)» — اما همین فایل، در بخش ۵.۱.۲ بالاتر، صراحتاً عنوان «اصلاحیه v2.12 ✅» دارد. یعنی این TODO خودش outdated شده (کار انجام شده، ولی یادداشت TODO پاک نشده).
**اصلاح پیشنهادی:** حذف یا به‌روزرسانی این بخش TODO منسوخ در پایان 05_architecture.md.

### مشکل ۱۲ (یافته متادیتا، نه محتوا) — تناقض اندازه‌گیری «نزدیک‌ترین چت بعدی» در 02_lessons.md
**وضعیت:** در طول بررسی فایل ۴ تأیید شد که جدول M-series شمارش (M1-M105، ۷۳ ثبت + ۳۲ Reserved) با شمارش مستقل من از جدول match شد — یعنی **این مورد تناقض نیست**، باید در گزارش نهایی به‌صراحت به‌عنوان «بررسی شد و درست بود» ذکر شود تا گزارش بیش‌از‌حد منفی به‌نظر نرسد.

### مشکل ۱۳ (جدید — کشف‌شده در چت دوم) — 05_architecture.md از آخرین دور Atomic Update (S3.x) جا مانده
**محل:** `docs/constitution/05_architecture.md` — بخش پایانی «📌 پایان 05_architecture.md»
**شرح:** footer این فایل می‌گوید «commit 6 — migration completed» — در حالی که بقیه ماژول‌های constitution (01_rules.md، 02_lessons.md، 04_principles.md، 06_meta.md) همگی در footer خود «S3.1» یا «S3.2 اتمیک v2.14 applied» دارند. یعنی 05_architecture.md در Atomic Update S3.x که سایر ماژول‌ها طی آن به‌روز شدند، شرکت نکرده — یا اگر شرکت کرده، footer آن به‌روزرسانی نشده.
**شواهد متقابل:** footer فایل‌های 01_rules.md («S3.1 اتمیک v2.14 applied»)، 02_lessons.md («S3.1 اتمیک v2.14 applied»)، 04_principles.md («S3.2 اتمیک v2.14 applied»)، 06_meta.md («S3.2 اتمیک v2.14 applied») **در مقابل** 05_architecture.md («commit 6 — migration completed»).
**رابطه با مشکل ۱۱:** مشکل ۱۱ (TODO منسوخ shell در همین فایل) احتمالاً همین ریشه را دارد — وقتی Atomic Update S3.x سایر ماژول‌ها را به‌روز می‌کرد، 05_architecture.md skip شد یا ناقص اضافه شد.
**اولویت:** 🟡 متوسط — در عمل محتوای این فایل تا حدودی up-to-date است (مشکل ۳ و ۹ که در این فایل هستند مربوط به محتوا هستند نه S3.x update)، اما footer نادرست یک tracking artifact است که باید اصلاح شود.
**اصلاح پیشنهادی:** آپدیت footer 05_architecture.md به «S3.x اتمیک v2.14 applied» (نسخه دقیق باید از CHAT_LOG زنده تأیید شود)، همراه با اصلاح مشکل‌های ۱۱ (TODO منسوخ) و ۳ (shell تناقض) که هر سه در همین فایل هستند — یعنی این سه اصلاح باید در یک Atomic Update واحد انجام شوند.

---

## بخش ۴ — یافته‌های تاریخی که چک متقابل شدند و **حل‌شده** تشخیص داده شدند (نباید دوباره به‌عنوان مشکل مطرح شوند)

طبق دستور صریح کاربر («اگر مشکلی قدیمی بعداً حل شده را به‌اشتباه به‌عنوان مشکل باز نیاور»)، جدول زیر تمام یافته‌های فایل تاریخی `CHAT_HANDOFF_MDRS_V2.md` (part02-era) را با وضعیت فعلی چک متقابل می‌کند:

| یافته در فایل تاریخی (part02) | نتیجه چک متقابل با وضعیت فعلی | باید دوباره مطرح شود؟ |
|---|---|---|
| Constitution v2.13، ۶۷ قانون | نسخه به v2.17/۸۸ قانون ارتقا یافته | ❌ خیر — کاملاً قدیمی و بی‌ربط |
| پیشنهاد قوانین #۶۸-۷۲ (MDRS v2) | تمام این‌ها (و بیشتر، تا #۷۷) رسماً Codify شدند | ❌ خیر — کاملاً انجام‌شده |
| پیشنهاد درس‌های M88-M92 | M88 و M93-M102 رسماً ثبت شدند (M89-M92 به‌صورت Reserved) | ❌ خیر — انجام‌شده (با شماره‌گذاری نهایی متفاوت) |
| Decision #65 در Roadmap منعکس نشده | در 05_architecture.md فعلی (بخش ۵.۱۶) کاملاً منعکس شده | ❌ خیر — حل‌شده |
| ساخت PROJECT_MANIFEST.md (D1-D3) | در part-های بعدی (S1) کامل ساخته شد، تأیید در PHASE_LEDGER و HELPER_PROTOCOL | ❌ خیر — حل‌شده |
| ساخت REVIEW_PROTOCOL/REVIEW_LOG/docs/reviews (D4-D7) | در S2 کامل ساخته شد، تأیید در CHAT_LOG | ❌ خیر — حل‌شده |
| ساخت Audit Check‌های #۸-۱۱ (D12) | در part09/S4 کامل اضافه شد (و بعداً تا check_13 در part19) | ❌ خیر — حل‌شده و فراتر رفته |
| `backend/app/infrastructure/database.py` معما (ENOENT) | **نامعلوم** — این یک فایل کد است که در این بررسی governance خوانده نشده | ⚠️ نیاز به verification جدا (بخش کد، نه governance) |
| ۹ مورد Documentation Drift در فایل‌های `docs/*.md` (PROJECT_CONTEXT، ARCHITECTURE.md، GIT_WORKFLOW، ...) | **نامعلوم** — این فایل‌ها در این بررسی خوانده نشدند | ⚠️ نیاز به بررسی مستقیم (در بخش ۲ این سند لیست شدند) |
| TASK_BACKLOG آمار inconsistency (32/76 vs 34/82) | **نامعلوم** — TASK_BACKLOG.md خوانده نشد | ⚠️ نیاز به بررسی مستقیم |
| 01_rules.md نزدیک ۵۰KB | تأیید شد و **بدتر شده** (الان ۷۵KB) | ✅ بله — این عیناً مشکل ۲ در بخش ۳ همین سند است |

---

## بخش ۵ — محدودیت‌های صادقانه این بررسی (باید به کاربر و چت بعدی شفاف گفته شود)

۱. **این بررسی فقط فایل‌های متنی governance/boot را پوشش داد، نه کد واقعی (`backend/`, `frontend/`).** بنابراین درباره صحت فنی ادعاهای architecture (مثل نسخه React، ساختار واقعی پوشه‌ها) فقط می‌توان «احتمال drift» گفت، نه قطعیت — تا زمانی که فایل‌های کد مستقیماً بررسی شوند.

۲. **بخش‌هایی از پروژه که منبعشان «helper chat» (نشست کمکی جداگانه، خارج از این چت اصلی) است، عمداً fabricate نشدند.** طبق هشدار صریح خودِ PHASE_LEDGER.md و PHASE1_PART20_HANDOFF.txt: «HELPER-SIDE (DEFER، منبع helper chat part09، خارج دسترس — fabricate نکن): HM-META-H/I/J/K + W4-W5». این بخش‌ها در فهرست مشکلات این سند **عمداً غایب‌اند** و باید همچنان غایب بمانند مگر این‌که آن helper chat در دسترس قرار گیرد.

۳. **فهرست فایل‌های نخوانده در بخش ۲ ممکن است کامل نباشد** — این لیست از طریق ارجاعات تصادفی بین فایل‌ها کشف شد، نه یک `list_directory` بازگشتی کامل از `docs/` و `claude_workspace/`. اولین اقدام چت بعدی باید این scan کامل باشد.

۴. **آینه‌های دو کادر دستی (`manual_boxes/*.md`) ممکن است با وضعیت واقعی کادرهای Claude.ai یکی نباشند** — هر دو فایل به‌صراحت اعتراف می‌کنند که آخرین sync‌شان «منتظر تأیید کاربر» یا نامشخص است. طبق QL-1، هر تغییری در این کادرها باید با گرفتن متن واقعی فعلی از کاربر شروع شود.

---

## بخش ۶ — وظایف دقیق چت بعدی (Action Items، به ترتیب اجرا)

### پیش‌نیاز صفر — Boot رسمی
چت بعدی باید **اول** boot sequence رسمی پروژه (`CHAT_BOOT_TRIGGER_TEMPLATE.md` STEP 0-4) را کامل انجام دهد و تأیید کاربر بگیرد، **سپس** این سند را به‌عنوان ورودی تکمیلی در نظر بگیرد. این سند جایگزین boot رسمی نیست.

### اقدام ۱ — تکمیل scan فایل‌های متنی نخوانده (بخش ۲ این سند)
یک `list_directory` بازگشتی کامل از `docs/` و `claude_workspace/` انجام شود تا فهرست بخش ۲ تکمیل و تأیید شود هیچ فایل متنی دیگری از قلم نیفتاده. سپس فایل‌های اولویت‌دار (`docs/PROJECT_MANIFEST.md`، `docs/TASK_BACKLOG.md`، `docs/PROJECT_GOVERNANCE.md`، `docs/REVIEW_PROTOCOL.md`، `docs/PRE_ADD_CHECKLIST.md`) خوانده شوند چون مستقیماً در HELPER_PROTOCOL.md و سایر فایل‌های اصلی cross-reference شده‌اند.

### اقدام ۲ — ارائه یافته‌های این سند به کاربر برای تأیید نهایی scope
پیش از هر ادیت، فهرست ۱۲ مشکل بخش ۳ (به‌علاوه هر یافته جدید از اقدام ۱) باید به کاربر ارائه شود تا کاربر تأیید کند کدام‌ها در scope این دور اصلاح قرار می‌گیرند.

### اقدام ۳ — اجرای اصلاحات به‌صورت Batch اتمیک، با رعایت Upfront Constraint Checklist
طبق HELPER_PROTOCOL.md §۷، پیش از نوشتن هر اصلاح:
- چک شود اصلاح با کدام فایل‌های دیگر تداخل دارد (مثلاً اصلاح مشکل ۳ روی هم 01_rules.md هم 05_architecture.md هم CHAT_BOOT_TRIGGER_TEMPLATE.md اثر دارد).
- یک Scope Contract صریح (طبق Rule #۷۸) نوشته شود: دقیقاً چند فایل، چه تغییری، با چه DoD قابل شمارش.
- اگر تغییر material روی کادرهای دستی اثر دارد، طبق Rule #۸۷ به کاربر یادآوری صریح داده شود.

### اقدام ۴ — اجرای check اسکریپت audit موجود پس از هر تغییر
`scripts/63_pre_commit_audit.py` (با ۱۳ check فعلی طبق part19) باید بعد از هر batch اجرا شود تا تأیید کند تغییرات جدید counts/version sync را به هم نزده‌اند.

### اقدام ۵ — رعایت Triple-Rule + قانون تداوم دوحلقه‌ای در chat-end
هر اصلاحی که در این چت بعدی انجام شود، باید در پایان آن چت SESSION_STATUS + CHAT_LOG + PENDING به‌صورت اتمیک به‌روز شوند، و یک ردیف جدید به PHASE_LEDGER.md اضافه شود + یک Handoff جدید برای چت بعد از آن ساخته شود (طبق check_12_continuity).

---

## بخش ۷ — مکانیزم پیشنهادی برای جلوگیری از تکرار این نوع مشکلات (پاسخ به درخواست خودکارسازی)

### پیشنهاد ۷.۱ — گسترش `scripts/63_pre_commit_audit.py` با یک Check جدید: «Header Version Sync»
**شرح:** یک check خودکار (مثلاً `check_14_header_version_sync`) که بررسی کند خط header «بخشی از Constitution vX.Y» در هر ۶ فایل ماژول، با نسخه فعلی اعلام‌شده در `main.md` یکی باشد. این **دقیقاً** مشکل ۱۰ (الگوی سیستماتیک header outdated) را برای همیشه از بین می‌برد، چون به‌جای تذکر انسانی، یک گارد مکانیکی می‌شود — این دقیقاً فلسفه QL-5 («هرگز به حافظه/توجه انسان متکی نشو؛ هر نیاز تکرارشونده = گارد مکانیکی») است که از قبل در پروژه (part19) به‌عنوان یک اصل بنیادین پذیرفته شده.
**این می‌تواند توسط خودِ Claude در چت بعدی نوشته و اضافه شود** — کاری نیست که نیاز به تصمیم انسانی داشته باشد جز تأیید نهایی.

### پیشنهاد ۷.۲ — افزودن یک Check جدید: «Cross-File Shell Consistency» (برای مشکل ۳)
**شرح:** یک check که بررسی کند آیا 01_rules.md و 05_architecture.md هر دو همان شل پیش‌فرض (PowerShell یا CMD) را اعلام می‌کنند. این نوع تناقض موضوعی (نه فقط نسخه) سخت‌تر به‌صورت کلی خودکار می‌شود، اما برای این مورد خاص (یک کلیدواژه ثابت) قابل پیاده‌سازی است.

### پیشنهاد ۷.۳ — افزودن `LOCKED_RULES_INBOX.md` به main.md Quick-start (برای مشکل ۶)، با یک Check تطبیقی
**شرح:** علاوه بر افزودن ارجاع دستی، یک check خودکار بسازیم که چک کند هر فایلی که در `CHAT_BOOT_TRIGGER_TEMPLATE.md` STEP 1 ذکر شده، در `main.md` Quick-start هم ذکر شده باشد (یا برعکس) — یعنی این دو منبع boot به‌صورت خودکار sync بمانند، نه با حافظه انسانی.

### پیشنهاد ۷.۴ — این اصل کلی: «هر تغییر در یک فایل constitution، باید چک کند آیا فایل‌های دیگر cross-reference دارند»
این دقیقاً بخش ۵ درخواست اصلی کاربر است. **پیشنهاد عملی:**
به‌عنوان یک رفتار همیشگی (نه فقط یک قانون نوشته‌شده)، Claude در هر چت آینده، **پیش از** هر ادیت روی یک فایل T1 (Constitution/governance)، باید:
۱. از `docs/PROJECT_MANIFEST.md` فهرست بقیه فایل‌های T1 را بگیرد (نه از حافظه — طبق اصل M88 genus).
۲. با `grep`-مانند جستجو (یا خواندن مستقیم) چک کند آیا فایل‌های دیگر به محتوای در حال تغییر cross-reference دارند.
۳. اگر تداخل احتمالی یافت، **قبل از نوشتن**، آن را به‌صراحت به کاربر اعلام کند و منتظر تصمیم بماند (دقیقاً طبق درخواست بند ۵ کاربر: «اگر موضوعی ممکن است اعمالش ناهماهنگی ایجاد کند باید به کاربر اعلام شود»).
این رفتار از قبل تا حدی در Rule #۷۸ (Scope Contract Mandatory) و Rule #۲۶ (Atomic Updates) پیش‌بینی شده — اما **پیشنهاد جدید این است که این رفتار، نه فقط برای درخواست‌های بزرگ بلکه برای هر ادیت کوچک روی فایل‌های T1، اجرا شود.**
**این می‌تواند به‌صورت یک قانون جدید (مثلاً Rule #۸۹ پیشنهادی، نام‌گذاری نهایی باید از منبع زنده گرفته شود) رسمیت یابد:** *"Pre-Edit Cross-File Impact Check"* — پیش از هر write روی فایل T1، یک پیمایش صریح (نه حدسی) از سایر فایل‌های T1 برای یافتن cross-reference انجام شود و در صورت یافتن تداخل، به کاربر اعلام و منتظر تصمیم بماند.

### پیشنهاد ۷.۵ — اتوماسیون‌هایی که **می‌توانند و باید** توسط خود Claude (نه کاربر) انجام شوند، بدون نیاز به تصمیم انسانی اضافه:
- نوشتن و افزودن check‌های ۷.۱ و ۷.۳ به `scripts/63_pre_commit_audit.py` — این صرفاً کد است، تصمیم سیاستی در آن نیست.
- اجرای آن audit script بعد از هر batch تغییر، به‌صورت خودکار، پیش از commit.
- استخراج خودکار اعداد/نسخه‌ها از منابع زنده (git، main.md) به‌جای کپی از این سند یا حافظه — این از قبل Rule #۸۶/M104 است و باید **به‌طور پیگیر** در هر اصلاح این چت رعایت شود.

---

## بخش ۸ — جدول خلاصه نهایی (برای مرور سریع)

| # | مشکل | اولویت | فایل(های) درگیر | Cross-check شده با |
|---|---|---|---|---|
| 1 | SESSION_STATUS Drift (۲ part) | 🔴 فوری | SESSION_STATUS.md | PHASE_LEDGER, CHAT_LOG |
| 2 | حجم 01_rules.md > حد هشدار | 🔴 فوری | 01_rules.md | CHAT_HANDOFF_MDRS_V2 (تاریخی) |
| 3 | تناقض سه‌طرفه CMD/PowerShell | 🔴 فوری | 01_rules.md, 05_architecture.md, PHASE1_PART20_HANDOFF | M84/M85/M87/#۶۷/M105 |
| 4 | CLAUDE_CHECKLIST منسوخ (کم‌خطر) | 🟢 پایین | CLAUDE_CHECKLIST.md | main.md (عدم ارجاع) |
| 5 | main.md آمار اشتباه | 🟡 متوسط | main.md | get_file_info مستقیم |
| 6 | LOCKED_RULES_INBOX غایب از main.md | 🔴 فوری | main.md, LOCKED_RULES_INBOX.md | CHAT_BOOT_TRIGGER_TEMPLATE, PHASE1_PART20_HANDOFF |
| 7 | تناقض ترتیب Boot سه‌گانه | 🔴 فوری | PROJECT_INSTRUCTIONS.md, CHAT_BOOT_TRIGGER_TEMPLATE.md, PHASE1_PART20_HANDOFF | — |
| 8 | Rule #۷۷ candidate vs Locked | 🟡 متوسط | HELPER_PROTOCOL.md | 01_rules.md |
| 9 | React 18 vs 19 — ✅ تأیید نهایی | 🟡 متوسط — ✅ تأیید شد | 05_architecture.md | package.json («React ^19.2.6») + SESSION_STATUS + PROJECT_KNOWLEDGE + DECISIONS_LOG |
| 10 | Header v2.14 در ۶ فایل (سیستماتیک) | 🔴 فوری | همه ۶ فایل constitution | main.md, CHAT_LOG, PHASE_LEDGER |
| 11 | TODO منسوخ در 05_architecture.md | 🟢 پایین | 05_architecture.md | همان فایل (تناقض داخلی) |
| 12 | (نه یک مشکل) M-series count match بود | ✅ تأیید سالم | 02_lessons.md | شمارش مستقل |
| 13 | 05_architecture.md از Atomic Update S3.x جا مانده | 🟡 متوسط | 05_architecture.md (footer) | footerهای 4 ماژول دیگر (S3.1/S3.2) |
| 14 | PROJECT_CONSTITUTION.md آمارهای شدیداً outdated دارد | 🟢 پایین | docs/PROJECT_CONSTITUTION.md | constitution/main.md (وضعیت فعلی) |
| 15 | CUSTOM_INSTRUCTIONS.md بسیار قدیمی است | 🟡 متوسط | claude_workspace/snapshots/CUSTOM_INSTRUCTIONS.md | PROJECT_KNOWLEDGE.md (فعلی v2.17) |
| 16 | PROJECT_MANIFEST.md چهار چت عقب است (part14/15، نه part19) | 🟡 متوسط | docs/PROJECT_MANIFEST.md | PHASE_LEDGER (آخرین چت = part19) |

### دسته H — فایل‌های خوانده‌شده در این چت (مرحله سوم — فایل‌های اولویت‌دار باقی‌مانده)

| # | فایل | یافته کلیدی |
|---|---|---|
| 35 | `docs/PROJECT_MANIFEST.md` | بدون مشکل جدید (Tier classification صحیح)؛ فقط outdated بودن تاریخ (part14/15، نه part19) = مشکل ۱۶ تأیید شد |
| 36 | `docs/PROJECT_GOVERNANCE.md` | **⚠️ DEPRECATED** از part17 (Constitution v2.16) — محتوی zip-workflow قدیمی، مشابه CLAUDE_CHECKLIST.md (مشکل ۴) — هیچ boot فعلی به آن ارجاع نمی‌دهد |
| 37 | `docs/REVIEW_PROTOCOL.md` | ✅ سالم و active — بدون مشکل |
| 38 | `docs/PRE_ADD_CHECKLIST.md` | ✅ سالم و active — بدون مشکل |
| 39 | `docs/TASK_BACKLOG.md` | ✅ تأیید شد: عمداً منجمد شده از چت ۹ (فاز ۰) — snapshot تاریخی طبق هشدار خودش، آمار آن (32/76) وضعیت جاری نیست |

**جمع این مرحله: ۵ فایل جدید (35-39).**
**جمع تجمیعی کل: ۳۹ فایل خوانده‌شده + scan کامل.**

| 17 | PROJECT_GOVERNANCE.md DEPRECATED است (مشابه مشکل ۴) | 🟢 پایین | docs/PROJECT_GOVERNANCE.md | اولین خط فایل |

طبق قرارداد نام‌گذاری پروژه (`TRADING-phase{N}-part{NN}-{topic-slug}`)، و با توجه به این‌که این بررسی خارج از چرخه رسمی part انجام شده، چت بعدی که این اصلاحات را اجرا می‌کند باید با شماره part واقعی (که باید از PHASE_LEDGER زنده گرفته شود، نه از این سند فرض شود) نام‌گذاری شود. پیشنهاد topic-slug:

`TRADING-phase1-part{NN}-governance-consistency-remediation`

(عدد `{NN}` باید در لحظه boot، از `claude_workspace/PHASE_LEDGER.md` زنده استخراج شود — طبق Rule #۸۶/M104/QL-4، نه از این سند کپی شود، چون ممکن است بین نوشتن این سند و شروع چت بعدی، part دیگری در پروژه رسمی انجام شده باشد.)

------------------------------------------------------------------
---

## ضمیمه — یافته‌های تکمیلی از مرور مجدد همین چت (پس از تولید سند اصلی)

> این بخش **بعد از** نوشتن سند اصلی، در نتیجه سه دور بازخوانی مستقل و مقابله با کل مکالمه اضافه شده. هر مورد به‌صراحت ارجاع می‌دهد به این‌که کدام بخش/مشکل از سند اصلی را تکمیل یا اصلاح می‌کند. ترتیب موارد، ترتیب کشف است، نه اولویت.

### تکمیلی ۱ — ارتباط `06_meta.md` با `manual_boxes/` — ✅ نیمه‌بسته شد در چت دوم
**مرتبط با:** بخش ۱ (یادداشت زیر جدول دسته A) و بخش ۳ مشکل ۷.
**شرح اولیه:** در یادداشت بخش ۱ آمده که `06_meta.md` بخشی به نام «Custom Instructions» با ارجاع نسخه v2.14 دارد و پل ارتباطی با manual_boxes صریح نوشته نشده.
**به‌روزرسانی چت دوم (2026-06-18):** `06_meta.md` در چت دوم کامل خوانده شد. §۶.۸ (Custom Instructions) صراحتاً به Rule #۸۷ (Materiality Threshold) و §۶.۸ آینه کادرها ارجاع می‌دهد. یعنی پل ارتباطی **در خودِ فایل نوشته شده** — این تکمیلی نیمه‌بسته است.
**اقدام باقی‌مانده:** تنها نکته باز این است که Custom Instructions پیشنهادی در §۶.۴ نسخه «v2.14» را درون متن پیشنهادی دارد (نه در header). این با مشکل ۱۰ هم‌خوانی دارد و باید در همان batch اصلاح شود.

### تکمیلی ۲ — راهکار خودکارسازی برای تناقض سه‌طرفه شل ناقص است
**مرتبط با:** بخش ۳ مشکل ۳، و بخش ۷ پیشنهاد ۷.۲.
**شرح:** مشکل ۳ به‌درستی تناقض را **سه‌طرفه** تشخیص داد (01_rules.md + 05_architecture.md + PHASE1_PART20_HANDOFF.txt). اما پیشنهاد ۷.۲ («Cross-File Shell Consistency» check) فقط دو فایل ثابت (01_rules.md و 05_architecture.md) را پوشش می‌دهد — نه واقعیت عملی روزمره‌ای که در یک Handoff موقت (سند سوم، غیرثابت) می‌آید. **اقدام لازم:** پیشنهاد ۷.۲ باید بازنویسی شود تا به‌جای چک کردن یک فایل سوم ثابت (که وجود ندارد)، به این صورت باشد: «بعد از هر چت، اگر Handoff آن چت دستورالعمل عملی شل می‌دهد، باید با بخش ۱.۷ مطابقت آن چک شود، نه فقط فایل‌های constitution با هم.»

### تکمیلی ۳ — نتیجه‌گیری بنیادی ابتدای مکالمه («Chat و Claude Code حافظه مشترک ندارند») در سند نیست
**مرتبط با:** نکته حیاتی ابتدای سند (خطوط ۸ تا ۱۳) — به‌عنوان زمینه/rationale.
**شرح:** اولین دلیلی که اساساً به ساخت CLAUDE.md / handoff رسید، این تشخیص بود: Chat (Projects) و Claude Code دو محیط کاملاً جدا با صفر حافظه مشترک‌اند، و تنها راه انتقال context، فایل‌های روی دیسک است. این چرایی بنیادی در سند نهایی جایی ندارد. **اقدام لازم:** یک جمله در «نکته حیاتی پیش از هر چیز» اضافه شود: «دلیل پایه‌ای نیاز به این سند و به فایل‌های مثل CLAUDE.md: هیچ دو session/محیط Claude (چه دو چت در Projects، چه Chat و Claude Code) حافظه مشترک ندارند؛ تنها پل انتقال context، فایل‌های persistent روی دیسک‌اند.»

### تکمیلی ۴ — رابطه `docs/PRECOMMIT.md` با `scripts/63_pre_commit_audit.py` روشن نیست
**مرتبط با:** بخش ۲ (فهرست فایل‌های نخوانده، که `docs/PRECOMMIT.md` در آن هست) و بخش ۷ (پیشنهادهای Check جدید).
**شرح:** پیشنهادهای ۷.۱ تا ۷.۳ فرض می‌کنند Check‌های جدید باید از صفر طراحی شوند. اما `docs/PRECOMMIT.md` (که هنوز خوانده نشده) ممکن است از قبل مشابه این Check‌ها را توضیح داده باشد یا نامی دیگر برایشان وجود داشته باشد. **اقدام لازم:** پیش از نوشتن هر Check جدید (اقدام ۳ در بخش ۶، و پیشنهادهای بخش ۷)، چت بعدی باید اول `docs/PRECOMMIT.md` را بخواند تا از طراحی تکراری یا نام‌گذاری ناهم‌خوان با Check‌های موجود پرهیز شود.

### تکمیلی ۵ — پیشنهاد ۷.۱ خودش ممکن است اصلی را که در مشکل ۲ گفته شد نقض کند
**مرتبط با:** بخش ۳ مشکل ۲ (هشدار M88 genus prevention) و بخش ۷ پیشنهاد ۷.۱.
**شرح:** مشکل ۲ هشدار می‌دهد که هر فایل/ابزار خلاصه که «لیست hardcoded از قوانین فعلی» بسازد، خودش منبع drift آینده می‌شود. پیشنهاد ۷.۱ یک Check می‌سازد که «هر ۶ فایل ماژول» را به‌صورت ثابت در کد چک می‌کند — اگر تعداد یا نام این فایل‌ها در آینده تغییر کند (مثلاً تقسیم شدن یک ماژول به دو)، خودِ این Check باید دستی به‌روزرسانی شود؛ این دقیقاً الگوی همان ریسکی است که مشکل ۲ هشدار می‌دهد. **اقدام لازم:** پیشنهاد ۷.۱ باید فهرست فایل‌های ماژول را از `docs/PROJECT_MANIFEST.md` (منبع زنده) بخواند، نه در کد Check هاردکد کند.

### تکمیلی ۶ — ناهماهنگی شمارش در عنوان سند اصلی («۱۵ فایل») با بدنه آن («۱۸ فایل»)
**مرتبط با:** خط ۴ (عنوان/هدف سند) در تناقض با خط ۵۹ (جمع‌بندی بخش ۱) و سرتیتر بخش ۱ («۱۵ فایل، خط‌به‌خط»).
**شرح:** این یک خطای نگارشی واقعی در خودِ سند است — جالب اینکه دقیقاً از همان نوع الگویی است که در مشکل ۱۰ (header های v2.14 در شش فایل پروژه) شناسایی شد: عددی در یک‌جا نوشته شده و در ادامه، بدون به‌روزرسانی آن نقطه اول، محتوا رشد کرده. **اقدام لازم:** هر دو محل («۱۵ فایل» در خط ۴ و سرتیتر بخش ۱) باید به «۱۸ فایل» اصلاح شوند.

### تکمیلی ۷ — چارچوب ریسک اولیه مقایسه Chat-Projects vs Claude Code استفاده نشده
**مرتبط با:** بخش ۵ (محدودیت‌های صادقانه) — به‌عنوان زمینه تکمیلی، نه یک مشکل جدید.
**شرح:** در ابتدای مکالمه (قبل از شروع بررسی فایل‌ها)، یک جدول ریسک سه‌سطحی (🔴بالا/🟡متوسط/🟢پایین) برای خود فرآیند انتقال Chat→Claude Code ارائه شد (از‌دست‌رفتن context مکالمات، قوانین پنهان، تفاوت رفتار، MCP جدا). این چارچوب درباره‌ی «ریسک ابزار»، نه «ریسک محتوای فایل»، است. **اقدام لازم:** اگر در آینده تصمیم نهایی گرفته شود که اجرای این اصلاحات در Claude Code انجام شود (نه در Chat با MCP)، آن جدول ریسک اولیه باید دوباره مرور شود — چون این handoff فرض کرده اجرا در محیطی با Filesystem MCP (یعنی همین چت Projects) ادامه می‌یابد، نه لزوماً Claude Code.

### تکمیلی ۸ — محدودیت «حتی بازخوانی دقیق هم ممکن است چیزی را جا بیندازد و بعد پیدا کند» در بخش ۵ نیامده
**مرتبط با:** بخش ۵ (محدودیت‌های صادقانه این بررسی) — پیشنهاد افزودن یک بند پنجم.
**شرح:** در طول همین چت، یک بار با بازخوانی سند، یک gap پیدا شد که در نگارش اول نبود؛ با دور دوم، ۵ مورد دیگر؛ با دور سوم، ۲ مورد دیگر. این نشان می‌دهد خودِ فرآیند «بازخوانی و یافتن گاف» محدود به یک سقف قطعی نیست. **اقدام لازم:** یک بند ۵ به فهرست محدودیت‌های بخش ۵ اضافه شود: «۵. فرآیند بازبینی خودِ این سند (و هر سند مشابه آینده) ذاتاً ممکن است سقف ثابتی نداشته باشد — هر دور بازخوانی می‌تواند مورد جدیدی بیابد. این یعنی باید یک معیار توقف عملی (مثلاً دو دور متوالی بدون یافته جدید) به‌جای «تضمین صفر خطا» ملاک قرار گیرد.»

### تکمیلی ۹ — پل ارتباطی «چرا اصلاً این گفتگو دربارهٔ بهبود فایل‌ها شروع شد» در سند نیست
**مرتبط با:** نکته حیاتی ابتدای سند — مکمل تکمیلی ۳.
**شرح:** مسیر این مکالمه: سؤال درباره Chat vs Code ← بحث MCP و کپی/پیست دستی دستورات ← مقایسه Claude Code ← نگرانی درباره انتقال context ← بررسی اینکه آیا context پروژه در فایل‌ها ثبت است ← کشف کیفیت پایین برخی فایل‌ها ← این بررسی عمیق. **اقدام لازم:** یک جمله یک‌خطی در ابتدای سند («این بررسی از یک پرسش عملی – آیا بهتر است کار از Chat به Claude Code منتقل شود – شروع شد و در حین بررسی آمادگی فایل‌ها برای چنین انتقال، به یک ممیزی کامل governance تبدیل شد») می‌تواند این زمینه را برای خوانندهٔ آینده (یا کاربر دیگر) روشن کند، بدون این‌که ابهامی ایجاد کند.

### تکمیلی ۱۰ — `frontend/package.json` فقط در بخش ۳ آمده، نه در فهرست مرکزی فایل‌های نخواندهٔ بخش ۲
**مرتبط با:** بخش ۲ (فهرست فایل‌های نخوانده) و بخش ۳ مشکل ۹.
**شرح:** مشکل ۹ به‌صراحت می‌گوید پیش از اصلاح، `frontend/package.json` باید خوانده شود. اما این فایل در فهرست مرکزی «فایل‌های متنی نخوانده» (بخش ۲) نیامده — یعنی اگر کسی فقط بخش ۲ را به‌عنوان چک‌لیست پیگیری کند، این فایل را فراموش می‌کند. **اقدام لازم:** افزودن یک ردیف به بخش ۲ (زیر یک عنوان جدید «از کد — فقط فایل‌های کانفیگ/متنی غیر‌اجرایی»): `frontend/package.json` — برای تأیید نسخه واقعی React (مرتبط با مشکل ۹).

### تکمیلی ۱۱ — ابهام در اینکه آیا چت بعدی اجازهٔ *نوشتن/ویرایش* اسکریپت دارد یا نه
**مرتبط با:** بخش ۶ اقدام ۳-۴ و بخش ۷ (پیشنهادهای ۷.۱، ۷.۲، ۷.۳، ۷.۵) — که همگی نوشتن/گسترش کد در `scripts/63_pre_commit_audit.py` را پیش‌بینی می‌کنند.
**شرح:** قاعدهٔ «فقط فایل‌های متنی خوانده شود، نه اسکریپت‌ها» که در همین چت تعیین شد، مربوط به **دامنهٔ خوانش این چت بررسی** بود، نه یک منع کلی برای چت بعدی در نوشتن کد. اگر این تفکیک به‌صراحت گفته نشود، چت بعدی ممکن است به‌اشتباه فکر کند اجازهٔ ویرایش هیچ اسکریپتی را ندارد، و یا برعکس، بدون تأیید صریح کاربر دست به ویرایش اسکریپت بزند. **اقدام لازم:** یک جمله در ابتدای بخش ۷ اضافه شود: «توجه: قاعدهٔ 'فقط فایل‌های متنی' که در چت بررسی رعایت شد، مربوط به دامنهٔ *خوانش* آن چت بود. نوشتن/ویرایش اسکریپت‌های پیشنهادی در این بخش، خود یک Action نیازمند Scope Contract و تأیید جدا از کاربر است، طبق Rule #۷۸ — نه چیزی که به‌صورت ضمنی از قاعدهٔ بالا ممنوع یا مجاز فرض شود.»

### تکمیلی ۱۲ — جمع‌بندی صریح برای رفع سردرگمی احتمالی این ضمیمه
این ضمیمه **هیچ مشکل جدیدی در فایل‌های پروژه کشف نکرده** — صرفاً موارد زیر را پوشش می‌دهد:
- پل‌های ارتباطی بین یافته‌های موجود که نوشته نشده بودند (تکمیلی ۱، ۴، ۱۰)
- نقص داخلی در خودِ راهکارهای پیشنهادی سند اصلی (تکمیلی ۲، ۵)
- خطای نگارشی در خودِ سند (تکمیلی ۶)
- زمینهٔ مکالمه‌ای که به فهم کلی کمک می‌کند ولی یافتهٔ فایل نیست (تکمیلی ۳، ۷، ۹)
- یک محدودیت روش‌شناختی صادقانه دربارهٔ خودِ فرآیند ممیزی (تکمیلی ۸)
- یک ابهام رویه‌ای که باید پیش از اجرا رفع شود (تکمیلی ۱۱)

هیچ‌کدام از این ۱۲ مورد، اولویت‌بندی 🔴/🟡/🟢 جدول بخش ۸ سند اصلی را تغییر نمی‌دهد یا با آن در تناقض نیست.
