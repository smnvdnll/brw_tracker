import os
from typing import Any, Dict
from urllib.parse import urlencode

from services.http_client import HTTPClient


class BRWAPI(HTTPClient):
    """
    Class for interaction with Belarusian Railway API
    """

    def __init__(self):
        super().__init__()
        self.user_key = os.getenv("RAILWAYS_USER_KEY")
        self.base_url = os.getenv("RAILWAYS_BASE_URL")
        self.headers = {
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive",
            "Host": "apicast.rw.by",
            "User-Agent": "okhttp/4.9.1",
        }

    async def get_schedule_for_date(
        self, departure_station: str, arrival_station: str, departure_date: str
    ) -> Dict[str, Any]:
        """
        Method for getting schedule for specific date
        """

        endpoint = "/rasp/ru/index/route?"
        params = {
            "format": "json",
            "from": departure_station,
            "to": arrival_station,
            "date": departure_date,
            "user_key": self.user_key,
        }

        query_string = urlencode(params)
        url = f"{self.base_url}{endpoint}{query_string}"
        schedule = await self.get_json_response(url=url, headers=self.headers)
        return schedule
