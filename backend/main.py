# -*- coding: utf-8 -*-
"""
نقطه ورود FastAPI — سامانه هوشمند ترید
================================================================
این فایل فقط شامل: app instance + middleware + handlers + router include.

قواعد قفل‌شده:
  - Business Logic در services/ — هرگز اینجا
  - Query در repositories/ — هرگز اینجا
  - Validation در schemas/ — هرگز اینجا

نحوه اجرا (در CMD 1):
    cd backend
    venv\\Scripts\\activate
    uvicorn main:app --reload
================================================================
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import health
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
