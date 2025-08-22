from typing import Any

from .exceptions import UnexpectedError
from ..utils.setup_logger import logger
from ..config import settings
from ..services.http_client import HttpClient
from ..schemas.schemas import RouteSchema
from .stations import get_station_code


class BrwAPI:
    def __init__(self, http_client: HttpClient):
        self.base_url = settings.BRW_BASE_URL
        self.http_client = http_client
        self.headers = settings.API_HEADERS
        self.user_key = settings.BRW_USER_KEY

    def _build_url(self, from_: str, to: str, date_iso: str) -> str:
        endpoint = "rasp/ru/index/route?"
        from_exp = get_station_code(from_)
        to_exp = get_station_code(to)
        url = f"{self.base_url}{endpoint}format=json&from_exp={from_exp}&to_exp={to_exp}&date={date_iso}&user_key={self.user_key}"
        return url

    async def _get_raw(self, from_: str, to: str, date_iso: str) -> str:
        url = self._build_url(from_, to, date_iso)
        logger.debug(f"Requesting URL: {url}")
        try:
            response_text = await self.http_client.get(url, headers=self.headers)
            return response_text
        except Exception as e:
            logger.error(f"Request failed. Error: {e}")
            raise

    async def _get_json(self, from_: str, to: str, date_iso: str) -> dict[str, Any]:
        import json
        raw = await self._get_raw(from_, to, date_iso)
        try:
            json_data = json.loads(raw)
            return json_data
        except json.JSONDecodeError:
            logger.error(f"JSON decode failed. Raw response: {raw[:300]}")
            raise

    def _raise_if_error(self, json_data: dict[str, Any]) -> None:
        err = json_data["e"].get("message")
        if err:
            raise UnexpectedError(err)

    async def _get_and_validate(self, from_: str, to: str, date_iso: str) -> RouteSchema:
        json_data = await self._get_json(from_, to, date_iso)
        self._raise_if_error(json_data)
        try:
            return RouteSchema.model_validate(json_data)
        except Exception as e:
            logger.error(f"Validation failed. Error: {e}")
            raise

    async def get_route_text(self, from_: str, to: str, date_iso: str) -> str:
        try:
            return await self._get_raw(from_, to, date_iso)
        except Exception as e:
            logger.critical(f"Failed to get route text: {e}")
            raise

    async def get_route(self, from_: str, to: str, date_iso: str) -> RouteSchema:
        try:
            return await self._get_and_validate(from_, to, date_iso)
        except Exception as e:
            logger.critical(f"Failed to get route: {e}")
            raise

