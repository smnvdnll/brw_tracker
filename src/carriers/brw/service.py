from .tracker import BrwTracker
from .schemas.dto import TrackerQuery
from .validator import RouteValidator
from .api import BrwAPI


class BrwService:
    def __init__(self, api: BrwAPI, tracker: BrwTracker):
        self.api = api
        self.tracker = tracker

    async def validate_tracker(self, from_: str, to: str, date: str) -> None:
        RouteValidator.validate_tracker(from_, to, date)

    async def get_trains(self, from_: str, to: str, date: str) -> list[str]:
        route = await self.api.get_route(from_, to, date)
        trains = [train.number for train in route.trains]
        return trains
