import os
import asyncio
from datetime import datetime
from typing import Any, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from common.lexicon import BRWMessages as lxc
from database.models import BRWTracker
from database.repository import BRWTrackerRepository
from services.brw_api import BRWAPI
from utils.exceptions import TrainNotFoundException, RwBackendException
from utils.loggers import logger
REQUEST_TIMEOUT = int(os.getenv("TIMEOUT_BETWEEN_REQUESTS"))


class BRWTrackerManager(BRWAPI):
    """
    Representing monitoring unit for one train by its number for specific user
    """

    def __init__(self, brw_tracker: BRWTracker, db_session: AsyncSession):
        super().__init__()
        self.brw_db_repo: BRWTrackerRepository = BRWTrackerRepository(db_session)
        self.brw_tracker: BRWTracker = brw_tracker

    async def get_train_info(self) -> Dict[str, Any]:
        """
        Метод для получения полной информации об одном конкретном поезде
        """
        schedule = await self.get_schedule_for_date(
            self.brw_tracker.departure_station,
            self.brw_tracker.arrival_station,
            self.brw_tracker.departure_date
        )

        # Если расписание не пустое
        if schedule is not None:

            # Если какая-то внутрення ошибка БЧ
            if schedule['e'].get('type') == "RwBackendException":
                logger.error(f"Some RwBackendException. schedule['e']: {schedule['e']}")
                raise RwBackendException()

            # Пытаемся найти поезд в расписании
            # try:
            logger.debug(f"Trying to find train")
            route = next(
                (
                    route
                    for route in schedule["routes"]
                    if route["train_number"] == self.brw_tracker.train_number
                ),
                None,
            )

            # Было получено нормальное расписание, но поезд найден все равно не был найден, завершаем мониторинг
            if route is None:
                raise TrainNotFoundException()

            return route
        # а чо если schedule is None

    def extract_places(self, route: dict[str, str]) -> dict[str, str]:
        try:
            logger.debug(f"Extracting places from route {route}")
            # TODO заточено только под один тип места, надо будет сделать для всех
            new_places = {
                place["classservice"]: place["places"]
                for place in route["places"][0]["price_multi"]
            }

            return new_places

        # Места пустые (route['places'][0]['price_multi'] == [])
        except IndexError:
            logger.info(f"IndexError")
        # TODO ак то более явно описать эту ошибку
            return {}
        except Exception as e:
            logger.error(f"Unexcepted error while extracting places. Error: {e}")

    def compare_places(self, old_places: dict[str, str], new_places: dict[str, str]) -> str:
        message = "Класс мест: старое количество -> новое количество\n"
        old_places = {} if old_places is None else old_places
        new_places = {} if new_places is None else new_places
        keys = set(new_places | old_places)
        for key in keys:
            difference = f"{key}: {old_places.get(key, 0)} -> {new_places.get(key, 0)}\n"
            message += difference
        return message

    async def send_to_telegram(self, message: str):
        url = f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/sendMessage"
        data = {
            "chat_id": self.brw_tracker.user_telegram_id,
            "text": message
        }
        async with self.session.post(url, data=data) as response:
            if response.status != 200:
                logger.error(
                    f"Failed to send message to Telegram: {response.status}"
                )

    async def monitor_places(self):
        old_places = None

        await self.send_to_telegram(lxc.monitoring_started)
        while self.brw_tracker.is_turned_on: # TODO может быть избавиться от параметра и проверять в целом на существование трекера в бд
            try:
                route = await self.get_train_info()

                departure_time = datetime.strptime(
                    route["from_time_formatted"], "%Y-%m-%d %H:%M:%S"
                )
                
                if datetime.now() >= departure_time:
                    await self.send_to_telegram(lxc.train_already_leaved)
                    break

                new_places = self.extract_places(route)

                if new_places != old_places:
                    message = self.compare_places(old_places, new_places)
                    await self.send_to_telegram(f"Изменения в мониторинге {self.brw_tracker}:\n\n{message}")
                    old_places = new_places

                await asyncio.sleep(REQUEST_TIMEOUT)

                await self.brw_db_repo.refresh(self.brw_tracker)
                self.brw_tracker.is_turned_on = await self.brw_db_repo.is_tracker_turned_on(self.brw_tracker.id)

            except TrainNotFoundException: # Поезд не был найден в расписании, завершаем мониторинг
                await self.send_to_telegram(lxc.train_not_found)
                logger.error(f"Train not found {self.brw_tracker}")
                break
            except RwBackendException: # Ошибка на стороне БЧ
                logger.error(f"RwBackendException {self.brw_tracker}")
                await asyncio.sleep(REQUEST_TIMEOUT)
            except Exception as e: # То что не попало в другие исключения
                logger.critical(f"Unexpected error while monitoring: {e}. Tracker: {self.brw_tracker}")
                await asyncio.sleep(REQUEST_TIMEOUT)

        await self.send_to_telegram(lxc.monitoring_ended)
        await self.brw_db_repo.delete(self.brw_tracker)
        await self.close_session()
