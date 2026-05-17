# -*- coding: utf-8 -*-
"""
اسکریپت ۲۰ — Endpoint GET /ohlcv
================================================================
نسخه پروژه: v0.1.4 (افزودن اولین endpoint OHLCV)

این اسکریپت idempotent است — می‌تواند چند بار اجرا شود:
  - فایل‌های جدید را می‌سازد
  - فایل‌های موجود را overwrite می‌کند
  - چیزی را پاک نمی‌کند

فایل‌های ساخته/به‌روزرسانی‌شده:
  1. app/repositories/ohlcv_repository.py   (جدید)
  2. app/repositories/symbol_repository.py  (جدید)
  3. app/repositories/__init__.py           (به‌روزرسانی — export های جدید)
  4. app/schemas/ohlcv.py                   (افزودن OhlcvCandleOut + OhlcvListData)
  5. app/schemas/__init__.py                (به‌روزرسانی — export های جدید)
  6. app/api/v1/routes/ohlcv.py             (جدید)
  7. main.py                                (افزودن include_router برای ohlcv)

پس از اجرا:
  cd backend
  venv\\Scripts\\activate
  uvicorn main:app --reload
  مرورگر: http://127.0.0.1:8000/docs

تست اول:
  GET /api/v1/ohlcv/1?timeframe=1d&limit=5
================================================================
"""

from pathlib import Path

# ============================================================
# تعیین مسیرها — نسبت به این اسکریپت
# ============================================================
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
APP_DIR = BACKEND_DIR / "app"


# ============================================================
# محتوای فایل ۱: app/repositories/ohlcv_repository.py
# ============================================================
OHLCV_REPOSITORY_PY = '''# -*- coding: utf-8 -*-
"""
OhlcvRepository — Query های اختصاصی OhlcvData
================================================================
این Repository از BaseRepository ارث می‌برد و Query های اختصاصی
برای جدول OhlcvData اضافه می‌کند.

استفاده در route ها:
    from app.repositories.ohlcv_repository import OhlcvRepository

    repo = OhlcvRepository(db)
    candles = await repo.list_by_symbol_and_timeframe(
        symbol_id=1,
        timeframe="1d",
        limit=100,
    )

قانون قفل‌شده (سند ۳.۳):
  - تمام Query های OhlcvData باید از این کلاس عبور کنند
  - هیچ select مستقیم از OhlcvData در api/ یا services/ نباشد
================================================================
"""

from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ohlcv_data import OhlcvData
from app.repositories.base import BaseRepository


class OhlcvRepository(BaseRepository[OhlcvData]):
    """Repository اختصاصی برای OhlcvData."""

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, OhlcvData)

    # ============================================================
    # Query های اختصاصی فاز ۰ — endpoint GET /ohlcv/{symbol_id}
    # ============================================================

    async def list_by_symbol_and_timeframe(
        self,
        symbol_id: int,
        timeframe: str,
        limit: int = 100,
        offset: int = 0,
        from_ts: datetime | None = None,
        to_ts: datetime | None = None,
    ) -> list[OhlcvData]:
        """
        لیست کندل‌ها برای یک نماد و تایم‌فریم خاص — مرتب صعودی
        بر اساس timestamp (قدیمی‌ترین اول).

        از ایندکس Critical (idx_ohlcv_symbol_tf_ts) برای کارایی
        استفاده می‌کند (سند ۵.۷).

        Args:
            symbol_id: شناسه نماد (FK→Symbols)
            timeframe: تایم‌فریم (مثلاً "1d", "1h", "15m")
            limit: حداکثر تعداد
            offset: شروع از کجا (برای pagination)
            from_ts: فقط کندل‌های با timestamp >= from_ts
            to_ts: فقط کندل‌های با timestamp <= to_ts

        Returns:
            list[OhlcvData] — می‌تواند خالی باشد
        """
        stmt = (
            select(OhlcvData)
            .where(
                OhlcvData.symbol_id == symbol_id,
                OhlcvData.timeframe == timeframe,
            )
            .order_by(OhlcvData.timestamp.asc())
        )
        if from_ts is not None:
            stmt = stmt.where(OhlcvData.timestamp >= from_ts)
        if to_ts is not None:
            stmt = stmt.where(OhlcvData.timestamp <= to_ts)

        stmt = stmt.offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count_by_symbol_and_timeframe(
        self,
        symbol_id: int,
        timeframe: str,
        from_ts: datetime | None = None,
        to_ts: datetime | None = None,
    ) -> int:
        """شمارش کل کندل‌های مطابق فیلتر — برای pagination metadata."""
        stmt = (
            select(func.count())
            .select_from(OhlcvData)
            .where(
                OhlcvData.symbol_id == symbol_id,
                OhlcvData.timeframe == timeframe,
            )
        )
        if from_ts is not None:
            stmt = stmt.where(OhlcvData.timestamp >= from_ts)
        if to_ts is not None:
            stmt = stmt.where(OhlcvData.timestamp <= to_ts)

        result = await self.db.execute(stmt)
        return int(result.scalar_one())
'''


