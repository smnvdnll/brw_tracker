import os
from loguru import logger
from logging import Handler
import aiohttp
import asyncio


logger.add(
    sink="logs/logs.log",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {function}:{line} - {exception} {message}",
    rotation="1 week"
)

# class TelegramHandler(Handler):
#     def emit(self, record):
#         log_entry = self.format(record)
#         asyncio.run(self.send_to_telegram(log_entry))

#     async def send_to_telegram(self, message: str):
#         url = f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/sendMessage"
#         data = {
#             "chat_id": 1776210788,
#             "text": message
#         }
#         print("qwe")
#         async with aiohttp.ClientSession() as session:
#             async with session.post(url, data=data) as response:
#                 if response.status != 200:
#                     logger.error(f"Failed to send message to Telegram: {response.status}")

# tg_handler = TelegramHandler()

# logger.add(sink=tg_handler, level="DEBUG", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {function}:{line} - {message}")



if __name__ == "__main__":
    logger.debug("Test message")
    logger.info("Test message")
    logger.warning("Test message")
    logger.error("Test message")
    logger.critical("Test message")