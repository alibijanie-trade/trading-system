import React from 'react';
import {
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
