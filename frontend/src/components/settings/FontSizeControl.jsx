/**
 * FontSizeControl — کنترل اندازه فونت با ۴ preset + preview زنده
 *
 * Props:
 *   value:    number (پیکسل فعلی)
 *   onChange: (px) => void
 *
 * Presets: 12 / 14 / 16 / 18 px
 * preview: متن نمونه که با تغییر value تغییر اندازه می‌دهد
 */
const PRESETS = [
  { label: "کوچک",     value: 12 },
  { label: "متوسط",    value: 14 },
  { label: "بزرگ",     value: 16 },
  { label: "خیلی بزرگ", value: 18 },
];

export default function FontSizeControl({ value, onChange }) {
  return (
    <div>
      {/* دکمه‌های preset */}
      <div
        role="radiogroup"
        aria-label="اندازه فونت"
        style={{ display: "flex", gap: 8, flexWrap: "wrap" }}
      >
        {PRESETS.map((p) => {
          const isActive = value === p.value;
          return (
            <button
              key={p.value}
              type="button"
              role="radio"
              aria-checked={isActive}
              onClick={() => onChange(p.value)}
              style={{
                flex: "1 1 110px",
                padding: "10px 12px",
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
              {p.label} ({p.value}px)
            </button>
          );
        })}
      </div>

      {/* preview زنده */}
      <div
        style={{
          marginTop: 14,
          padding: "14px 16px",
          background: "var(--color-bg-elevated)",
          border: "1px solid var(--color-border)",
          borderRadius: 4,
          color: "var(--color-text)",
          fontSize: `${value}px`,
          lineHeight: 1.6,
        }}
      >
        نمونه متن: قیمت BTC/USDT برابر است با ۱۰۲٬۳۴۵ دلار آمریکا.
      </div>
    </div>
  );
}
