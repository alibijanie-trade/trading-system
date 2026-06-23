# PROJECT_CONSTITUTION — Redirect Stub (v2.18)

> ⚠️ **این فایل فقط یک redirect است.**
>
> سند جامع پروژه از **v2.12** به ساختار modular مهاجرت کرد. نسخه فعال: **v2.18**.

---

## 📍 محل جدید Constitution

**Constitution v2.18 (Modular):** [`docs/constitution/main.md`](./constitution/main.md)

ساختار:
- [`constitution/main.md`](./constitution/main.md) — index + cross-refs (شروع از اینجا)
- [`constitution/01a_rules_core.md`](./constitution/01a_rules_core.md) — جدول قوانین Locked #۱-۹۰ (boot-critical)
- [`constitution/01_rules.md`](./constitution/01_rules.md) — شرح کامل قوانین #۱-۹۰ (on-demand)
- [`constitution/02_lessons.md`](./constitution/02_lessons.md) — درس‌نامه M1-M110 + HM-1..HM-7
- [`constitution/03_bugs.md`](./constitution/03_bugs.md) — Bug catalog
- [`constitution/04_principles.md`](./constitution/04_principles.md) — ۸ اصل + metarules
- [`constitution/05_architecture.md`](./constitution/05_architecture.md) — Stack + DB + API + UI
- [`constitution/06_meta.md`](./constitution/06_meta.md) — Session + Templates + MCP + Tooling

---

## 📜 نسخه‌های قدیمی (archive)

نسخه‌های v2.6–v2.11 (مونولیتیک) برای reference تاریخی در:

[`docs/constitution/archive/`](./constitution/archive/)

طبق قانون #۲۴ (No-Deletion)، این فایل‌ها به‌عنوان snapshot تاریخی حفظ شده‌اند. **برای کار جاری از modular constitution استفاده کنید.**

---

## ⚙️ چرا modular split؟

| دلیل | جزئیات |
|---|---|
| **MCP performance** | فایل واحد ~۲۱۶KB با Filesystem MCP کند بود (درس M66) |
| **Context efficiency** | چت‌های جدید فقط بخش‌های مرتبط را load می‌کنند |
| **بهینه‌سازی audit** | هر ماژول < ۵۰KB، MCP-safe |
| **سرعت navigation** | متن مرتبط در یک ماژول، نه scroll در ۲۲۰KB |

---

## 🔄 برای Claude بعدی

اگر Claude بعدی به این فایل می‌رسد، بداند:
1. این فایل **deprecated** است و فقط redirect می‌کند
2. ترتیب خواندن طبق `06_meta.md` بخش ۶.۱
3. در هیچ‌جا این فایل را به‌عنوان منبع authoritative استفاده نکن

---

**تاریخ ساخت:** ۲۰۲۶-۰۵-۲۱ | **چت ۱۱.۰.الف commit 8** | **Branch:** `infra/governance-overhaul`
