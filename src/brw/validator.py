from datetime import datetime, timedelta

from ..utils.setup_logger import logger
from .exceptions import InvalidDate, StationNotFound
from .stations import get_station_code


class RouteValidator:
    @staticmethod
    def is_station_has_code(station_name: str) -> bool:
        logger.trace("Validating tracker's station code")
        station_uic = get_station_code(station_name)
        logger.trace(f"Checking station '{station_name}' UIC code: {station_uic}")
        return station_uic is not None

    @staticmethod
    def is_date_valid(date_ru: str) -> bool:
        logger.trace("Validating tracker's date")
        try:
            parsed_date = datetime.strptime(date_ru, "%d.%m.%Y")
        except ValueError:
            return False
        
        now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if parsed_date < now or parsed_date > now + timedelta(days=55):
            return False

        return True

    @staticmethod
    def validate_tracker(from_: str, to: str, date_ru: str) -> None:
        logger.trace("Validating tracker...")
        if not RouteValidator.is_station_has_code(from_):
            raise StationNotFound(name=from_)
        if not RouteValidator.is_station_has_code(to):
            raise StationNotFound(name=to)
        if not RouteValidator.is_date_valid(date_ru):
            raise InvalidDate()
        logger.trace("Tracker validation passed")
