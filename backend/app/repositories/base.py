# -*- coding: utf-8 -*-
"""
BaseRepository — کلاس پایه Generic برای همه Repository ها
================================================================
این کلاس CRUD کامل + Pagination + Filtering + Soft Delete را
به‌صورت Generic برای SQLAlchemy 2.0 async فراهم می‌کند.

نمونه استفاده در فازهای بعد:

    from sqlalchemy import select
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.models import User
    from app.repositories.base import BaseRepository


    class UserRepository(BaseRepository[User]):
        def __init__(self, db: AsyncSession) -> None:
            super().__init__(db, User)

        async def get_by_username(self, username: str) -> User | None:
            stmt = select(User).where(
                User.username == username,
                User.is_deleted.is_(False),
            )
            result = await self.db.execute(stmt)
            return result.scalar_one_or_none()


قوانین قفل‌شده مرتبط:
  - سند ۳.۳: تمام Query ها در Repository ها — هرگز در services/ یا api/
  - سند ۵.۰: Soft Delete پیش‌فرض (نادیده گرفتن is_deleted=True در queries)

مدیریت Transaction:
  - این کلاس فقط flush() می‌زند (برای پر شدن id و آپدیت stateحرف)
  - commit() مسئولیت لایه service است
  - rollback() در get_db (session.py) خودکار در صورت Exception
================================================================
"""

from typing import Any, Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    BusinessLogicError,
    ConflictError,
    NotFoundError,
)
from app.core.logging import get_logger
from app.infrastructure.database import Base

logger = get_logger(__name__)


