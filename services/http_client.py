from sys import exc_info
from typing import Dict
import aiohttp
import backoff

from utils.decorators import log_execution_time
from utils.exceptions import TrainNotFoundException
from utils.loggers import logger

class HTTPClient:
    def __init__(self):
        self.session: aiohttp.ClientSession = None
        self.base_url: str = None
        self.init_session()

    def init_session(self) -> None:
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def close_session(self) -> None:
        if self.session:
            await self.session.close()
            self.session = None

    # TODO сюда backoff добавить, тестить логгер, тестить обработку исключений
    # @backoff.on_exception(
    #     backoff.expo,
    #     (),
    #     jitter=backoff.full_jitter,
    # )
    @log_execution_time
    async def get_json_response(self, url: str, *args, **kwargs) -> Dict[str, str]:
        try:
            logger.info(f"sending request for url {url}...")
            async with self.session.get(url, *args, **kwargs) as response:
                if response.status == 200:
                    return await response.json()
        except Exception as e:
            logger.error(f"Failed to get response from {url}: {e}", exc_info=True)
            return None

    async def post_json_response(self, url: str, *args, **kwargs) -> Dict[str, str]:
        async with self.session.post(url, *args, **kwargs) as response:
            if response.status == 200:
                return await response.json()

    # async def delete_json_response(self, url: str, *args, **kwargs):
    #     ...
