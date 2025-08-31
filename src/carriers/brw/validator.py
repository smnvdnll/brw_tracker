from datetime import date, timedelta

from src.infrastructure.setup_logger import logger
from .exceptions import InvalidDate, StationNotFound
from .stations import get_station_code
from .schemas.dto import TrackerQueryDraft


class RouteValidator:
    @staticmethod
    def is_station_has_code(station_name: str) -> bool:
        logger.trace("Validating tracker's station code")
        station_uic = get_station_code(station_name)
        logger.trace(f"Checking station '{station_name}' UIC code: {station_uic}")
        return station_uic is not None

    @staticmethod
    def is_date_valid(date: date) -> bool:
        logger.trace("Validating tracker's date")        
        now = date.today()
        if date < now or date > now + timedelta(days=55):
            return False

        return True

    @staticmethod
    def validate_tracker(query: TrackerQueryDraft) -> None:
        logger.trace("Validating tracker...")
        if query.from_ is not None and not RouteValidator.is_station_has_code(query.from_):
            raise StationNotFound(name=query.from_)
        if query.to is not None and not RouteValidator.is_station_has_code(query.to):
            raise StationNotFound(name=query.to)
        if query.date_ is not None and not RouteValidator.is_date_valid(query.date_):
            raise InvalidDate()
        logger.trace("Tracker validation passed")
