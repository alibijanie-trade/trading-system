/**
 * ThemeCard — کارت انتخاب تم با پیش‌نمایش رنگ‌ها
 *
 * Props:
 *   theme:    object { id, name, isDark, vars }
 *   isActive: boolean
 *   onClick:  () => void
 *
 * نکته معماری:
 *   رنگ‌های preview از خود theme.vars خوانده می‌شوند، نه از :root.
 *   دلیل: می‌خواهیم رنگ‌های تم‌های دیگر را نشان دهیم نه تم فعال.
 *   این تنها استثنای قانون "بدون hex hardcoded" است و قاعده‌مند است
 *   (مقادیر از theme object می‌آیند، نه hardcoded).
 *
 * بقیه عناصر کارت (متن، border، badge):
 *   - بدنه کارت از تم فعلی: var(--color-card)
 *   - متن از تم فعلی: var(--color-text)
 *   - border فعال: var(--color-primary)
 */
export default function ThemeCard({ theme, isActive, onClick }) {
  const v = theme.vars;

  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={isActive}
      style={{
        position: "relative",
        background: "var(--color-card)",
        border: isActive
          ? "2px solid var(--color-primary)"
          : "1px solid var(--color-border)",
        borderRadius: 8,
        padding: 14,
        textAlign: "start",
        cursor: "pointer",
        overflow: "hidden",
        width: "100%",
      }}
    >
      {/* پیش‌نمایش رنگ‌ها — از theme.vars خود تم */}
      <div
        style={{
          display: "flex",
          gap: 6,
          marginBottom: 12,
          height: 36,
        }}
      >
        <div
          aria-hidden="true"
          title="bg"
          style={{
            flex: 1,
            background: v["--color-bg"],
            borderRadius: 4,
            border: `1px solid ${v["--color-border"]}`,
          }}
        />
        <div
          aria-hidden="true"
          title="card"
          style={{
            flex: 1,
            background: v["--color-card"],
            borderRadius: 4,
            border: `1px solid ${v["--color-border"]}`,
          }}
        />
        <div
          aria-hidden="true"
          title="primary"
          style={{
            width: 36,
            background: v["--color-primary"],
            borderRadius: 4,
          }}
        />
        <div
          aria-hidden="true"
          title="success"
          style={{
            width: 36,
            background: v["--color-success"],
            borderRadius: 4,
          }}
        />
        <div
          aria-hidden="true"
          title="danger"
          style={{
            width: 36,
            background: v["--color-danger"],
            borderRadius: 4,
          }}
        />
      </div>

      {/* نام تم + badge فعال */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          gap: 8,
        }}
      >
        <span
          style={{
            fontSize: "1rem",
            fontWeight: 600,
            color: "var(--color-text)",
          }}
        >
          {theme.name}
        </span>
        {isActive && (
          <span
            style={{
              fontSize: "0.79rem",
              padding: "3px 10px",
              background: "var(--color-primary)",
              color: "var(--color-text-inverse)",
              borderRadius: 12,
              fontWeight: 600,
              whiteSpace: "nowrap",
            }}
          >
            ✓ فعال
          </span>
        )}
      </div>
    </button>
  );
}
