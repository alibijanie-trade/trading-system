/* ============================================================
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
