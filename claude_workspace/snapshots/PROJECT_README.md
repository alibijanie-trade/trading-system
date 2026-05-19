# PROJECT KNOWLEDGE — راهنمای استفاده

> این پوشه شامل فایل‌هایی است که در **Project Knowledge** در Claude Desktop آپلود می‌شوند.
> **مسیر در Claude Desktop:** Project → Project Knowledge → Add files

## 📋 فایل‌های این پوشه

### ۱. `PROJECT_KNOWLEDGE.md`

**کاربرد:** فایل اصلی Project Knowledge. خلاصه فشرده پروژه برای Claude.

**حجم:** کم (~۳-۵KB)

**روش آپلود:**
1. Claude Desktop باز کنید
2. به Project خود بروید
3. Click on **Project Knowledge** (یا گزینه مشابه)
4. **Add files** → انتخاب `PROJECT_KNOWLEDGE.md`

---

### ۲. `CUSTOM_INSTRUCTIONS.md`

**کاربرد:** متن این فایل را در **Project Settings → Custom Instructions** کپی کنید.

**نه آپلود فایل** — فقط محتوای text را copy و paste کنید در فیلد Custom Instructions.

**مسیر در Claude Desktop:**
- Project → Settings → Custom Instructions (یا "What should Claude know about this project")
- متن داخل بلوک ``` ``` در `CUSTOM_INSTRUCTIONS.md` را paste کنید
- Save

---

### ۳. هر فایل دیگری که می‌خواهید Claude همیشه به آن دسترسی داشته باشد

**توصیه نمی‌شود** فایل‌های زیر را آپلود کنید چون با Filesystem MCP خوانده می‌شوند:
- ❌ `docs/سند_جامع_v2_9.md` (171KB - زیادی است)
- ❌ `docs/CLAUDE_CHECKLIST.md`
- ❌ `docs/SESSION_STATUS.md`
- ❌ `docs/CHAT_LOG.md`

Claude با Filesystem MCP این‌ها را به‌صورت پویا می‌خواند، نیازی نیست در Project Knowledge باشند.

---

## 🔄 قانون آپدیت (#۵۵)

**هر زمان که** قانون جدیدی به سند جامع اضافه شد یا تغییر مهمی صورت گرفت:

1. Claude خودش `PROJECT_KNOWLEDGE.md` به‌روز را تولید می‌کند
2. به شما اعلام می‌کند: "این فایل را در Project Knowledge جایگزین کن"
3. شما در Project Knowledge:
   - فایل قدیمی را delete کنید
   - فایل جدید را add کنید
4. در چت‌های بعدی، Claude نسخه جدید را می‌بیند

این فرآیند **در پایان هر چت** خودکار توسط Claude اجرا می‌شود (طبق قانون #۵۵).

---

## ⚙️ نکات

- **حجم Project Knowledge:** Claude Max 5x اجازه می‌دهد چندین MB
- **فرمت پشتیبانی:** Markdown (.md)، plain text (.txt)، PDF (تا حدی)
- **اولویت:** اگر Project Knowledge + Filesystem MCP هر دو موجودند، Project Knowledge مرجع اولیه است (سریع‌تر)، Filesystem برای deep dive

---

## 🎯 اقدام پیشنهادی الان

1. ✅ `PROJECT_KNOWLEDGE.md` را در Project Knowledge آپلود کنید
2. ✅ متن `CUSTOM_INSTRUCTIONS.md` را در Project Settings → Custom Instructions paste کنید
3. ✅ Settings → Capabilities → Memory: هر دو toggle را روشن کنید (Search and reference chats + Generate memory from chat history)
4. ✅ Settings → Capabilities → Visuals: همان‌طور بماند
5. ✅ Settings → Capabilities → Code execution: همان‌طور بماند

پس از این، در چت ۸ Claude:
- خودکار از Project Knowledge می‌خواند
- Custom Instructions را اعمال می‌کند
- با Memory، تاریخچه چت‌های قبلی را دارد
- با MCP، به فایل‌های پروژه دسترسی دارد

**handoff message در شروع چت ۸ خیلی کوتاه می‌شود — فقط چند خط!**
