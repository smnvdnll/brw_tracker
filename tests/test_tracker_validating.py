from datetime import date
import pytest

from freezegun import freeze_time

from src.carriers.brw.exceptions import InvalidDate, StationNotFound
from src.carriers.brw.validator import RouteValidator
from src.carriers.brw.stations import get_station_code
from src.carriers.brw.schemas.dto import TrackerQueryDraft


def test_existing_stations(mocker):
    mocker.patch("src.carriers.brw.stations.load_stations", return_value={"Минск": "2100000"})
    assert RouteValidator.is_station_has_code("Минск") is True
    assert get_station_code("Минск") == "2100000"

def test_non_existing_stations(mocker):
    mocker.patch("src.carriers.brw.stations.load_stations", return_value={"Минск": "2100000"})
    assert RouteValidator.is_station_has_code("Хогвартс") is False
    assert get_station_code("Хогвартс") is None

@freeze_time("2025-08-20")
def test_valid_date(mocker):
    assert RouteValidator.is_date_valid(date(2025, 8, 20)) 
    assert RouteValidator.is_date_valid(date(2025, 10, 14)) # + 55 days
    assert not RouteValidator.is_date_valid(date(2025, 10, 15)) # + 56 days
    assert not RouteValidator.is_date_valid(date(2025, 8, 19)) # < today

@freeze_time("2025-08-20")
def test_validate_tracker(mocker):
    mocker.patch("src.carriers.brw.stations.load_stations", return_value={"Минск": "2100000", "Брест": "2100150"})
    class FrozenDate(date):
        @classmethod
        def today(cls):
            return cls(2025, 8, 20)

    mocker.patch("datetime.date", FrozenDate)
    assert RouteValidator.validate_tracker(TrackerQueryDraft(from_="Минск", to="Брест", date_=date(2025, 8, 20))) is None
    assert RouteValidator.validate_tracker(TrackerQueryDraft(from_="Брест", to="Минск", date_=date(2025, 8, 20))) is None
    with pytest.raises(StationNotFound):
        RouteValidator.validate_tracker(TrackerQueryDraft(from_="Хогвартс", to="Брест", date_=date(2025, 8, 20)))
    with pytest.raises(InvalidDate):
        RouteValidator.validate_tracker(TrackerQueryDraft(from_="Минск", to="Брест", date_=date(2025, 10, 15)))
    with pytest.raises(InvalidDate):
        RouteValidator.validate_tracker(TrackerQueryDraft(from_="Минск", to="Брест", date_=date(2024, 10, 15)))