# ============================================================
# محتوای فایل ۲: app/repositories/symbol_repository.py
# ============================================================
SYMBOL_REPOSITORY_PY = '''# -*- coding: utf-8 -*-
"""
SymbolRepository — Repository نماد
================================================================
این Repository ساده — فقط ارث از BaseRepository — برای دسترسی
به Symbol استفاده می‌شود. متدهای CRUD از Base می‌آیند:
  - get(id) / get_or_404(id)
  - list / count / exists
  - create / update / delete (soft)

در فازهای بعد متدهای اختصاصی اضافه خواهد شد (مثلاً
get_by_exchange_and_symbol).
================================================================
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.symbol import Symbol
from app.repositories.base import BaseRepository


class SymbolRepository(BaseRepository[Symbol]):
    """Repository نماد — متدهای CRUD از BaseRepository."""

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, Symbol)
'''


# ============================================================
# محتوای فایل ۳: app/repositories/__init__.py
# ============================================================
REPOSITORIES_INIT_PY = '''# -*- coding: utf-8 -*-
"""
Repositories — export سطح بالا
================================================================
این پکیج Repository های پروژه را export می‌کند.

استفاده پایه:
    from app.repositories import BaseRepository

استفاده Repository های اختصاصی:
    from app.repositories import OhlcvRepository, SymbolRepository

قانون قفل‌شده (سند ۳.۳):
  - هرگز Query مستقیم خارج از repositories/
  - service ها از Repository استفاده می‌کنند، نه از session مستقیم
================================================================
"""

from app.repositories.base import BaseRepository
from app.repositories.ohlcv_repository import OhlcvRepository
from app.repositories.symbol_repository import SymbolRepository

__all__ = [
    "BaseRepository",
    "OhlcvRepository",
    "SymbolRepository",
]
'''


# ============================================================
# محتوای فایل ۴: app/schemas/ohlcv.py
# ============================================================
SCHEMAS_OHLCV_PY = '''# -*- coding: utf-8 -*-
"""
Pydantic Schemas برای OHLCV
================================================================
دو گروه schema:

۱) Schema های DataSource Layer (فاز ۶):
   - OhlcvRowSchema    : یک ردیف داده خام
   - OhlcvImportResult : نتیجه import یک فایل

۲) Schema های API Response (فاز ۰ — endpoint GET /ohlcv):
   - OhlcvCandleOut : یک کندل برای پاسخ API (بدون id و row_index)
   - OhlcvListData  : بخش data پاسخ GET /ohlcv/{symbol_id}
================================================================
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# Schema های DataSource Layer (فاز ۶)
# ============================================================

class OhlcvRowSchema(BaseModel):
    """یک ردیف داده OHLCV — مستقل از منبع."""

    model_config = ConfigDict(from_attributes=True)

    row_index: int = Field(..., ge=0, description="شماره ردیف از صفر")
    timestamp: datetime = Field(..., description="زمان شروع کندل (UTC)")
    open: float = Field(..., gt=0)
    high: float = Field(..., gt=0)
    low: float = Field(..., gt=0)
    close: float = Field(..., gt=0)
    volume: float = Field(..., ge=0)


class OhlcvImportResult(BaseModel):
    """نتیجه import یک فایل/منبع OHLCV."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    rows: list[OhlcvRowSchema]
    symbol_info: dict[str, str] = Field(
        ..., description="symbol, base_asset, quote_asset, market_type",
    )
    timeframe: str
    source_metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def row_count(self) -> int:
        return len(self.rows)


# ============================================================
# Schema های API Response (فاز ۰ — endpoint GET /ohlcv)
# ============================================================

class OhlcvCandleOut(BaseModel):
    """
    یک کندل برای پاسخ API — بدون id، symbol_id، timeframe، row_index.

    این فیلدها در سطح parent (OhlcvListData) قرار دارند تا
    payload سبک‌تر باشد.
    """

    model_config = ConfigDict(from_attributes=True)

    timestamp: datetime = Field(..., description="زمان شروع کندل (UTC)")
    open: float
    high: float
    low: float
    close: float
    volume: float


class OhlcvListData(BaseModel):
    """
    بخش data پاسخ GET /ohlcv/{symbol_id}.

    ساختار نهایی پاسخ:
        {
            "success": true,
            "message": "...",
            "data": OhlcvListData,
            "errors": null
        }
    """

    symbol_id: int
    timeframe: str
    count: int = Field(..., description="تعداد کندل در این پاسخ")
    total: int = Field(..., description="کل کندل‌های مطابق فیلتر")
    limit: int
    offset: int
    candles: list[OhlcvCandleOut]
'''


