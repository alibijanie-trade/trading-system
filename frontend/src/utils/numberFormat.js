/**
 * numberFormat — توابع کمکی برای فرمت‌بندی اعداد با جداکننده سه‌رقمی
 * طبق سند ۸.۳ (جداکننده سه‌رقمی Real-time در input های عددی) — فاز ۰: نمایش
 *
 * استفاده از Intl.NumberFormat (built-in، بدون کتابخانه خارجی).
 *
 * مثال‌ها:
 *   formatNumber(1714)                  → "1,714"
 *   formatNumber(102345.67)             → "102,345.67"
 *   formatNumber(102345.67, { decimals: 0 }) → "102,346"
 *   formatNumber(null)                  → ""
 *   formatNumber("abc")                 → ""
 */

const DEFAULT_LOCALE = "en-US";

export function formatNumber(value, options = {}) {
  if (value === null || value === undefined || value === "") return "";

  const num = typeof value === "number" ? value : Number(value);
  if (!Number.isFinite(num)) return "";

  const {
    locale = DEFAULT_LOCALE,
    decimals,
    minDecimals,
    maxDecimals,
  } = options;

  const fmtOptions = {};
  if (decimals !== undefined) {
    fmtOptions.minimumFractionDigits = decimals;
    fmtOptions.maximumFractionDigits = decimals;
  } else {
    if (minDecimals !== undefined) fmtOptions.minimumFractionDigits = minDecimals;
    if (maxDecimals !== undefined) fmtOptions.maximumFractionDigits = maxDecimals;
  }

  return new Intl.NumberFormat(locale, fmtOptions).format(num);
}

/**
 * تجزیه رشته فرمت‌شده به عدد:
 *   parseFormattedNumber("1,714")     → 1714
 *   parseFormattedNumber("102,345.67") → 102345.67
 *   parseFormattedNumber("")           → null
 *   parseFormattedNumber("abc")        → null
 */
export function parseFormattedNumber(str) {
  if (str === null || str === undefined || str === "") return null;
  const cleaned = String(str).replace(/,/g, "").trim();
  if (cleaned === "") return null;
  const n = Number(cleaned);
  return Number.isFinite(n) ? n : null;
}
