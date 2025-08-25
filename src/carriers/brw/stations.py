import json
from pathlib import Path
from functools import lru_cache


@lru_cache(maxsize=1)
def load_stations() -> dict[str, str]:
    data_path = Path(__file__).resolve().parent / "data" / "belarusian_stations.json"
    with data_path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def get_station_code(station_name: str) -> str | None:
    stations = load_stations()
    return stations.get(station_name)