# ============================================================
# محتوای فایل ۵: app/schemas/__init__.py
# ============================================================
SCHEMAS_INIT_PY = '''# -*- coding: utf-8 -*-
"""Pydantic schemas — DTO های پروژه."""

from app.schemas.ohlcv import (
    OhlcvCandleOut,
    OhlcvImportResult,
    OhlcvListData,
    OhlcvRowSchema,
)

__all__ = [
    "OhlcvRowSchema",
    "OhlcvImportResult",
    "OhlcvCandleOut",
    "OhlcvListData",
]
'''


# ============================================================
# محتوای فایل ۶: app/api/v1/routes/ohlcv.py
# ============================================================
ROUTES_OHLCV_PY = '''# -*- coding: utf-8 -*-
"""
Endpoint های OHLCV — سند ۶.۸
================================================================
| Method | Endpoint               | کاربرد                    | Auth                  |
| ------ | ---------------------- | ------------------------- | --------------------- |
| GET    | /ohlcv/{symbol_id}     | کندل‌ها با timeframe       | (در زیرگام ۵ افزوده) |

نکته فاز ۰:
  - فعلاً بدون auth — برای تست از Swagger UI
  - پس از زیرگام ۵ (Auth)، یک Depends(get_current_user) اضافه
    خواهد شد

ساختار پاسخ — طبق سند ۶.۲:
    {
        "success": true,
        "message": "N کندل بازگردانده شد",
        "data": {
            "symbol_id": 1,
            "timeframe": "1d",
            "count": 100,
            "total": 1714,
            "limit": 100,
            "offset": 0,
            "candles": [
                {"timestamp": "2017-08-17T00:00:00+00:00",
                 "open": ..., "high": ..., "low": ...,
                 "close": ..., "volume": ...},
                ...
            ]
        },
        "errors": null
    }
================================================================
"""

from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.core.response import success_response
from app.infrastructure.database import get_db
from app.repositories.ohlcv_repository import OhlcvRepository
from app.repositories.symbol_repository import SymbolRepository
from app.schemas.ohlcv import OhlcvCandleOut, OhlcvListData

router = APIRouter(prefix="/ohlcv", tags=["OHLCV"])
logger = get_logger(__name__)


@router.get("/{symbol_id}")
async def get_ohlcv(
    symbol_id: int,
    timeframe: str = Query(..., description="مثلاً 1d, 1h, 15m, 5m"),
    limit: int = Query(100, ge=1, le=1000, description="حداکثر کندل (1..1000)"),
    offset: int = Query(0, ge=0, description="شروع از کندل چندم"),
    from_ts: datetime | None = Query(
        None,
        description="ISO 8601 — مثل 2020-01-01T00:00:00Z (فقط کندل‌های >= این زمان)",
    ),
    to_ts: datetime | None = Query(
        None,
        description="ISO 8601 — فقط کندل‌های <= این زمان",
    ),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    دریافت کندل‌های یک نماد در یک تایم‌فریم خاص — مرتب صعودی.

    Raises:
        404 NotFoundError: اگر symbol_id موجود نباشد یا soft-delete شده
    """
    # ۱) اعتبارسنجی وجود symbol
    sym_repo = SymbolRepository(db)
    await sym_repo.get_or_404(symbol_id)

    # ۲) دریافت کندل‌ها از Repository
    ohlcv_repo = OhlcvRepository(db)

    candles = await ohlcv_repo.list_by_symbol_and_timeframe(
        symbol_id=symbol_id,
        timeframe=timeframe,
        limit=limit,
        offset=offset,
        from_ts=from_ts,
        to_ts=to_ts,
    )

    total = await ohlcv_repo.count_by_symbol_and_timeframe(
        symbol_id=symbol_id,
        timeframe=timeframe,
        from_ts=from_ts,
        to_ts=to_ts,
    )

    # ۳) ساخت پاسخ
    data = OhlcvListData(
        symbol_id=symbol_id,
        timeframe=timeframe,
        count=len(candles),
        total=total,
        limit=limit,
        offset=offset,
        candles=[OhlcvCandleOut.model_validate(c) for c in candles],
    )

    logger.info(
        "GET /ohlcv/%s tf=%s offset=%d limit=%d --> %d/%d",
        symbol_id, timeframe, offset, limit, len(candles), total,
    )

    return success_response(
        data=data.model_dump(mode="json"),
        message=f"{len(candles)} کندل بازگردانده شد",
    )
'''


