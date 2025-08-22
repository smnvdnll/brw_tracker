import aiohttp

from src.config import settings
from .setup_logger import logger

class TelegramNotifier():
    def __init__(self, user_id: int, session: aiohttp.ClientSession) -> None:
        self.user_id: int = user_id
        self.session: aiohttp.ClientSession = session

    async def send_message(self, message: str):
        url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"
        data = { # pyright: ignore[reportUnknownVariableType]
            "chat_id": self.user_id,
            "text": message
        }
        async with self.session.post(url, data=data) as response:
            if response.status != 200:
                logger.error(
                    f"Failed to send message to Telegram: {response.status}"
                )