# -*- coding: utf-8 -*-
"""
نقطه ورود FastAPI — سامانه هوشمند ترید
================================================================
این فایل فقط شامل: app instance + middleware + router include.

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


# ============================================================
# Lifecycle Events (Startup / Shutdown)
# ============================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """مدیریت چرخه عمر اپلیکیشن"""
    # ===== Startup =====
    print("=" * 60)
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"   Environment: {settings.APP_ENV}")
    print(f"   API: http://{settings.API_HOST}:{settings.API_PORT}{settings.API_PREFIX}")
    print(f"   Docs: http://{settings.API_HOST}:{settings.API_PORT}/docs")
    print("=" * 60)

    yield

    # ===== Shutdown =====
    print(f"👋 {settings.APP_NAME} shutting down...")


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
# CORS — اجازه دسترسی Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# نکته: سایر middleware ها (Rate Limit, Auth, RBAC, Input Sanitize,
# Audit Log) طبق ترتیب سند ۶ در گام‌های بعد اضافه می‌شوند.


# ============================================================
# Router Registration
# ============================================================
app.include_router(health.router, prefix=settings.API_PREFIX)


# ============================================================
# Root Endpoint
# ============================================================
@app.get("/")
async def root() -> dict:
    """صفحه ریشه — اطلاعات کلی"""
    return {
        "success": True,
        "message": "سامانه هوشمند ترید فعال است",
        "data": {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "health": f"{settings.API_PREFIX}/health",
        },
        "errors": None,
    }
