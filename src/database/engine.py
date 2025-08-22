from ..config import settings

from sqlalchemy.ext.asyncio import (
    AsyncSession, 
    async_sessionmaker,
    create_async_engine
)

engine = create_async_engine(
    url=settings.db_uri,
)

sessionmaker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    # autoflush=True
)