# Generic Type Variable - bound به Base یعنی هر مدلی که از Base ارث برده
ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    کلاس پایه CRUD برای همه Repository ها.

    Type Parameter:
        ModelType: نوع مدل SQLAlchemy (باید زیرکلاس Base باشد)

    Soft Delete:
        اگر مدل ستون `is_deleted` داشته باشد، queries پیش‌فرض
        رکوردهای is_deleted=True را نادیده می‌گیرند.
        برای دیدن همه (شامل حذف‌شده) از include_deleted=True.
    """

    def __init__(self, db: AsyncSession, model: type[ModelType]) -> None:
        """
        Args:
            db: AsyncSession جاری (معمولاً از get_db تزریق می‌شود)
            model: کلاس مدل SQLAlchemy (مثلاً User)
        """
        self.db = db
        self.model = model

    # ================================================================
    # توابع کمکی داخلی
    # ================================================================

    def _supports_soft_delete(self) -> bool:
        """آیا مدل از soft delete پشتیبانی می‌کند؟ (ستون is_deleted دارد؟)"""
        return hasattr(self.model, "is_deleted")

    def _apply_soft_delete_filter(self, stmt, include_deleted: bool):
        """افزودن فیلتر `is_deleted == False` در صورت لزوم."""
        if not include_deleted and self._supports_soft_delete():
            stmt = stmt.where(self.model.is_deleted.is_(False))
        return stmt

    def _apply_filters(self, stmt, filters: dict[str, Any]):
        """اعمال فیلترهای کلید=مقدار (مثلاً user_id=5)."""
        for key, value in filters.items():
            if not hasattr(self.model, key):
                raise BusinessLogicError(
                    message=f"فیلد {key!r} در {self.model.__name__} وجود ندارد",
                    code="INVALID_FILTER_FIELD",
                )
            stmt = stmt.where(getattr(self.model, key) == value)
        return stmt

    # ================================================================
    # Read Operations
    # ================================================================

    async def get(
        self,
        id: int,
        include_deleted: bool = False,
    ) -> ModelType | None:
        """
        دریافت رکورد با id. None در صورت نبود.

        Args:
            id: شناسه رکورد
            include_deleted: شامل رکوردهای حذف‌شده هم باشد؟
        """
        stmt = select(self.model).where(self.model.id == id)
        stmt = self._apply_soft_delete_filter(stmt, include_deleted)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_or_404(self, id: int) -> ModelType:
        """دریافت رکورد یا raise NotFoundError."""
        obj = await self.get(id)
        if obj is None:
            raise NotFoundError(
                message=f"{self.model.__name__} با شناسه {id} یافت نشد",
                code=f"{self.model.__name__.upper()}_NOT_FOUND",
            )
        return obj

    async def list(
        self,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
        order_by: str | None = None,
        **filters: Any,
    ) -> list[ModelType]:
        """
        لیست رکوردها با pagination و filtering.

        Args:
            skip: تعداد رکوردهای رد‌شده (offset)
            limit: حداکثر تعداد نتیجه
            include_deleted: شامل رکوردهای حذف‌شده؟
            order_by: نام ستون برای ترتیب صعودی (پیش‌فرض id)
            **filters: فیلترهای کلید=مقدار (مثلاً user_id=5)

        Returns:
            list مدل‌ها (می‌تواند خالی باشد)
        """
        stmt = select(self.model)
        stmt = self._apply_filters(stmt, filters)
        stmt = self._apply_soft_delete_filter(stmt, include_deleted)

        # تعیین ترتیب
        if order_by:
            if not hasattr(self.model, order_by):
                raise BusinessLogicError(
                    message=f"فیلد ترتیب {order_by!r} در {self.model.__name__} وجود ندارد",
                    code="INVALID_ORDER_FIELD",
                )
            stmt = stmt.order_by(getattr(self.model, order_by))
        else:
            stmt = stmt.order_by(self.model.id)

        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count(
        self,
        include_deleted: bool = False,
        **filters: Any,
    ) -> int:
        """شمارش رکوردها با filter."""
        stmt = select(func.count()).select_from(self.model)
        stmt = self._apply_filters(stmt, filters)
        stmt = self._apply_soft_delete_filter(stmt, include_deleted)
        result = await self.db.execute(stmt)
        return int(result.scalar_one())

    async def exists(self, **filters: Any) -> bool:
        """آیا حداقل یک رکورد با این فیلترها وجود دارد؟"""
        return (await self.count(**filters)) > 0

    # ================================================================
    # Write Operations
    # ================================================================

    async def create(self, **kwargs: Any) -> ModelType:
        """
        ایجاد رکورد جدید.

        Args:
            **kwargs: مقادیر ستون‌ها

        Returns:
            رکورد ساخته‌شده با id پر شده

        Raises:
            ConflictError: اگر تعارض دیتابیس رخ دهد (UNIQUE/FK)
        """
        obj = self.model(**kwargs)
        self.db.add(obj)
        try:
            await self.db.flush()        # برای پر شدن id
            await self.db.refresh(obj)   # برای خواندن default ها (created_at, ...)
        except IntegrityError as e:
            logger.warning(
                "IntegrityError هنگام create %s: %s",
                self.model.__name__, getattr(e, "orig", e),
            )
            raise ConflictError(
                message=f"تعارض دیتابیس در ایجاد {self.model.__name__}",
                code="DB_INTEGRITY_ERROR",
                details={"reason": str(getattr(e, "orig", e))},
            ) from e
        return obj

    async def update(self, id: int, **kwargs: Any) -> ModelType:
        """
        به‌روزرسانی رکورد.

        Args:
            id: شناسه رکورد
            **kwargs: ستون‌هایی که باید آپدیت شوند

        Raises:
            NotFoundError: اگر رکورد یافت نشود
            ConflictError: اگر تعارض دیتابیس رخ دهد
            BusinessLogicError: اگر کلیدی نامعتبر باشد
        """
        obj = await self.get_or_404(id)
        for key, value in kwargs.items():
            if not hasattr(obj, key):
                raise BusinessLogicError(
                    message=f"فیلد {key!r} در {self.model.__name__} وجود ندارد",
                    code="INVALID_UPDATE_FIELD",
                )
            setattr(obj, key, value)
        try:
            await self.db.flush()
            await self.db.refresh(obj)
        except IntegrityError as e:
            logger.warning(
                "IntegrityError هنگام update %s id=%d: %s",
                self.model.__name__, id, getattr(e, "orig", e),
            )
            raise ConflictError(
                message=f"تعارض دیتابیس در به‌روزرسانی {self.model.__name__}",
                code="DB_INTEGRITY_ERROR",
                details={"reason": str(getattr(e, "orig", e))},
            ) from e
        return obj

    # ================================================================
    # Delete Operations
    # ================================================================

    async def soft_delete(self, id: int) -> ModelType:
        """
        حذف نرم — فقط is_deleted=True تنظیم می‌شود.

        Raises:
            BusinessLogicError: اگر مدل از soft delete پشتیبانی نکند
            NotFoundError: اگر رکورد یافت نشود
        """
        if not self._supports_soft_delete():
            raise BusinessLogicError(
                message=f"{self.model.__name__} از soft delete پشتیبانی نمی‌کند",
                code="SOFT_DELETE_NOT_SUPPORTED",
            )
        obj = await self.get_or_404(id)
        obj.is_deleted = True
        await self.db.flush()
        await self.db.refresh(obj)
        return obj

    async def restore(self, id: int) -> ModelType:
        """
        بازگردانی رکورد حذف‌شده (is_deleted=False).

        Raises:
            BusinessLogicError: اگر مدل از soft delete پشتیبانی نکند
            NotFoundError: اگر رکورد یافت نشود
        """
        if not self._supports_soft_delete():
            raise BusinessLogicError(
                message=f"{self.model.__name__} از soft delete پشتیبانی نمی‌کند",
                code="SOFT_DELETE_NOT_SUPPORTED",
            )
        obj = await self.get(id, include_deleted=True)
        if obj is None:
            raise NotFoundError(
                message=f"{self.model.__name__} با شناسه {id} یافت نشد",
                code=f"{self.model.__name__.upper()}_NOT_FOUND",
            )
        obj.is_deleted = False
        await self.db.flush()
        await self.db.refresh(obj)
        return obj

    async def hard_delete(self, id: int) -> None:
        """
        حذف فیزیکی رکورد — قابل بازگشت نیست.

        ⚠ هشدار: ترجیح بدهید از soft_delete استفاده کنید.
        این متد فقط برای موارد خاص (پاکسازی audit log قدیمی،
        پاکسازی session های منقضی، حذف غیرقابل بازگشت توسط admin) است.

        Raises:
            NotFoundError: اگر رکورد یافت نشود
        """
        obj = await self.get(id, include_deleted=True)
        if obj is None:
            raise NotFoundError(
                message=f"{self.model.__name__} با شناسه {id} یافت نشد",
                code=f"{self.model.__name__.upper()}_NOT_FOUND",
            )
        await self.db.delete(obj)
        await self.db.flush()
        logger.info(
            "Hard delete %s id=%d انجام شد",
            self.model.__name__, id,
        )
