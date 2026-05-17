# -*- coding: utf-8 -*-
"""
اسکریپت ۳۱ — زیرگام ۸.۵: Numeric Separator + Persian Calendar
================================================================
این اسکریپت idempotent است — قابل اجرا چندبار بدون شکست.

محتوای زیرگام ۸.۵ (آخرین زیرگام فاز ۰):
  ۱) utils/numberFormat.js — formatNumber با Intl.NumberFormat
  ۲) utils/dateFormat.js   — formatDate با Intl + پشتیبانی شمسی
       Intl.DateTimeFormat("fa-IR-u-ca-persian", ...) — بدون کتابخانه خارجی
  ۳) stores/preferencesStore.js — Zustand persist
       state: calendar ('gregorian' | 'jalali')
       پیش‌فرض: 'gregorian' (طبق تصمیم Session 1)
  ۴) components/settings/CalendarToggle.jsx — radiogroup + preview تاریخ
  ۵) pages/SettingsPage.jsx — بخش "زبان و تقویم" + reset گسترش‌یافته
  ۶) pages/ChartPage.jsx:
       - متن "1714 کندل" → "1,714 کندل" با formatNumber
       - lightweight-chart.localization.dateFormat با تقویم انتخابی

اصول طراحی:
  - بدون کتابخانه خارجی (Intl کافی است)
  - بدون hex hardcoded
  - مطابق Variant Indicator Pattern (CalendarToggle)
  - reset سراسری: themeStore.resetAll + preferencesStore.reset
  - ChartPage useEffect deps گسترش می‌یابد: [..., calendar]

فایل‌های جدید:
  frontend/src/utils/numberFormat.js
  frontend/src/utils/dateFormat.js
  frontend/src/stores/preferencesStore.js
  frontend/src/components/settings/CalendarToggle.jsx

فایل‌های به‌روزرسانی:
  frontend/src/pages/SettingsPage.jsx
  frontend/src/pages/ChartPage.jsx
================================================================
"""

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
FRONTEND = PROJECT_ROOT / "frontend" / "src"

UTILS_DIR = FRONTEND / "utils"
STORES_DIR = FRONTEND / "stores"
SETTINGS_COMP_DIR = FRONTEND / "components" / "settings"
PAGES_DIR = FRONTEND / "pages"

NUMBER_FORMAT = UTILS_DIR / "numberFormat.js"
DATE_FORMAT = UTILS_DIR / "dateFormat.js"
PREFS_STORE = STORES_DIR / "preferencesStore.js"
CALENDAR_TOGGLE = SETTINGS_COMP_DIR / "CalendarToggle.jsx"
SETTINGS_PAGE = PAGES_DIR / "SettingsPage.jsx"
CHART_PAGE = PAGES_DIR / "ChartPage.jsx"


# ============================================================
# utils/numberFormat.js
# ============================================================

NUMBER_FORMAT_JS = """/**
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
"""


# ============================================================
# utils/dateFormat.js
# ============================================================

DATE_FORMAT_JS = """/**
 * dateFormat — فرمت‌بندی تاریخ با پشتیبانی تقویم شمسی و میلادی
 * طبق سند ۸.۷ (تقویم شمسی/میلادی toggle) — پیش‌فرض میلادی (تصمیم Session 1)
 *
 * استفاده از Intl.DateTimeFormat (built-in، بدون کتابخانه خارجی):
 *   - Gregorian: Intl.DateTimeFormat("en-US", ...)
 *   - Jalali:    Intl.DateTimeFormat("fa-IR-u-ca-persian", ...)
 *
 * مثال‌ها:
 *   formatDate(new Date("2024-01-15"), "gregorian")  → "01/15/2024"
 *   formatDate(new Date("2024-01-15"), "jalali")     → "۱۴۰۲/۱۰/۲۵"
 *   formatDate("2024-01-15T10:30:00Z", "jalali", { withTime: true })
 *     → "۱۴۰۲/۱۰/۲۵، ۱۴:۰۰" (بسته به timezone)
 */

export const CALENDARS = {
  GREGORIAN: "gregorian",
  JALALI: "jalali",
};

export const CALENDAR_LABELS = {
  gregorian: "میلادی",
  jalali: "شمسی",
};

export function isValidCalendar(calendar) {
  return calendar === CALENDARS.GREGORIAN || calendar === CALENDARS.JALALI;
}

/**
 * @param {Date | string | number} input
 * @param {"gregorian" | "jalali"} calendar
 * @param {object} options
 * @param {boolean} [options.withTime=false]
 * @returns {string}
 */
export function formatDate(input, calendar = CALENDARS.GREGORIAN, options = {}) {
  if (input === null || input === undefined || input === "") return "";

  const date = input instanceof Date ? input : new Date(input);
  if (!(date instanceof Date) || isNaN(date.getTime())) return "";

  const { withTime = false } = options;

  const dtOptions = {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    ...(withTime && {
      hour: "2-digit",
      minute: "2-digit",
      hour12: false,
    }),
  };

  // Jalali — Intl با locale fa-IR-u-ca-persian
  if (calendar === CALENDARS.JALALI) {
    try {
      return new Intl.DateTimeFormat("fa-IR-u-ca-persian", dtOptions).format(date);
    } catch (e) {
      // fallback اگر مرورگر پشتیبانی نکرد (بسیار نادر)
      return new Intl.DateTimeFormat("en-US", dtOptions).format(date);
    }
  }

  // Gregorian (پیش‌فرض)
  return new Intl.DateTimeFormat("en-US", dtOptions).format(date);
}
"""


