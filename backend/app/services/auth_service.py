# -*- coding: utf-8 -*-
"""
AuthService — منطق کسب‌وکار احراز هویت
================================================================
این Service فقط با Repository ها کار می‌کند — هیچ Query مستقیمی
ندارد (قانون سند ۳.۳).

عملیات:
  - authenticate : چک username/password
  - login        : authenticate + ساخت tokens + ذخیره refresh در DB
  - refresh      : چک refresh token در DB + ساخت access جدید
  - logout       : revoke refresh token
================================================================
"""

from datetime import datetime, timezone

from app.core.config import settings
from app.core.exceptions import AuthenticationError
from app.core.logging import get_logger
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.user_session_repository import UserSessionRepository
from app.schemas.auth import TokenPair
from sqlalchemy.ext.asyncio import AsyncSession

logger = get_logger(__name__)


class AuthService:
    """منطق احراز هویت."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.users = UserRepository(db)
        self.sessions = UserSessionRepository(db)

    # ============================================================
    # Authentication
    # ============================================================
    async def authenticate(self, username: str, password: str) -> User:
        """
        چک username/password.

        Raises:
            AuthenticationError: اعتبارنامه نادرست یا کاربر غیرفعال
        """
        user = await self.users.get_by_username(username)
        if user is None or not verify_password(password, user.password_hash):
            raise AuthenticationError(
                message="نام کاربری یا رمز عبور اشتباه است",
                code="INVALID_CREDENTIALS",
            )
        if not user.is_active:
            raise AuthenticationError(
                message="حساب کاربری غیرفعال است",
                code="USER_INACTIVE",
            )
        return user

    # ============================================================
    # Login
    # ============================================================
    async def login(
        self,
        username: str,
        password: str,
        ip_address: str | None = None,
    ) -> TokenPair:
        """
        ورود + ساخت access + refresh + ذخیره refresh در DB.

        Returns:
            TokenPair
        """
        user = await self.authenticate(username, password)

        # ساخت tokens
        access_token = create_access_token(
            user_id=user.id,
            username=user.username,
            role=user.role,
        )
        refresh_token, refresh_expires_at = create_refresh_token(user_id=user.id)

        # ذخیره refresh در DB
        await self.sessions.create(
            user_id=user.id,
            token=refresh_token,
            expires_at=refresh_expires_at,
            ip_address=ip_address,
            is_revoked=False,
        )

        # به‌روزرسانی last_login
        user.last_login = datetime.now(timezone.utc)

        # commit کل تراکنش (نشست + last_login)
        await self.db.commit()

        logger.info("login: user_id=%d username=%s", user.id, user.username)

        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    # ============================================================
    # Refresh
    # ============================================================
    async def refresh(self, refresh_token: str) -> TokenPair:
        """
        صدور access token جدید با refresh token معتبر.
        refresh token خودش تغییر نمی‌کند.

        Raises:
            AuthenticationError: refresh نامعتبر/منقضی/revoke شده
        """
        # ۱) decode JWT (شامل چک expire توسط jose)
        payload = decode_token(refresh_token, expected_type="refresh")
        user_id = int(payload["sub"])

        # ۲) رکورد در DB پیدا شود + revoke نشده باشد
        sess = await self.sessions.get_by_token(refresh_token)
        if sess is None:
            raise AuthenticationError(
                message="توکن refresh یافت نشد",
                code="REFRESH_NOT_FOUND",
            )
        if sess.is_revoked:
            raise AuthenticationError(
                message="توکن refresh لغو شده است",
                code="REFRESH_REVOKED",
            )

        # ۳) ساخت access جدید
        user = await self.users.get_or_404(user_id)
        new_access = create_access_token(
            user_id=user.id,
            username=user.username,
            role=user.role,
        )

        logger.info("refresh: user_id=%d", user.id)

        return TokenPair(
            access_token=new_access,
            refresh_token=refresh_token,  # همان قبلی
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    # ============================================================
    # Logout
    # ============================================================
    async def logout(self, refresh_token: str) -> None:
        """
        revoke کردن refresh token. اگر نشست پیدا نشد، silently OK
        (idempotent).
        """
        sess = await self.sessions.get_by_token(refresh_token)
        if sess is None or sess.is_revoked:
            return
        sess.is_revoked = True
        await self.db.commit()
        logger.info("logout: user_id=%d", sess.user_id)
