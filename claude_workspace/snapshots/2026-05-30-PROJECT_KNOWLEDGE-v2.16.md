# PROJECT KNOWLEDGE — trading-system

> **هدف این فایل:** خلاصهٔ فشرده برای Project Knowledge در Claude Desktop.
> **مرجع کامل (زنده، با Filesystem MCP):** `docs/constitution/` (modular — `main.md` + `01_rules.md` … `06_meta.md`)
> **آخرین به‌روزرسانی:** part17 (2026-05-30) — همگام Constitution **v2.16**
> ⚠️ اسناد جامع v2.6–v2.11 و PROJECT_GOVERNANCE/CLAUDE_CHECKLIST/PROJECT_CONTEXT/ARCHITECTURE **منسوخ (DEPRECATED)** شدند؛ مرجع فعال modular است.

---

## 🎯 دربارهٔ پروژه

- **نام:** trading-system (سامانهٔ هوشمند ترید — کریپتو + فارکس)
- **مسیر local:** `D:\Projects\trading-system`
- **OS:** Windows 11 · **Shell:** CMD/PowerShell + venv
- **زبان ارتباط:** فارسی + اصطلاحات فنی انگلیسی
- **Filesystem MCP:** ✅ فعال (دسترسی به `D:\Projects\trading-system`)
- **GitHub:** `alibijanie-trade/trading-system` (Private، SSH)
- **Branch فعال:** `infra/v2.14-source-of-truth`

## 🛠️ Stack تکنیکال

| لایه | تکنولوژی |
|---|---|
| Backend | FastAPI 0.111 + SQLAlchemy 2.0 + aiosqlite 0.20 + ccxt 4.3.98 + websockets 12.0 |
| Frontend | React 19.2 + Vite 8.0 + Vitest 3.x + Zustand 4.5 |
| Auth | JWT + bcrypt 4.1 + Fernet |
| Database | SQLite (`backend/trading.db`) |
| Tests | pytest 8.2 + pytest-asyncio + pytest-cov |
| Hooks | pre-commit 3.7 + black 24.4 + isort (Hybrid mode) |
| Python | 3.11 |

## 📊 وضعیت جاری (part17)

