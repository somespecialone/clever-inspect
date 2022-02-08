from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from app.core.config import settings

__all__ = ("engine", "BaseModel")

engine = create_async_engine(
    settings.DB_URL,
    future=True,
    poolclass=AsyncAdaptedQueuePool,
    pool_size=2,
)

BaseModel = declarative_base()
