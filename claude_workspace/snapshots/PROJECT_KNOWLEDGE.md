# PROJECT KNOWLEDGE — trading-system

> **هدف این فایل:** خلاصه‌ای فشرده برای Project Knowledge در Claude Desktop.
> **سند کامل:** `docs/سند_جامع_v2_9.md` (با Filesystem MCP خوانده می‌شود)
> **آخرین به‌روزرسانی:** پایان چت ۷ (2026-05-18)

---

## 🎯 درباره پروژه

- **نام:** trading-system (سامانه هوشمند ترید)
- **مسیر local:** `D:\Projects\trading-system`
- **OS:** Windows 11
- **زبان ارتباط:** فارسی + اصطلاحات فنی انگلیسی
- **Filesystem MCP:** ✅ فعال (دسترسی به `D:\Projects\trading-system`)

## 🛠️ Stack تکنیکال

| لایه | تکنولوژی |
|---|---|
| Backend | FastAPI 0.111.0 + SQLAlchemy 2.0.30 + aiosqlite 0.20 |
| Frontend | React 19.2 + Vite 8.0 + Vitest 3.x |
| Auth | JWT + bcrypt 4.1 |
| Database | SQLite (`backend/trading.db`) |
| Tests | pytest 8.2.2 + pytest-asyncio + pytest-cov 5.0 |
| Hooks | pre-commit 3.7.1 + black 24.4 + isort 5.13 (Hybrid mode) |
| Python | 3.11 |

## 📊 وضعیت جاری (پایان چت ۷)

- **فاز ۰:** ۱۰۰٪ ✅
- **Tier 2 Quality Hardening:** ۹/۹ DONE ✅
- **Git HEAD:** `1d8bddb`
- **قوانین قفل‌شده:** ۵۵ (M1-M55 پس از v2.10، در حال حاضر ۴۸ تا v2.9)
- **درس‌نامه اشتباهات Claude:** ۳۳ مورد (M1-M33) -- مرجع: `docs/سند_جامع_v2_9.md` بخش ۱۸
- **Tests:** ۳۰/۳۰ vitest + ۲۵/۲۵ pytest + همه pre-commit hooks pass

## 🔒 قوانین پایه (مهم‌ترین‌ها)

### رفتاری

- **#۲۷:** پایان چت فقط با تأیید صریح کاربر
- **#۳۰:** اصلاحات کوچک = اسکریپت Python idempotent
- **#۳۱:** بالای هر کادر کد دستوری: 🟦/🟩/🟧/🟥 + شماره tab
- **#۳۴:** zip ها در root پروژه دانلود می‌شوند (نه Downloads)
- **#۳۸:** اسکریپت‌های `.py` تنها → `scripts/`، zip → root
- **#۴۶:** ASCII-only در `print()` اسکریپت‌های Windows + `sys.stdout.reconfigure(encoding="utf-8")`
- **#۴۷:** قبل از هر کار جدید، بخش ۱۸ سند جامع (درس‌نامه) خوانده شود

### Tier 2 (Quality)

- **#۳۷:** read-back verify بعد از write
- **#۳۶:** verify signature قبل از تست‌نویسی
- **#۴۰:** verify argparse syntax قبل از پیشنهاد
- **#۴۱:** `.get()` به‌جای `[]` در `or` assertion
- **#۴۲:** `--no-verify` با `[skip-hooks: REASON]`

### Filesystem MCP (#۴۹-۵۱)

- **#۴۹:** read-only tools → Always allow؛ write/delete/copy → Needs approval
- **#۵۰:** Filesystem MCP پس از نصب در چت‌های **جدید** load می‌شود، نه چت‌های جاری
- **#۵۱:** قبل از هر write/delete با MCP، تأیید کاربر گرفته شود

### Project Knowledge (#۵۵ -- در v2.10)

- **#۵۵:** اگر فایل Project Knowledge به‌روز شد، Claude باید نسخه جدید را تولید کند تا کاربر در Project آپلود کند

## 📋 ابزارهای Claude در دسترس

### Filesystem MCP (۱۱ ابزار)

- read_text_file, read_multiple_files, list_directory, search_files
- write_file, edit_file, create_directory, move_file (نیاز به approval)

### Built-in

- Web search, web fetch
- Artifacts (✅), Inline visualizations (✅), Cloud code execution (✅)
- Memory: Search and reference chats + Generate memory from chat history

## 🤖 Model Selection Guide (سند ۱۹.۲)

| موقعیت | Model |
|---|---|
| Atomic End-of-Chat | **Opus 4.7** + Adaptive |
| Documentation روتین | Sonnet 4.6 |
| Repository Layer (فاز ۱) | Sonnet 4.6 |
| Indicators (فاز ۲) | **Opus 4.7** |
| Trading Strategies (فاز ۳) | **Opus 4.7** |
| UI Components (فاز ۴) | Sonnet 4.6 |
| Debugging پیچیده | **Opus 4.7** |
| Code review | **Opus 4.7** |

**قانون عملی:** ≥۳ مورد از پیچیدگی-تعدد فایل-تصمیم معماری → Opus، در غیر این صورت → Sonnet

## 📋 پروتکل اجباری شروع چت جدید (قانون #۴۷)

Claude **باید** ابتدا این فایل‌ها را با Filesystem MCP بخواند:

1. `docs/سند_جامع_v2_9.md` بخش ۱۸ (درس‌نامه M1-M33)
2. `docs/CLAUDE_CHECKLIST.md` (قوانین #۱-۵۴)
3. `docs/SESSION_STATUS.md` (وضعیت جاری)
4. `docs/CHAT_LOG.md` آخرین چت
5. آخرین `docs/CHAT{N}_FINALIZE.md`

سپس تأیید کند و منتظر دستور بعدی بماند.

## 🚧 معلق برای چت ۸

- **T2.10:** توسعه ARCHITECTURE.md
- **T2.13:** ریشه‌یابی Bug #50 (React imports false positive)
- مرور همه تنظیمات Claude Desktop
- GitHub setup
- اتصال Custom Instructions
- بررسی Memory + Project + Filesystem MCP کامل

## ⚠️ هشدارهای مهم

- **هرگز** کد malicious تولید نکن
- **هرگز** فایل `.env` را با MCP تغییر نده (هرچند MCP اجازه دارد)
- **هرگز** خارج از پوشه `D:\Projects\trading-system` عمل نکن
- **هرگز** پایان چت را خودکار شروع نکن (قانون #۲۷)

---

## 📌 یادداشت برای Claude

اگر در شروع چت این فایل را می‌خوانی:
1. تأیید کن این فایل را خوانده‌ای
2. با MCP فایل‌های `docs/` را بخوان
3. منتظر دستور بعدی بمان
4. هر زمان قانون جدید یا تغییر اساسی، **این فایل را در آپدیت سند، به‌روز کن و به کاربر بگو فایل جدید را در Project Knowledge جایگزین کند**