- **فاز:** Phase 1 Skeleton ✅ + MDRS v2 + **Phase 3 remediation در جریان** 🔄
- **Constitution:** **v2.16** (modular)
- **Git HEAD:** `81a3562` (chat-end part16) · **Tag:** `v0.6.0` (`5730173` روی main)
- **قوانین قفل‌شده:** **۸۶** (#۱-۸۶) + ۲ Reserved (#۵۲، #۵۳)
- **درس‌نامه:** **M1-M104** (۷۲ ثبت + ۳۲ Reserved) + **HM-1..HM-7**
- **Reviews:** **۹** (#۰۰۱-۰۰۹؛ #۰۰۹ Approved/در انتظار commit part17)
- **Tests:** pytest **۲۵/۲۵** + vitest **۳۰/۳۰** · audit **۱۲/۱۲** + companion **۱۴/۱۴** PASS

## 🎯 سه Objective

1. **Phase 2 (Trust Rules → v2.15):** ✅ CLOSED (part12)
2. **Phase 3 (Remediation + full-refresh):** ⏳ IN PROGRESS (part13→part17: check_12، full-refresh، codify v2.16، deprecate legacy، بازسازی این فایل، …)
3. **Phase 4 (اسکن ۱۰۰٪ ۲۸۲ فایل classified):** 🔮 TODO

## 🔒 مهم‌ترین قوانین (مرجع کامل: `01_rules.md`)

### رفتاری / فرمت
- **#۲۴:** No-Deletion — منسوخ با banner `[DEPRECATED]`، هرگز حذف
- **#۲۷:** پایان چت فقط با تأیید صریح کاربر (هرگز خودکار)
- **#۲۹:** فایل با Artifact/code block، نه paste متن
- **#۳۱/#۶۳:** نام + رنگ tab بالای هر کادر کد (🟦۱backend / 🟩۲scripts / 🟧۳frontend / 🟥BACKUP) + تیتر `🟢 ▶️ EXECUTE`
- **#۴۶:** ASCII-only در `print()` ویندوز + `sys.stdout.reconfigure(encoding="utf-8")`
- **#۵۹:** اعلام مسیر دانلود برای هر فایل
- **#۶۱:** پیشنهاد گزینهٔ مطلوب خودِ Claude در چندگزینه‌ای
- **#۶۵:** ثبت درس از اشتباهات با نمایش به کاربر

### Workflow / حاکمیت
- **#۴۸:** پروتکل اجباری شروع چت (boot)
- **#۵۱:** تأیید صریح قبل از write/delete با MCP
- **#۵۵:** به‌روزرسانی Project Knowledge — Claude نسخهٔ جدید را تولید می‌کند تا کاربر در Project جایگزین کند
- **#۶۰:** PENDING-EOC در لحظه ثبت
- **#۶۲:** فایل handoff دائمی پایان چت
- **#۶۶:** push اجباری در پایان هر چت
- **#۶۷:** Cross-shell EXECUTE blocks اجباری
- **#۶۸-۷۷ (v2.14 MDRS v2):** Tier hierarchy، Review trigger، Path validator، VERSION SSoT، Manifest self-awareness، Triple-Rule atomic (#۷۳)، Z-ID permanence، Scope closure، Pre-Action checklist، Continuous discovery logging

### Trust & Anti-Sycophancy (#۷۸-۸۵، v2.15) + #۸۶ (v2.16)
- **#۷۸ SCM:** Scope Contract اجباری برای trigger words («کامل/همه/جامع/…»)
- **#۷۹ QHP:** اعداد N/M، بدون واژگان مبهم
- **#۸۰ NSISN:** بدون self-narrowing خودسرانه
- **#۸۱ RDEM:** تفکیک صریح 🚫 REFUSE (capability) از ⚠️ DEFER (judgment)
- **#۸۲ MPTC:** Pre-Task Checkpoint پیش از task با ۳+ tool/file
- **#۸۳ HAT:** بلوک `🔍 Honesty Audit` پایین هر گزارش پیشرفت
- **#۸۴ APMM:** بدون extrapolation از sample؛ هر مورد مستقل verify
- **#۸۵ Self-Activation Lock:** قواعد #۷۸-۸۴ خودکار، نه با یادآوری کاربر
- **#۸۶ Escape-Aware Sequence Derivation:** شناسه‌های دنباله‌ای (handoff/ledger/hash/شماره) از منبع زنده مشتق شوند، نه حافظه؛ escape ≠ chat-end

## 🔁 قانون تداوم دوحلقه‌ای (canonical)

هر chat-end: **حلقهٔ ۱** ردیف در `claude_workspace/PHASE_LEDGER.md` (append-only، #۲۴) → **حلقهٔ ۲** فایل `PHASE1_PART{N+1}_HANDOFF.txt` (شمارهٔ مکانیکی #۸۶) → هر دو در **یک commit** + push. Enforcement مکانیکی: `check_12_continuity` (invariant **H==L+1**).

## 📋 پروتکل اجباری شروع چت (#۴۸)

Claude **باید** اول `claude_workspace/CHAT_BOOT_TRIGGER_TEMPLATE.md` را follow کند (STEP 0→4). فایل‌های mandatory read (به ترتیب):
1. `docs/constitution/main.md` (index v2.16)
2. `docs/constitution/01_rules.md` (#۱-۸۶)
3. `docs/constitution/02_lessons.md` (M1-M104 + HM)
4. `docs/constitution/06_meta.md`
5. `docs/constitution/04_principles.md` + `05_architecture.md`
6. `docs/HELPER_PROTOCOL.md`
7. `docs/SESSION_STATUS.md`
8. `docs/PENDING_FOR_NEXT_VERSION.md`
9-12. فایل‌های handoff/escape-note/deferred-note مرتبط در `claude_workspace/incoming_permanent/`

و **اول از همه** `claude_workspace/PHASE_LEDGER.md` (قصهٔ تجمعی part01→جاری). سپس STEP 2 acknowledgment + STEP 3 منتظر تأیید کاربر؛ هیچ task قبل از تأیید.

## 🤖 Model Selection (خلاصه)

Atomic end-of-chat / Indicators / Strategies / Debugging پیچیده / Code review → **Opus**؛ Documentation روتین / Repository / UI → **Sonnet**. قانون عملی: ≥۳ مورد پیچیدگی → Opus.

## 🧰 ابزارهای Claude

- **Filesystem MCP:** read-only → Always Allow؛ write/edit/delete → Needs Approval (#۴۹/#۵۱). هرگز `.env`.
- Web search/fetch · Artifacts · Memory.

## ⚠️ هشدارهای مهم

- **هرگز** کد malicious تولید نکن.
- **هرگز** فایل `.env` را با MCP تغییر نده.
- **هرگز** خارج از `D:\Projects\trading-system` عمل نکن.
- **هرگز** پایان چت را خودکار شروع نکن (#۲۷).
- هش/شماره‌های مکانیکی را از منبع زنده بگیر، نه حافظه (#۸۶/M104).

---

## 📌 یادداشت برای Claude در شروع چت

1. اول `CHAT_BOOT_TRIGGER_TEMPLATE.md` را follow کن، سپس `PHASE_LEDGER.md`.
2. acknowledgment بده (STEP 2)، منتظر تأیید کاربر بمان (STEP 3).
3. هر تغییر قانون/درس اساسی → **این فایل را در آپدیت، به‌روز کن و به کاربر بگو نسخهٔ جدید را در Project Knowledge جایگزین کند** (#۵۵).