# ============================================================
# محتوای فایل ۷: main.py
# ============================================================
MAIN_PY = '''# -*- coding: utf-8 -*-
"""
نقطه ورود FastAPI — سامانه هوشمند ترید
================================================================
این فایل فقط شامل: app instance + middleware + handlers + router include.

قواعد قفل‌شده:
  - Business Logic در services/ — هرگز اینجا
  - Query در repositories/ — هرگز اینجا
  - Validation در schemas/ — هرگز اینجا

نحوه اجرا (در tab «1 backend»):
    cd backend
    venv\\\\Scripts\\\\activate
    uvicorn main:app --reload
================================================================
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import health, ohlcv
from app.core.config import settings
from app.core.handlers import register_exception_handlers
from app.core.logging import get_logger, setup_logging

# تنظیم لاگ پیش از هر چیز
setup_logging()
logger = get_logger(__name__)


# ============================================================
# Lifecycle Events (Startup / Shutdown)
# ============================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """مدیریت چرخه عمر اپلیکیشن"""
    # ===== Startup =====
    logger.info("=" * 60)
    logger.info(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"   Environment: {settings.APP_ENV}")
    logger.info(f"   API: http://{settings.API_HOST}:{settings.API_PORT}{settings.API_PREFIX}")
    logger.info(f"   Docs: http://{settings.API_HOST}:{settings.API_PORT}/docs")
    logger.info("=" * 60)

    yield

    # ===== Shutdown =====
    logger.info(f"👋 {settings.APP_NAME} shutting down...")


# ============================================================
# ساخت FastAPI app
# ============================================================
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="سامانه هوشمند ترید — کریپتو و فارکس",
    lifespan=lifespan,
)


# ============================================================
# Middleware
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Exception Handlers
# ============================================================
register_exception_handlers(app)


# ============================================================
# Router Registration
# ============================================================
app.include_router(health.router, prefix=settings.API_PREFIX)
app.include_router(ohlcv.router, prefix=settings.API_PREFIX)


# ============================================================
# Root Endpoint
# ============================================================
from app.core.response import success_response


@app.get("/")
async def root() -> dict:
    """صفحه ریشه — اطلاعات کلی"""
    return success_response(
        message="سامانه هوشمند ترید فعال است",
        data={
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "health": f"{settings.API_PREFIX}/health",
        },
    )
'''


# ============================================================
# نقشه فایل‌ها → محتوا
# ============================================================
FILES_TO_WRITE: dict[Path, str] = {
    APP_DIR / "repositories" / "ohlcv_repository.py": OHLCV_REPOSITORY_PY,
    APP_DIR / "repositories" / "symbol_repository.py": SYMBOL_REPOSITORY_PY,
    APP_DIR / "repositories" / "__init__.py": REPOSITORIES_INIT_PY,
    APP_DIR / "schemas" / "ohlcv.py": SCHEMAS_OHLCV_PY,
    APP_DIR / "schemas" / "__init__.py": SCHEMAS_INIT_PY,
    APP_DIR / "api" / "v1" / "routes" / "ohlcv.py": ROUTES_OHLCV_PY,
    BACKEND_DIR / "main.py": MAIN_PY,
}


# ============================================================
# اجرا
# ============================================================
def main() -> None:
    print("=" * 60)
    print("اسکریپت ۲۰ — Endpoint GET /ohlcv")
    print("=" * 60)
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Backend dir : {BACKEND_DIR}")
    print()

    if not BACKEND_DIR.exists():
        print(f"[ERROR] پوشه backend پیدا نشد: {BACKEND_DIR}")
        raise SystemExit(1)

    for path, content in FILES_TO_WRITE.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        rel = path.relative_to(PROJECT_ROOT)
        print(f"  ✓ {rel}")

    print()
    print("=" * 60)
    print(f"✅ {len(FILES_TO_WRITE)} فایل نوشته/به‌روز شد.")
    print("=" * 60)
    print()
    print("مرحله بعد:")
    print("  ۱) در tab «1 backend» اگر uvicorn روشن است، با Ctrl+C ببندید")
    print("  ۲) دوباره uvicorn را اجرا کنید (تا router جدید load شود)")
    print("  ۳) مرورگر: http://127.0.0.1:8000/docs")
    print("  ۴) اولین تست:")
    print("       GET /api/v1/ohlcv/1?timeframe=1d&limit=5")


if __name__ == "__main__":
    main()
