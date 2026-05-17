# -*- coding: utf-8 -*-
"""
Pydantic Schemas برای Auth — سند ۶.۶
================================================================
درخواست:
  - LoginRequest        : ورود (در عمل از OAuth2PasswordRequestForm)
  - RefreshRequest      : درخواست access جدید
  - LogoutRequest       : خروج (revoke refresh token)

پاسخ:
  - TokenPair           : access + refresh + expires_in
  - UserMe              : اطلاعات کاربر فعلی
================================================================
"""

from pydantic import BaseModel, ConfigDict, Field


class TokenPair(BaseModel):
    """جفت توکن access + refresh — پاسخ /login و /refresh."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(..., description="مدت اعتبار access token به ثانیه")


class RefreshRequest(BaseModel):
    """درخواست POST /auth/refresh"""

    refresh_token: str = Field(..., min_length=1)


class LogoutRequest(BaseModel):
    """درخواست POST /auth/logout"""

    refresh_token: str = Field(..., min_length=1)


class UserMe(BaseModel):
    """پاسخ GET /auth/me — اطلاعات کاربر فعلی."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    role: str
    is_active: bool
