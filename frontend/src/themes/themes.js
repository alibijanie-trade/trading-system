/* ============================================================
   تعریف تم‌ها — هر تم یک object از CSS variables است.
   ThemeProvider مقادیر را روی :root تزریق می‌کند.
   ============================================================ */

export const THEMES = {
  "binance-dark": {
    id: "binance-dark",
    name: "بایننس تاریک",
    isDark: true,
    vars: {
      "--color-primary": "#F0B90B",
      "--color-primary-hover": "#FCD535",
      "--color-bg": "#181A20",
      "--color-bg-elevated": "#1E2329",
      "--color-card": "#1E2329",
      "--color-card-hover": "#2B2F36",
      "--color-border": "#2B3139",
      "--color-border-strong": "#474D57",
      "--color-text": "#EAECEF",
      "--color-text-muted": "#848E9C",
      "--color-text-inverse": "#181A20",
      "--color-success": "#0ECB81",
      "--color-success-bg": "#0F2A1F",
      "--color-danger": "#F6465D",
      "--color-danger-bg": "#2A1517",
      "--color-info": "#1890FF",
      "--color-warning": "#F0B90B",
      "--color-link": "#F0B90B",
      "--color-grid": "#2B3139",
      "--shadow-card": "0 4px 12px rgba(0,0,0,0.5)",
    },
  },

  "light-minimal": {
    id: "light-minimal",
    name: "روشن مینیمال",
    isDark: false,
    vars: {
      "--color-primary": "#F0B90B",
      "--color-primary-hover": "#E0A900",
      "--color-bg": "#ffffff",
      "--color-bg-elevated": "#f8f9fa",
      "--color-card": "#ffffff",
      "--color-card-hover": "#f1f3f5",
      "--color-border": "#e9ecef",
      "--color-border-strong": "#ced4da",
      "--color-text": "#212529",
      "--color-text-muted": "#6c757d",
      "--color-text-inverse": "#ffffff",
      "--color-success": "#2e7d32",
      "--color-success-bg": "#e8f5e9",
      "--color-danger": "#c62828",
      "--color-danger-bg": "#ffebee",
      "--color-info": "#1565c0",
      "--color-warning": "#ef6c00",
      "--color-link": "#1565c0",
      "--color-grid": "#eef0f2",
      "--shadow-card": "0 2px 8px rgba(0,0,0,0.06)",
    },
  },

  "dark-modern": {
    id: "dark-modern",
    name: "تاریک مدرن",
    isDark: true,
    vars: {
      "--color-primary": "#7c3aed",
      "--color-primary-hover": "#a78bfa",
      "--color-bg": "#0f0e17",
      "--color-bg-elevated": "#1a1825",
      "--color-card": "#1f1d2e",
      "--color-card-hover": "#2a2740",
      "--color-border": "#2e2c43",
      "--color-border-strong": "#3a384f",
      "--color-text": "#e0def4",
      "--color-text-muted": "#908caa",
      "--color-text-inverse": "#0f0e17",
      "--color-success": "#9ccfd8",
      "--color-success-bg": "#1a2e33",
      "--color-danger": "#eb6f92",
      "--color-danger-bg": "#3a1e2a",
      "--color-info": "#3e8fb0",
      "--color-warning": "#f6c177",
      "--color-link": "#a78bfa",
      "--color-grid": "#262338",
      "--shadow-card": "0 4px 16px rgba(0,0,0,0.4)",
    },
  },

  "pastel": {
    id: "pastel",
    name: "پاستلی",
    isDark: false,
    vars: {
      "--color-primary": "#ff8a9a",
      "--color-primary-hover": "#ff6b80",
      "--color-bg": "#fff5f5",
      "--color-bg-elevated": "#ffeaea",
      "--color-card": "#ffffff",
      "--color-card-hover": "#fff0f3",
      "--color-border": "#f5d6dc",
      "--color-border-strong": "#e8b4be",
      "--color-text": "#4a4453",
      "--color-text-muted": "#8a8294",
      "--color-text-inverse": "#ffffff",
      "--color-success": "#8fbc8f",
      "--color-success-bg": "#edf6ed",
      "--color-danger": "#cd5c5c",
      "--color-danger-bg": "#fbe8e8",
      "--color-info": "#a8c5dd",
      "--color-warning": "#ddb892",
      "--color-link": "#b56576",
      "--color-grid": "#f5e8eb",
      "--shadow-card": "0 2px 8px rgba(180,120,140,0.12)",
    },
  },

  "sky-blue": {
    id: "sky-blue",
    name: "آبی آسمانی",
    isDark: false,
    vars: {
      "--color-primary": "#0284c7",
      "--color-primary-hover": "#0369a1",
      "--color-bg": "#f0f9ff",
      "--color-bg-elevated": "#e0f2fe",
      "--color-card": "#ffffff",
      "--color-card-hover": "#f0f9ff",
      "--color-border": "#bae6fd",
      "--color-border-strong": "#7dd3fc",
      "--color-text": "#0c4a6e",
      "--color-text-muted": "#0369a1",
      "--color-text-inverse": "#ffffff",
      "--color-success": "#16a34a",
      "--color-success-bg": "#dcfce7",
      "--color-danger": "#dc2626",
      "--color-danger-bg": "#fee2e2",
      "--color-info": "#0284c7",
      "--color-warning": "#ea580c",
      "--color-link": "#0284c7",
      "--color-grid": "#e0f2fe",
      "--shadow-card": "0 2px 10px rgba(2,132,199,0.1)",
    },
  },
};

export const DEFAULT_THEME_ID = "binance-dark";

export function getTheme(themeId) {
  return THEMES[themeId] || THEMES[DEFAULT_THEME_ID];
}

export function listThemes() {
  return Object.values(THEMES);
}
