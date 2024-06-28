from sqlalchemy import Column, DateTime, String, func, BigInteger
from sqlalchemy.sql.sqltypes import Boolean


class BaseModelMixin:
    is_active = Column(Boolean, default=True, nullable=False)
    views = Column(BigInteger, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        index=True,
    )

    def increment_views(self):
        self.views += 1
        self.save()


class SlugBaseModelMixin(BaseModelMixin):
    slug = Column(String, index=True, unique=True, nullable=False)
