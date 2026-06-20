# ماژول ۰۲ — درس‌نامه اشتباهات Claude

> بخشی از **Constitution v2.17 (Modular)** — [بازگشت به main](./main.md)
>
> **محتوا:** درس‌نامه اشتباهات Claude (M1-M63 از v2.11) با علت ریشه‌ای، راه‌حل، cross-refs.
> **منبع:** سند جامع v2.11 → سند ۱۸ (درس‌نامه اشتباهات Claude — AI Mistakes Log)
> **Created in commit:** `<git log --diff-filter=A --oneline -- docs/constitution/02_lessons.md>` (migrate سند ۱۸ → 02_lessons، commit 3/8؛ هش از git مشتق شود — نه hardcode در ماژول، per #۸۶/check_5)
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
| **Documentation drift** | M71-M73, M74-M79 | به ۲.۸ + ۲.۹ مراجعه کنید |
| **Manifest/Audit hazards** 🆕 v2.14 | M88, M96, M101 | Hidden regeneration + Z-ID permanence + Post-handoff drift |
| **Atomic governance** 🆕 v2.14 | M93, M98, M99, M100 | Triple-Rule + Scope closure + -F flag + visibility |
| **Shell encoding hazards** 🆕 v2.14 | M95, M97 | CMD pipe + quote-tracking catastrophe |
| **Rule design quality** 🆕 v2.14 | M102 | Interface-implementation decoupling |
| **Process pattern positive** 🆕 v2.14 | M94 | Black auto-reformat re-stage |
| **Helper consultation** 🆕 v2.14 | HM-1 to HM-7 | به §۲.۹ مراجعه کنید |

---

## ۲.۳ جدول کامل اشتباهات (M1-M63 + M88-M105 — M64-M87 در §۲.۷ خلاصه)

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
| **M88** ⭐⭐⭐ | Hidden Regeneration Hazard — explicit-list anti-pattern در governance docs، drift hazard | hardcoded list به‌جای principle + authoritative source | principle-based با reference به authoritative source (manifest، script). illustration examples allowed، enumeration نه | S2.2 + S2.5 |
| **M89** | ⚠️ Reserved | — | — | — |
| **M90** | ⚠️ Reserved | — | — | — |
| **M91** | ⚠️ Reserved | — | — | — |
| **M92** | ⚠️ Reserved | — | — | — |
| **M93** ⭐⭐⭐ | Triple-Rule Atomic Boundary — state-of-record files جدا commit شدند → drift | فرض «بعداً commit می‌کنم» در stage boundary | SESSION_STATUS + CHAT_LOG + PENDING (+ REVIEW_LOG if applicable) atomic در یک commit. Rule #۷۳ enforcement | Phase 3 cleanup |
| **M94** ✨ | Black Auto-Reformat Re-Stage Pattern (positive) — expected workflow، نه anti-pattern | فرض «auto-format = issue»، در حالی که normal pre-commit cycle است | re-stage پس از auto-format → re-commit. expected per `.pre-commit-config.yaml` design | S1 sub-commits |
| **M95** ⭐ | CMD Pipe Character in Commit Messages — `\|` در `-m` در CMD = pipe → command parse error | فرض CMD escape مثل bash | ASCII-only commit subject، special chars (`\|`, `&`, `<`, `>`) ممنوع. اگر لازم → -F flag (M99) | S2.1 |
| **M96** ⭐ | Z-ID Permanence Anti-pattern — Z-IDs در permanent docs reference شدند → dangling پس از v(X+1) merge | Z-IDs lifecycle ابهام | permanent docs به permanent IDs (Rule #N, M-N, Decision #). Z-IDs فقط در PENDING. Rule #۷۴ enforcement | S2.2 |
| **M97** ⭐⭐⭐ | CMD Quote-Tracking Catastrophic Failure — em-dash + redirect در multi-line CMD = stray file created with garbage name | CMD encoding cp1252 + multi-line quote tracking | ASCII-only commit messages، redirect operations فقط با ASCII content. -F flag از فایل (M99) | S2.2 |
| **M98** ⭐ | Review Scope Closure (Temporally Closed Reviews) — Review file forward-reference به upcoming sub-stage داشت → scope creep | فرض «Review می‌تواند ongoing scope را cover کند» | هر Review scope-closed، atomic. forward-reference ممنوع within atomic commit. **استثنا (caveat):** T1 governance docs می‌توانند planning intent references داشته باشند — distinct از scope creep. Rule #۷۵ enforcement | S2.3 |
| **M99** ⭐⭐⭐ | CMD Long-Command Paste-Break + -F Flag Standard — multi-line `-m` در CMD inline = 100% failure | CMD line buffer + quote tracking limits | `git commit -F claude_workspace/commit_msg_{stage}.txt` standard برای commit messages > 2-3 lines. ASCII-only فایل (M95+M97) | S2.3 |
| **M100** ⭐⭐⭐ | Hidden-Checklist Completion (Implicit Validation Failure) — mental checking → partner cannot catch missed steps | فرض «در ذهن چک کردم = enough» | explicit Yes/No + reasoning per check در chat surface. format: bullet/table. Rule #۷۶ enforcement | S2.4 |
| **M101** ⭐ | Post-Handoff State Drift — chat-end commit hash در خود commit نمی‌تواند ثبت شود (chicken-and-egg M77 extension) | self-reference impossibility در atomic commit | mutual chain backfill: چت بعدی در boot، hash چت قبل را در CHAT_LOG ثبت کند. precedent chain: part04 → part05 → D24 → part07 (hashes ثبت در CHAT_LOG.md boot sections) | part04→part05 transition |
| **M102** ⭐ | Rule-Implementation Decoupling (Interface-Implementation separation) — قانون normative text با implementation detail mixed → drift در implementation = rule violation | فرض «detail در rule body بهتر است» | Rules: Normative paragraph + جدا Implementation Notes section. detail در script/config/companion doc. normative stays stable، implementation evolves | S3.1 design phase |
| **M103** ⭐⭐⭐ | Audit Over-Promise Pattern — ادعای «deep-scan تقریباً کامل» با ~۳۵٪ coverage واقعی + self-imposed scope narrowing + optimistic reporting (screenshot coverage = project coverage) | اعتماد به pattern-matching + خوش‌بینی در گزارش به‌جای اعداد دقیق | ۸ Trust Rule #۷۸-۸۵ (scope contract + quantitative honesty + no self-narrowing + refuse/defer + pre-task checkpoint + honesty audit + anti-pattern-matching + self-activation lock) | part10 |
| **M104** ⭐⭐⭐ | Mechanical-Claim Verification before Persisting — عدد/شناسهٔ مکانیکی (handoff/hash/ledger/قانون/Review/نسخه) باید از منبع زنده استخراج شود نه حافظه/الگو/استنتاج دنباله‌ای | اعتماد به استنتاج دنباله‌ای به‌جای استخراج از frontier واقعی + بدون cross-check با invariant فعال | قانون #۸۶ + corollary escape (frontier پس از escape جلو نمی‌رود) | part14 |
| **M105** ⭐ | EXECUTE Command Paste-Integrity (`&`-chain) — دستورهای چندتایی CMD در خطوط جدا هنگام یک‌paste وسط زنجیره متوقف می‌شوند (آخری منتظر Enter) | CMD line-buffering خطوط متعدد را جدا اجرا می‌کند؛ echo/خروجی طولانی buffering را بدتر می‌کند | دستورهای کوتاه/مرتبط را با `&` در یک خط زنجیر کن (یک paste + یک Enter)؛ مکمل #۶۷/M99 | part18 |

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

**مجموع Reserved تا پایان v2.13:** ۲۸ مورد (M22, M24, M29, M32-M43, M45-M55, M80, M81).

**🆕 v2.14 Reserved اضافه‌شده:**

| ID | وضعیت | علت |
|---|---|---|
| **M89-M92** | ⚠️ Reserved (۴ مورد) | CVE-like gap preservation per M79 policy — ID space between critical M88 (Hidden Regeneration) and M93 (Triple-Rule) reserved برای potential discoveries در آینده |

**مجموع Reserved تا پایان v2.14:** ۳۲ مورد.

---

## 🚧 وضعیت این ماژول

✅ **Migration کامل از v2.11** — درس‌های M1-M63 (با ۲۶ Reserved explicit) ثبت شدند.

## ۲.۷ درس‌های جدید v2.12-v2.14 (M64-M102) — اعمال‌شده

> خلاصه لیست پایین canonical است. توضیحات کامل critical lessons در §۲.۸. درس‌های HM-series helper-side در §۲.۹ مستقل.

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

### درس چت ۱۱.۰.ج (M87)
- **M87** ⭐⭐⭐ Active-Writing Self-Binding Failure — جزئیات در ۲.۸ (تبدیل از Z2.20 PENDING به Locked، پشتیبان قانون #۶۷)

### درس‌های v2.14 — S3.1 از MDRS v2 (M88, M93-M102)

- **M88** ⭐⭐⭐ Hidden Regeneration Hazard — جزئیات در ۲.۸
- **M89-M92** → Reserved (CVE-like gap)
- **M93** ⭐⭐⭐ Triple-Rule Atomic Boundary — جزئیات در ۲.۸
- **M94** ✨ Black Auto-Reformat Re-Stage Pattern (positive)
- **M95** ⭐ CMD Pipe Character in Commit Messages — جزئیات در ۲.۸
- **M96** ⭐ Z-ID Permanence Anti-pattern — جزئیات در ۲.۸
- **M97** ⭐⭐⭐ CMD Quote-Tracking Catastrophic Failure — جزئیات در ۲.۸
- **M98** ⭐ Review Scope Closure — جزئیات در ۲.۸
- **M99** ⭐⭐⭐ CMD Long-Command Paste-Break + -F Flag Standard — جزئیات در ۲.۸
- **M100** ⭐⭐⭐ Hidden-Checklist Completion — جزئیات در ۲.۸
- **M101** ⭐ Post-Handoff State Drift (mutual chain backfill) — جزئیات در ۲.۸
- **M102** ⭐ Rule-Implementation Decoupling — جزئیات در ۲.۸

### درس‌های v2.15 — Trust & Anti-Sycophancy

- **M103** ⭐⭐⭐ Audit Over-Promise Pattern (part10 origin) — جزئیات در ۲.۸. پشتیبان ۸ قانون Trust #۷۸-۸۵.

### درس v2.16 — Mechanical-Claim Verification

- **M104** ⭐⭐⭐ Mechanical-Claim Verification before Persisting (part14 origin) — جزئیات در ۲.۸. پشتیبان قانون #۸۶.

### درس v2.17 — EXECUTE Paste-Integrity

- **M105** ⭐ EXECUTE Command Paste-Integrity (`&`-chain) (part18 origin) — جزئیات در ۲.۸. دستورهای چندتایی ترمینال با `&` در یک خط؛ مکمل #۶۷/M99.

### درس‌های helper-side v2.14 — HM-series

HM-namespace جداگانه برای helper-side patterns. ↓ به §۲.۹ مراجعه کنید.

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

### M87 ⭐⭐⭐ — Active-Writing Self-Binding Failure (v2.13)

**کشف‌شده در:** چت ۱۱.۰.الف enforcement test M85 | **اهمیت:** 🔴 critical | **Cross-refs:** M62, M85, قانون #۶۷

**اشتباه:** Claude در چت ۱۱.۰.الف، M85 (Terminal Type Awareness) را نوشت و بلافاصله در EXECUTE block بعدی، به کاربر CMD دستورات PowerShell-only (Copy-Item، Test-Path، Get-Item) داد. خروجی خطا: «not recognized».

**علت:** نوشتن قانون ≠ ساختن habit. Memory از "just wrote X" ضعیف‌تر از pattern عادتی است.

**تفاوت با M62:**
- M62 (Self-binding): Claude قانون موجود را ذکر می‌کند ولی فراموش می‌کند
- M87 (Active-Writing): Claude قانون جدید را می‌سازد ولی در همان چت نقض می‌کند — چون writing جدید القای رعایت می‌کند بدون انکه habit واقعی بسازد

**راه‌حل سه‌لایه در v2.13:**

*Layer 1 — Positive Constraint:* قانون #۶۷ با لیست صریح cmdlets ممنوع و label اجباری. تقلید الگوی موفق قانون #۴۶ (ASCII-only).

*Layer 2 — Visible Pre-EXECUTE Verification:* Claude قبل از هر EXECUTE block، یک خط verification در پاسخ بنویسد که visible باشد برای کاربر. جزئیات: `06_meta.md` Template 9.

*Layer 3 — Audit Extension (آینده):* Layer 1 audit می‌تواند گسترش یابد. در v2.13 پیاده نشده.

**درس عمیق‌تر:** «نوشتن یک درس در constitution، باعث رعایت آن توسط Claude در همان چت نمی‌شود.» برای رفع واقعی، نیاز به تغییر ساختاری: positive constraint + explicit list در قانون (نه صرفاً «حواست باشد» در درس).

---

### M88 ⭐⭐⭐ — Hidden Regeneration Hazard

**کشف‌شده در:** S2.2 (Tier rules design) + S2.5 (manifest regeneration) | **اهمیت:** 🔴 critical | **Cross-refs:** Z3.8, Rule #۶۸, Golden Rule

**اشتباه:** Constitution یا governance doc explicit list (T1 file list، rule pattern list) hardcode می‌کند → آینده drift inevitable است (artifact جدید اضافه می‌شود، list نمی‌خواند به‌روز شود → silent inconsistency).

**علت:** فرض «list = simplicity»، در حالی که enumeration = drift hazard. mental model: list برای human readability خوب است، ولی برای machine truth منبع authoritative single point of truth لازم است.

**راه‌حل:** principle-based authoring با illustration examples، نه enumeration. authoritative source explicit: «authoritative source = `scripts/64_generate_manifest.py` TIER_RULES» یا «manifest output». اگر list ذکر می‌شود → with explicit note «illustration only, not authoritative».

**Pattern signature:**
- ❌ "T1 files include: A, B, C, D, ..." (hardcoded enumeration)
- ✅ "T1 files: see PROJECT_MANIFEST.md Tier=T1 entries (authoritative source)"

**Self-application evidence:** HELPER_PROTOCOL §۲.۲ Layer A خود این principle را اعمال کرد (manifest-lookup به‌جای hardcode list). Rule #۶۸ خود M88 را codify می‌کند.

---

### M93 ⭐⭐⭐ — Triple-Rule Atomic Boundary

**کشف‌شده در:** Z3.11 (Phase 3 cleanup) | **اهمیت:** 🔴 critical | **Cross-refs:** Rule #۷۳, Rule #۲۶

**اشتباه:** state-of-record files (SESSION_STATUS + CHAT_LOG + PENDING) را جدا commit کردم → یکی update شد، دیگران stale ماندند تا چت بعد.

**علت:** فرض «بعداً سینک می‌کنم»، در حالی که atomic boundary = single point of synchronization. partial state = state drift.

**راه‌حل:** در هر stage boundary، state-of-record files atomic در یک commit:
- `SESSION_STATUS.md` (همیشه)
- `CHAT_LOG.md` (همیشه)
- `PENDING_FOR_NEXT_VERSION.md` (همیشه)
- `REVIEW_LOG.md` (اگر Review status transition)
- `PROJECT_MANIFEST.md` (اگر stage-final یا mid-stage drift detected per Z3.21 policy)

**Pattern signature:**
- ❌ commit 1: SESSION_STATUS فقط → commit 2 (چت بعد): CHAT_LOG → drift detected
- ✅ single commit: همه atomic → consistent snapshot

**Rule #۷۳ این principle را Lock می‌کند.**

---

### M94 ✨ — Black Auto-Reformat Re-Stage Pattern (positive)

**کشف‌شده در:** S1 sub-commits 2, 3 | **اهمیت:** 🟢 positive workflow | **Cross-refs:** قانون #۴۲, #۴۳

**Pattern:** pre-commit black hook auto-formats Python files، فایل modified می‌شود، commit fail می‌دهد. re-stage + re-commit → موفق. این **expected workflow** است، نه anti-pattern.

**نکته:** قبل از v2.14، Claude گاهی این را به‌عنوان "fix" تلقی می‌کرد. در حقیقت تنها روش صحیح pre-commit hook chain با auto-formatting است.

**Workflow standard:**
```
git add .
git commit -m "..."           # black reformat → fail
git add .                     # re-stage formatted files
git commit -m "..."           # success
git push origin <branch>
```

این non-anti-pattern لازم به ثبت explicit چون historically misclassified.

---

### M95 ⭐ — CMD Pipe Character in Commit Messages

**کشف‌شده در:** S2.1 attempt 1 | **اهمیت:** 🟠 high | **Cross-refs:** M97, M99

**اشتباه:** `git commit -m "feat(docs): X | Y | Z"` در CMD → CMD pipe `|` را به‌عنوان command separator interpret کرد → command parse error.

**علت:** CMD shell special chars (`|`, `&`, `<`, `>`, `^`) در quoted strings نیز literal نیستند مگر با escape `^`.

**راه‌حل:** ASCII-only + simple commit subjects. اگر pipe لازم → `-F` flag (M99).

**Prevention:**
- subject ASCII-only، special chars اجتناب
- اگر pipe/& لازم → -F flag
- در CMD، quote tracking + escape rules ضعیف

---

### M96 ⭐ — Z-ID Permanence Anti-pattern

**کشف‌شده در:** S2.2 design (user catch) | **اهمیت:** 🟠 high | **Cross-refs:** Rule #۷۴, Z3.17

**اشتباه:** Review #۰۰۱ early draft به Z3.x reference داشت — Z-IDs در PENDING transient هستند، در v(X+1) ادغام، evaporate یا با RESOLVED marker می‌مانند. Reference در permanent doc → dangling.

**علت:** Z-IDs lifecycle ambiguous بود.

**راه‌حل:** permanent docs به permanent IDs reference دهند:
- Rule #N (constitution)
- M-N / HM-N (lessons)
- Decision # (DECISIONS_LOG)
- Bug #N (constitution/TROUBLESHOOTING)

Z-IDs فقط در PENDING + transient workspace docs.

**Rule #۷۴ این boundary را Lock می‌کند.**

**Transitional note:** atomic v(X+1) update window می‌تواند Z→permanent reference را acknowledge کند (e.g., "this Rule resolves Z3.17") — این temporary acceptable است، post-merge Z با RESOLVED marker می‌ماند per Z2.20 precedent.

---

### M97 ⭐⭐⭐ — CMD Quote-Tracking Catastrophic Failure

**کشف‌شده در:** S2.2 attempt 1 (stray file `M` evidence) | **اهمیت:** 🔴 critical | **Cross-refs:** M95, M99

**اشتباه:** `git commit -m "feat: X — done > file"` در CMD multi-line paste → em-dash `—` (non-ASCII utf-8) + redirect `>` → CMD quote tracking broke → فایل با نام `M` (single char از scrambled parse) با garbage content ساخته شد.

**علت:** CMD cp1252 + utf-8 mismatch + multi-line quote tracking + redirect operations همگی fragile.

**راه‌حل:** ASCII-only همه چیز در commit operations. -F flag از فایل (M99). em-dash → hyphen-hyphen `--`.

**Prevention:**
- ASCII-only enforce strictly
- -F flag standard for any complex commit
- redirect operations فقط با ASCII content
- multi-line commit messages NEVER inline

**Severity:** critical چون silent data corruption ایجاد می‌کند (stray file با garbage)، نه clean error.

---

### M98 ⭐ — Review Scope Closure (Temporally Closed Reviews)

**کشف‌شده در:** S2.3 design (user trio catches) | **اهمیت:** 🟠 high | **Cross-refs:** Rule #۷۵, REVIEW_PROTOCOL §۹.۱

**اشتباه:** Review #۰۰۱ early draft شامل forward-reference به upcoming sub-stage داشت (S2.5+) — این scope creep بود، Review را open-ended می‌کرد.

**علت:** فرض «Review می‌تواند ongoing scope را cover کند».

**راه‌حل:** هر Review scope-closed، atomic. forward-reference ممنوع within atomic commit boundary.

**Caveat (M98 distinct):**
T1 governance docs (مثل HELPER_PROTOCOL.md) می‌توانند **planning intent references** داشته باشند — این متفاوت از scope creep در atomic commit است.
- T1 governance doc planning intent (e.g., "implementation در part07") = inherent forward-looking design، acceptable
- Atomic commit scope creep (e.g., Review file references upcoming sub-stage) = unacceptable

Distinction: doc design vs commit boundary. هر دو scope-closed، ولی در دو scope جداگانه.

**Rule #۷۵ این boundary را Lock می‌کند.**

---

### M99 ⭐⭐⭐ — CMD Long-Command Paste-Break + -F Flag Standard

**کشف‌شده در:** S2.3 attempt 1 (100% inline failure) | **اهمیت:** 🔴 critical | **Cross-refs:** M95, M97

**اشتباه:** multi-line `git commit -m "line1" -m "line2" -m "line3"` در CMD paste → CMD line buffer limit + quote tracking break → فقط line1 commit شد، خطوط بعد به‌عنوان separate commands اجرا.

**علت:** CMD inline commit messages با > 2-3 lines = unreliable.

**راه‌حل (standard):** `-F` flag از فایل:
```cmd
git commit -F claude_workspace/commit_msg_{stage}.txt
```

**Requirements:**
- فایل ASCII-only (M95+M97)
- در `claude_workspace/` (T5 workspace، نه T1)
- naming convention: `commit_msg_{stage}.txt` (e.g., `commit_msg_s3_1.txt`)
- پس از commit، فایل preserved per Z3.18/Z3.23 policy (consumed but not deleted)

**Rule #۹۹ standard (de facto در v2.14 با Template 12 در S3.2 formalize می‌شود).**

---

### M100 ⭐⭐⭐ — Hidden-Checklist Completion (Implicit Validation Failure)

**کشف‌شده در:** S2.4 design (user catch) | **اهمیت:** 🟠 high | **Cross-refs:** Rule #۷۶, M86

**اشتباه:** «checks را در ذهن انجام دادم، نتیجه را preview نوشتم» — این mental checking برای partner (انسان یا future audit) invisible است.

**علت:** فرض «mental verification = enough».

**راه‌حل:** explicit Yes/No + reasoning per check در chat surface (visible to partner).

**Format options:**
- bullet list با ✅/❌/⏸ marker
- table با ستون Result + Note (نمونه‌ها در PRE_ADD_CHECKLIST.md §۵)
- per-check paragraph

**درس عمیق‌تر:**
- mental checking = invisible to partner
- partner نمی‌تواند ۱-۲ check missed را catch کند
- future audit (D12/D21) impossible
- visibility = collaborative quality

**Rule #۷۶ این principle را Lock می‌کند.**

---

### M101 ⭐ — Post-Handoff State Drift (mutual chain backfill)

**کشف‌شده در:** part03→part04 transition (Discovery #۸) | **اهمیت:** 🟠 high | **Cross-refs:** M77, M86, Rule #۷۳

**اشتباه:** chat-end commit شامل reference به HEAD خود (chicken-and-egg) — مثال: SESSION_STATUS می‌گوید "Branch HEAD: this commit"، ولی hash تا commit شدن مشخص نیست.

**علت:** atomic commit cannot reference its own hash (M77 genus extension).

**راه‌حل:** mutual chain backfill mechanism:
- placeholder `<filled at chat-end>` در فایل
- چت بعدی در boot، hash چت قبل را از `git rev-parse HEAD~N` بازیابی + در CHAT_LOG.md ثبت
- این یک forward-anticipation explicit در PENDING/SESSION_STATUS است

**Mutual chain evidence (precedent):**
- part04 chat-end → `<part04-hash>` (backfill در part05 boot)
- part05 chat-end → `<part05-hash>` (backfill در D24 boot)
- D24 chat-end → `<D24-hash>` (backfill در part07 boot — این چت)
- part07 chat-end → `<future>` (backfill در next chat)

**Note:** Actual hashes ثبت در `CHAT_LOG.md` per-chat boot section per mechanism design (M101 self-prevents inline documentation).

**Implementation:** boot section در CHAT_LOG.md هر چت explicit `Parent commit: <hash از git rev-parse>` ثبت می‌کند. این یک systematic backfill chain است.

---

### M102 ⭐ — Rule-Implementation Decoupling (Interface-Implementation separation)

**کشف‌شده در:** S3.1 design phase Q3 user catch (Discovery #۱ part04) | **اهمیت:** 🟠 high | **Cross-refs:** Rule #۷۱, Rule #۷۳

**اشتباه:** Rule normative text با implementation detail mixed → detail change in implementation = rule violation alarm، در حالی که rule intent تغییر نکرده.

**علت:** فرض «detail در rule body بهتر است for clarity»، در حالی که این interface و implementation را couple می‌کند.

**راه‌حل:** structural separation در rule design:
- **Normative paragraph:** stable intent، principle، policy
- **Implementation Notes section (separate):** detail، file paths، script references، transitional pinning
- implementation evolves → Implementation Notes update، normative stays unchanged

**Pattern signature in v2.14 rules:**
- Rules #۶۸-#۷۷ همه این pattern را follow می‌کنند (Normative + Implementation Notes section explicit)
- precedent از Rule #۶۶ و #۶۷ (v2.12-v2.13)

**Anti-pattern:**
- ❌ Rule: "نسخه audit script must equal v2.13 — ACCEPTABLE_VERSIONS = ['v2.12', 'v2.13']"
- ✅ Rule Normative: "Audit script must accept current version" + Implementation: "ACCEPTABLE_VERSIONS list (transitional)"

**Transitional safety:** Implementation Notes می‌تواند transitional pinning صراحت ذکر کند (e.g., ACCEPTABLE_VERSIONS list during migration window) بدون اینکه normative rule را تغییر دهد.

---

### M103 ⭐⭐⭐ — Audit Over-Promise Pattern

**کشف‌شده در:** part10 audit session (`TRADING-phase1-part10-mdrs-v2-infrastructure-sprint`) | **اهمیت:** 🔴 critical | **Cross-refs:** M77, M88, M82, Rules #۷۸-۸۵

**اشتباه:** Claude در audit deep-scan part10 ادعا کرد «Phase 1 deep-scan تقریباً کامل» در حالی که coverage واقعی ~۳۵٪ بود (۳۵-۴۰ فایل از ۲۷۸ classified خوانده شد، ۲۳۰+ ندیده). همچنین «~۹۸٪ coverage» گفت که مربوط به screenshots بود نه پروژه. و خودسرانه Tier 3 code (۲۱۴ فایل) و Legacy سند جامع v2.6-v2.11 را skip کرد بدون permission.

**علت ریشه‌ای (سه genus به‌هم‌پیوسته):**
1. **Optimistic reporting** — صفت مبهم («تقریباً کامل») به‌جای عدد دقیق (N/M).
2. **Self-imposed scope narrowing** — تصمیم خودسرانه برای skip بدون SCOPE NARROWING REQUEST.
3. **Pattern matching / extrapolation** — استنباط از sample کوچک به کل population.

**رابطه با درس‌های قبل:**
- **M88 (Hidden Regeneration Hazard):** هر دو از فرض «خلاصه/الگو = واقعیت» می‌آیند؛ M88 در docs، M103 در reporting.
- **M82 (Verification Claim Must Be Verified) / M77:** M103 یک verification-claim failure در سطح audit است.

**راه‌حل:** ۸ Trust Rule #۷۸-۸۵ (v2.15): #۷۸ SCM · #۷۹ QHP · #۸۰ NSISN · #۸۱ RDEM · #۸۲ MPTC · #۸۳ HAT · #۸۴ APMM · #۸۵ Self-Activation Lock.

**درس عمیق‌تر:** «نوشتن قانون honesty» کافی نیست (M87 spirit)؛ Rule #۸۵ (Self-Activation Lock) خودکارسازی per-turn را تضمین می‌کند تا قواعد بدون یادآوری کاربر فعال بمانند.

---

### M104 ⭐⭐⭐ — Mechanical-Claim Verification before Persisting

**کشف‌شده در:** part14 escape-note off-by-one (PART16 به‌جای مکانیکیِ PART15) | **اهمیت:** 🔴 critical | **Cross-refs:** #۸۴ (نمونهٔ خاص)، #۸۶ (مکمل)، check_12، M101، M82

**Lesson (Normative):** هر عدد/شناسهٔ مکانیکی در artifact پایدار (شمارهٔ handoff، hash، ردیف ledger، شمارهٔ قانون/درس/Review، نسخه) باید پیش از نوشتن از منبع زنده (اسکریپت/فایل/git) استخراج شود، نه از حافظه/الگو/استنتاج دنباله‌ای. اگر قابل‌استخراج نیست → فرمول/اشتقاق («بالاترین موجود + ۱») یا placeholder + TODO، نه hard-code.

**Corollary (Escape):** پس از escape، شمارنده‌های frontier جلو نمی‌روند؛ هر عدد دنباله‌ای مشکوک است و باید با frontier واقعی + invariant فعال (check_12: H==L+1) cross-check شود.

**Genesis:** part14 escape-note off-by-one (PART16 به‌جای مکانیکیِ PART15).

**درس عمیق‌تر:** هم‌خانوادهٔ M82 (Verification Claim Must Be Verified) اما در سطح **اعداد مکانیکی** — «درست به نظر رسیدن» الگوی دنباله کافی نیست؛ منبع زنده authoritative است. قانون #۸۶ این را به سطح Locked می‌برد.

---

### M105 ⭐ — EXECUTE Command Paste-Integrity (`&`-chain)

**کشف‌شده در:** part18 (گزارش کاربر) | **اهمیت:** 🟠 high (workflow friction تکرارشونده) | **Cross-refs:** #۶۳ (Convention EXECUTE)، #۶۷ (cross-shell)، M99 (دستور طولانی)، M86

**اشتباه:** EXECUTE block‌هایی که چند دستور را در **خطوط جداگانه** دادند — کاربر کل کادر را کپی می‌کرد ولی همه با هم اجرا نمی‌شدند؛ باید می‌دید تا کدام دستور اجرا شده و ادامه را دوباره کپی می‌کرد (اتلاف وقت + ریسک خطا).

**علت:** CMD خطوط متعددِ paste‌شده را جداگانه buffer/اجرا می‌کند؛ خطوطی که خروجی چندخطی (مثل `echo` یا `git log`) تولید می‌کنند buffering را برهم می‌زنند و دستور آخر منتظر Enter دستی می‌ماند.

**راه‌حل (standard EXECUTE format):** دستورهای کوتاه/مرتبط را با `&` در **یک خط** زنجیر کن تا CMD کل را یک فرمان واحد ببیند (یک paste + یک Enter):

```cmd
cd /d D:\Projects\trading-system & echo [1] & <cmd1> & echo [2] & <cmd2> & echo [DONE]
```

- `&` = «بعدی را در هر صورت اجرا کن» (برای query‌هایی که خطایشان مهم نیست).
- `&&` = «فقط اگر قبلی موفق بود» (توقف روی خطا — برای زنجیرهٔ وابسته مثل add→commit→push).
- برچسب `echo [N]` بین دستورها خوانایی خروجی را بالا می‌برد.

**استثنا:** دستورهای واقعاً مستقل یا طولانی (مثل commit با -F) می‌توانند کادر جدا داشته باشند، ولی هر کدام تک‌خطی. هیچ‌وقت چند خط جدا که وسطش گیر کند.

**تمایز با M99:** M99 دربارهٔ *commit message* چندخطی است (راه‌حل: -F flag)؛ M105 دربارهٔ *چند دستور جدا* در یک EXECUTE block است (راه‌حل: `&`-chain تک‌خطی). هر دو از همان genus‌اند: CMD multi-line paste غیرقابل‌اعتماد.

---

## ۲.۹ Helper Consultation Lessons (HM-series)

### HM-namespace rationale

HM = Helper-Memory / Helper-Meta. این namespace جدا از M-series است:
- **M-series:** main chat Claude mistakes/insights
- **HM-series:** helper consultation patterns + helper-side anti-patterns

**Rationale (deliberate distinction):**
- semantic separation: helper-side ≠ main-side
- Z3.24 spirit: namespace categorization explicit
- Reserved IDs در M-series نقض نمی‌شود
- Cross-refs distinct (`HM-3` vs `M-3` no collision)
- Future audit می‌تواند هر دو را independently track

**Storage:** HM entries در همین فایل `02_lessons.md` §۲.۹ (این sub-section)، نه فایل جداگانه. منطق: structurally lessons hastand، visual + structural cohesion با M-series.

**Numbering:** sequential از HM-1 (no zero-pad initially). Reserved IDs allowed.

**Reference:** HELPER_PROTOCOL.md §۵ design + Rule #۶۸ (Tier classification) + Z3.24 (namespace categorization).

---

### HM-1 — Helper Consultative Misinterpretation

**کشف‌شده در:** Discovery #10 part05 (`TRADING-phase1-part05-mdrs-v2-s31-redo`) | **اهمیت:** 🟡 medium | **Cross-refs:** HELPER_PROTOCOL §۱.۲, §۱.۴

**Pattern:** main chat فرض کرد «helper findings = approval gate» — یعنی اگر helper تأیید کرد، می‌توان commit کرد بدون user approval explicit.

**Root cause:** helper role ambiguous بود قبل از HELPER_PROTOCOL.md.

**Lesson:** helper consultation = advisory only، نه approval gate. Authority hierarchy (HELPER_PROTOCOL §۱.۴):
1. User explicit approval (absolute per Rule #۵۱ broader scope)
2. Constitution
3. State-of-record
4. Main chat Claude reasoning
5. Helper findings (advisory)

helper finding conflict با levels 1-4 → conflict explicit surfaced to user for resolution.

**Prevention:** HELPER_PROTOCOL.md §۱.۲ و §۱.۳ explicit positive و negative definition.

---

### HM-2 — Late-Catch Cascade Pattern

**کشف‌شده در:** Discovery #13 part05 (turn 10، strategic decision trigger) | **اهمیت:** 🔴 critical | **Cross-refs:** HELPER_PROTOCOL §۳.۳, §۳.۴, Review #۰۰۳ (D24 decision record — direct driver)

**Pattern:** draft در چند iteration helper review می‌شود و در هر iteration N catches ظاهر می‌شوند (e.g., 6 catches turn N → 1-3 catches turn N+1 → 1 catch turn N+2). این signal است که process upstream نیاز به تغییر دارد، نه drafting.

**Symptoms:**
- ۳+ iteration روی یک chunk
- ۲+ structural concerns (نه precision)
- self-violation از rules که خود نوشتیم (eat-your-own-dogfood failure)
- Helper reviews می‌گویند "X% ready" که افزایش می‌یابد ولی fundamental concerns ongoing

**Trigger:** ۳ iteration روی یک substantive chunk با ۱۰+ total catches → stop، evaluate process، not draft.

**Resolution (Bounded Bootstrap pattern):** HELPER_PROTOCOL §۳.۳:
- Upfront constraint checklist
- Batch comprehensive draft
- 1 helper round (max 2)
- Escalation criteria §۳.۴: > 5 catches OR critical → bootstrap mode escape

**Evidence:** part05 turn 9-10 (full trace)، D24 self-application (proof of process functional).

**این HM-2 خود driver D24 (Helper Infrastructure) deliverable بود.**

---

### HM-3 — Chat Naming Convention Adherence

**کشف‌شده در:** Discovery #5 D24 (`TRADING-phase1-part06-mdrs-v2-D24-helper-infrastructure`) | **اهمیت:** 🟠 high | **Cross-refs:** HANDOFF_TEMPLATE.md "NEXT CHAT NAME" section

**Pattern:** project standard pattern `TRADING-phase{N}-part{NN}-{topic-slug}`. D24 initial chat name `TRADING-mdrs-v2-D24-helper-infrastructure` این pattern را نقض کرد (phase/part missing).

**Root cause:** boot files صراحت در next-chat-name pattern نداشتند → Claude initial naming drifted.

**Lesson:**
- Each chat-end handoff explicit declare next chat name pattern (HANDOFF_TEMPLATE "NEXT CHAT NAME (MANDATORY PATTERN)" section)
- SESSION_STATUS «next chat» section explicit با pattern reference
- New-chat Claude boot procedure: naming verification check (alert if drift detected)
- Boot mandatory file reads include chat-name self-check

**Anti-pattern signatures:**
- `TRADING-{topic}` (missing phase/part) — historical pattern
- `TRADING-mdrs-v2-{topic}` (missing phase/part) — D24 initial drift

**Prevention:** HANDOFF_TEMPLATE.md updated در D24 با "NEXT CHAT NAME (MANDATORY PATTERN)" section (precedent).

---

### HM-4 — Modified Round-1.5 Edge Case

**کشف‌شده در:** Discovery #1 D24 | **اهمیت:** 🟠 high | **Cross-refs:** HELPER_PROTOCOL §۳.۴

**Pattern:** Bounded Bootstrap §۳.۴ escalation criteria define می‌کند: > 5 catches OR critical → bootstrap mode (skip round 2). ولی edge case: > 5 catches با critical → single batch fix + skip round 2 = یک hybrid حالت بین "round 2" و "bootstrap mode".

**Lesson:** "Modified Round-1.5" یک valid intermediate state است:
- main chat Claude apply همه findings (including critical) در single batch
- skip helper round 2
- user direct review
- این فرم compressed از round 2 + bootstrap mode هر دو است

**Recognition criterion:** اگر round 1 findings actionable و scope clear است، Modified Round-1.5 = efficient. اگر round 1 findings systemic confusion را نشان دهند، true bootstrap mode (escape) preferred.

**Documentation:** HELPER_PROTOCOL §۳.۴ "Modified Round-1.5" به‌عنوان valid intermediate state added در post-D24 maintenance (یا v1.1 HELPER_PROTOCOL update).

---

### HM-5 — Self-Referential First-Application chicken-and-egg

**کشف‌شده در:** Discovery #3 D24 (self-application) | **اهمیت:** 🟡 medium | **Cross-refs:** M77, M101

**Pattern:** helper applies 8-Layer Framework که خود subject under review است (HELPER_PROTOCOL.md). این یک chicken-and-egg: framework در فایلی که خود review می‌شود defined شده، ولی review needs framework.

**Genus:** M77 (HEAD Self-Reference) extension + M101 (Post-Handoff State Drift) extension. self-reference impossibility در first-application context.

**Resolution:** retroactive application:
- helper round 1 applied 8-Layer Framework based on draft text (not committed yet)
- post-round-1 fix incorporates findings
- framework در final committed version reflects post-fix state
- این یک valid bootstrap pattern است، نه paradox

**Lesson:** first-application of any framework = bootstrap exception (precedent Review #۰۰۱ — self-establishing protocol). REVIEW_PROTOCOL §۹.۲ Bootstrap Exception clause same genus.

**Future-prevention:** if frameworks revised، helper applies new version retroactively to revision itself (recursive bootstrap).

---

### HM-6 — Post-Correction Propagation Audit

**کشف‌شده در:** Discovery #6 D24 (sub-cascade از Discovery #5) | **اهمیت:** 🟠 high | **Cross-refs:** HM-3, M74 (Full-Range Audit)

**Pattern:** correction در یک layer (chat name) applied، ولی downstream references با old mental model continued. مثال D24: chat name corrected، ولی handoff filename و K7 references با old numbering ماندند.

**Genus:** Late-Catch Cascade (HM-2) micro-form + Full-Range Decision Audit (M74) genus.

**Lesson:** هر naming correction (یا any structural rename) باید explicit cascade check به downstream artifacts را trigger:
- handoff filenames
- cross-references در state-of-record files
- PENDING references
- commit message templates در workspace

**Audit procedure:**
1. correction identified در layer N
2. `grep -r "old-pattern"` در project (یا Filesystem MCP search_files)
3. cascade-correct در همه occurrences
4. verify with read-back per M82

**Prevention:** هر rename یا naming convention change → explicit cascade audit step در stage-end protocol.

---

### HM-7 — D24 Iteration Budget Self-Assessment

**کشف‌شده در:** Discovery #7 D24 (self-criticism) | **اهمیت:** 🟡 medium | **Cross-refs:** HM-2 inverse signal

**Pattern:** D24 itself ~15+ turn over-budget per industry standard برای T1 doc creation. Justifiable چون self-application infrastructure (creating the infrastructure being applied).

**Lesson:** post-deploy، helper consultation efficiency باید measurably بهبود یابد. اگر artifacts post-D24 با مشابه budget D24 produce شدند، evidence که HELPER_PROTOCOL needs refinement.

**Metric proposed:** turns-per-artifact / catches-per-iteration. baseline = part05 (high cost)، target = post-D24 measurably lower.

**Post-part07 evaluation:** S3.1 خود این metric را test می‌کند. اگر S3.1 با < 10 turn (bootstrap mode escape upfront) موفق → HELPER_PROTOCOL effective حتی در bootstrap mode. اگر > 15 turn → refinement needed.

**Self-criticism principle:** infrastructure را با خود infrastructure measure کن — recursive metric.

---

## 🚧 وضعیت این ماژول

✅ **Migration کامل از v2.11 + Atomic Updates v2.12 + v2.13 + v2.14 (S3.1)**

**جمع‌بندی درس‌ها:**
- M-series ثبت: ۷۳ (M1-M63 + M64-M87 + M88 + M93-M105)
- M-series Reserved: ۳۲ (M22, M24, M29, M32-M43, M45-M55, M80, M81, M89-M92)
- HM-series: ۷ (HM-1 to HM-7)

✅ **افزوده‌های v2.14 اعمال‌شده (S3.1 part07):**
- M88 (Hidden Regeneration Hazard)
- M89-M92 Reserved (CVE-like gap)
- M93-M102 (۱۰ critical lesson)
- §۲.۹ NEW — HM-series sub-section (HM-1 to HM-7)
- §۲.۲ fast-look table: ۶ category جدید
- §۲.۷ index: M88+M93-M102 listing + HM-series pointer

🔮 **افزوده‌های بعدی (S3.2-S3.4):**
- ماژول header v2.12 → v2.14 (S3.3 atomic با ACCEPTABLE_VERSIONS)
- State-of-record atomic refresh (S3.4 Triple-Rule M93)

---

**📌 پایان 02_lessons.md (S3.1 اتمیک v2.14 applied)**
