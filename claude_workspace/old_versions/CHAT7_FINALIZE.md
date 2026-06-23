# CHAT7 FINALIZE — جمع‌بندی چت ۷

> **چت:** `TRADING-phase0-part07-quality-hardening-continued`
> **تاریخ پایان:** 2026-05-18
> **اسم پیشنهادی چت بعد:** `TRADING-phase0-part08-pre-phase1-setup`

---

## 📊 خلاصه

این چت سه مرحله داشت:
- **مرحله A** -- Atomic Update قوانین #۲۳-۳۲ (T2.11)
- **مرحله B** -- ۵ task از Tier 2 (T2.05, T2.06, T2.07, T2.08, T2.09)
- **مرحله C** -- پایان چت + ارتقای سند v2.8 -> v2.9

پس از چت ۷، Tier 2 Quality Hardening **۹/۹ DONE** است.

## 📦 خروجی‌های اصلی

### اسکریپت‌های جدید (در `scripts/`)

| Range | تعداد | کاربرد |
|---|---|---|
| 47-49 | 6 | Atomic Update چت ۶ -> چت ۷ |
| 50-50b | 2 | Git Workflow |
| 51-51b | 2 | API Docs |
| 52-52b | 2 | Anti-Patterns |
| 53-53d | 5 | Backend pytest + fixups |
| 54-54f | 6 | Pre-commit hooks + fixups |
| 55-55b | 2 | Doc v2.9 upgrade |
| 56-56b | 2 | Atomic Update چت ۷ |
| check_anti_patterns, install_git_hooks | 2 | infrastructure |

### اسناد جدید (در `docs/`)

- `سند_جامع_v2_9.md` (171KB، 3108 خط)
- `GIT_WORKFLOW.md` (16KB، 524 خط)
- `API_DOCS.md` (18KB، 619 خط)
- `ANTI_PATTERNS.md` (22KB، 644 خط)
- `BACKEND_TESTING.md` (16KB، 472 خط)
- `PRECOMMIT.md` (9.5KB، 376 خط)
- `CHAT7_FINALIZE.md` (این فایل)

### Tests

- **30/30** vitest (frontend)
- **25/25** pytest (backend smoke tests)
- **همه** pre-commit hooks pass

## 🆕 قوانین جدید (15 قانون #۳۳-۴۷)

ثبت‌شده در جدول ۱.۹ سند جامع v2.9. مرجع: بخش "خلاصه تغییرات v2.8 → v2.9".

## 🎓 درس‌نامه (۲۱ اشتباه ثبت‌شده)

ثبت‌شده در بخش ۱۸ سند جامع v2.9 (M1-M21). از این به بعد، **در ابتدای هر چت Claude باید این بخش را بخواند**.

## 🚀 برنامه چت ۸

طبق درخواست کاربر، چت ۸ به‌ترتیب:

1. **T2.10** -- توسعه ARCHITECTURE.md
2. **T2.13** -- ریشه‌یابی Bug #50 (React imports)
3. **مرور همه تنظیمات Claude Desktop** (نه فقط Feature Preview):
   - Profile / Custom Instructions
   - Appearance
   - Account
   - Feature Preview
   - Connectors / Integrations
   - Privacy
   - Notifications
   - Keyboard shortcuts
   - Workspaces (اگر موجود)
   - هر گزینه دیگر در sidebar Settings
4. **GitHub setup** -- اتصال پروژه به repo
5. **سایر آماده‌سازی‌های قبل از فاز ۱:**
   - تأیید Custom Instructions
   - تأیید پلن Max 5x (سالانه/ماهانه)
   - تنظیم Workspaces/Projects
   - بررسی MCP connectors (GitHub, Filesystem)
   - بررسی Claude Code (برای Tier 3)
   - تنظیم Model selection guide برای فاز ۱

## 🔄 پروتکل شروع چت ۸

طبق قانون #۴۷، در ابتدای چت ۸ Claude باید:

1. `docs/سند_جامع_v2_9.md` بخش ۱۸ (M1-M21) را بخواند
2. `docs/CLAUDE_CHECKLIST.md` (قوانین #۱-۴۷) را بخواند
3. `docs/SESSION_STATUS.md` (وضعیت جاری) را بخواند
4. شروع طبق برنامه بالا

## 📌 پایان چت ۷

نسخه‌بندی:
- سند جامع: v2.8 -> **v2.9**
- CLAUDE_CHECKLIST: v1.1 -> **v1.2**
- PROJECT_GOVERNANCE: v1.1 -> **v1.2**
- TASK_BACKLOG: v1.3 -> **v1.4**
- CHAT_LOG: v1.2 -> **v1.3**
- قوانین قفل‌شده: ۳۲ -> **۴۷**
- درس‌نامه: 0 -> **۲۱ مورد**
