# Session Status — وضعیت جاری پروژه

> **آخرین به‌روزرسانی:** 2026-05-18 (پایان چت ۷)

> ⚠️ **یادداشت چت ۸ (بعدی):** این فایل وضعیت پایان چت ۷ را نشان می‌دهد. در پایان چت ۸ (طبق قانون #۲۷) بازنویسی می‌شود.

---

## 📍 وضعیت کلی

- **فاز جاری:** ۰ -- تکمیل شد ۱۰۰٪
- **Tier جاری:** Tier 2 Quality Hardening -- **۹/۹ DONE**
- **Git HEAD:** `532fc9f` (و چند commit بعدی برای پایان چت)
- **آخرین چت:** چت ۷ -- `phase0-part07-quality-hardening-continued`
- **نام چت بعدی:** `TRADING-phase0-part08-pre-phase1-setup`

## ✅ کارهای DONE در چت ۷

### مرحله A -- Atomic Update قوانین #۲۳-۳۲ (Tier 2 T2.11)
- ارتقای سند جامع v2.7 -> v2.8
- اسکریپت‌های 47، 47b، 48، 48b، 48c، 49

### مرحله B -- Task های Tier 2
- **T2.05** Git Workflow doc + tests
- **T2.06** Pre-commit hooks (Hybrid mode)
- **T2.07** Anti-Patterns A1-A10 doc
- **T2.08** Backend pytest + 25 smoke tests
- **T2.09** API Docs (6 endpoints)

### مرحله C -- پایان چت ۷
- سند جامع v2.8 -> v2.9 (15 قانون جدید + 4 بخش جدید)
- درس‌نامه ۲۱ اشتباه Claude (M1-M21)
- Atomic Update ۵ سند Governance

## 📋 برنامه چت ۸ (به‌ترتیب)

1. **T2.10** -- توسعه ARCHITECTURE.md
2. **T2.13** -- ریشه‌یابی Bug #50 (React imports)
3. **مرور همه تنظیمات Claude** -- همه گزینه‌های Settings (نه فقط Feature Preview)
4. **GitHub setup** -- اتصال پروژه به repo (طبق سند ۲۱)
5. **سایر آماده‌سازی‌های قبل از فاز ۱:**
   - تأیید Custom Instructions
   - تأیید پلن (سالانه/ماهانه)
   - تنظیم Workspaces / Projects
   - بررسی MCP connectors
   - بررسی نیاز به Claude Code

## 📊 آمار پروژه

- **قوانین قفل‌شده:** ۴۷ (پس از v2.9)
- **بخش‌های سند جامع:** ۲۱
- **درس‌نامه اشتباهات:** ۲۱ مورد
- **Test ها:** ۳۰/۳۰ vitest + ۲۵/۲۵ pytest = **۵۵ pass**
- **اسکریپت‌های `*b_test_*.py`:** ۲۵+ مورد
- **سند Markdown در `docs/`:** ۲۲

## 🔧 محیط فعال

- Python: 3.11
- Backend: FastAPI 0.111.0 + SQLAlchemy 2.0.30 + aiosqlite 0.20
- Frontend: React 19.2 + Vite 8.0 + Vitest 3.x
- DB: SQLite (`backend/trading.db`)
- Auth: JWT + bcrypt 4.1
- Tests: pytest 8.2.2 + pytest-asyncio + pytest-cov 5.0
- Hooks: pre-commit 3.7.1 + black 24.4 + isort 5.13 (Hybrid mode)

## 🚧 معلق (Tier 2 -- نه برای فاز ۱)

- **T2.10** ARCHITECTURE.md expansion (برنامه: چت ۸)
- **T2.13** React imports root-cause investigation (برنامه: چت ۸)

## 🔜 Tier 3 -- بعد از فاز ۱

- **T2.12** Claude Code / GitHub MCP migration evaluation

---

## نکته شروع چت ۸

طبق قانون #۴۷، Claude در ابتدای چت ۸ باید:
1. `docs/سند_جامع_v2_9.md` بخش ۱۸ (درس‌نامه M1-M21) را بخواند
2. `docs/CLAUDE_CHECKLIST.md` (قوانین قفل‌شده #۱-۴۷) را بخواند
3. این فایل را بخواند برای context وضعیت
