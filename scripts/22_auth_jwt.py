# -*- coding: utf-8 -*-
"""
اسکریپت ۲۲ — زیرگام ۵: Auth + JWT
================================================================
نسخه پروژه: v0.2.0 (Auth + JWT — MINOR feature)

این اسکریپت idempotent است:
  - فایل‌های جدید را می‌سازد
  - فایل‌های موجود را overwrite می‌کند
  - چیزی را پاک نمی‌کند

فایل‌های ساخته/به‌روزرسانی‌شده (۱۴ فایل):
  ۱) backend/app/core/security.py                (جدید)
  ۲) backend/app/core/config.py                  (به‌روزرسانی — APP_VERSION → 0.2.0)
  ۳) backend/app/repositories/user_repository.py (جدید)
  ۴) backend/app/repositories/user_session_repository.py (جدید)
  ۵) backend/app/repositories/__init__.py        (به‌روزرسانی)
  ۶) backend/app/schemas/auth.py                 (جدید)
  ۷) backend/app/schemas/__init__.py             (به‌روزرسانی)
  ۸) backend/app/services/auth_service.py        (جدید)
  ۹) backend/app/services/__init__.py            (به‌روزرسانی)
  ۱۰) backend/app/api/v1/dependencies.py         (جدید)
  ۱۱) backend/app/api/v1/routes/auth.py          (جدید)
  ۱۲) backend/app/api/v1/routes/ohlcv.py         (به‌روزرسانی — افزودن Depends)
  ۱۳) backend/main.py                            (به‌روزرسانی)
  ۱۴) backend/requirements.txt                   (به‌روزرسانی — افزودن python-multipart)

پس از اجرا — قبل از تست:
  cd backend
  venv\\Scripts\\activate
  pip install python-multipart==0.0.9
================================================================
"""

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
APP_DIR = BACKEND_DIR / "app"


# ============================================================
# ۱) app/core/security.py
# ============================================================
CORE_SECURITY_PY = '''# -*- coding: utf-8 -*-
"""
Security utilities — bcrypt + JWT
================================================================
توابع کمکی برای:
  - hash و verify رمز عبور (bcrypt via passlib)
  - encode/decode JWT (HS256 via python-jose)

استفاده در service layer:
    from app.core.security import (
        hash_password, verify_password,
        create_access_token, create_refresh_token, decode_token,
    )

قانون قفل‌شده (سند ۹.۱):
  - تنها این فایل JWT/bcrypt را مستقیم استفاده می‌کند
  - service ها از این توابع استفاده می‌کنند
================================================================
"""

from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.exceptions import AuthenticationError

# ============================================================
# Password Hashing (bcrypt)
# ============================================================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    """ساخت hash بکمت برای رمز عبور."""
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """بررسی مطابقت رمز عبور با hash."""
    return pwd_context.verify(plain, hashed)


# ============================================================
# JWT Tokens
# ============================================================
def _create_token(
    payload: dict[str, Any],
    expires_delta: timedelta,
    token_type: str,
) -> str:
    """ساخت JWT با iat + exp + type."""
    now = datetime.now(timezone.utc)
    data = payload.copy()
    data.update({
        "iat": now,
        "exp": now + expires_delta,
        "type": token_type,
    })
    return jwt.encode(
        data,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_access_token(user_id: int, username: str, role: str) -> str:
    """ساخت access token کوتاه‌مدت (پیش‌فرض ۳۰ دقیقه)."""
    return _create_token(
        payload={"sub": str(user_id), "username": username, "role": role},
        expires_delta=timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="access",
    )


def create_refresh_token(user_id: int) -> tuple[str, datetime]:
    """
    ساخت refresh token بلندمدت (پیش‌فرض ۷ روز).

    Returns:
        (token, expires_at) — expires_at برای ذخیره در DB
    """
    expires_delta = timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    token = _create_token(
        payload={"sub": str(user_id), "jti": str(uuid4())},
        expires_delta=expires_delta,
        token_type="refresh",
    )
    expires_at = datetime.now(timezone.utc) + expires_delta
    return token, expires_at


def decode_token(token: str, expected_type: str) -> dict[str, Any]:
    """
    decode + اعتبارسنجی JWT.

    Args:
        token: رشته JWT
        expected_type: "access" یا "refresh"

    Raises:
        AuthenticationError: توکن نامعتبر / منقضی / نوع اشتباه
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except JWTError as e:
        raise AuthenticationError(
            message="توکن نامعتبر یا منقضی است",
            code="INVALID_TOKEN",
        ) from e

    if payload.get("type") != expected_type:
        raise AuthenticationError(
            message=f"نوع توکن صحیح نیست (انتظار: {expected_type})",
            code="WRONG_TOKEN_TYPE",
        )
    return payload
'''


