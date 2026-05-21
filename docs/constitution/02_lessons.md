# ماژول ۰۲ — درس‌نامه اشتباهات Claude

> بخشی از **Constitution v2.12 (Modular)** — [بازگشت به main](./main.md)
>
> **محتوا:** درس‌نامه اشتباهات Claude (M1-M63 از v2.11) با علت ریشه‌ای، راه‌حل، cross-refs.
> **منبع:** سند جامع v2.11 → سند ۱۸ (درس‌نامه اشتباهات Claude — AI Mistakes Log)
> **Created in commit:** `<git log -1 --format=%h پس از commit 3 پر شود>`
>
> **توجه:** درس‌های M64-M86 و موارد جدید در **commit 8** (Atomic Update v2.12) افزوده می‌شوند. این فایل در حال حاضر فقط migrate از v2.11 است (single-purpose commit).

---

## ۲.۰ چرا این ماژول وجود دارد

Claude گاهی کد، دستور، یا پیشنهادی می‌دهد که در عمل کار نمی‌کند. وقتی این اتفاق می‌افتد:

1. کاربر خروجی اشتباه را به Claude گزارش می‌دهد
2. Claude کد اصلاحی می‌دهد
3. این چرخه گاهی چندبار تکرار می‌شود

این درس‌نامه، **هر اشتباه را با علت ریشه‌ای و راه‌حل** ثبت می‌کند، تا Claude در چت‌های آینده قبل از تکرار اشتباه، آن را بشناسد و اجتناب کند.

---

## ۲.۱ پروتکل اعمال (طبق قانون #۴۸)

در ابتدای هر چت جدید، Claude باید:

1. **این ماژول را بخواند** (یا حداقل از خلاصه fast-look استفاده کند — بخش ۲.۲ پایین)
2. قبل از نوشتن کد یا پیشنهاد، چک کند: **آیا این موقعیت یکی از M1-M83+ را تکرار می‌کند؟**
3. اگر بله، از راه‌حل ثبت‌شده استفاده کند

---

## ۲.۲ خلاصه fast-look (دسته‌بندی موضوعی)

برای مراجعه سریع بدون خواندن کامل:

| دسته | درس‌های مرتبط | راه‌حل کلی |
|---|---|---|
| **Verify-before-act** | M1, M37, M61 | بعد از هر write/install/configure، read-back verify |
| **Self-binding** | M62 | قوانینی که Claude ذکر می‌کند، خودکار در همان چت اجرا شوند |
| **Cargo cult flags** | M5, M40 | pip flags ≠ npm flags؛ verify argparse قبل از پیشنهاد |
| **Encoding/Unicode** | M9, M13, M14 | ASCII-only در Windows print() + `.gitattributes` به‌جای hook |
| **MCP/Tool limitations** | M30, M44, M66 | MCP فقط در چت جدید load می‌شود |
| **Process — handoff** | M23, M56, M57, M58, M59, M63 | فایل handoff + prefix های صریح + source-of-truth واحد |
| **Documentation drift** | (همه drift های جدید در commit 8 افزوده می‌شوند) | به Reserved M74+ مراجعه کنید |

---

## ۲.۳ جدول کامل اشتباهات (M1-M63)

