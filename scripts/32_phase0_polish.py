# -*- coding: utf-8 -*-
"""
اسکریپت ۳۲ — رفع ۳ Bug + افزودن انتخاب فرمت میلادی
================================================================
این اسکریپت idempotent است — قابل اجرا چندبار بدون شکست.

محتوای این اصلاحیه:

  Bug #47: Font Size scale نمی‌شد
  ─────────────────────────────────
  مشکل: body در index.css با var(--font-size-base) ست بود، ولی همه
  inline styles فایل‌های .jsx مقادیر px ثابت (مثلاً fontSize: 13)
  داشتند که body را override می‌کردند.
  راه‌حل:
    - index.css: html { font-size: var(--font-size-base); }
    - تبدیل همه inline `fontSize: <N>` به `fontSize: '<N/14>rem'`
      در ۹ فایل (LoginPage, HomePage, ChartPage, SettingsPage,
      Toast, ConfirmDialog, ThemeCard, FontSizeControl, CalendarToggle)

  Bug #48: tooltip تاریخ روی نمودار نشان داده نمی‌شد
  ─────────────────────────────────
  مشکل: lightweight-charts v4.x در localization.dateFormat فقط
  string قبول می‌کند، نه function. تابع silently ignore می‌شد.
  راه‌حل: استفاده از timeFormatter (که برای function طراحی شده).

  Bug #49: HomePage عدد '1714 کندل' را با کاما نشان نمی‌داد
  ─────────────────────────────────
  مشکل: 1714 hardcoded در JSX بود.
  راه‌حل: import formatNumber + {formatNumber(1714)} کندل.

  Feature: انتخاب فرمت تاریخ میلادی
  ─────────────────────────────────
  افزودن گزینه‌های فرمت میلادی:
    - iso       (2024-01-15)
    - us-short  (01/15/2024)
    - eu-short  (15/01/2024)
    - long      (January 15, 2024)

  ذخیره در preferencesStore.gregorianFormat
  UI در CalendarToggle (یک select زیر دکمه‌های radio)

فایل‌های به‌روزرسانی:
  ۱) frontend/src/index.css                              (html font-size)
  ۲) frontend/src/utils/dateFormat.js                    (افزودن format)
  ۳) frontend/src/stores/preferencesStore.js             (gregorianFormat)
  ۴) frontend/src/components/settings/CalendarToggle.jsx (محتوای جدید)
  ۵) frontend/src/pages/SettingsPage.jsx                 (passing format)
  ۶) frontend/src/pages/HomePage.jsx                     (formatNumber + rem)
  ۷) frontend/src/pages/ChartPage.jsx                    (timeFormatter + rem)
  ۸) frontend/src/pages/LoginPage.jsx                    (regex: px → rem)
  ۹) frontend/src/components/common/Toast.jsx            (regex: px → rem)
  ۱۰) frontend/src/components/common/ConfirmDialog.jsx   (regex: px → rem)
  ۱۱) frontend/src/components/settings/ThemeCard.jsx     (regex: px → rem)
  ۱۲) frontend/src/components/settings/FontSizeControl.jsx (regex: px → rem)
================================================================
"""

import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
FRONTEND = PROJECT_ROOT / "frontend" / "src"

# فایل‌های با محتوای کامل جدید
INDEX_CSS = FRONTEND / "index.css"
DATE_FORMAT = FRONTEND / "utils" / "dateFormat.js"
PREFS_STORE = FRONTEND / "stores" / "preferencesStore.js"
CALENDAR_TOGGLE = FRONTEND / "components" / "settings" / "CalendarToggle.jsx"
SETTINGS_PAGE = FRONTEND / "pages" / "SettingsPage.jsx"
HOME_JSX = FRONTEND / "pages" / "HomePage.jsx"
CHART_JSX = FRONTEND / "pages" / "ChartPage.jsx"

# فایل‌های با regex transform (font px → rem)
REGEX_TARGETS = [
    FRONTEND / "pages" / "LoginPage.jsx",
    FRONTEND / "components" / "common" / "Toast.jsx",
    FRONTEND / "components" / "common" / "ConfirmDialog.jsx",
    FRONTEND / "components" / "settings" / "ThemeCard.jsx",
    FRONTEND / "components" / "settings" / "FontSizeControl.jsx",
]


