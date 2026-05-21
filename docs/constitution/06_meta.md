# ماژول ۰۶ — Meta (Session/Templates/Tooling)

> بخشی از **Constitution v2.12 (Modular)** — [بازگشت به main](./main.md)
>
> **محتوا:** Session/Context + Templates پاسخ Claude + MCP + Claude Desktop + claude_workspace + Skills
> **منبع v2.11:** سند ۱۳ (Session) + سند ۱۳.۵ (تکامل) + سند ۱۴ (Chat Handoff) + سند ۱۵ (وضعیت اجرایی) + سند ۱۶ (مدیریت دانش) + سند ۱۷ (Templates) + سند ۱۹ (Claude MAX) + سند ۲۰ (Pre-commit) + سند ۲۱ (GitHub) + سند ۲۲ (Filesystem MCP) + سند ۲۳ (Claude Desktop) + سند ۲۴ (claude_workspace) + سند ۲۵ (Skills)
> **به‌روزرسانی v2.12:**
> - اصلاحیه shell default به PowerShell+venv (تناقض ۹)
> - افزودن M30 (MCP در چت‌های جدید) به Templates
> - افزودن workflow GitHub backup (قانون #۶۶ Locked) به session protocol
> **Created in commit:** `<git log -1 --format=%h پس از commit 7 پر شود>`

---

## 📋 فهرست بخش‌ها (پس از migration)

> این فهرست در commit 7 (مرحله ۳ Migration) از منبع v2.11 پر می‌شود.

### بخش ۱ — Session Management

- ساختار `SESSION_STATUS.md` (پویا، در پایان هر چت به‌روز)
- ساختار `PROJECT_CONTEXT.md` (Stack + مسیرها + قوانین + CMD‌ها + Decisions)
- ساختار `CHAT_LOG.md` (تاریخچه هر چت با Template)
- پروتکل شروع چت (قانون #۴۸)
- پروتکل پایان چت (۱۲ مرحله، قانون #۲۷ تأیید + قانون #۶۲ handoff فایل)

### بخش ۲ — Chat Handoff Protocol (سند ۱۴ منبع)

- شرایط فعال‌سازی: افت کیفیت + پایان طبیعی
- ۷ مرحله اجباری
- تشخیص علائم پایان طبیعی (فارسی + انگلیسی)
- استثنا: درخواست صریح کاربر

### بخش ۳ — راهنمای تکامل پروژه (سند ۱۳.۵)

- سطح‌بندی 🔒/🎯/💡 (cross-ref به `04_principles.md`)
- شرایط مجاز پیشنهاد تغییر
- فرآیند ۷-مرحله پیشنهاد + الزامات فرمت
- تغییرات ممنوع بدون توافق

### بخش ۴ — مدیریت دانش (سند ۱۶ منبع)

- محدودیت Context Claude (شفافیت)
- ۱۲ سند مرجع پروژه
- چک‌لیست شروع چت (۸ مرحله)
- چک‌لیست پایان چت (۱۲ مرحله)
- کلمات Trigger
- handoff به برنامه‌نویس جدید

### بخش ۵ — Templates پاسخ Claude (سند ۱۷ منبع، ۱۰ template)

1. اولین پاسخ در هر چت
2. پاسخ به «ادامه بده» یا کلمات مبهم
3. اعلام Bug
4. اعلام تصمیم معماری لازم
5. پایان چت
6. اعتراف اشتباه
7. هشدار context اشباع
8. ابهام در درخواست
9. تحویل اسکریپت
10. حالت احتمالی E1 (افت کیفیت)

### بخش ۶ — Claude MAX Real-Time (سند ۱۹ منبع)

- انتخاب Model بر اساس فاز (Opus/Sonnet + Adaptive Thinking)
- تنظیمات Settings پیشنهادی
- Custom Instructions پیشنهادی
- پروتکل توصیه Real-Time

### بخش ۷ — Pre-commit Hooks (سند ۲۰ منبع)

- فلسفه Hybrid mode
- جدول hooks (critical اجباری، minor warning)
- Bypass در اضطرار (قانون #۴۲)
- Mass Reformat اولیه

### بخش ۸ — GitHub Integration (سند ۲۱ منبع)

- چک‌لیست استاندارد اتصال (۵ مرحله)
- Authentication: PAT vs SSH
- Best Practices
- ⭐ v2.12 update: قانون #۶۶ Locked — Push اجباری در پایان هر چت

### بخش ۹ — Filesystem MCP (سند ۲۲ منبع)

- چیست و چرا
- Tools موجود (read-only Always Allow + write/delete Needs Approval)
- Permissions setup (قانون #۴۹)
- Workflow عملی (Preview → Approve → Write → Read-back → Verify → Confirm)
- استثنائات و توصیه‌ها
- Troubleshooting (شامل M83: retry first)

### بخش ۱۰ — Claude Desktop Configuration (سند ۲۳ منبع)

- Memory toggles (Settings → Capabilities → Memory)
- Project Knowledge (محتوا و به‌روزرسانی)
- Custom Instructions
- Settings audit (Connectors + Feature Preview)
- ⚠️ هشدار: Memory جایگزین فایل نیست (M56)

### بخش ۱۱ — claude_workspace Structure (سند ۲۴ منبع)

- ۵ پوشه: incoming_permanent، old_versions، screenshots، snapshots، zip_temp
- gitignore policy
- Naming conventions
- ارتباط با قوانین #۵۶-۵۹

### بخش ۱۲ — Skills اختصاصی پروژه (سند ۲۵ منبع، placeholder)

- Skills رسمی فعال (docx، xlsx، pdf، frontend-design، skill-creator، …)
- Skills اختصاصی آینده (trading-script-generator، trading-endof-chat، …)
- زمان ساخت (پایان چت ۸ یا اوایل چت ۹)
- ساختار Skill

---

## 🚧 وضعیت این ماژول

⚠️ **این فایل فعلاً skeleton است.** محتوای کامل meta در **commit 7** از منابع v2.11 (سند ۱۳-۱۷، ۱۹-۲۵) migrate می‌شود.

پس از migration، انتظار می‌رود این ماژول ~۳۵KB باشد — درون آستانه MCP-safe.

---

## 🔮 افزوده‌های v2.12 (در commit 7)

علاوه بر migration:
- اصلاحیه shell default در بخش ۱ از CMD به PowerShell+venv (تناقض ۹)
- یادآوری M30 (MCP در چت‌های جدید load می‌شود، نه current chat) در بخش ۹ Templates
- افزودن workflow GitHub backup (قانون #۶۶ Locked در v2.12) در بخش ۸

---

**📌 پایان skeleton 06_meta.md — منتظر محتوای migration در commit 7**