| # | اشتباه | علت ریشه‌ای | راه‌حل آینده | چت |
|---|---|---|---|---|
| **M1** | اسکریپت ۴۸ گزارش «updated» داد، فایل‌ها به‌روز نشدند | اسکریپت به `/tmp/zip_stage/` می‌نوشت نه workspace | بعد از write، read-back verify (قانون #۳۷) | ۷ |
| **M2** | فرض کردم zip در `%USERPROFILE%\Downloads` است | مسیر دانلود کاربر متفاوت | پرسیدن یا قانون #۳۴ (zip در root) | ۷ |
| **M3** | پیشنهاد `--zip ... --dry-run` برای اسکریپت ۴۳ | argparse positional بود | verify argparse (قانون #۴۰) | ۷ |
| **M4** | اسکریپت ۴۳ فقط `docs/` را شناخت، `scripts/` گم شد | اسکریپت ۴۳ single-root است | multi-root → `python -m zipfile -e` (قانون #۳۹) | ۷ |
| **M5** | پیشنهاد `pip install --no-audit --no-fund` | این flags فقط npm هستند | pip flags ≠ npm (قانون #۳۵) | ۷ |
| **M6** | تست با `create_access_token(subject="...")` -- signature واقعی متفاوت | بدون چک signature فرض زدم | verify signature (قانون #۳۶) | ۷ |
| **M7** | `payload["user_id"]` در `or` → KeyError | `or` short-circuit با exception کار نمی‌کند | `.get()` در `or` (قانون #۴۱) | ۷ |
| **M8** | تک‌تک نگفتم فایل‌های `.py` کجا کپی شوند | فرض کردم کاربر می‌داند | همیشه مسیر کپی صریح (قانون #۳۸) | ۷ |
| **M9** | Unicode `✓` در `print()` با cp1252 ویندوز کرش | Windows پیش‌فرض cp1252 است | ASCII-only + `reconfigure(encoding="utf-8")` (قانون #۴۶) | ۷ |
| **M10** | مسیر relative در `entry:` pre-commit با Windows ناسازگار | tokenizer Windows | `python wrapper.py` (قانون #۴۵) | ۷ |
| **M11** | Backslash double-escape در template string | template Python پیچیده | از `pathlib.Path` و read/replace استفاده شود | ۷ |
| **M12** | فراموش کردن فعال‌سازی venv قبل از pre-commit | فرض global PATH | همیشه `venv\Scripts\activate` در راهنما | ۷ |
| **M13** | built-in `mixed-line-ending` hook کرش با cp1252 | hook خود Unicode error می‌دهد | `.gitattributes` (قانون #۴۴) | ۷ |
| **M14** | `entry: cmd /c scripts\\foo.cmd` ناسازگار | YAML escape + Windows tokenize | `python wrapper.py` cross-platform | ۷ |
| **M15** | اولین pre-commit، 78 فایل reformat کرد | پروژه legacy با CRLF mixed | پذیرش mass-format در چت اول hook | ۷ |
| **M16** | pytest hook با env var مشکل | env در hook موجود نیست | hook ها فقط سریع + بدون env | ۷ |
| **M17** | نمی‌توانم تنظیمات کاربر را تغییر دهم | محدودیت طبیعی Claude | راهنمایی، نه تغییر مستقیم | ۷ |
| **M18** | دادن دو فایل `54c`/`54d` با هدف مشابه کاربر را گیج کرد | فایل قدیمی hint نداشت | `[REPLACES PREVIOUS]` در نام | ۷ |
| **M19** | کاربر فقط دستور‌های مهم را اجرا کرد، نه همه | دستور‌ها واضح branding نشده | شماره + نام مرحله برجسته | ۷ |
| **M20** | A1 false positive روی `readVar("..", "#fallback")` | regex خیلی سختگیر | تست hook روی codebase قبل از deploy (قانون #۴۷) | ۷ |
| **M21** | اسکریپت `54e` خودش fail شد به‌خاطر `\\\\b` template | template Python با backslash مضاعف | read/replace به‌جای template (قانون #۳۷) | ۷ |
| **M22** | ⚠️ Reserved / Unknown | — | — | ۷ |
| **M23** ⭐⭐⭐ | Claude در پایان چت ۷ پیام handoff به چت بعد **تولید نکرد** با وجود نوشتن قانون آن در همان چت | اعتماد به حافظه فعال به‌جای چک‌لیست فعال سند ۱۷.۵ | فرآیند جدید (قانون #۶۰): PENDING-EOC در فایل ثبت شود. **مهم‌ترین درس کل پروژه — اگر این حل نشود، همه قوانین فقط روی کاغذند** | ۷ |
| **M24** | ⚠️ Reserved / Unknown | — | — | ۷ |
| **M25** | پاسخ به سؤالات misunderstanding با تأیید ساده، بدون مثال تفاوت‌ها | فرض درست‌بودن سؤال کاربر | تفاوت‌ها با مثال نشان داده شود، نه فقط تأیید. مثال: «MCP ≠ حافظه بین چت‌ها» | ۷ |
| **M26** | اطلاعات نصب Filesystem MCP از حافظه (نه web_search) | فرض به‌روز بودن دانش Claude | web_search برای موارد سریع‌تغییر (Claude Desktop features، نسخه extension ها) | ۷ |
| **M27** | پس از install/configure، چک‌لیست post-install ارائه نشد | فقدان pattern استاندارد | پس از هر install/configure، چک‌لیست تأیید (verification checks) ارائه شود | ۷ |
| **M28** | فرض «Enable توگل = Configure شد» | عدم تشخیص دو مرحله جدا | Enable toggle ≠ Configure — دو گام مستقل. در راهنمای نصب هر دو گام جدا توضیح داده شود | ۷ |
| **M29** | ⚠️ Reserved / Unknown | — | — | ۷ |
| **M30** ⭐ | فرض «Filesystem MCP در همین چت کار خواهد کرد» | عدم اطلاع از reload mechanism | MCP فقط در چت‌های **جدید** load می‌شود. هر extension/connector جدید باید در چت جدید تست شود | ۷ |
| **M31** | پاسخ به «چه قابلیت‌های دیگری وجود دارد» از حافظه (بدون search) | فرض به‌روز بودن قابلیت‌ها | web_search قبل از پاسخ به سؤالات «چه قابلیتی…» | ۷ |
| **M32-M43** | ⚠️ Reserved / Unknown — بازه ۱۲ درس در Memory ظاهر نشد | — | — | ۷ |
| **M44** | فراموش کردن یادآوری به کاربر که Filesystem MCP در چت قبلی در دسترس نیست | فرض اطلاع کاربر از M30 | با هر سؤال «این کار را انجام بده» در چت‌های پیش از MCP، یادآوری محدودیت سیستمی | ۷ |
| **M45-M55** | ⚠️ Reserved / Unknown — بازه ۱۱ درس در Memory ظاهر نشد | — | — | ۷ |
| **M56** | تکیه به Memory برای بازیابی اعداد دقیق و لیست‌های کامل | Memory برای جستجوی مفهومی خوب است، نه ثبت دقیق | برای ثبت دقیق، **فایل** لازم است (نه فقط Memory). مبنای قانون #۶۰ شد | ۸ |
| **M57** | تناقض اعداد در پایان چت (۴۸ vs ۵۹ vs ۵۲ برای قوانین) | بازشمارش بدون مرجع واحد در پایان چت | پایان چت همیشه از یک فایل **source-of-truth** (PENDING_FOR_NEXT_VERSION.md) استفاده شود | ۸ |
| **M58** | متن handoff به‌صورت inline در پیام (نه فایل دانلودی) — کاربر گمان کرد فایل قابل دانلود وجود دارد | عبارت مبهم «این را استفاده کنید» | یا صریح بگو «این **متن** را copy کنید»، یا فایل قابل دانلود تولید کن | ۸ |
| **M59** | موارد جدید (قانون، درس، تصمیم) را **خارج** از متن paste گفتن، نه داخل آن | فرض دیدن همه context چت توسط Claude بعدی | هر موضوع جدید باید **داخل** متن copy/paste باشد، چون Claude بعدی فقط همان متن را می‌بیند | ۸ |
| **M60** ⭐ | Write مستقیم فایل بزرگ/مهم با MCP بدون preview ساختار | عجله یا فرض درست بودن طراحی Claude | قبل از هر write فایل بزرگ/مهم با MCP، ساختار preview شود و تأیید کاربر گرفته شود | ۸ |
| **M61** | اعتماد به status موفقیت کافی نیست (write/install/configure که موفق گزارش می‌شود) | فرض = «گزارش موفق ⇒ نتیجه درست». مثال M1 | همیشه read-back / verify مستقل پس از هر اقدام. چرخه کامل safety: **Preview → Approve → Write → Read-back → Verify → Confirm**. مکمل M1 و M60 | ۸ |
| **M62** | Claude در پیامی قانون #۳۷ را ذکر کرد، ولی در پاسخ بعدی همان چت کاربر باید یادآوری کند که read-back لازم است | قوانینی که خود Claude ذکر می‌کند priority پایین‌تر از یادآوری کاربر می‌گیرند | self-binding: اگر Claude قانونی را ذکر کند، در همان چت ملزم به اجرای آن است | ۸ |
| **M63** ⭐ | Claude در ابتدای چت ۹ فرض کرد «ساخت Project در Claude Desktop» انجام نشده، چون در پیام handoff به‌عنوان «اولین گام» ذکر شده بود — درحالی‌که کاربر قبلاً ساخته بود | پیام handoff کارهای آینده + کارهای انجام‌شده + یادآوری‌ها را در یک لیست ترکیب می‌کند، بدون status صریح | هر آیتم در پیام handoff باید با یکی از prefix های صریح همراه باشد: `✅ DONE`، `📋 TODO`، `⚠️ CHECK`، `💡 NOTE` | ۹ |

---

## ۲.۴ شرح کامل درس‌های بحرانی

### M1 — اعتماد به status موفقیت کافی نیست

**کشف‌شده در:** چت ۷
**اهمیت:** 🔴 critical
**Cross-refs:** قانون #۳۷، M60، M61

#### اشتباه
اسکریپت ۴۸ گزارش «updated» داد، ولی فایل‌ها در workspace به‌روز نشده بودند.

#### علت ریشه‌ای
اسکریپت به `/tmp/zip_stage/` می‌نوشت (مسیر staging موقت)، نه به workspace پروژه. status موفق فقط به این معنا بود که write به آن مسیر staging موفق بود.

#### راه‌حل
بعد از هر write file، فایل را در مسیر **نهایی** (نه staging) **دوباره بخوان** و verify کن. اعتماد به status «updated» کافی نیست — این نقطه شروع قانون #۳۷ است که در همه نسخه‌های بعدی پیشرفت کرد.

#### قوانین مشتق
- **#۳۷:** read-back verify بعد از write
- **#۶۰:** PENDING-EOC در لحظه ثبت (شامل verify در همان لحظه)

---

### M23 ⭐⭐⭐ — مهم‌ترین درس کل پروژه

**کشف‌شده در:** چت ۷
**اهمیت:** 🔴 critical
**Cross-refs:** قانون #۶۰، M56، M57

#### اشتباه
Claude در پایان چت ۷ پیام handoff به چت بعد **تولید نکرد**، با وجود نوشتن قانون آن در همان چت.

#### علت ریشه‌ای
اعتماد به حافظه فعال به‌جای چک‌لیست فعال سند ۱۷.۵. Claude در میانه چت اقدام را قول داد، ولی در پایان چت آن اقدام را فراموش کرد. این اولین مثال از **gap بین قول و عمل** در پروژه بود.

#### راه‌حل
فرآیند جدید (قانون #۶۰): **PENDING-EOC در لحظه ثبت** در `docs/PENDING_FOR_NEXT_VERSION.md` با Filesystem MCP. هر PENDING که در چت ذکر می‌شود، همان لحظه فایل وار ثبت می‌شود. در پایان چت، فایل به سند v(X+1) ادغام می‌شود.

#### چرا مهم‌ترین درس کل پروژه؟
اگر این درس حل نشود، همه قوانین، تصمیمات، و درس‌های دیگر فقط روی کاغذند — چون Claude بعدی آنها را در پایان چت قبلی فراموش می‌کند و چت بعدی بدون اطلاع شروع می‌شود.

#### قوانین مشتق
- **#۶۰:** PENDING-EOC در لحظه ثبت
- **#۶۲:** فایل handoff دائمی پایان چت

---

### M30 ⭐ — MCP فقط در چت جدید load می‌شود

**کشف‌شده در:** چت ۷
**اهمیت:** 🟠 high
**Cross-refs:** M44

#### اشتباه
Claude فرض کرد Filesystem MCP که در همین چت نصب شد، **در همان چت** قابل استفاده است.

#### علت ریشه‌ای
عدم اطلاع از reload mechanism Claude Desktop. هر extension/connector جدید باید در چت **بعدی** test شود، نه current chat.

#### راه‌حل
- پس از نصب هر MCP/extension، اعلام: «این در چت بعدی فعال می‌شود»
- در چت جاری ادامه workflow بدون MCP
- در چت بعدی، اولین قدم: تست MCP با `list_allowed_directories`

---

### M56 — Memory ≠ ثبت دقیق

**کشف‌شده در:** چت ۸
**اهمیت:** 🟠 high
**Cross-refs:** قانون #۶۰، M57

#### اشتباه
تکیه به Memory برای بازیابی اعداد دقیق و لیست‌های کامل (مثل تعداد قوانین، آیتم‌های PENDING).

#### علت ریشه‌ای
Memory برای جستجوی **مفهومی** خوب است («درباره X صحبت کردیم؟»)، نه ثبت **دقیق** («دقیقاً چند مورد؟»).

#### راه‌حل
برای ثبت دقیق، **فایل** لازم است:
- آمار → `SESSION_STATUS.md`
- PENDING → `PENDING_FOR_NEXT_VERSION.md`
- Decisions → `DECISIONS_LOG.md`

Memory صرفاً به‌عنوان hint استفاده شود، نه source of truth.

---

### M60 ⭐ — Preview قبل از Write

**کشف‌شده در:** چت ۸
**اهمیت:** 🔴 critical
**Cross-refs:** قانون #۳۷، M1، M61

#### اشتباه
Write مستقیم فایل بزرگ/مهم با MCP بدون preview ساختار.

#### علت ریشه‌ای
عجله یا فرض درست بودن طراحی Claude — بدون اطلاع کاربر از structure نهایی.

#### راه‌حل
قبل از هر write فایل بزرگ/مهم با MCP:
1. ساختار preview شود (outline + بخش‌ها)
2. تأیید کاربر گرفته شود
3. سپس write
4. سپس read-back verify (M1)
5. سپس confirm

**مزایا:**
- کاهش ریسک data loss
- امکان اصلاح ساختار قبل از commit
- rollback آسان‌تر

---

### M61 — چرخه کامل safety

**کشف‌شده در:** چت ۸
**اهمیت:** 🔴 critical
**Cross-refs:** M1، M60

#### اشتباه
اعتماد به status موفقیت کافی نیست (write/install/configure که موفق گزارش می‌شود ولی نتیجه نهایی متفاوت است).

#### علت ریشه‌ای
فرض = «گزارش موفق ⇒ نتیجه درست». این فرض در چندین درس قبلی (M1, M5, M9) نقض شد.

#### راه‌حل
چرخه کامل safety:
```
Preview → Approve → Write → Read-back → Verify → Confirm
```

هر مرحله مستقل verify می‌شود، نه فقط مرحله نهایی.

---

### M62 — Self-binding

**کشف‌شده در:** چت ۸
**اهمیت:** 🟠 high
**Cross-refs:** قانون #۲۴، #۲۶

#### اشتباه
Claude در پیامی قانون #۳۷ را ذکر کرد، ولی در پاسخ بعدی همان چت کاربر باید یادآوری کند که read-back لازم است.

#### علت ریشه‌ای
قوانینی که خود Claude ذکر می‌کند priority پایین‌تر از یادآوری کاربر می‌گیرند (نقض self-enforcement).

#### راه‌حل
**self-binding:** اگر Claude قانونی را ذکر کند، در همان چت ملزم به اجرای آن است — حتی اگر کاربر یادآوری نکند. این یعنی Claude نمی‌تواند قانون را به‌عنوان "knowledge" ذکر کند ولی به‌عنوان "behavior" رعایت نکند.

---

### M63 ⭐ — Prefix های صریح در handoff

**کشف‌شده در:** چت ۹
**اهمیت:** 🟠 high
**Cross-refs:** قانون #۶۲

#### اشتباه
Claude در ابتدای چت ۹ فرض کرد «ساخت Project در Claude Desktop» انجام نشده، چون در پیام handoff به‌عنوان «اولین گام» ذکر شده بود — درحالی‌که کاربر قبلاً ساخته بود.

#### علت ریشه‌ای
پیام handoff کارهای آینده + کارهای انجام‌شده + یادآوری‌ها را در یک لیست ترکیب می‌کند، بدون status صریح (DONE/PENDING/TODO). Claude مجبور به استنتاج می‌شود — و گاهی اشتباه استنتاج می‌کند.

#### راه‌حل
هر آیتم در پیام handoff باید با یکی از prefix های صریح همراه باشد:
- ✅ DONE
- 📋 TODO
- ⚠️ CHECK
- 💡 NOTE

خصوصاً برای کارهایی که خارج از فایل‌سیستم پروژه انجام می‌شوند (Project در Claude Desktop، GitHub settings، Connectors، ...).

#### قوانین مشتق
- **#۶۲ (v2.11):** فایل handoff دائمی با prefix های اجباری

---

## ۲.۵ شرح کوتاه‌تر سایر درس‌ها (M2-M22, M25-M28, M31, M44, M57-M59)

### M2 — مسیر zip
**اشتباه:** فرض موقعیت zip در `%USERPROFILE%\Downloads`.
**راه‌حل:** پرسیدن یا قانون #۳۴ (zip در root پروژه دانلود شود).

### M3 — argparse syntax
**اشتباه:** پیشنهاد `--zip ... --dry-run` برای اسکریپت با positional args.
**راه‌حل:** قانون #۴۰ — verify argparse syntax قبل از پیشنهاد.

### M4 — single-root zip
**اشتباه:** اسکریپت ۴۳ فقط `docs/` را شناخت.
**راه‌حل:** قانون #۳۹ — multi-root → `python -m zipfile -e`.

### M5 — pip vs npm flags
**اشتباه:** پیشنهاد `pip install --no-audit --no-fund`.
**راه‌حل:** قانون #۳۵ — `--no-audit --no-fund` فقط برای npm.

### M6 — signature verification
**اشتباه:** تست با signature فرضی.
**راه‌حل:** قانون #۳۶ — `findstr /N "def funcname"` قبل از تست‌نویسی.

### M7 — Python `or` short-circuit
**اشتباه:** `payload["user_id"]` در `or` → KeyError.
**راه‌حل:** قانون #۴۱ — `.get()` به‌جای `[]`.

### M8 — مسیر صریح کپی
**اشتباه:** فرض دانش کاربر درباره مسیر فایل‌های `.py`.
**راه‌حل:** قانون #۳۸ — همیشه مسیر صریح.

### M9 — Unicode در Windows print
**اشتباه:** `print("✓")` در Windows cp1252 crash.
**راه‌حل:** قانون #۴۶ — ASCII-only + `sys.stdout.reconfigure(encoding="utf-8")`.

### M10 — Windows pre-commit entry
**اشتباه:** مسیر relative در `entry:` ناسازگار با Windows.
**راه‌حل:** قانون #۴۵ — `python wrapper.py`.

### M11 — backslash double-escape
**اشتباه:** template string با `\\\\b`.
**راه‌حل:** `pathlib.Path` + read/replace.

### M12 — venv activation
**اشتباه:** فراموش‌کردن `venv\Scripts\activate`.
**راه‌حل:** همیشه در راهنما ذکر شود.

### M13 — mixed-line-ending hook
**اشتباه:** built-in hook با cp1252 crash.
**راه‌حل:** قانون #۴۴ — `.gitattributes`.

### M14 — cmd /c در pre-commit
**اشتباه:** `entry: cmd /c scripts\\foo.cmd` ناسازگار.
**راه‌حل:** قانون #۴۵ — `python wrapper.py`.

### M15 — mass reformat
**اشتباه:** اولین pre-commit، 78 فایل reformat کرد.
**راه‌حل:** پذیرش mass-format در commit جدا + `[skip-hooks]`.

### M16 — pytest hook + env
**اشتباه:** pytest hook با env var مشکل داشت.
**راه‌حل:** hook ها فقط سریع + بدون env (pytest به pre-push).

### M17 — تنظیمات کاربر
**اشتباه:** فرض می‌توانم تنظیمات Settings کاربر را تغییر دهم.
**راه‌حل:** راهنمایی، نه تغییر مستقیم.

### M18 — versioning فایل‌های Claude
**اشتباه:** دادن دو فایل `54c`/`54d` بدون hint.
**راه‌حل:** `[REPLACES PREVIOUS]` در نام.

### M19 — branding دستورات
**اشتباه:** کاربر فقط دستورات مهم را اجرا کرد.
**راه‌حل:** شماره + نام مرحله برجسته (مبنای قانون #۶۳).

### M20 — false positive regex
**اشتباه:** A1 hook روی `readVar("..", "#fallback")` false-positive.
**راه‌حل:** قانون #۴۷ — تست hook روی codebase قبل از deploy.

### M21 — template Python با backslash
**اشتباه:** اسکریپت `54e` خودش fail شد.
**راه‌حل:** read/replace به‌جای template + قانون #۳۷ (read-back).

### M25 — misunderstanding
**اشتباه:** پاسخ به سؤال misunderstanding با تأیید ساده.
**راه‌حل:** تفاوت‌ها با مثال نشان داده شود. مثال: «MCP ≠ حافظه بین چت‌ها».

### M26 — web_search برای دانش به‌روز
**اشتباه:** پاسخ به سؤال نصب MCP از حافظه.
**راه‌حل:** web_search برای موارد سریع‌تغییر (Claude Desktop features، نسخه‌ها).

### M27 — post-install checklist
**اشتباه:** پس از install/configure، چک‌لیست تأیید ارائه نشد.
**راه‌حل:** pattern استاندارد — همیشه verification checks پس از install.

### M28 — Enable ≠ Configure
**اشتباه:** فرض «Enable توگل = Configure شد».
**راه‌حل:** دو گام مستقل — هر دو در راهنما جدا توضیح داده شود.

### M31 — web_search برای قابلیت‌ها
**اشتباه:** پاسخ به «چه قابلیتی…» از حافظه.
**راه‌حل:** web_search قبل از پاسخ‌های قابلیت‌محور.

### M44 — یادآوری محدودیت
**اشتباه:** فراموش‌کردن یادآوری به کاربر که MCP در چت قبلی فعال نیست.
**راه‌حل:** با هر سؤال «این کار را انجام بده» در چت‌های پیش از MCP، یادآوری M30.

### M57 — تناقض اعداد در پایان چت
**اشتباه:** بازشمارش بدون مرجع واحد.
**راه‌حل:** پایان چت همیشه از یک فایل source-of-truth (PENDING_FOR_NEXT_VERSION.md).

### M58 — متن inline vs فایل دانلودی
**اشتباه:** عبارت مبهم «این را استفاده کنید».
**راه‌حل:** صریح بگو «این **متن** را copy کنید» یا فایل قابل دانلود تولید کن.

### M59 — موارد جدید داخل متن
**اشتباه:** ذکر موارد جدید خارج از متن paste.
**راه‌حل:** هر موضوع جدید **داخل** متن copy/paste باشد، چون Claude بعدی فقط همان را می‌بیند.

---

## ۲.۶ Reserved IDs (سیاست Conservative Numbering)

طبق قانون «conservative numbering policy» (v2.10) و M79، شماره‌های زیر **Reserved** اند:

| ID | وضعیت | علت |
|---|---|---|
| **M22, M24, M29** | ⚠️ Reserved / Unknown | در Memory ظاهر نشد |
| **M32-M43** | ⚠️ Reserved / Unknown (۱۲ درس) | gap بزرگ چت ۷ |
| **M45-M55** | ⚠️ Reserved / Unknown (۱۱ درس) | gap دوم چت ۷ |

**فلسفه:** مثل CVE numbers، gap های شناخته نگه داشته می‌شوند تا اگر در آینده کشف شدند، جای آن‌ها مشخص باشد. این نسبت به re-numbering ایمن‌تر است.

**مجموع Reserved تا پایان v2.11:** ۲۶ مورد (M22, M24, M29, M32-M43, M45-M55).

---

## 🚧 وضعیت این ماژول

✅ **Migration کامل از v2.11** — درس‌های M1-M63 (با ۲۶ Reserved explicit) ثبت شدند.

## ۲.۷ درس‌های جدید v2.12 (M64-M86) — اعمال‌شده در commit 8

> خلاصه لیست پایین canonical است. توضیحات کامل در chat history چت‌های ۱۰، ۱۱، ۱۱.۰.الف تحلیل شده. M82-M86 (critical) در بخش ۲.۸ با جزئیات بیشتر آمده.

### درس‌های فنی چت ۱۰ (M64-M70)
- **M64** JSX runtime در plugin-react vs esbuild
- **M65** تشخیص shell از prompt
- **M66** ⚠️ Filesystem MCP و فایل‌های >۲۰۰KB hang می‌کند
- **M67** 🔴 BOM لازم برای pip روی Windows
- **M68** نسخه‌های pinned باید با PyPI verify شوند
- **M69** asyncio.run() در FastAPI handler crash می‌کند
- **M70** سادگی workflow > لایه‌بندی پیچیده

### درس‌های process چت ۱۰ cleanup round 1 (M71-M73)
- **M71** ⚠️ Documentation Drift Self-Reference Paradox
- **M72** End-of-Chat Verification Checklist
- **M73** Cross-Document Consistency Audit

### درس‌های چت ۱۱ cleanup round 2 (M74-M79)
- **M74** Full-Range Decision Audit (نه Local)
- **M75** Within-File Consistency Check
- **M76** Decision vs Rule تمایز مبهم (Locked vs Proposed)
- **M77** ⭐ HEAD Self-Reference نباید Hardcode باشد
- **M78** Re-read After Edit
- **M79** Reserved IDs Explicit مستند شوند

### درس‌های چت ۱۱.۰.الف (M80-M86)
- **M80, M81** → Reserved (سیاست gap)
- **M82** ⭐ Verification Claim Must Be Verified Itself — جزئیات در ۲.۸
- **M83** Retry First, Restructure Last — جزئیات در ۲.۸
- **M84** Multi-line `-m` در CMD vs PowerShell — جزئیات در ۲.۸
- **M85** Terminal Type Awareness (CMD vs PowerShell prompt)
- **M86** Two-step commit-then-push (همیشه در دو کادر جدا) — جزئیات در ۲.۸

---

## ۲.۸ توضیحات کامل critical lessons M82-M86

### M82 ⭐ — Verification Claim Must Be Verified Itself

**کشف‌شده در:** چت ۱۱.۰.الف | **اهمیت:** 🔴 critical | **Cross-refs:** M1, M37, M61

**اشتباه:** Claude در cleanup round 1 چت ۱۰ ادعا کرد «همه سند sync شدند» بدون این‌که خودش را verify کند. تناقض واقعی در چت ۱۱ کشف شد.
**علت:** فرض «ادعای انجام = انجام واقعی» — تکیه به memory به‌جای read-back.
**راه‌حل:** هر ادعای «X انجام شد» خودش یک claim است که نیاز به verify دارد. در پروژه فعلی: پس از هر write_file/edit_file، حتماً read_text_file با head/tail برای verify — نه تکیه به diff output.

### M83 — Retry First, Restructure Last

**کشف‌شده در:** چت ۱۱.۰.الف | **اهمیت:** 🟡 medium

**اشتباه:** در واجهه با transient MCP failure، پیشنهاد rename/restructure.
**ترتیب درست در tool failure:**
1. **Retry ساده** — خیلی رایج، MCP transient bugs
2. **Restart MCP/tool_search مجدد** — اگر retry کار نکرد
3. **Workaround موقت** — مثل روش جایگزین
4. **تغییر ساختاری دائمی** — آخرین گزینه (تغییر نام فایل، بازسازی ساختار)

**مثال عملی:** در چت ۱۱.۰.الف edit_file با‌ «could not find match» غلط داد. با خواندن دوباره فایل (پیروی از M83) معلوم شد اختلاف در arrow character (`←` vs `→`) بود. بدون restructure حل شد.

### M84 — Multi-line `-m` در CMD vs PowerShell

**کشف‌شده در:** چت ۱۱.۰.الف (commit 1) | **اهمیت:** 🟡 medium | **Cross-refs:** M85

**اشتباه:** `git commit -m "خط 1\nخط 2"` در CMD فقط خط اول را commit کرد، بقیه به‌عنوان دستور CMD اجرا شدند.
**علت:** CMD و PowerShell دستورات multi-line را متفاوت parse می‌کنند. `\n` literal در CMD تفسیر نمی‌شود.
**راه‌حل (cross-shell):** استفاده از چند `-m` پشت سر هم (یک `-m` برای هر پاراگراف). git خود خط خالی بین آن‌ها قرار می‌دهد. در هر دو shell کار می‌کند.

```bash
git commit -m "عنوان" -m "پاراگراف ۲" -m "پاراگراف ۳"
```

### M85 — Terminal Type Awareness

**کشف‌شده در:** چت ۱۱.۰.الف | **اهمیت:** 🟠 high (ارتقا از medium پس از enforcement test) | **Cross-refs:** M65

| Terminal | Prompt | ویژگی |
|---|---|---|
| PowerShell | `(venv) PS D:\...>` | UTF-8 native، multi-line friendly |
| CMD | `(venv) D:\...>` | cp1252، سنتی‌تر |

**راه‌حل:** Claude در هر خروجی terminal، prompt را verify کند. دستورات را cross-shell بدهد (M84 روش).

#### ⭐ Enforcement Test واقعی (در همین چت)

**تاریخ:** ۲۰۲۶-۰۵-۲۱ | **رویداد:** Claude در همان چتی که M85 را نوشت، آن را نقض کرد.

**سناریو:** در commit 8 EXECUTE block برای copy فایل archive، Claude PowerShell cmdlets داد (Copy-Item, Test-Path, Get-Item) در حالی که prompt کاربر صریح `(venv) D:\Projects\trading-system>` (CMD) بود.

**خروجی خطا:**
```
'Copy-Item' is not recognized as an internal or external command
'Test-Path' is not recognized as an internal or external command
'Get-Item' is not recognized as an internal or external command
```

**درس عمیق‌تر:**
- نوشتن یک قانون در constitution، باعث رعایت آن توسط Claude در همان چت نمی‌شود
- writing pattern A سپس violating pattern A یک فرم جدید از documentation drift است (احتمالاً M87 در چت ۱۱.۰.ج)
- ورود اجباری: Claude **پیش از هر EXECUTE block،** باید آخرین prompt واقعی کاربر را صریح verify کند — نه memory جلسه لحظه‌ای

**اصلاح اعمال‌شده:** از commit 8 به بعد، هر EXECUTE block باید cross-shell باشد. برای فایل operations: `copy`/`dir` (در هر دو کار می‌کند) ترجیح داده شود بر PowerShell-only cmdlets.

**Cross-shell جدول مرجع:**

| عملیات | CMD-only | PowerShell-only | Cross-shell ✅ |
|---|---|---|---|
| copy file | `copy A B` | `Copy-Item A B` | `copy A B` (هم در PS تعریف شده) |
| list files | `dir` | `Get-ChildItem` / `gci` | `dir` (alias در هر دو) |
| check exists | `if exist A ...` | `Test-Path A` | git-style یا تفکیک |
| change dir | `cd /d D:\...` | `cd D:\...` | `cd D:\...` (در PS بدون /d کار می‌کند، در CMD /d لازم است تنها اگر drive تغییر کند) |
| remove file | `del A` | `Remove-Item A` | `del A` |
| make dir | `mkdir A` | `New-Item -ItemType Directory A` | `mkdir A` |

**کلید طلایی:** دستورات سبک CMD تقریباً همیشه در PowerShell هم کار می‌کنند (جهت backward-compat). عکس آن صحیح نیست. **در شک → CMD-style.**

### M86 — Two-step commit-then-push

**کشف‌شده در:** چت ۱۱.۰.الف (commits 1، 2) | **اهمیت:** 🟡 medium | **Cross-refs:** قانون #۶۶

**اشتباه:** دستورات commit + push در یک کادر یکجا داده شد، کاربر فقط بخش اول را paste کرد.
**راه‌حل:** commit در یک کادر کد، push در کادر کد جداگانه بعدی — در دو مرحله EXECUTE block. این برای اتمینان از انجام هر دو گام است.

---

## 🚧 وضعیت این ماژول

✅ **Migration کامل از v2.11 + Atomic Update v2.12** — درس‌های M1-M86 ثبت شد.

✅ **افزوده‌های v2.12 اعمال‌شده:**
- M64-M70 (فنی چت ۱۰): خلاصه در ۲.۷
- M71-M73 (process cleanup round 1): خلاصه در ۲.۷
- M74-M79 (cleanup round 2): خلاصه در ۲.۷
- M80-M81 (Reserved)
- M82-M86 (چت ۱۱.۰.الف): خلاصه در ۲.۷ + جزئیات کامل در ۲.۸

جمع جدید: ۶۳ درس ثبت + ۲۸ Reserved.

---

**📌 پایان 02_lessons.md (commit 8 — atomic update v2.12 applied)**