# ============================================================
# جدول تبدیل px → rem (baseline = 14px)
# ============================================================
FONT_REM_MAP = {
    10: "0.71rem",
    11: "0.79rem",
    12: "0.86rem",
    13: "0.93rem",
    14: "1rem",
    15: "1.07rem",
    16: "1.14rem",
    17: "1.21rem",
    18: "1.29rem",
    20: "1.43rem",
    22: "1.57rem",
    24: "1.71rem",
}

# Pattern: `fontSize:\s*N` که N بعدش یک علامت غیر-عددی/غیر-نقطه‌ای می‌آید
# جلوگیری از match در: fontSize: 13.5 یا fontSize: 13px یا fontSize: 13rem
FONT_PX_PATTERN = re.compile(r"(fontSize:\s*)(\d+)(?=\s*[,\}\)\s])")


def px_to_rem(n: int) -> str:
    if n in FONT_REM_MAP:
        return FONT_REM_MAP[n]
    # محاسبه دینامیک برای اعداد غیر-استاندارد
    val = round(n / 14, 2)
    if val == int(val):
        return f"{int(val)}rem"
    return f"{val}rem"


def transform_font_px_to_rem(src: str) -> tuple:
    """تبدیل inline fontSize: N → fontSize: 'X.XXrem'"""
    count = [0]

    def replacer(match):
        prefix, num_str = match.group(1), match.group(2)
        n = int(num_str)
        rem = px_to_rem(n)
        count[0] += 1
        return f'{prefix}"{rem}"'

    new_src = FONT_PX_PATTERN.sub(replacer, src)
    return (new_src, count[0])


# ============================================================
# محتواهای کامل فایل‌های جدید
# ============================================================

