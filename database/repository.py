from typing import Type, TypeVar, Generic, List
from sqlalchemy import select, update
import sqlalchemy
import sqlalchemy.exc
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User, BRWTracker

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def get_all(self) -> List[T]:
        query = select(self.model)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_all_by_params(self, *args, **kwargs) -> T:
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_first_by_params(self, *args, **kwargs) -> T:
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def set_value_by_params(self, filters: dict, values: dict) -> None:
        query = update(self.model).filter_by(**filters).values(**values)
        await self.session.execute(query)
        await self.session.commit()

    async def add(self, entity: T) -> None:
        try:
            self.session.add(entity)
            await self.session.flush()
            new_entity = entity
            await self.session.commit()
            return new_entity
        # трекеры так или иначе уникальные, и второй раз добавить такой же не получится, а юзер пытается добавиться каждый раз при /start
        except sqlalchemy.exc.IntegrityError:
            pass

    async def delete(self, entity: T) -> None:
        await self.session.delete(entity)
        await self.session.commit()

    async def refresh(self, entity: T) -> T:
        await self.session.refresh(entity)
        return entity


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=User)

    async def get_user_by_telegram_id(self, telegram_id: int):
        user = await self.get_by_params(telegram_id=telegram_id)
        return user


class BRWTrackerRepository(BaseRepository[BRWTracker]):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=BRWTracker)

    async def get_brw_tracker_by_id(self, tracker_id) -> BRWTracker:
        query = select(BRWTracker).where(BRWTracker.id == tracker_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_brw_trackers_by_user_id(self, user_id: int) -> list[BRWTracker]:
        query = select(BRWTracker).where(BRWTracker.user_telegram_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def is_tracker_turned_on(self, tracker_id: int) -> bool:
        tracker: BRWTracker = await self.get_brw_tracker_by_id(tracker_id)
        return tracker.is_turned_on
