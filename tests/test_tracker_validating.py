from datetime import datetime
import pytest

from src.carriers.brw.exceptions import InvalidDate, StationNotFound
from src.carriers.brw.validator import RouteValidator
from src.carriers.brw.stations import get_station_code


def test_existing_stations(mocker):
    mocker.patch("src.carriers.brw.stations.load_stations", return_value={"Минск": "2100000"})
    assert RouteValidator.is_station_has_code("Минск") is True
    assert get_station_code("Минск") == "2100000"

def test_non_existing_stations(mocker):
    mocker.patch("src.carriers.brw.stations.load_stations", return_value={"Минск": "2100000"})
    assert RouteValidator.is_station_has_code("Хогвартс") is False
    assert get_station_code("Хогвартс") is None

def test_valid_date(mocker):
    class FrozenDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(2025, 8, 20, tzinfo=tz)

    mocker.patch("src.carriers.brw.validator.datetime", FrozenDatetime)
    assert RouteValidator.is_date_valid("20.08.2025")
    assert RouteValidator.is_date_valid("14.10.2025") # + 55 days
    assert not RouteValidator.is_date_valid("15.10.2025") # + 56 days
    assert not RouteValidator.is_date_valid("19.08.2025") # < today

def test_validate_tracker(mocker):
    mocker.patch("src.carriers.brw.stations.load_stations", return_value={"Минск": "2100000", "Брест": "2100150"})
    class FrozenDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(2025, 8, 20, tzinfo=tz)

    mocker.patch("src.carriers.brw.validator.datetime", FrozenDatetime)
    assert RouteValidator.validate_tracker("Минск", "Брест", "20.08.2025") is None
    assert RouteValidator.validate_tracker("Брест", "Минск", "20.09.2025") is None
    with pytest.raises(StationNotFound):
        RouteValidator.validate_tracker("Хогвартс", "Брест", "20.08.2025")
    with pytest.raises(InvalidDate):
        RouteValidator.validate_tracker("Минск", "Брест", "15.10.2025")
    with pytest.raises(InvalidDate):
        RouteValidator.validate_tracker("Минск", "Брест", "15.10.2024")