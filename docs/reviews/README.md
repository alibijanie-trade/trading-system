# Reviews Directory

> **هدف:** ذخیره‌سازی تک‌تک Review Report فایل‌ها.

## ساختار

هر فایل اینجا یک **Review Report** کامل است که با ساختار `# Review #{N} — {Subject}` شروع می‌شود. این فایل‌ها صرفاً storage هستند؛ master index در `docs/REVIEW_LOG.md` نگه‌داری می‌شود.

## Filename Convention

```
docs/reviews/YYYY-MM-DD-{slug}.md
```

- `YYYY-MM-DD` — تاریخ ISO 8601 از زمان initiation (نه completion)
- `{slug}` — kebab-case، ۱-۵ کلمه descriptive، باید با `slug` column در `REVIEW_LOG.md` match کند

**مثال:**  
`2026-05-22-mdrs-v2-review-infrastructure-bootstrap.md`  
→ Slug در LOG: `mdrs-v2-review-infrastructure-bootstrap`

## Lifecycle و Connections

- **پروسه:** نگاه به `docs/REVIEW_PROTOCOL.md` برای جریان کار کامل
- **Index:** نگاه به `docs/REVIEW_LOG.md` برای فهرست همه reports
- **Pre-add gate:** نگاه به `docs/PRE_ADD_CHECKLIST.md` (وقتی ساخته شد در D7) برای checklist قبل از reaching trigger

## Numbering Integrity

ID‌ها متوالی هستند (001, 002, 003 — no gaps). Future audit check این یکپارچگی را enforce می‌کند:
- File ID در heading با LOG row ID match کند
- Slug در filename با LOG slug column match کند
- هر file یک row در LOG داشته باشد (و برعکس)

## No-Deletion Policy

طبق قانون #۲۴، هیچ Review Report file حذف نمی‌شود. حتی Rejected reviews در این پوشه می‌مانند (با Status=Rejected در LOG) برای historical record.

---

**نسخه:** v1.0 (S2 D6 از MDRS v2)
**ساخته توسط:** Claude در `TRADING-phase1-part03-mdrs-v2-implementation`
