/**
 * dateFormat — فرمت‌بندی تاریخ با پشتیبانی شمسی/میلادی + ۴ فرمت میلادی
 *
 * استفاده از Intl (built-in، بدون کتابخانه خارجی):
 *   - Gregorian: ۴ فرمت (iso/us-short/eu-short/long)
 *   - Jalali:    Intl.DateTimeFormat("fa-IR-u-ca-persian", ...)
 *
 * نسخه ۳۲ — افزودن انتخاب فرمت میلادی.
 *
 * مثال‌ها:
 *   formatDate("2024-01-15", "gregorian", { format: "iso" })       → "2024-01-15"
 *   formatDate("2024-01-15", "gregorian", { format: "us-short" })  → "01/15/2024"
 *   formatDate("2024-01-15", "gregorian", { format: "eu-short" })  → "15/01/2024"
 *   formatDate("2024-01-15", "gregorian", { format: "long" })      → "January 15, 2024"
 *   formatDate("2024-01-15", "jalali")                             → "۱۴۰۲/۱۰/۲۵"
 */

export const CALENDARS = {
  GREGORIAN: "gregorian",
  JALALI: "jalali",
};

export const CALENDAR_LABELS = {
  gregorian: "میلادی",
  jalali: "شمسی",
};

export const GREGORIAN_FORMATS = ["iso", "us-short", "eu-short", "long"];

export const GREGORIAN_FORMAT_LABELS = {
  "iso":      "ISO  (2024-01-15)",
  "us-short": "آمریکایی  (01/15/2024)",
  "eu-short": "اروپایی  (15/01/2024)",
  "long":     "کامل  (January 15, 2024)",
};

export const DEFAULT_GREGORIAN_FORMAT = "us-short";

export function isValidCalendar(calendar) {
  return calendar === CALENDARS.GREGORIAN || calendar === CALENDARS.JALALI;
}

export function isValidGregorianFormat(fmt) {
  return GREGORIAN_FORMATS.includes(fmt);
}

/**
 * @param {Date | string | number} input
 * @param {"gregorian" | "jalali"} calendar
 * @param {object} options
 * @param {boolean} [options.withTime=false]
 * @param {"iso"|"us-short"|"eu-short"|"long"} [options.format="us-short"]
 *        (فقط برای gregorian — برای jalali ignore می‌شود)
 * @returns {string}
 */
export function formatDate(input, calendar = CALENDARS.GREGORIAN, options = {}) {
  if (input === null || input === undefined || input === "") return "";

  const date = input instanceof Date ? input : new Date(input);
  if (!(date instanceof Date) || isNaN(date.getTime())) return "";

  const { withTime = false, format = DEFAULT_GREGORIAN_FORMAT } = options;

  // ---------- Jalali ----------
  if (calendar === CALENDARS.JALALI) {
    const dtOptions = {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      ...(withTime && { hour: "2-digit", minute: "2-digit", hour12: false }),
    };
    try {
      return new Intl.DateTimeFormat("fa-IR-u-ca-persian", dtOptions).format(date);
    } catch (e) {
      return new Intl.DateTimeFormat("en-US", dtOptions).format(date);
    }
  }

  // ---------- Gregorian — ISO ----------
  if (format === "iso") {
    const yyyy = date.getFullYear();
    const mm = String(date.getMonth() + 1).padStart(2, "0");
    const dd = String(date.getDate()).padStart(2, "0");
    let s = `${yyyy}-${mm}-${dd}`;
    if (withTime) {
      const HH = String(date.getHours()).padStart(2, "0");
      const MM = String(date.getMinutes()).padStart(2, "0");
      s += ` ${HH}:${MM}`;
    }
    return s;
  }

  // ---------- Gregorian — Long ----------
  if (format === "long") {
    return new Intl.DateTimeFormat("en-US", {
      dateStyle: "long",
      ...(withTime && { timeStyle: "short" }),
    }).format(date);
  }

  // ---------- Gregorian — Short (us / eu) ----------
  const locale = format === "eu-short" ? "en-GB" : "en-US";
  return new Intl.DateTimeFormat(locale, {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    ...(withTime && { hour: "2-digit", minute: "2-digit", hour12: false }),
  }).format(date);
}
