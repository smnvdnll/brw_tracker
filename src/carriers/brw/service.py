from .schemas.dto import TrackerQueryDraft
from .validator import RouteValidator
from .api import BrwAPI


class BrwService:
    def __init__(self, api: BrwAPI):
        self.api = api

    async def validate_tracker(self, query: TrackerQueryDraft) -> None:
        RouteValidator.validate_tracker(query)

    async def get_trains(self, query: TrackerQueryDraft) -> list[str]:
        if not query.can_search_trains():
            raise ValueError("Not all fields are filled")

        assert query.from_ is not None
        assert query.to is not None
        assert query.date_ is not None

        route = await self.api.get_route(
            query.from_, 
            query.to, 
            query.date_.isoformat()
        )
        trains = [train.number for train in route.trains if not train.is_left]
        return trains
