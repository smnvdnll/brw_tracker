import asyncio
from datetime import datetime, timezone

from src.settings import settings
from src.infrastructure.setup_logger import logger
from src.infrastructure.telegram import TelegramNotifier
from .api import BrwAPI
from .schemas.schemas import TrainSchema
from .schemas.dto import TrackerQuery


class BrwTracker:
    def __init__(
            self,
            query: TrackerQuery,
            tg_notifier: TelegramNotifier,
            brw_api: BrwAPI,
            user_id: int
        ) -> None:
        self.query: TrackerQuery = query
        self.tg_notifier: TelegramNotifier = tg_notifier
        self.api: BrwAPI = brw_api

        self.prev_train: TrainSchema | None = None
        self.dep_time: datetime | None = None

    async def _get_train(self, query: TrackerQuery) -> TrainSchema | None:
        logger.trace("Getting train...")
        route = await self.api.get_route(
            from_=query.from_,
            to=query.to,
            date_iso=self._ru_date_to_iso(query.date_ru)
        )
        logger.trace("Got train")
        return next((train for train in route.trains if train.number == query.train_number), None)

    async def _init_state(self, query: TrackerQuery) -> None:
        logger.trace("Initializing state...")
        train = await self._get_train(query)
        if not train:
            logger.error("Initial state failed: train is none")
            return
        self.prev_train = train
        self.dep_time = train.dep_time
        logger.trace(f"Initial state set: {self.prev_train}, dep_time: {self.dep_time}")

    def _get_diff(self, prev: TrainSchema, curr: TrainSchema) -> str:
        pm = {(p.type, s.class_service): s.free_places for p in prev.places for s in p.serving_class}
        cm = {(p.type, s.class_service): s.free_places for p in curr.places for s in p.serving_class}
        return "\n".join(
            f"{t} {c}: {(b:=pm.get((t,c),0))}→{(a:=cm.get((t,c),0))} ({(a-b):+d})"
            for (t, c) in sorted(set(pm) | set(cm))
            if pm.get((t,c),0) != cm.get((t,c),0)
        ) or "без изменений"

    def _ru_date_to_iso(self, date_ru: str) -> str:
        r = datetime.strptime(date_ru, "%d.%m.%Y").date().isoformat()
        return r

    async def run(self) -> None:
        logger.trace("Starting tracker...")
        await self._init_state(self.query)
        if not self.dep_time or not self.prev_train:
            logger.error("Initialization failed: dep_time or prev_train is None")
            return
        await asyncio.sleep(settings.API_TIMEOUT)

        logger.trace("Starting cycle...")
        while datetime.now().astimezone(timezone.utc) < self.dep_time:
            try:
                curr = await self._get_train(self.query)
            except Exception as e:
                logger.critical(f"Error while getting train: {e}")
                await asyncio.sleep(settings.API_TIMEOUT)

            if not curr:
                logger.error(f"Train {self.query.train_number} not found in route.")
                await asyncio.sleep(settings.API_TIMEOUT)
                continue

            if self.prev_train is not None:
                diff = self._get_diff(self.prev_train, curr)
                if diff != "без изменений":
                    logger.debug(f"Train {self.prev_train} has changed")
                    diff = self._get_diff(self.prev_train, curr)
                    logger.debug(f"Diff: {diff}")
                    message = (
                        f"Изменения в расписании поезда {self.prev_train}:\n{diff}"
                    )
                    logger.trace("Sending message to Telegram")
                    await self.tg_notifier.send_message(message)
                    logger.trace("Sent Telegram message")
                self.prev_train = curr

            await asyncio.sleep(settings.API_TIMEOUT)