INDEX_CSS_NEW = """/* ============================================================
   Reset + پایه — زیرگام ۸ (Theme Engine)
   متغیرهای CSS توسط ThemeProvider روی :root تزریق می‌شوند.
   ۲۷c — رنگ‌های fallback بایننس واقعی
   ۲۷e — interactive states
   ۲۸  — Toast animations
   ۲۹  — Skeleton + Dialog
   🆕 ۳۲ — html font-size scaling (Bug #47)
   ============================================================ */

:root {
  --color-primary: #F0B90B;
  --color-primary-hover: #FCD535;
  --color-bg: #181A20;
  --color-bg-elevated: #1E2329;
  --color-card: #1E2329;
  --color-card-hover: #2B2F36;
  --color-border: #2B3139;
  --color-border-strong: #474D57;
  --color-text: #EAECEF;
  --color-text-muted: #848E9C;
  --color-text-inverse: #181A20;
  --color-success: #0ECB81;
  --color-success-bg: #0F2A1F;
  --color-danger: #F6465D;
  --color-danger-bg: #2A1517;
  --color-info: #1890FF;
  --color-warning: #F0B90B;
  --color-link: #F0B90B;
  --color-grid: #2B3139;
  --shadow-card: 0 4px 12px rgba(0,0,0,0.5);

  --font-size-base: 14px;
  --font-family-ui: "Vazirmatn", "Segoe UI", system-ui, -apple-system, sans-serif;
}

*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* 🆕 ۳۲ — html font-size = baseline برای rem scaling سراسری.
   ThemeProvider مقدار را با fontSize انتخابی کاربر به‌روز می‌کند.
   همه inline styles از rem استفاده می‌کنند، پس همه‌جا scale می‌شود. */
html {
  font-size: var(--font-size-base);
}

html, body, #root {
  min-height: 100vh;
}

body {
  font-family: var(--font-family-ui);
  font-size: 1rem;
  line-height: 1.6;
  background: var(--color-bg);
  color: var(--color-text);
  direction: rtl;
  transition: background-color 0.2s ease, color 0.2s ease;
}

/* ============================================================
   Interactive states (۲۷e)
   ============================================================ */

button {
  cursor: pointer;
  font-family: inherit;
  font-size: inherit;
  border: none;
  outline: none;
  background: transparent;
  color: inherit;
  transition: filter 0.15s ease, transform 0.05s ease, background 0.15s ease, border-color 0.15s ease;
}

button:hover:not(:disabled) { filter: brightness(1.12); }
button:active:not(:disabled) { transform: translateY(1px); filter: brightness(0.95); }
button:focus-visible { outline: 2px solid var(--color-primary); outline-offset: 2px; }
button:disabled { cursor: not-allowed; opacity: 0.5; filter: none; }

a {
  color: var(--color-link);
  text-decoration: none;
  transition: opacity 0.15s ease;
}

a:hover { text-decoration: underline; opacity: 0.85; }

input, select, textarea {
  font-family: inherit;
  font-size: inherit;
  outline: none;
  background: transparent;
  color: inherit;
  transition: border-color 0.15s ease, background 0.15s ease;
}

select { cursor: pointer; }
select:hover { border-color: var(--color-border-strong) !important; background: var(--color-card-hover) !important; }
select:focus { border-color: var(--color-primary) !important; outline: none; }
input:focus, textarea:focus { border-color: var(--color-primary) !important; outline: none; }

[data-card-link="true"] {
  display: block;
  transition: background 0.15s ease, border-color 0.15s ease, transform 0.15s ease;
  cursor: pointer;
}

[data-card-link="true"]:hover {
  background: var(--color-card-hover) !important;
  border-color: var(--color-border-strong) !important;
  text-decoration: none !important;
  opacity: 1;
}

/* ============================================================
   Toast animations (۲۸)
   ============================================================ */

@keyframes toast-slide-in {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ============================================================
   Skeleton + Dialog animations (۲۹)
   ============================================================ */

.skeleton-block {
  display: block;
  background: linear-gradient(
    90deg,
    var(--color-card-hover) 0%,
    var(--color-border-strong) 50%,
    var(--color-card-hover) 100%
  );
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.4s ease-in-out infinite;
  border-radius: 4px;
}

@keyframes skeleton-shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

@keyframes dialog-fade-in {
  from { opacity: 0; }
  to   { opacity: 1; }
}

@keyframes dialog-slide-in {
  from { opacity: 0; transform: translateY(-8px) scale(0.98); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}

@media (prefers-reduced-motion: reduce) {
  .skeleton-block {
    animation: none;
    background: var(--color-card-hover);
  }
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* ============================================================
   اسکرول‌بار سفارشی
   ============================================================ */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: var(--color-bg); }
::-webkit-scrollbar-thumb {
  background: var(--color-border-strong);
  border-radius: 5px;
  transition: background 0.15s ease;
}
::-webkit-scrollbar-thumb:hover { background: var(--color-text-muted); }
"""


DATE_FORMAT_NEW = """/**
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
"""


PREFS_STORE_NEW = """/* ============================================================
   Zustand store برای ترجیحات کاربر (calendar + gregorianFormat + ...)
   نسخه ۳۲ — افزودن gregorianFormat
   persist در localStorage با کلید "preferences-storage"
   ============================================================ */
import { create } from "zustand";
import { persist } from "zustand/middleware";
import {
  CALENDARS,
  DEFAULT_GREGORIAN_FORMAT,
  isValidGregorianFormat,
} from "../utils/dateFormat.js";

export const DEFAULT_CALENDAR = CALENDARS.GREGORIAN;

const usePreferencesStore = create(
  persist(
    (set) => ({
      calendar: DEFAULT_CALENDAR,
      gregorianFormat: DEFAULT_GREGORIAN_FORMAT,

      setCalendar: (calendar) => set({ calendar }),

      setGregorianFormat: (fmt) => {
        if (isValidGregorianFormat(fmt)) set({ gregorianFormat: fmt });
      },

      reset: () =>
        set({
          calendar: DEFAULT_CALENDAR,
          gregorianFormat: DEFAULT_GREGORIAN_FORMAT,
        }),
    }),
    {
      name: "preferences-storage",
      version: 2, // bump به‌خاطر افزودن gregorianFormat
      migrate: (state, fromVersion) => {
        // افزودن gregorianFormat برای کاربرانی که از v1 ارتقا می‌دهند
        if (fromVersion < 2 && state && !state.gregorianFormat) {
          state.gregorianFormat = DEFAULT_GREGORIAN_FORMAT;
        }
        return state;
      },
    }
  )
);

export default usePreferencesStore;
"""


