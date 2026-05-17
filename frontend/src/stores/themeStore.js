/* ============================================================
   Zustand store برای تم — themeId + fontSize + customColors
   persist در localStorage با کلید "theme-storage"
   ============================================================ */
import { create } from "zustand";
import { persist } from "zustand/middleware";
import { DEFAULT_THEME_ID } from "../themes/themes.js";

export const DEFAULT_FONT_SIZE = 14;
export const MIN_FONT_SIZE = 11;
export const MAX_FONT_SIZE = 20;

const useThemeStore = create(
  persist(
    (set) => ({
      themeId: DEFAULT_THEME_ID,
      fontSize: DEFAULT_FONT_SIZE,
      customColors: {}, // override های کاربر: { "--color-primary": "#ff0000", ... }

      setTheme: (id) => set({ themeId: id }),

      setFontSize: (px) => {
        const n = Number(px) || DEFAULT_FONT_SIZE;
        const clamped = Math.max(MIN_FONT_SIZE, Math.min(MAX_FONT_SIZE, n));
        set({ fontSize: clamped });
      },

      setCustomColor: (varName, value) =>
        set((s) => ({ customColors: { ...s.customColors, [varName]: value } })),

      removeCustomColor: (varName) =>
        set((s) => {
          const next = { ...s.customColors };
          delete next[varName];
          return { customColors: next };
        }),

      resetCustomColors: () => set({ customColors: {} }),

      resetAll: () =>
        set({
          themeId: DEFAULT_THEME_ID,
          fontSize: DEFAULT_FONT_SIZE,
          customColors: {},
        }),
    }),
    {
      name: "theme-storage",
      version: 1,
    }
  )
);

export default useThemeStore;
