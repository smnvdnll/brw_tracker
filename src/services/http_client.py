import asyncio
import time
from functools import wraps

import aiohttp

from ..utils.setup_logger import logger


def log_execution_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()

        r = await func(*args, **kwargs)

        end_time = time.perf_counter()
        took_time = end_time - start_time

        logger.debug(f"Request took: {took_time:.4f} seconds")
        return r
    return wrapper


class HttpClient:
    def __init__(self, total_timeout: int = 5):
        timeout = aiohttp.ClientTimeout(
            total=total_timeout # no point in waiting longer, cause server may take up 60s to respond
        )
        self.session = aiohttp.ClientSession(timeout=timeout)

    async def close_session(self) -> None:
        if self.session:
            await self.session.close()

    @log_execution_time
    async def get(self, url: str, headers: dict[str, str]) -> str:
        try:
            async with self.session.get(url, headers=headers) as response:
                response.raise_for_status()
                html = await response.text()
            return str(html)
        except asyncio.TimeoutError:
            logger.error("Request timed out")
            raise
        except Exception as e:
            logger.error(f"Error occurred while making GET request: {e}")
            raise