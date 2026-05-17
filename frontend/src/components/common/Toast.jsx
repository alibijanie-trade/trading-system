import useToastStore from "../../stores/toastStore.js";

const TYPE_CONFIG = {
  success: { icon: "✓", color: "var(--color-success)" },
  error:   { icon: "✕", color: "var(--color-danger)" },
  warning: { icon: "⚠", color: "var(--color-warning)" },
  info:    { icon: "ℹ", color: "var(--color-info)" },
};

export default function Toast({ id, type, message }) {
  const dismiss = useToastStore((s) => s.dismiss);
  const cfg = TYPE_CONFIG[type] || TYPE_CONFIG.info;

  return (
    <div
      role="alert"
      style={{
        display: "flex",
        alignItems: "flex-start",
        gap: 10,
        minWidth: 280,
        maxWidth: 420,
        padding: "12px 16px",
        background: "var(--color-card)",
        border: "1px solid var(--color-border)",
        borderInlineStart: `3px solid ${cfg.color}`,
        borderRadius: 4,
        boxShadow: "var(--shadow-card)",
        animation: "toast-slide-in 0.2s ease-out",
      }}
    >
      <span
        aria-hidden="true"
        style={{
          color: cfg.color,
          fontSize: "1.14rem",
          lineHeight: 1.2,
          marginTop: 1,
          fontWeight: 700,
        }}
      >
        {cfg.icon}
      </span>
      <span
        style={{
          flex: 1,
          color: "var(--color-text)",
          fontSize: "0.93rem",
          lineHeight: 1.5,
        }}
      >
        {message}
      </span>
      <button
        onClick={() => dismiss(id)}
        aria-label="بستن"
        style={{
          color: "var(--color-text-muted)",
          fontSize: "1.29rem",
          lineHeight: 1,
          padding: 0,
          marginRight: -4,
          marginTop: -2,
        }}
      >
        ×
      </button>
    </div>
  );
}
