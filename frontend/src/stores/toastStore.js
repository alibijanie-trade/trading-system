/* ============================================================
   Zustand store برای Toast notifications
   API: useToastStore().success(msg, [duration])
        useToastStore().error(msg, [duration])
        useToastStore().warning(msg)
        useToastStore().info(msg)
        useToastStore().dismiss(id)
        useToastStore().clear()
   duration=0 → بدون auto-dismiss (پاک کردن دستی)
   ============================================================ */
import { create } from "zustand";

let nextId = 1;
const DEFAULT_DURATION = 4000;

const useToastStore = create((set, get) => ({
  toasts: [],

  add: (type, message, duration = DEFAULT_DURATION) => {
    const id = nextId++;
    set((s) => ({ toasts: [...s.toasts, { id, type, message, duration }] }));
    if (duration > 0) {
      setTimeout(() => get().dismiss(id), duration);
    }
    return id;
  },

  dismiss: (id) =>
    set((s) => ({ toasts: s.toasts.filter((t) => t.id !== id) })),

  clear: () => set({ toasts: [] }),

  success: (msg, dur) => get().add("success", msg, dur),
  error: (msg, dur) => get().add("error", msg, dur),
  warning: (msg, dur) => get().add("warning", msg, dur),
  info: (msg, dur) => get().add("info", msg, dur),
}));

export default useToastStore;