# ============================================================
# stores/preferencesStore.js
# ============================================================

PREFS_STORE_JS = """/* ============================================================
   Zustand store برای ترجیحات کاربر (calendar، locale، ...)
   جدا از themeStore — چون این‌ها به ظاهر تم ربطی ندارند.
   persist در localStorage با کلید "preferences-storage"
   ============================================================ */
import { create } from "zustand";
import { persist } from "zustand/middleware";
import { CALENDARS } from "../utils/dateFormat.js";

export const DEFAULT_CALENDAR = CALENDARS.GREGORIAN; // طبق تصمیم Session 1

const usePreferencesStore = create(
  persist(
    (set) => ({
      calendar: DEFAULT_CALENDAR,

      setCalendar: (calendar) => set({ calendar }),

      reset: () =>
        set({
          calendar: DEFAULT_CALENDAR,
        }),
    }),
    {
      name: "preferences-storage",
      version: 1,
    }
  )
);

export default usePreferencesStore;
"""


# ============================================================
# components/settings/CalendarToggle.jsx
# ============================================================

CALENDAR_TOGGLE_JSX = """import { formatDate, CALENDARS, CALENDAR_LABELS } from "../../utils/dateFormat.js";

/**
 * CalendarToggle — انتخاب تقویم میلادی/شمسی + preview تاریخ امروز
 *
 * Props:
 *   value:    "gregorian" | "jalali"
 *   onChange: (calendar) => void
 *
 * شامل ۲ دکمه radio + ناحیه preview که با تغییر value به‌روز می‌شود.
 */

const OPTIONS = [
  { value: CALENDARS.GREGORIAN, label: CALENDAR_LABELS.gregorian },
  { value: CALENDARS.JALALI,    label: CALENDAR_LABELS.jalali    },
];

export default function CalendarToggle({ value, onChange }) {
  return (
    <div>
      <div
        role="radiogroup"
        aria-label="نوع تقویم"
        style={{ display: "flex", gap: 8, flexWrap: "wrap" }}
      >
        {OPTIONS.map((opt) => {
          const isActive = value === opt.value;
          return (
            <button
              key={opt.value}
              type="button"
              role="radio"
              aria-checked={isActive}
              onClick={() => onChange(opt.value)}
              style={{
                flex: "1 1 120px",
                padding: "10px 16px",
                background: isActive
                  ? "var(--color-primary)"
                  : "var(--color-card)",
                color: isActive
                  ? "var(--color-text-inverse)"
                  : "var(--color-text)",
                border: `1px solid ${
                  isActive ? "var(--color-primary)" : "var(--color-border)"
                }`,
                borderRadius: 4,
                fontSize: 13,
                fontWeight: isActive ? 600 : 500,
              }}
            >
              {opt.label}
            </button>
          );
        })}
      </div>

      {/* preview تاریخ امروز با تقویم انتخابی */}
      <div
        style={{
          marginTop: 14,
          padding: "14px 16px",
          background: "var(--color-bg-elevated)",
          border: "1px solid var(--color-border)",
          borderRadius: 4,
          color: "var(--color-text)",
          fontSize: 14,
          lineHeight: 1.7,
        }}
      >
        <div style={{ color: "var(--color-text-muted)", fontSize: 12, marginBottom: 4 }}>
          نمونه — تاریخ امروز:
        </div>
        <div style={{ fontWeight: 600 }}>
          {formatDate(new Date(), value)}
        </div>
        <div style={{ color: "var(--color-text-muted)", fontSize: 12, marginTop: 6 }}>
          همراه ساعت: {formatDate(new Date(), value, { withTime: true })}
        </div>
      </div>
    </div>
  );
}
"""


