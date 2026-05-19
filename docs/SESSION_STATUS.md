# Session Status — وضعیت جاری پروژه

> **آخرین به‌روزرسانی:** 2026-05-19 (در حال انجام چت ۸ — بلوک ۱-A تکمیل)

> ⚠️ **یادداشت:** این فایل snapshot میانه چت ۸ است. در پایان چت ۸ (مرحله G3) با state نهایی بازنویسی می‌شود.

---

## 📍 وضعیت کلی

- **فاز جاری:** ۰ — تکمیل ۱۰۰٪
- **Tier جاری:** Tier 2 + Infrastructure — **۱۴/۲۱ DONE** ✅ (T2.05-T2.09 + T2.11 + T2.14-T2.16 + T2.17 + T2.19 + T2.18 IN-PROGRESS)
- **سند جامع:** **v2.10** (200.8KB) — تازه از v2.9 ارتقا یافت
- **Git HEAD:** `d6bc75c` (پایان چت ۷ — در بلوک ۴ چت ۸ commit جدید ساخته می‌شود)
- **چت جاری:** **چت ۸** — `TRADING-phase0-part08-pre-phase1-setup`
- **نام چت بعدی پیشنهادی:** `TRADING-phase1-part01-ccxt-websocket-setup` (شروع فاز ۱)

## ✅ کارهای DONE در چت ۸ (تا این لحظه)

### بلوک ۱-A — Documentation Backlog (تکمیل ۶/۷)

