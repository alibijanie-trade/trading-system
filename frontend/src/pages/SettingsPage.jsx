import { Link } from "react-router-dom";
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