# ============================================================
# pages/SettingsPage.jsx — به‌روز با CalendarToggle + reset گسترش
# ============================================================

SETTINGS_PAGE_JSX = """import { Link } from "react-router-dom";
import useThemeStore from "../stores/themeStore.js";
import useConfirmStore from "../stores/confirmStore.js";
import useToastStore from "../stores/toastStore.js";
import usePreferencesStore from "../stores/preferencesStore.js";
import { listThemes } from "../themes/themes.js";
import ThemeCard from "../components/settings/ThemeCard.jsx";
import FontSizeControl from "../components/settings/FontSizeControl.jsx";
import CalendarToggle from "../components/settings/CalendarToggle.jsx";

/**
 * SettingsPage — صفحه /settings
 *
 * بخش‌ها:
 *   ۱) ظاهر و تم (۵ کارت preview)
 *   ۲) اندازه فونت (۴ preset + preview زنده)
 *   ۳) زبان و تقویم (gregorian/jalali + preview تاریخ امروز)
 *   ۴) بازگشت به پیش‌فرض — ریست هر دو store
 */
export default function SettingsPage() {
  const themeId = useThemeStore((s) => s.themeId);
  const setTheme = useThemeStore((s) => s.setTheme);
  const fontSize = useThemeStore((s) => s.fontSize);
  const setFontSize = useThemeStore((s) => s.setFontSize);
  const resetTheme = useThemeStore((s) => s.resetAll);

  const calendar = usePreferencesStore((s) => s.calendar);
  const setCalendar = usePreferencesStore((s) => s.setCalendar);
  const resetPreferences = usePreferencesStore((s) => s.reset);

  const askConfirm = useConfirmStore((s) => s.confirm);
  const toastSuccess = useToastStore((s) => s.success);

  const themes = listThemes();

  const handleReset = async () => {
    const ok = await askConfirm({
      title: "بازگشت به تنظیمات پیش‌فرض",
      message:
        "همه تنظیمات (تم، اندازه فونت، تقویم و رنگ‌های سفارشی) به حالت پیش‌فرض بازمی‌گردند. آیا مطمئن هستید؟",
      variant: "warning",
      confirmText: "بازگشت به پیش‌فرض",
      cancelText: "انصراف",
    });
    if (!ok) return;
    resetTheme();
    resetPreferences();
    toastSuccess("تنظیمات به حالت پیش‌فرض بازگشت.");
  };

  return (
    <div style={{ padding: 24, maxWidth: 900, margin: "0 auto" }}>
      <div style={{ marginBottom: 16 }}>
        <Link to="/">← بازگشت به صفحه اصلی</Link>
      </div>

      <header
        style={{
          marginBottom: 32,
          paddingBottom: 16,
          borderBottom: "1px solid var(--color-border)",
        }}
      >
        <h1
          style={{
            fontSize: 22,
            fontWeight: 600,
            color: "var(--color-text)",
          }}
        >
          ⚙️ تنظیمات
        </h1>
        <p
          style={{
            marginTop: 4,
            fontSize: 13,
            color: "var(--color-text-muted)",
          }}
        >
          تم، اندازه فونت، تقویم و سایر تنظیمات ظاهری برنامه
        </p>
      </header>

      {/* بخش ۱ — انتخاب تم */}
      <section style={{ marginBottom: 36 }}>
        <SectionHeader
          title="ظاهر و تم"
          description="یک تم را برای ظاهر کلی برنامه انتخاب کنید"
        />
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
            gap: 12,
          }}
        >
          {themes.map((t) => (
            <ThemeCard
              key={t.id}
              theme={t}
              isActive={t.id === themeId}
              onClick={() => setTheme(t.id)}
            />
          ))}
        </div>
      </section>

      {/* بخش ۲ — اندازه فونت */}
      <section style={{ marginBottom: 36 }}>
        <SectionHeader
          title="اندازه فونت"
          description="اندازه متن سراسری برنامه — preview در پایین"
        />
        <FontSizeControl value={fontSize} onChange={setFontSize} />
      </section>

      {/* بخش ۳ — زبان و تقویم (🆕 زیرگام ۸.۵) */}
      <section style={{ marginBottom: 36 }}>
        <SectionHeader
          title="زبان و تقویم"
          description="نوع تقویم برای نمایش تاریخ‌ها در نمودارها و گزارش‌ها"
        />
        <CalendarToggle value={calendar} onChange={setCalendar} />
      </section>

      {/* بخش ۴ — ریست */}
      <section
        style={{
          paddingTop: 20,
          borderTop: "1px solid var(--color-border)",
        }}
      >
        <SectionHeader
          title="بازنشانی"
          description="تمام تنظیمات را به حالت پیش‌فرض برگردانید"
        />
        <button
          type="button"
          onClick={handleReset}
          style={{
            padding: "10px 18px",
            background: "var(--color-card)",
            color: "var(--color-warning)",
            border: "1px solid var(--color-warning)",
            borderRadius: 4,
            fontSize: 13,
            fontWeight: 600,
          }}
        >
          🔄 بازگشت به تنظیمات پیش‌فرض
        </button>
      </section>
    </div>
  );
}

function SectionHeader({ title, description }) {
  return (
    <div style={{ marginBottom: 14 }}>
      <h2
        style={{
          fontSize: 15,
          fontWeight: 600,
          color: "var(--color-text)",
          marginBottom: 4,
        }}
      >
        {title}
      </h2>
      <p
        style={{
          fontSize: 12,
          color: "var(--color-text-muted)",
        }}
      >
        {description}
      </p>
    </div>
  );
}
"""