# ============================================================
# ۲) app/core/config.py
# ============================================================
CORE_CONFIG_PY = '''# -*- coding: utf-8 -*-
"""
تنظیمات اپلیکیشن — بارگذاری از .env
================================================================
تمام مقادیر پیکربندی از .env خوانده می‌شوند.
هرگز مقدار Hardcode در کد قرار نمی‌گیرد (قانون قفل‌شده).

نحوه استفاده در سایر فایل‌ها:
    from app.core.config import settings
    print(settings.APP_VERSION)
================================================================
"""

from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


# مسیر ریشه پوشه backend (که .env در آن قرار دارد)
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """کلاس تنظیمات اصلی — بارگذاری از .env با Pydantic v2"""

    model_config = SettingsConfigDict(
        env_file=str(BACKEND_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # === Application ===
    APP_ENV: Literal["development", "production"] = "development"
    APP_NAME: str = "Trading System"
    APP_VERSION: str = "0.2.0"

    # === API ===
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    API_PREFIX: str = "/api/v1"

    # === Security (اجباری از .env) ===
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # === Encryption (Fernet key — اجباری از .env) ===
    ENCRYPTION_KEY: str

    # === Database ===
    DB_PATH: str = "./trading.db"

    # === CORS ===
    FRONTEND_URL: str = "http://localhost:5173"

    # === Timezone ===
    TIMEZONE: str = "UTC"
    DISPLAY_TIMEZONE: str = "Asia/Tehran"

    # ============================================================
    # خصوصیات محاسبه‌شده
    # ============================================================

    @property
    def DATABASE_URL(self) -> str:
        """آدرس اتصال SQLAlchemy برای SQLite + aiosqlite.

        اگر DB_PATH مسیر relative باشد (مثل './trading.db')،
        آن را نسبت به BACKEND_DIR resolve می‌کنیم تا مسیر DB
        ثابت بماند حتی اگر اپ از پوشه دیگری اجرا شود.
        """
        db_path = Path(self.DB_PATH)
        if not db_path.is_absolute():
            db_path = BACKEND_DIR / self.DB_PATH
        return f"sqlite+aiosqlite:///{db_path.as_posix()}"

    @property
    def IS_DEVELOPMENT(self) -> bool:
        """آیا در محیط توسعه هستیم؟"""
        return self.APP_ENV == "development"

    @property
    def CORS_ORIGINS(self) -> list[str]:
        """لیست منشأهای مجاز برای CORS"""
        return [self.FRONTEND_URL]


# نمونه singleton — در سرتاسر برنامه از این استفاده می‌شود
settings = Settings()
'''


# ============================================================
# ۳) app/repositories/user_repository.py
# ============================================================
USER_REPOSITORY_PY = '''# -*- coding: utf-8 -*-
"""
UserRepository — Query های اختصاصی User
================================================================
متدهای CRUD از BaseRepository ارث می‌رسد + متدهای اختصاصی برای
احراز هویت.
================================================================
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository کاربر."""

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, User)

    async def get_by_username(self, username: str) -> User | None:
        """
        پیدا کردن کاربر فعال با username (soft-delete رعایت می‌شود).

        Returns:
            User یا None در صورت نبود
        """
        stmt = select(User).where(
            User.username == username,
            User.is_deleted.is_(False),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
'''