CALENDAR_TOGGLE_NEW = """import {
  formatDate,
  CALENDARS,
  CALENDAR_LABELS,
  GREGORIAN_FORMATS,
  GREGORIAN_FORMAT_LABELS,
} from "../../utils/dateFormat.js";

/**
 * CalendarToggle — انتخاب تقویم میلادی/شمسی + فرمت میلادی + preview
 *
 * Props:
 *   value:           "gregorian" | "jalali"
 *   onChange:        (calendar) => void
 *   format:          "iso" | "us-short" | "eu-short" | "long"
 *   onFormatChange:  (format) => void
 *
 * نسخه ۳۲ — افزودن select فرمت میلادی (فقط هنگام انتخاب gregorian).
 */

const OPTIONS = [
  { value: CALENDARS.GREGORIAN, label: CALENDAR_LABELS.gregorian },
  { value: CALENDARS.JALALI,    label: CALENDAR_LABELS.jalali    },
];

export default function CalendarToggle({ value, onChange, format, onFormatChange }) {
  const isGregorian = value === CALENDARS.GREGORIAN;

  return (
    <div>
      {/* radiogroup: انتخاب نوع تقویم */}
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
                fontSize: "0.93rem",
                fontWeight: isActive ? 600 : 500,
              }}
            >
              {opt.label}
            </button>
          );
        })}
      </div>

      {/* انتخاب فرمت میلادی — فقط هنگام gregorian */}
      {isGregorian && (
        <div style={{ marginTop: 14 }}>
          <label
            htmlFor="gregorian-format-select"
            style={{
              display: "block",
              marginBottom: 6,
              fontSize: "0.86rem",
              color: "var(--color-text-muted)",
            }}
          >
            فرمت تاریخ میلادی:
          </label>
          <select
            id="gregorian-format-select"
            value={format}
            onChange={(e) => onFormatChange(e.target.value)}
            style={{
              width: "100%",
              padding: "10px 12px",
              background: "var(--color-card)",
              color: "var(--color-text)",
              border: "1px solid var(--color-border)",
              borderRadius: 4,
              fontSize: "0.93rem",
            }}
          >
            {GREGORIAN_FORMATS.map((f) => (
              <option key={f} value={f}>
                {GREGORIAN_FORMAT_LABELS[f]}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* preview تاریخ امروز */}
      <div
        style={{
          marginTop: 14,
          padding: "14px 16px",
          background: "var(--color-bg-elevated)",
          border: "1px solid var(--color-border)",
          borderRadius: 4,
          color: "var(--color-text)",
          fontSize: "1rem",
          lineHeight: 1.7,
        }}
      >
        <div style={{ color: "var(--color-text-muted)", fontSize: "0.86rem", marginBottom: 4 }}>
          نمونه — تاریخ امروز:
        </div>
        <div style={{ fontWeight: 600 }}>
          {formatDate(new Date(), value, { format })}
        </div>
        <div style={{ color: "var(--color-text-muted)", fontSize: "0.86rem", marginTop: 6 }}>
          همراه ساعت: {formatDate(new Date(), value, { format, withTime: true })}
        </div>
      </div>
    </div>
  );
}
"""