# ============================================================
# pages/ChartPage.jsx — به‌روز با formatNumber + localization
# ============================================================

CHART_PAGE_JSX = """import { useEffect, useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { createChart, CrosshairMode } from "lightweight-charts";
import api from "../services/api.js";
import useThemeStore from "../stores/themeStore.js";
import usePreferencesStore from "../stores/preferencesStore.js";
import SkeletonBlock from "../components/common/SkeletonBlock.jsx";
import { formatNumber } from "../utils/numberFormat.js";
import { formatDate } from "../utils/dateFormat.js";

const TIMEFRAMES = [
  { value: "1d", label: "روزانه (1d)" },
  { value: "1h", label: "یک‌ساعته (1h)" },
  { value: "15m", label: "۱۵ دقیقه (15m)" },
];

/* تبدیل ISO 8601 (بدون timezone) → Unix seconds UTC */
function isoToUnix(isoStr) {
  const withZ = isoStr.endsWith("Z") ? isoStr : isoStr + "Z";
  return Math.floor(new Date(withZ).getTime() / 1000);
}

/* خواندن یک متغیر CSS از :root (در زمان فراخوانی) */
function readVar(name, fallback = "") {
  if (typeof window === "undefined") return fallback;
  const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return v || fallback;
}

export default function ChartPage() {
  const { symbolId } = useParams();
  const chartContainerRef = useRef(null);
  const chartRef = useRef(null);

  // به‌روزرسانی نمودار با تغییر تم/تقویم — در dep array
  const themeId = useThemeStore((s) => s.themeId);
  const calendar = usePreferencesStore((s) => s.calendar);

  const [timeframe, setTimeframe] = useState("1d");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [meta, setMeta] = useState({ count: 0, total: 0 });

  useEffect(() => {
    let cancelled = false;

    const load = async () => {
      setLoading(true);
      setError("");

      try {
        const resp = await api.get(
          `/ohlcv/${symbolId}?timeframe=${timeframe}&limit=1000`
        );
        if (cancelled) return;

        const data = resp.data.data;
        setMeta({ count: data.count, total: data.total });

        if (!data.candles || data.candles.length === 0) {
          setError(`داده‌ای برای تایم‌فریم ${timeframe} موجود نیست`);
          setLoading(false);
          return;
        }

        const candleData = data.candles.map((c) => ({
          time: isoToUnix(c.timestamp),
          open: c.open,
          high: c.high,
          low: c.low,
          close: c.close,
        }));

        // رنگ‌ها از CSS variables تم فعلی
        const upColor = readVar("--color-success", "#26a69a");
        const downColor = readVar("--color-danger", "#ef5350");
        const bgColor = readVar("--color-card", "#1e222d");
        const textColor = readVar("--color-text", "#d1d4dc");
        const gridColor = readVar("--color-grid", "#2a2e39");
        const borderColor = readVar("--color-border", "#363a45");

        const volumeData = data.candles.map((c) => ({
          time: isoToUnix(c.timestamp),
          value: c.volume,
          color: c.close >= c.open ? `${upColor}80` : `${downColor}80`,
        }));

        // پاک کردن نمودار قبلی
        if (chartRef.current) {
          chartRef.current.remove();
          chartRef.current = null;
        }

        const chart = createChart(chartContainerRef.current, {
          width: chartContainerRef.current.clientWidth,
          height: 500,
          layout: {
            background: { color: bgColor },
            textColor: textColor,
          },
          grid: {
            vertLines: { color: gridColor },
            horzLines: { color: gridColor },
          },
          crosshair: { mode: CrosshairMode.Normal },
          timeScale: {
            timeVisible: true,
            secondsVisible: false,
            borderColor: borderColor,
          },
          rightPriceScale: { borderColor: borderColor },
          // 🆕 زیرگام ۸.۵ — localization برای تقویم انتخابی
          localization: {
            dateFormat: (time) => {
              // time در lightweight-charts معمولاً UTCTimestamp (number) است
              const d = typeof time === "number"
                ? new Date(time * 1000)
                : new Date(time);
              return formatDate(d, calendar);
            },
            priceFormatter: (price) =>
              formatNumber(price, { maxDecimals: 2 }),
          },
        });
        chartRef.current = chart;

        const candleSeries = chart.addCandlestickSeries({
          upColor: upColor,
          downColor: downColor,
          borderVisible: false,
          wickUpColor: upColor,
          wickDownColor: downColor,
        });
        candleSeries.setData(candleData);

        const volumeSeries = chart.addHistogramSeries({
          priceFormat: { type: "volume" },
          priceScaleId: "",
        });
        volumeSeries.priceScale().applyOptions({
          scaleMargins: { top: 0.8, bottom: 0 },
        });
        volumeSeries.setData(volumeData);

        chart.timeScale().fitContent();

        setLoading(false);
      } catch (err) {
        if (cancelled) return;
        if (err.code === "ERR_NETWORK") {
          setError("خطا در ارتباط با سرور");
        } else if (err.response?.status === 404) {
          setError("نماد یافت نشد");
        } else {
          setError(err.response?.data?.message || "خطای ناشناخته");
        }
        setLoading(false);
      }
    };

    load();

    const handleResize = () => {
      if (chartRef.current && chartContainerRef.current) {
        chartRef.current.applyOptions({
          width: chartContainerRef.current.clientWidth,
        });
      }
    };
    window.addEventListener("resize", handleResize);

    return () => {
      cancelled = true;
      window.removeEventListener("resize", handleResize);
      if (chartRef.current) {
        chartRef.current.remove();
        chartRef.current = null;
      }
    };
  }, [symbolId, timeframe, themeId, calendar]); // 🆕 calendar در deps

  return (
    <div style={{ padding: 24, maxWidth: 1200, margin: "0 auto" }}>
      <div style={{ marginBottom: 16 }}>
        <Link to="/">← بازگشت به صفحه اصلی</Link>
      </div>

      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 16,
        }}
      >
        <h1 style={{ fontSize: 22 }}>BTC/USDT</h1>
        <select
          value={timeframe}
          onChange={(e) => setTimeframe(e.target.value)}
          style={{
            background: "var(--color-card)",
            color: "var(--color-text)",
            padding: "8px 12px",
            borderRadius: 4,
            border: "1px solid var(--color-border)",
            fontSize: 14,
          }}
        >
          {TIMEFRAMES.map((tf) => (
            <option key={tf.value} value={tf.value}>
              {tf.label}
            </option>
          ))}
        </select>
      </header>

      {/* متادیتا — هنگام loading جایگزین با Skeleton */}
      {loading ? (
        <div style={{ marginBottom: 12 }}>
          <SkeletonBlock variant="text" width={220} height={13} />
        </div>
      ) : meta.count > 0 && !error ? (
        <div
          style={{
            fontSize: 13,
            color: "var(--color-text-muted)",
            marginBottom: 12,
          }}
        >
          {formatNumber(meta.count)} از {formatNumber(meta.total)} کندل نمایش داده می‌شود
        </div>
      ) : null}

      {error && (
        <div
          style={{
            padding: 12,
            background: "var(--color-danger-bg)",
            color: "var(--color-danger)",
            border: "1px solid var(--color-danger)",
            borderRadius: 4,
            marginBottom: 12,
            fontSize: 14,
          }}
        >
          {error}
        </div>
      )}

      <div style={{ position: "relative" }}>
        <div
          ref={chartContainerRef}
          style={{
            width: "100%",
            minHeight: 500,
            background: "var(--color-card)",
            borderRadius: 4,
            opacity: loading ? 0 : 1,
            transition: "opacity 0.2s ease",
          }}
        />
        {loading && (
          <div
            style={{
              position: "absolute",
              inset: 0,
              padding: 16,
              display: "flex",
              flexDirection: "column",
              gap: 12,
              background: "var(--color-card)",
              borderRadius: 4,
              border: "1px solid var(--color-border)",
            }}
          >
            <div style={{ display: "flex", gap: 12 }}>
              <SkeletonBlock variant="rect" width={120} height={20} />
              <SkeletonBlock variant="rect" width={80} height={20} />
            </div>
            <SkeletonBlock
              variant="rect"
              width="100%"
              height="100%"
              style={{ flex: 1, minHeight: 380 }}
            />
            <SkeletonBlock variant="rect" width="100%" height={24} />
          </div>
        )}
      </div>
    </div>
  );
}
"""


