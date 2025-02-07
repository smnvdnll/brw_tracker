import json
from pathlib import Path


def load_stations():
    base_dir = Path(__file__).resolve().parent.parent
    stations_path = base_dir / "common" / "stations.json"
    with stations_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def is_station_exists(station: str) -> bool:
    stations = load_stations()
    return station in stations