SETTINGS_PAGE_NEW = """import { Link } from "react-router-dom";
import useThemeStore from "../stores/themeStore.js";
import useConfirmStore from "../stores/confirmStore.js";
import useToastStore from "../stores/toastStore.js";
import usePreferencesStore from "../stores/preferencesStore.js";
import { listThemes } from "../themes/themes.js";
import ThemeCard from "../components/settings/ThemeCard.jsx";
import FontSizeControl from "../components/settings/FontSizeControl.jsx";
import CalendarToggle from "../components/settings/CalendarToggle.jsx";

export default function SettingsPage() {
  const themeId = useThemeStore((s) => s.themeId);
  const setTheme = useThemeStore((s) => s.setTheme);
  const fontSize = useThemeStore((s) => s.fontSize);
  const setFontSize = useThemeStore((s) => s.setFontSize);
  const resetTheme = useThemeStore((s) => s.resetAll);

  const calendar = usePreferencesStore((s) => s.calendar);
  const setCalendar = usePreferencesStore((s) => s.setCalendar);
  const gregorianFormat = usePreferencesStore((s) => s.gregorianFormat);
  const setGregorianFormat = usePreferencesStore((s) => s.setGregorianFormat);
  const resetPreferences = usePreferencesStore((s) => s.reset);

  const askConfirm = useConfirmStore((s) => s.confirm);
  const toastSuccess = useToastStore((s) => s.success);

  const themes = listThemes();

  const handleReset = async () => {
    const ok = await askConfirm({
      title: "بازگشت به تنظیمات پیش‌فرض",
      message:
        "همه تنظیمات (تم، اندازه فونت، تقویم، فرمت تاریخ و رنگ‌های سفارشی) به حالت پیش‌فرض بازمی‌گردند. آیا مطمئن هستید؟",
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
        <h1 style={{ fontSize: "1.57rem", fontWeight: 600, color: "var(--color-text)" }}>
          ⚙️ تنظیمات
        </h1>
        <p style={{ marginTop: 4, fontSize: "0.93rem", color: "var(--color-text-muted)" }}>
          تم، اندازه فونت، تقویم و سایر تنظیمات ظاهری برنامه
        </p>
      </header>

      <section style={{ marginBottom: 36 }}>
        <SectionHeader title="ظاهر و تم" description="یک تم را برای ظاهر کلی برنامه انتخاب کنید" />
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

      <section style={{ marginBottom: 36 }}>
        <SectionHeader title="اندازه فونت" description="اندازه متن سراسری برنامه — همه‌جا اعمال می‌شود" />
        <FontSizeControl value={fontSize} onChange={setFontSize} />
      </section>

      <section style={{ marginBottom: 36 }}>
        <SectionHeader
          title="زبان و تقویم"
          description="نوع تقویم و فرمت تاریخ برای نمایش در نمودارها و گزارش‌ها"
        />
        <CalendarToggle
          value={calendar}
          onChange={setCalendar}
          format={gregorianFormat}
          onFormatChange={setGregorianFormat}
        />
      </section>

      <section style={{ paddingTop: 20, borderTop: "1px solid var(--color-border)" }}>
        <SectionHeader title="بازنشانی" description="تمام تنظیمات را به حالت پیش‌فرض برگردانید" />
        <button
          type="button"
          onClick={handleReset}
          style={{
            padding: "10px 18px",
            background: "var(--color-card)",
            color: "var(--color-warning)",
            border: "1px solid var(--color-warning)",
            borderRadius: 4,
            fontSize: "0.93rem",
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
      <h2 style={{ fontSize: "1.07rem", fontWeight: 600, color: "var(--color-text)", marginBottom: 4 }}>
        {title}
      </h2>
      <p style={{ fontSize: "0.86rem", color: "var(--color-text-muted)" }}>
        {description}
      </p>
    </div>
  );
}
"""


