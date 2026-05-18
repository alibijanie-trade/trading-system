# -*- coding: utf-8 -*-
"""
Endpoint های OHLCV — سند ۶.۸
================================================================
| Method | Endpoint               | کاربرد                    | Auth |
| ------ | ---------------------- | ------------------------- | ---- |
| GET    | /ohlcv/{symbol_id}     | کندل‌ها با timeframe       | ✅   |

🆕 v0.2.0: محافظت با access token (Bearer).
================================================================
"""

from datetime import datetime

from app.api.v1.dependencies import get_current_user
from app.core.logging import get_logger
from app.core.response import success_response
from app.infrastructure.database import get_db
from app.models.user import User
from app.repositories.ohlcv_repository import OhlcvRepository
from app.repositories.symbol_repository import SymbolRepository
from app.schemas.ohlcv import OhlcvCandleOut, OhlcvListData
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

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
        description="ISO 8601 — فقط کندل‌های >= این زمان",
    ),
    to_ts: datetime | None = Query(
        None,
        description="ISO 8601 — فقط کندل‌های <= این زمان",
    ),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    دریافت کندل‌های یک نماد در یک تایم‌فریم خاص — مرتب صعودی.

    🔒 نیاز به access token (Bearer).

    Raises:
        401: توکن نامعتبر یا منقضی
        404: symbol_id یافت نشد
    """
    # اعتبارسنجی وجود symbol
    sym_repo = SymbolRepository(db)
    await sym_repo.get_or_404(symbol_id)

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
        "GET /ohlcv/%s tf=%s user=%s --> %d/%d",
        symbol_id,
        timeframe,
        current_user.username,
        len(candles),
        total,
    )

    return success_response(
        data=data.model_dump(mode="json"),
        message=f"{len(candles)} کندل بازگردانده شد",
    )
