@echo off
REM run_vitest.cmd — اجرای vitest (frontend tests)

cd /d "%~dp0\..\frontend"
if not exist "node_modules\.bin\vitest" (
  echo [WARN] frontend node_modules نصب نیست — skip vitest
  exit /b 0
)

call npm test -- --run --reporter=dot
