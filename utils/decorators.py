import time

from loguru import logger
from functools import wraps


def log_execution_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()

        r = await func(*args, **kwargs)

        end_time = time.perf_counter()
        took_time = end_time - start_time

        logger.debug(f"Function {func.__name__} took: {took_time:.4f} seconds")
        return r
    return wrapper
