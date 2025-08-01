import json
import aiohttp
import backoff

from utils.decorators import log_execution_time
from utils.exceptions import InvalidResponseException
from utils.loggers import logger

class HTTPClient:
    def __init__(self, ):
        self.session: aiohttp.ClientSession = None
        self.init_session()

    def init_session(self) -> None:
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def close_session(self) -> None:
        if self.session:
            await self.session.close()
            self.session = None

    ### json.JSONDecodeError возникает только если schedule['e'] из-за неверной даты 
    # TODO придумать другую задержку
    @backoff.on_exception(
        backoff.expo,
        (json.JSONDecodeError, aiohttp.ClientError, InvalidResponseException),
        on_backoff=lambda details: logger.error(
            f"Error while sending request, retrying. Try: {details['tries']}, waiting: {details['wait']}, exception: {details['exception']}"
        ),
    )
    @log_execution_time
    async def get_json_response(self, url: str, *args, **kwargs) -> dict[str, str]:
        async with self.session.get(url, *args, **kwargs) as response:
            if response.status == 200:
                return await response.json()
            else:
                logger.error(f"Error while getting response: {response.status}")
                raise InvalidResponseException()

    async def post_json_response(self, url: str, *args, **kwargs) -> dict[str, str]:
        async with self.session.post(url, *args, **kwargs) as response:
            if response.status == 200:
                return await response.json()

    # async def delete_json_response(self, url: str, *args, **kwargs):
    #     ...
