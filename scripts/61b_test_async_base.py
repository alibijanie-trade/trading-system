"""
61b_test_async_base.py — تست افزودن read_ohlcv_async و backwards compat

۵ تست:
1. base.py دارای import asyncio
2. DataSource دارای متد read_ohlcv_async
3. read_ohlcv_async **غیر-abstract** است (default impl دارد)
4. ExcelDataSource بدون تغییر کار می‌کند (read_ohlcv sync + name='excel')
5. ExcelDataSource read_ohlcv_async را به ارث می‌برد
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))


def t_base_imports_asyncio() -> bool:
    """base.py باید asyncio را import کرده باشد."""
    try:
        from app.infrastructure.data_sources import base as base_mod
    except Exception as e:
        print(f"[FAIL] cannot import base module: {e}")
        return False

    if not hasattr(base_mod, "asyncio"):
        print("[FAIL] base module does not expose 'asyncio'")
        return False
    print("[OK] base.py imports asyncio")
    return True


def t_data_source_has_async_method() -> bool:
    """DataSource باید read_ohlcv_async داشته باشد."""
    from app.infrastructure.data_sources.base import DataSource

    if not hasattr(DataSource, "read_ohlcv_async"):
        print("[FAIL] DataSource missing 'read_ohlcv_async'")
        return False

    method = DataSource.read_ohlcv_async
    if not callable(method):
        print("[FAIL] read_ohlcv_async is not callable")
        return False

    print("[OK] DataSource has read_ohlcv_async method")
    return True


def t_async_method_not_abstract() -> bool:
    """read_ohlcv_async نباید abstract باشد (default impl دارد)."""
    from app.infrastructure.data_sources.base import DataSource

    method = DataSource.read_ohlcv_async
    if getattr(method, "__isabstractmethod__", False):
        print("[FAIL] read_ohlcv_async marked abstract — would break ExcelDataSource")
        return False

    print("[OK] read_ohlcv_async has default impl (not abstract)")
    return True


def t_excel_data_source_intact() -> bool:
    """ExcelDataSource باید بدون تغییر کار کند."""
    from app.infrastructure.data_sources.excel_source import ExcelDataSource

    source = ExcelDataSource()

    # name property
    if source.name != "excel":
        print(f"[FAIL] ExcelDataSource.name = {source.name!r} (expected 'excel')")
        return False

    # read_ohlcv method exists
    if not callable(getattr(source, "read_ohlcv", None)):
        print("[FAIL] ExcelDataSource missing read_ohlcv")
        return False

    print("[OK] ExcelDataSource intact (name='excel', read_ohlcv callable)")
    return True


def t_excel_inherits_async() -> bool:
    """ExcelDataSource باید read_ohlcv_async را به ارث ببرد."""
    from app.infrastructure.data_sources.excel_source import ExcelDataSource

    source = ExcelDataSource()
    if not callable(getattr(source, "read_ohlcv_async", None)):
        print("[FAIL] ExcelDataSource missing inherited read_ohlcv_async")
        return False

    print("[OK] ExcelDataSource inherits read_ohlcv_async from DataSource")
    return True


def main() -> int:
    tests = [
        t_base_imports_asyncio,
        t_data_source_has_async_method,
        t_async_method_not_abstract,
        t_excel_data_source_intact,
        t_excel_inherits_async,
    ]
    print(f"=== Running {len(tests)} tests ===")
    print()
    results = []
    for t in tests:
        try:
            results.append(t())
        except Exception as e:
            print(f"[ERROR] {t.__name__}: {type(e).__name__}: {e}")
            results.append(False)
    print()
    passed = sum(results)
    total = len(results)
    print(f"=== {passed}/{total} pass ===")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