- **A1 ✅** ادغام PENDING → سند جامع v2.10 (171KB → 200.8KB)
  - +۱۴ قانون قفل‌شده (#۴۸-۶۱) به جدول ۱.۹
  - +۲۱ ردیف درس‌نامه (M22-M62 شامل ۲۵ Reserved)
  - +۴ بخش جدید (سند ۲۲ MCP، سند ۲۳ Claude Desktop، سند ۲۴ workspace، سند ۲۵ Skills)
- **A2 ✅** Atomic Update CLAUDE_CHECKLIST v1.2 → v1.3 (+sub-checklist MCP + مرحله ۱۱.۵)
- **A3 ✅** Atomic Update PROJECT_GOVERNANCE v1.2 → v1.3 (+C26-C30 + A11 + G8)
- **A4 ✅** Atomic Update TASK_BACKLOG v1.4 → v1.5 (+T2.14-T2.21)
- **A5 ✅** تکمیل CHAT_LOG چت ۷ (T2.19 — تست عملی M23) + افزودن چت ۸
- **A6 ✅** اصلاح آمار CHAT_LOG (۲۶ → ۶۱ قانون)
- **A7 🚧** SESSION_STATUS (همین فایل — همین لحظه!)

## 📋 برنامه باقیمانده چت ۸

### بلوک ۱-B — Infrastructure audit (autonomous)

- **B1** verify Filesystem MCP tools list
- **B2** verify Memory toggles
- **B3** verify Project Knowledge presence
- **B4** verify `claude_workspace/` structure
- **B5** verify `.gitignore` policy for `claude_workspace/screenshots/` و `zip_temp/`

### بلوک ۲ — تعاملی (نیاز به کاربر)

- **D1** GitHub setup طبق سند ۲۱ (cmd + auth)
- **C1-C8** Audit ۸ tab از Settings (نیاز به ۸ screenshot از کاربر)

### بلوک ۳ — Tier 2 پایانی + Phase 1 readiness

- **D2** Claude Code evaluation
- **D3** GitHub MCP connector evaluation
- **F1** Model Selection Guide نهایی (سند جامع ۱۹.۲)
- **E2** Bug #50 root cause (T2.13، timebox ۳۰ دقیقه)
- **E1** ARCHITECTURE.md expansion (T2.10 — Repository Layer + CCXT connector)

### بلوک ۴ — Phase 1 readiness + پایان چت

- **F2** run test suite (pytest 25/25 + vitest 30/30 + pre-commit)
- **F3** env check (Python, Node, pip mirrors)
- **F4** backlog review نهایی
- **G1** پاک‌سازی PENDING_FOR_NEXT_VERSION.md (بخش‌های ۱-۶، طبق پروتکل ۷.۳)
- **G2** CHAT8_FINALIZE.md
- **G3** بازنویسی نهایی این فایل (SESSION_STATUS)
- **G4** PROJECT_KNOWLEDGE.md snapshot جدید + commit + push
- **G5** پیام handoff برای چت ۹

## 📊 آمار پروژه

- **قوانین قفل‌شده:** **۶۱** (با ۲ Reserved — #۵۲، #۵۳)
- **درس‌نامه اشتباهات:** **۶۲ ردیف** (۳۷ کشف‌شده + ۲۵ Reserved)
- **بخش‌های سند جامع:** **۲۵** (+۴ بخش جدید v2.10)
- **سند Markdown در `docs/`:** **~۲۴** (+PENDING_FOR_NEXT_VERSION)
- **Test ها:** ۳۰/۳۰ vitest + ۲۵/۲۵ pytest = **۵۵ pass** (carry forward از چت ۷)
- **اسکریپت‌های `*b_test_*.py`:** ۲۵+
- **چت‌های کامل:** **۸**

## 🔧 محیط فعال

- **Python:** 3.11
- **Backend:** FastAPI 0.111.0 + SQLAlchemy 2.0.30 + aiosqlite 0.20
- **Frontend:** React 19.2 + Vite 8.0 + Vitest 3.x
- **DB:** SQLite (`backend/trading.db`)
- **Auth:** JWT + bcrypt 4.1
- **Tests:** pytest 8.2.2 + pytest-asyncio + pytest-cov 5.0
- **Hooks:** pre-commit 3.7.1 + black 24.4 + isort 5.13 (Hybrid mode)
- **Claude Desktop:** Filesystem MCP فعال + Memory ON + Project Knowledge آپلود شده

## 🆕 ابزارها/تنظیمات جدید فعال در چت ۸

- ✅ **Filesystem MCP** (نصب چت ۷، استفاده گسترده چت ۸)
- ✅ **Project Knowledge** با `PROJECT_KNOWLEDGE.md` + Custom Instructions
- ✅ **Memory toggles** (Search past chats + Generate memory)
- ✅ **`claude_workspace/`** با ۵ subfolder + `.gitkeep`
- ✅ **`docs/PENDING_FOR_NEXT_VERSION.md`** ⭐⭐⭐ (بنیادی — قانون #۶۰)

## 🚧 معلق (Tier 2 — برای بلوک‌های بعدی چت ۸)

- **T2.10** ARCHITECTURE.md expansion (بلوک ۳ — E1)
- **T2.13** Bug #50 root cause (بلوک ۳ — E2، timebox ۳۰ دقیقه)
- **T2.18** Atomic Updates Governance (بلوک ۱ — همه‌اش به جز SESSION_STATUS تمام شد)
- **T2.20** GitHub setup (بلوک ۲ — D1)
- **T2.21** Audit Settings Claude Desktop (بلوک ۲ — C1-C8)

## 🔜 Tier 3 — بعد از فاز ۱

- **T2.12** Claude Code / GitHub MCP migration evaluation (در بلوک ۳ ارزیابی می‌شود ولی پیاده‌سازی به فاز ۱+)

---

## نکته بحرانی — درس M23 و قانون #۶۰

این چت اولین چتی است که **قانون #۶۰ (PENDING-EOC در لحظه ثبت با MCP)** را عملی اجرا می‌کند. درس M23 (مهم‌ترین درس کل پروژه) نشان داد که اعتماد به حافظه فعال در پایان چت کافی نیست — راه‌حل ریشه‌ای: ثبت لحظه‌ای در `docs/PENDING_FOR_NEXT_VERSION.md` با Filesystem MCP.

این فایل (SESSION_STATUS) **در پایان چت ۸ (مرحله G3) با state نهایی بازنویسی می‌شود** — شامل لینک به CHAT8_FINALIZE.md، آمار نهایی، Git HEAD جدید، و پیام handoff کامل برای چت ۹.

---

## نکته شروع چت ۹

طبق قانون #۴۸ و چک‌لیست v1.3 فاز ۱، Claude در ابتدای چت ۹ باید:

1. `docs/PROJECT_GOVERNANCE.md` v1.3 را بخواند
2. `docs/CLAUDE_CHECKLIST.md` v1.3 را بخواند
3. این فایل را بخواند برای context وضعیت (بازنویسی نهایی در G3)
4. `docs/CHAT_LOG.md` v1.3 بخش چت ۸ را بخواند
5. `docs/TASK_BACKLOG.md` v1.5 را بخواند
6. **`docs/PENDING_FOR_NEXT_VERSION.md`** را بخواند (طبق قانون #۴۸+#۶۰) — اگر خالی است یعنی همه PENDING در v2.10 ادغام شد
7. `docs/سند_جامع_v2_10.md` کامل — به‌خصوص **بخش ۱۸ درس‌نامه M1-M62**

شروع کار فاز ۱:
- اولین گام: T2.10 (ARCHITECTURE.md expansion برای Repository Layer + CCXT connector)
- یا اگر T2.10 در چت ۸ تمام شد: شروع فاز ۱ زیرگام CCXT integration