HOME_JSX_NEW = """import { useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api.js";
import useAuthStore from "../stores/authStore.js";
import useConfirmStore from "../stores/confirmStore.js";
import { formatNumber } from "../utils/numberFormat.js";

export default function HomePage() {
  const navigate = useNavigate();
  const user = useAuthStore((s) => s.user);
  const setUser = useAuthStore((s) => s.setUser);
  const logout = useAuthStore((s) => s.logout);

  const askConfirm = useConfirmStore((s) => s.confirm);

  useEffect(() => {
    if (!user) {
      api
        .get("/auth/me")
        .then((resp) => setUser(resp.data.data))
        .catch(() => {});
    }
  }, [user, setUser]);

  const handleLogout = async () => {
    const ok = await askConfirm({
      title: "خروج از حساب",
      message: "آیا مطمئن هستید که می‌خواهید خارج شوید؟",
      variant: "warning",
      confirmText: "خروج",
      cancelText: "انصراف",
    });
    if (!ok) return;
    logout();
    navigate("/login", { replace: true });
  };

  return (
    <div style={{ padding: 24, maxWidth: 900, margin: "0 auto" }}>
      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 32,
          paddingBottom: 16,
          borderBottom: "1px solid var(--color-border)",
        }}
      >
        <div>
          <h1 style={{ fontSize: "1.57rem", marginBottom: 4, fontWeight: 600 }}>
            سامانه هوشمند ترید
          </h1>
          {user ? (
            <div style={{ fontSize: "0.93rem", color: "var(--color-text-muted)" }}>
              کاربر:{" "}
              <strong style={{ color: "var(--color-text)" }}>
                {user.username}
              </strong>
              {" — "}نقش: {user.role}
            </div>
          ) : (
            <div style={{ fontSize: "0.93rem", color: "var(--color-text-muted)" }}>
              در حال بارگذاری...
            </div>
          )}
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <Link
            to="/settings"
            title="تنظیمات"
            aria-label="تنظیمات"
            style={{
              display: "inline-flex",
              alignItems: "center",
              justifyContent: "center",
              width: 38,
              height: 38,
              background: "var(--color-card)",
              color: "var(--color-text)",
              borderRadius: 4,
              border: "1px solid var(--color-border)",
              fontSize: "1.29rem",
              textDecoration: "none",
            }}
          >
            ⚙️
          </Link>

          <button
            onClick={handleLogout}
            style={{
              background: "var(--color-card)",
              color: "var(--color-text)",
              padding: "8px 16px",
              borderRadius: 4,
              border: "1px solid var(--color-border)",
              fontSize: "0.93rem",
              fontWeight: 500,
            }}
          >
            خروج
          </button>
        </div>
      </header>

      <section>
        <h2
          style={{
            fontSize: "1rem",
            marginBottom: 12,
            color: "var(--color-text-muted)",
            fontWeight: 500,
            textTransform: "uppercase",
            letterSpacing: "0.5px",
          }}
        >
          نمودارها
        </h2>
        <ul style={{ listStyle: "none" }}>
          <li>
            <Link
              to="/chart/1"
              data-card-link="true"
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                padding: "14px 16px",
                background: "var(--color-card)",
                borderRadius: 4,
                border: "1px solid var(--color-border)",
                fontSize: "1.07rem",
                color: "var(--color-link)",
                fontWeight: 500,
              }}
            >
              <span>📊 BTC/USDT — روزانه</span>
              <span
                style={{
                  color: "var(--color-text-muted)",
                  fontSize: "0.86rem",
                  fontWeight: 400,
                }}
              >
                {formatNumber(1714)} کندل
              </span>
            </Link>
          </li>
        </ul>
      </section>
    </div>
  );
}
"""


