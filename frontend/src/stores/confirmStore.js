import { create } from "zustand";

/**
 * confirmStore — مدیریت ConfirmDialog سراسری
 *
 * Usage در هر کامپوننت:
 *   const askConfirm = useConfirmStore((s) => s.confirm);
 *   const ok = await askConfirm({
 *     title: "خروج",
 *     message: "آیا مطمئنید؟",
 *     variant: "warning",      // "danger" | "warning" | "info"
 *     confirmText: "خروج",
 *     cancelText: "انصراف",
 *   });
 *   if (!ok) return;
 *
 * هر بار فقط یک dialog فعال است (single-instance).
 * Promise با true (تأیید) یا false (انصراف/Escape/backdrop) resolve می‌شود.
 */

const INITIAL_STATE = {
  isOpen: false,
  title: "",
  message: "",
  variant: "info",
  confirmText: "تأیید",
  cancelText: "انصراف",
  resolver: null,
};

const useConfirmStore = create((set, get) => ({
  ...INITIAL_STATE,

  confirm: (opts = {}) =>
    new Promise((resolve) => {
      // اگر dialog قبلی باز است، آن را با false reject کن
      const prev = get().resolver;
      if (prev) prev(false);

      set({
        isOpen: true,
        title: opts.title || "",
        message: opts.message || "",
        variant: opts.variant || "info",
        confirmText: opts.confirmText || "تأیید",
        cancelText: opts.cancelText || "انصراف",
        resolver: resolve,
      });
    }),

  confirmAccept: () => {
    const { resolver } = get();
    if (resolver) resolver(true);
    set({ ...INITIAL_STATE });
  },

  confirmReject: () => {
    const { resolver } = get();
    if (resolver) resolver(false);
    set({ ...INITIAL_STATE });
  },
}));

export default useConfirmStore;
