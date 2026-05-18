@echo off
REM run_pytest_unit.cmd — اجرای pytest unit tests (سریع)
REM فقط tests/unit/ — integration ها skip می‌شوند برای سرعت

cd /d "%~dp0\..\backend"
if not exist "venv\Scripts\activate.bat" (
  echo [WARN] backend venv پیدا نشد — skip pytest
  exit /b 0
)

call venv\Scripts\activate.bat
pytest tests/unit -q --no-header --tb=short
