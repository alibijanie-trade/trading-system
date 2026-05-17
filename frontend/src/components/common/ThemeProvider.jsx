/* ============================================================
   ThemeProvider — متغیرهای CSS تم فعلی را روی :root اعمال می‌کند.
   هر بار themeId/fontSize/customColors تغییر کند، اعمال مجدد می‌شود.
   ============================================================ */
import { useEffect } from "react";
import useThemeStore from "../../stores/themeStore.js";
import { getTheme } from "../../themes/themes.js";

export default function ThemeProvider({ children }) {
  const themeId = useThemeStore((s) => s.themeId);
  const fontSize = useThemeStore((s) => s.fontSize);
  const customColors = useThemeStore((s) => s.customColors);

  useEffect(() => {
    const theme = getTheme(themeId);
    const root = document.documentElement;

    // اعمال متغیرهای تم
    Object.entries(theme.vars).forEach(([k, v]) => {
      root.style.setProperty(k, v);
    });

    // اعمال override های کاربر
    Object.entries(customColors).forEach(([k, v]) => {
      root.style.setProperty(k, v);
    });

    // font-size base
    root.style.setProperty("--font-size-base", `${fontSize}px`);

    // attributeهای کمکی برای styling شرطی
    root.setAttribute("data-theme", themeId);
    root.setAttribute("data-theme-mode", theme.isDark ? "dark" : "light");
    root.style.colorScheme = theme.isDark ? "dark" : "light";
  }, [themeId, fontSize, customColors]);

  return children;
}