# ============================================================
# ۴) app/repositories/user_session_repository.py
# ============================================================
USER_SESSION_REPOSITORY_PY = '''# -*- coding: utf-8 -*-
"""
UserSessionRepository — Repository نشست‌های احراز هویت
================================================================
هر رکورد UserSession یک refresh token را نگه می‌دارد.
- login : ایجاد رکورد جدید
- logout: is_revoked=True
- refresh: فقط چک معتبر بودن (revoke نمی‌کنیم)

نکته: UserSession ستون is_deleted ندارد — BaseRepository این را
خودش از طریق hasattr تشخیص می‌دهد و filter سافت-دیلیت اعمال نمی‌شود.
================================================================
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_session import UserSession
from app.repositories.base import BaseRepository


class UserSessionRepository(BaseRepository[UserSession]):
    """Repository نشست‌های کاربر (refresh token)."""

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, UserSession)

    async def get_by_token(self, token: str) -> UserSession | None:
        """پیدا کردن نشست با مقدار token."""
        stmt = select(UserSession).where(UserSession.token == token)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
'''


# ============================================================
# ۵) app/repositories/__init__.py
# ============================================================
REPOSITORIES_INIT_PY = '''# -*- coding: utf-8 -*-
"""
Repositories — export سطح بالا
================================================================
استفاده پایه:
    from app.repositories import (
        BaseRepository,
        OhlcvRepository,
        SymbolRepository,
        UserRepository,
        UserSessionRepository,
    )

قانون قفل‌شده (سند ۳.۳):
  - هرگز Query مستقیم خارج از repositories/
  - service ها از Repository استفاده می‌کنند، نه از session مستقیم
================================================================
"""

from app.repositories.base import BaseRepository
from app.repositories.ohlcv_repository import OhlcvRepository
from app.repositories.symbol_repository import SymbolRepository
from app.repositories.user_repository import UserRepository
from app.repositories.user_session_repository import UserSessionRepository

__all__ = [
    "BaseRepository",
    "OhlcvRepository",
    "SymbolRepository",
    "UserRepository",
    "UserSessionRepository",
]
'''


# ============================================================
# ۶) app/schemas/auth.py
# ============================================================
SCHEMAS_AUTH_PY = '''# -*- coding: utf-8 -*-
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
'''


# ============================================================
# ۷) app/schemas/__init__.py
# ============================================================
SCHEMAS_INIT_PY = '''# -*- coding: utf-8 -*-
"""Pydantic schemas — DTO های پروژه."""

from app.schemas.auth import (
    LogoutRequest,
    RefreshRequest,
    TokenPair,
    UserMe,
)
from app.schemas.ohlcv import (
    OhlcvCandleOut,
    OhlcvImportResult,
    OhlcvListData,
    OhlcvRowSchema,
)

__all__ = [
    # OHLCV
    "OhlcvRowSchema",
    "OhlcvImportResult",
    "OhlcvCandleOut",
    "OhlcvListData",
    # Auth
    "TokenPair",
    "RefreshRequest",
    "LogoutRequest",
    "UserMe",
]
'''


# ============================================================
# ۸) app/services/auth_service.py
# ============================================================
AUTH_SERVICE_PY = '''# -*- coding: utf-8 -*-
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

from sqlalchemy.ext.asyncio import AsyncSession

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
'''


# ============================================================
# ۹) app/services/__init__.py
# ============================================================
SERVICES_INIT_PY = '''# -*- coding: utf-8 -*-
"""Services — منطق کسب‌وکار."""

from app.services.auth_service import AuthService

__all__ = ["AuthService"]
'''


# ============================================================
# ۱۰) app/api/v1/dependencies.py
# ============================================================
DEPENDENCIES_PY = '''# -*- coding: utf-8 -*-
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
'''


# ============================================================
# ۱۱) app/api/v1/routes/auth.py
# ============================================================
ROUTES_AUTH_PY = '''# -*- coding: utf-8 -*-
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
'''


