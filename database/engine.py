import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from database.models import Base

engine = create_async_engine(url=os.getenv("DB_URL"))
sessionmaker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