CHART_JSX_NEW = """import { useEffect, useRef, useState } from "react";
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

function isoToUnix(isoStr) {
  const withZ = isoStr.endsWith("Z") ? isoStr : isoStr + "Z";
  return Math.floor(new Date(withZ).getTime() / 1000);
}

function readVar(name, fallback = "") {
  if (typeof window === "undefined") return fallback;
  const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return v || fallback;
}

export default function ChartPage() {
  const { symbolId } = useParams();
  const chartContainerRef = useRef(null);
  const chartRef = useRef(null);

  const themeId = useThemeStore((s) => s.themeId);
  const calendar = usePreferencesStore((s) => s.calendar);
  const gregorianFormat = usePreferencesStore((s) => s.gregorianFormat);

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
          // 🆕 Bug #48 fix — timeFormatter به جای dateFormat (lightweight-charts v4.x API):
          //   dateFormat فقط string قبول می‌کند، timeFormatter تابع است.
          localization: {
            locale: "en-US",
            timeFormatter: (time) => {
              const d = typeof time === "number"
                ? new Date(time * 1000)
                : new Date(time);
              return formatDate(d, calendar, { format: gregorianFormat });
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
  }, [symbolId, timeframe, themeId, calendar, gregorianFormat]);

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
        <h1 style={{ fontSize: "1.57rem" }}>BTC/USDT</h1>
        <select
          value={timeframe}
          onChange={(e) => setTimeframe(e.target.value)}
          style={{
            background: "var(--color-card)",
            color: "var(--color-text)",
            padding: "8px 12px",
            borderRadius: 4,
            border: "1px solid var(--color-border)",
            fontSize: "1rem",
          }}
        >
          {TIMEFRAMES.map((tf) => (
            <option key={tf.value} value={tf.value}>
              {tf.label}
            </option>
          ))}
        </select>
      </header>

      {loading ? (
        <div style={{ marginBottom: 12 }}>
          <SkeletonBlock variant="text" width={220} height={13} />
        </div>
      ) : meta.count > 0 && !error ? (
        <div
          style={{
            fontSize: "0.93rem",
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
            fontSize: "1rem",
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


def apply_font_rem_transform(path: Path) -> str:
    """فقط regex transform px → rem روی فایل موجود."""
    rel = path.relative_to(PROJECT_ROOT)
    if not path.exists():
        print(f"  ⚠️  یافت نشد: {rel}  (skip)")
        return "skipped"

    src = path.read_text(encoding="utf-8")
    new_src, n = transform_font_px_to_rem(src)

    if n == 0:
        print(f"  - بدون تغییر: {rel}  (هیچ fontSize: <N> یافت نشد)")
        return "unchanged"

    if src == new_src:
        # نظری نباید اتفاق بیفتد ولی برای ایمنی
        print(f"  - بدون تغییر: {rel}  (idempotent — همه قبلاً rem بودند)")
        return "unchanged"

    path.write_text(new_src, encoding="utf-8", newline="\n")
    print(f"  ✓ به‌روز:   {rel}  ({n} تبدیل px → rem)")
    return "updated"


# ============================================================
# اجرای اصلی
# ============================================================


def main() -> int:
    print("=" * 64)
    print("اسکریپت ۳۲ — رفع ۳ Bug + افزودن انتخاب فرمت میلادی")
    print("=" * 64)
    print()

    if not FRONTEND.exists():
        print("[ERROR] دایرکتوری frontend/src یافت نشد.")
        return 1

    print("--- فایل‌های با محتوای کامل جدید ---")
    write_if_changed(INDEX_CSS, INDEX_CSS_NEW, "html font-size scaling")
    write_if_changed(DATE_FORMAT, DATE_FORMAT_NEW, "افزودن GREGORIAN_FORMATS")
    write_if_changed(PREFS_STORE, PREFS_STORE_NEW, "افزودن gregorianFormat (v2)")
    write_if_changed(CALENDAR_TOGGLE, CALENDAR_TOGGLE_NEW, "select فرمت میلادی")
    write_if_changed(SETTINGS_PAGE, SETTINGS_PAGE_NEW, "passing format به CalendarToggle")
    write_if_changed(HOME_JSX, HOME_JSX_NEW, "formatNumber + rem")
    write_if_changed(CHART_JSX, CHART_JSX_NEW, "timeFormatter + rem")

    print()
    print("--- فایل‌های با regex transform (px → rem) ---")
    for path in REGEX_TARGETS:
        apply_font_rem_transform(path)

    print()
    print("=" * 64)
    print("✅ اصلاحیه ۳۲ اعمال شد.")
    print("=" * 64)
    print()
    print("Bug Fix ها:")
    print("  ✓ Bug #47 — Font Size scaling (همه inline px → rem + html font-size)")
    print("  ✓ Bug #48 — tooltip تاریخ نمودار (timeFormatter به جای dateFormat)")
    print("  ✓ Bug #49 — HomePage 1714 با کاما")
    print()
    print("Feature:")
    print("  ✓ انتخاب فرمت میلادی (iso/us-short/eu-short/long)")
    print()
    print("گام بعدی:")
    print("  🟩 tab «2 scripts»:  python scripts/32b_test_fixes.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
