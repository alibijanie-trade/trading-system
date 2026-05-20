/**
 * SkeletonBlock — placeholder متحرک برای حالات بارگذاری
 * طبق سند ۸.۳ (Skeleton Screen برای loading states)
 *
 * Props:
 *   variant: "rect" | "text" | "circle" | "line"  (default: "rect")
 *   width:   string | number  (default: depends on variant)
 *   height:  string | number  (default: depends on variant)
 *   radius:  string | number  (default: depends on variant)
 *   count:   number           (default: 1) — برای variant های text/line
 *   gap:     number           (default: 8) — فاصله بین آیتم‌ها
 *   style:   object           — استایل اضافی
 *
 * رنگ از CSS variables تم — هیچ hex hardcoded:
 *   --color-card-hover   (پایه)
 *   --color-border-strong (موج shimmer)
 *
 * Accessibility:
 *   aria-hidden="true" + role="presentation"
 *   prefers-reduced-motion — animation غیرفعال می‌شود (در index.css)
 */
export default function SkeletonBlock({
  variant = "rect",
  width,
  height,
  radius,
  count = 1,
  gap = 8,
  style = {},
}) {
  const defaults = VARIANT_DEFAULTS[variant] || VARIANT_DEFAULTS.rect;

  const finalWidth = width ?? defaults.width;
  const finalHeight = height ?? defaults.height;
  const finalRadius = radius ?? defaults.radius;

  const toUnit = (v) => (typeof v === "number" ? `${v}px` : v);

  const items = Array.from({ length: Math.max(1, count) }, (_, i) => (
    <div
      key={i}
      className="skeleton-block"
      role="presentation"
      aria-hidden="true"
      style={{
        width: toUnit(finalWidth),
        height: toUnit(finalHeight),
        borderRadius: toUnit(finalRadius),
        marginBottom: count > 1 && i < count - 1 ? gap : 0,
        ...style,
      }}
    />
  ));

  return count > 1 ? <>{items}</> : items[0];
}

const VARIANT_DEFAULTS = {
  rect:   { width: "100%", height: 16, radius: 4 },
  text:   { width: "100%", height: 12, radius: 4 },
  circle: { width: 40,     height: 40, radius: "50%" },
  line:   { width: "100%", height: 1,  radius: 0 },
};
