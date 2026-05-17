# -*- coding: utf-8 -*-
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
