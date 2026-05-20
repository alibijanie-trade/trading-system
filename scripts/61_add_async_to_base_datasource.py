"""
61_add_async_to_base_datasource.py — افزودن read_ohlcv_async به DataSource

طبق Decision معماری چت ۱۰ سؤال ۱: gradient interface.

تغییرات در backend/app/infrastructure/data_sources/base.py:
1. افزودن `import asyncio` (بالا)
2. افزودن متد `read_ohlcv_async` (با default impl = to_thread)
   بین read_ohlcv و name property

ویژگی‌ها:
- Idempotent: بر اساس دو marker (import + method)
- Read-back verify
- Backwards compat: ExcelDataSource بدون تغییر کار می‌کند
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_FILE = ROOT / "backend" / "app" / "infrastructure" / "data_sources" / "base.py"

IMPORT_MARKER = "import asyncio"
ASYNC_METHOD_MARKER = "async def read_ohlcv_async"

OLD_IMPORT_LINE = "from abc import ABC, abstractmethod"
NEW_IMPORT_LINES = "import asyncio\nfrom abc import ABC, abstractmethod"

OLD_NAME_BLOCK = "    @property\n" "    @abstractmethod\n" "    def name(self) -> str:"

NEW_METHOD_BLOCK = '''    async def read_ohlcv_async(
        self, source: Any, **kwargs: Any
    ) -> OhlcvImportResult:
        """
        نسخه async متد read_ohlcv.

        پیاده‌سازی پیش‌فرض: متد sync را در thread pool اجرا می‌کند
        تا event loop FastAPI block نشود. کلاس‌هایی که native async
        دارند (مثل CCXTDataSource) باید این متد را override کنند.

        Args:
            source: همان argument متد sync
            **kwargs: همان kwargs

        Returns:
            OhlcvImportResult (همان sync)
        """
        return await asyncio.to_thread(self.read_ohlcv, source, **kwargs)


'''


def main() -> int:
    if not BASE_FILE.exists():
        print(f"[ERROR] file not found: {BASE_FILE}")
        return 1

    content = BASE_FILE.read_text(encoding="utf-8")
    changed = False

    # Step 1: Add 'import asyncio' if missing
    if IMPORT_MARKER not in content:
        if OLD_IMPORT_LINE not in content:
            print("[ERROR] cannot find import marker 'from abc import ABC, abstractmethod'")
            return 2
        content = content.replace(OLD_IMPORT_LINE, NEW_IMPORT_LINES, 1)
        print("[INFO] added 'import asyncio'")
        changed = True
    else:
        print("[SKIP] 'import asyncio' already present")

    # Step 2: Add 'read_ohlcv_async' method if missing
    if ASYNC_METHOD_MARKER not in content:
        if OLD_NAME_BLOCK not in content:
            print("[ERROR] cannot find name property block — file structure changed?")
            return 3
        content = content.replace(OLD_NAME_BLOCK, NEW_METHOD_BLOCK + OLD_NAME_BLOCK, 1)
        print("[INFO] added 'read_ohlcv_async' method")
        changed = True
    else:
        print("[SKIP] 'read_ohlcv_async' already present")

    if not changed:
        print("[OK] base.py already in target state (no change made)")
        return 0

    # Write
    BASE_FILE.write_text(content, encoding="utf-8")

    # Read-back verify
    verify = BASE_FILE.read_text(encoding="utf-8")
    if ASYNC_METHOD_MARKER not in verify or IMPORT_MARKER not in verify:
        print("[FAIL] read-back: markers missing after write")
        return 4

    print("[OK] base.py updated successfully")
    print()
    print("Next: python scripts/61b_test_async_base.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