# ============================================================
# ۱۲) app/api/v1/routes/ohlcv.py — افزودن Depends(get_current_user)
# ============================================================
ROUTES_OHLCV_PY = '''# -*- coding: utf-8 -*-
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

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user
from app.core.logging import get_logger
from app.core.response import success_response
from app.infrastructure.database import get_db
from app.models.user import User
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
        symbol_id, timeframe, current_user.username, len(candles), total,
    )

    return success_response(
        data=data.model_dump(mode="json"),
        message=f"{len(candles)} کندل بازگردانده شد",
    )
'''


# ============================================================
# ۱۳) backend/main.py — افزودن include_router(auth)
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

from app.api.v1.routes import auth, health, ohlcv
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
app.include_router(auth.router, prefix=settings.API_PREFIX)
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
# ۱۴) backend/requirements.txt
# ============================================================
REQUIREMENTS_TXT = """# ============================================================
# requirements.txt — سامانه هوشمند ترید
# نسخه: v0.2.0 (زیرگام ۵: Auth + JWT)
# ============================================================

# --- Web Framework ---
fastapi==0.111.0
uvicorn[standard]==0.29.0
python-multipart==0.0.9    # OAuth2PasswordRequestForm (multipart/form-data)

# --- Database & ORM ---
sqlalchemy==2.0.30
aiosqlite==0.20.0
alembic==1.13.1

# --- Validation & Settings ---
pydantic==2.7.1
pydantic-settings==2.2.1

# --- Authentication & Security ---
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
cryptography==42.0.7

# --- Environment ---
python-dotenv==1.0.1
colorama==0.4.6    # Windows ANSI colors support

# --- HTTP Client ---
httpx==0.27.0

# --- Data Processing (فاز ۶ - Excel Reader) ---
pandas==2.2.2
openpyxl==3.1.2

# ============================================================
# نکته: ccxt، websockets، python-telegram-bot
# در فازهای آینده طبق نیاز اضافه خواهند شد.
# ============================================================
"""


# ============================================================
# نقشه فایل‌ها → محتوا
# ============================================================
FILES_TO_WRITE: dict[Path, str] = {
    # core
    APP_DIR / "core" / "security.py": CORE_SECURITY_PY,
    APP_DIR / "core" / "config.py": CORE_CONFIG_PY,
    # repositories
    APP_DIR / "repositories" / "user_repository.py": USER_REPOSITORY_PY,
    APP_DIR / "repositories" / "user_session_repository.py": USER_SESSION_REPOSITORY_PY,
    APP_DIR / "repositories" / "__init__.py": REPOSITORIES_INIT_PY,
    # schemas
    APP_DIR / "schemas" / "auth.py": SCHEMAS_AUTH_PY,
    APP_DIR / "schemas" / "__init__.py": SCHEMAS_INIT_PY,
    # services
    APP_DIR / "services" / "auth_service.py": AUTH_SERVICE_PY,
    APP_DIR / "services" / "__init__.py": SERVICES_INIT_PY,
    # api
    APP_DIR / "api" / "v1" / "dependencies.py": DEPENDENCIES_PY,
    APP_DIR / "api" / "v1" / "routes" / "auth.py": ROUTES_AUTH_PY,
    APP_DIR / "api" / "v1" / "routes" / "ohlcv.py": ROUTES_OHLCV_PY,
    # root
    BACKEND_DIR / "main.py": MAIN_PY,
    BACKEND_DIR / "requirements.txt": REQUIREMENTS_TXT,
}


def main() -> None:
    print("=" * 64)
    print("اسکریپت ۲۲ — زیرگام ۵: Auth + JWT (v0.2.0)")
    print("=" * 64)
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
    print("=" * 64)
    print(f"✅ {len(FILES_TO_WRITE)} فایل نوشته/به‌روز شد.")
    print("=" * 64)
    print()
    print("مراحل بعد:")
    print()
    print("  [tab «2 scripts»]")
    print("    pip install python-multipart==0.0.9")
    print()
    print("  [tab «1 backend»]")
    print("    Ctrl+C  (توقف uvicorn اگر روشن است)")
    print("    uvicorn main:app --reload")
    print()
    print("  [tab «2 scripts»]")
    print("    python scripts\\23_test_auth.py")


if __name__ == "__main__":
    main()