# ============================================================
# تابع نوشتن idempotent
# ============================================================

def write_if_changed(path: Path, content: str, label: str) -> str:
    rel = path.relative_to(PROJECT_ROOT)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        print(f"  ✓ ایجاد:    {rel}  ({label})")
        return "created"

    current = path.read_text(encoding="utf-8")
    if current == content:
        print(f"  - بدون تغییر: {rel}  (idempotent)")
        return "unchanged"

    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"  ✓ به‌روز:   {rel}  ({label})")
    return "updated"


# ============================================================
# اجرای اصلی
# ============================================================

def main() -> int:
    print("=" * 64)
    print("اسکریپت ۳۱ — زیرگام ۸.۵: Numeric Separator + Persian Calendar")
    print("=" * 64)
    print()

    if not FRONTEND.exists():
        print("[ERROR] دایرکتوری frontend/src یافت نشد.")
        return 1

    # پیش‌چک: SettingsPage باید موجود باشد (از زیرگام ۸.۴)
    if not SETTINGS_PAGE.exists():
        print("[ERROR] SettingsPage.jsx یافت نشد.")
        print("        ابتدا اسکریپت ۳۰ (Settings Page) را اجرا کنید.")
        return 1

    # پیش‌چک: SkeletonBlock باید موجود باشد (از زیرگام ۸.۳)
    skeleton = FRONTEND / "components" / "common" / "SkeletonBlock.jsx"
    if not skeleton.exists():
        print("[ERROR] SkeletonBlock.jsx یافت نشد.")
        print("        ابتدا اسکریپت ۲۹ را اجرا کنید.")
        return 1

    print("--- فایل‌های جدید ---")
    write_if_changed(NUMBER_FORMAT,    NUMBER_FORMAT_JS,    "formatNumber + parseFormattedNumber")
    write_if_changed(DATE_FORMAT,      DATE_FORMAT_JS,      "formatDate + CALENDARS")
    write_if_changed(PREFS_STORE,      PREFS_STORE_JS,      "preferencesStore (calendar)")
    write_if_changed(CALENDAR_TOGGLE,  CALENDAR_TOGGLE_JSX, "CalendarToggle")

    print()
    print("--- فایل‌های به‌روزرسانی ---")
    write_if_changed(SETTINGS_PAGE, SETTINGS_PAGE_JSX, "بخش زبان و تقویم + reset گسترش")
    write_if_changed(CHART_PAGE,    CHART_PAGE_JSX,    "formatNumber + localization")

    print()
    print("=" * 64)
    print("✅ زیرگام ۸.۵ اعمال شد.")
    print("=" * 64)
    print()
    print("🎉 با این کار، **زیرگام ۸ کامل** و **فاز ۰ به ۱۰۰٪** می‌رسد!")
    print()
    print("گام بعدی:")
    print("  🟩 tab «2 scripts»:  python scripts/31b_test_numeric_calendar.py")
    print()
    print("سپس چک بصری در 🟧 tab «3 frontend»:")
    print("  ۱) /chart/1 → متادیتا '1,714 از 1,714 کندل' (با کاما)")
    print("  ۲) hover روی نمودار → tooltip تاریخ به فرمت میلادی")
    print("  ۳) /settings → بخش جدید 'زبان و تقویم'")
    print("  ۴) کلیک 'شمسی' → preview آنی به شمسی + Toast نیست (صرفاً سوییچ)")
    print("  ۵) /chart/1 → tooltip تاریخ به شمسی (۱۴۰۲/۱۰/۲۵)")
    print("  ۶) ریست → همه stores پاک می‌شوند (تم + فونت + تقویم)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
