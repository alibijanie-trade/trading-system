import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react({ jsxRuntime: 'automatic' })],

  // M64: vitest از esbuild داخلی استفاده می‌کند که تنظیم plugin-react را نمی‌بیند
  // — esbuild top-level برای test pipeline لازم است (Bug #50 follow-up)
  esbuild: {
    jsx: 'automatic',
  },

  // پیکربندی Vitest — همراه با Vite در یک فایل
  // مرجع: https://vitest.dev/config/
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.js'],
    css: false, // تست‌ها نیازی به پردازش CSS ندارند
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      include: ['src/**/*.{js,jsx}'],
      exclude: [
        'src/**/*.test.{js,jsx}',
        'src/test/**',
        'src/main.jsx',
        'src/assets/**',
      ],
    },
  },
})
