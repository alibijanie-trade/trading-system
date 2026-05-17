# -*- coding: utf-8 -*-
"""
Dependencies — توابع تزریق وابستگی FastAPI
================================================================
این فایل توابع Depends() مشترک را ارائه می‌کند.

عمده‌ترین آن: get_current_user — استخراج کاربر از access token

استفاده:
    from app.api.v1.dependencies import get_current_user
    from app.models.user import User

    @router.get("/me")
    async def me(current_user: User = Depends(get_current_user)):
        return current_user
================================================================
"""

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import AuthenticationError
from app.core.security import decode_token
from app.infrastructure.database import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository

# OAuth2 password flow — Swagger UI خودش UI لاگین می‌سازد
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_PREFIX}/auth/login",
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    استخراج کاربر فعلی از access token.

    کاربر در request.state قرار نمی‌گیرد — مستقیم return می‌شود.

    Raises:
        AuthenticationError: توکن نامعتبر / کاربر یافت نشد / غیرفعال
    """
    payload = decode_token(token, expected_type="access")
    user_id = int(payload["sub"])

    users = UserRepository(db)
    user = await users.get(user_id)
    if user is None:
        raise AuthenticationError(
            message="کاربر یافت نشد",
            code="USER_NOT_FOUND",
        )
    if not user.is_active:
        raise AuthenticationError(
            message="حساب کاربری غیرفعال است",
            code="USER_INACTIVE",
        )
    return user
