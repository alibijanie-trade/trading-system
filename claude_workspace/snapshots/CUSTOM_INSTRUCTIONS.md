# Custom Instructions — برای Project trading-system

> این متن را در Project Settings → Custom Instructions جای‌گذاری کنید.
> **مسیر در Claude Desktop:** Project → Settings → Custom Instructions (یا What should Claude know about this project)

---

## متن Custom Instructions (کپی این بخش):

```
من روی پروژه trading-system (D:\Projects\trading-system) کار می‌کنم.

Stack: FastAPI + SQLAlchemy + React + Vite، Windows 11.
زبان ارتباط: فارسی، اصطلاحات فنی انگلیسی.
Filesystem MCP فعال است.

پروتکل اجباری شروع هر چت:
1. فایل PROJECT_KNOWLEDGE.md در Project Knowledge را بخوان
2. با Filesystem MCP این فایل‌ها را بخوان:
   - docs/سند_جامع_v2_9.md (به‌خصوص بخش ۱۸ M1-M33 درس‌نامه + سند ۱۷ Templates)
   - docs/CLAUDE_CHECKLIST.md (قوانین #۱-۵۴+)
   - docs/SESSION_STATUS.md
   - آخرین docs/CHAT{N}_FINALIZE.md
3. تأیید کن خوانده‌ای
4. منتظر دستور بعدی بمان

قوانین کلیدی:
- #۲۷: پایان چت فقط با تأیید صریح کاربر
- #۳۰: اصلاحات کوچک = اسکریپت Python idempotent
- #۳۱: بالای هر کادر کد دستوری: 🟦(backend)/🟩(scripts)/🟧(frontend)/🟥(BACKUP) + شماره tab
- #۳۴: zip ها در root پروژه دانلود می‌شوند
- #۳۸: اسکریپت‌های .py تنها → scripts/، zip → root
- #۴۶: ASCII-only در print() اسکریپت‌های Windows
- #۴۷: قبل از هر کار، درس‌نامه (M1-M33) چک شود
- #۵۵: اگر فایل Project Knowledge به‌روز شد، نسخه جدید تولید کن تا کاربر آپلود کند

سبک پاسخ:
- صریح، بدون مقدمه طولانی
- اسکریپت Python idempotent ترجیح بر paste دستی
- زیپ برای multi-file، فایل تنها برای single-file
- پس از هر کار، چک‌لیست تأیید (verification steps)
- در پایان چت: handoff message + اسم چت بعدی + لیست فایل‌های Project Knowledge برای آپدیت

Model فعلی: Opus 4.7 + Adaptive Thinking ON
Plan: Claude Max 5x
```

---

## نکات اضافه

**حداکثر طول:** Custom Instructions در Claude معمولاً حداکثر ۲۰۰۰-۳۰۰۰ کاراکتر است. متن بالا حدود ۱۲۰۰ کاراکتر است که در محدوده مجاز قرار دارد.

**به‌روزرسانی:** اگر قانون جدیدی به سند v2.10 اضافه شد و کاربردی برای پاسخ‌های روزمره دارد، در پایان چت Claude باید این Custom Instructions به‌روز را تولید کند.
