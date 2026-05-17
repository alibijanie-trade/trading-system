# -*- coding: utf-8 -*-
"""
Endpoints احراز هویت — سند ۶.۶
================================================================
| Method | Endpoint            | کاربرد                  | Auth |
| ------ | ------------------- | ----------------------- | ---- |
| POST   | /auth/login         | ورود (OAuth2 form)      | ❌   |
| POST   | /auth/refresh       | access token جدید       | ❌   |
| POST   | /auth/logout        | خروج (revoke refresh)   | ✅   |
| GET    | /auth/me            | اطلاعات کاربر فعلی     | ✅   |

نکته: /login از OAuth2PasswordRequestForm استفاده می‌کند که با
multipart/form-data ارسال می‌شود (نه JSON). این استاندارد OAuth2
است و Swagger UI خودش UI «Authorize» می‌سازد.
================================================================
"""

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user
from app.core.logging import get_logger
from app.core.response import success_response
from app.infrastructure.database import get_db
from app.models.user import User
from app.schemas.auth import LogoutRequest, RefreshRequest, UserMe
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])
logger = get_logger(__name__)


# ============================================================
# POST /auth/login
# ============================================================
@router.post("/login")
async def login(
    request: Request,
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    ورود کاربر — استاندارد OAuth2 password flow.

    Form fields:
      - username
      - password

    در Swagger UI: روی دکمه «Authorize» (آیکون قفل) کلیک کن،
    فقط username/password بده. توکن خودکار در همه endpoint های
    دارای auth استفاده می‌شود.
    """
    service = AuthService(db)
    ip = request.client.host if request.client else None
    tokens = await service.login(form.username, form.password, ip_address=ip)
    return success_response(
        data=tokens.model_dump(),
        message="ورود موفق",
    )


# ============================================================
# POST /auth/refresh
# ============================================================
@router.post("/refresh")
async def refresh(
    body: RefreshRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """صدور access token جدید با refresh token معتبر."""
    service = AuthService(db)
    tokens = await service.refresh(body.refresh_token)
    return success_response(
        data=tokens.model_dump(),
        message="توکن جدید صادر شد",
    )


# ============================================================
# POST /auth/logout
# ============================================================
@router.post("/logout")
async def logout(
    body: LogoutRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    خروج — refresh token لغو می‌شود.

    نکته: access token همچنان تا انقضای طبیعی معتبر می‌ماند
    (پایان ۳۰ دقیقه پیش‌فرض). برای blacklist access token،
    باید یک Redis/cache لایه افزود (در فاز ۵+).
    """
    service = AuthService(db)
    await service.logout(body.refresh_token)
    return success_response(message="خروج موفق")


# ============================================================
# GET /auth/me
# ============================================================
@router.get("/me")
async def me(current_user: User = Depends(get_current_user)) -> dict:
    """اطلاعات کاربر فعلی — مفید برای تست توکن."""
    return success_response(
        data=UserMe.model_validate(current_user).model_dump(),
        message="اطلاعات کاربر",
    )
