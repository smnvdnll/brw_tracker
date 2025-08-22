from typing import Generic, Type, TypeVar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User, BrwTracker


T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]) -> None:
        self.session = session
        self.model = model

    async def get_all(self) -> list[T]:
        query = select(self.model)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def add(self, item: T) -> None:
        self.session.add(item)
        await self.session.commit()

    async def delete(self, item: T) -> None:
        await self.session.delete(item)
        await self.session.commit()


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)


class BrwTrackerRepository(BaseRepository[BrwTracker]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, BrwTracker)

    async def get_by_tg_id(self, tg_id: int) -> list[BrwTracker]:
        query = select(self.model).where(self.model.user_id == tg_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())