import asyncio
import logging
import os

from dotenv import find_dotenv, load_dotenv
# load должен быть выше остальных импортов
load_dotenv(find_dotenv(), override=True)

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeDefault

from database.engine import create_all, sessionmaker
from handlers.user import user_router
from middlewares.database import DBSession



async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    dp.include_router(user_router)
    dp.update.middleware(DBSession(session_pool=sessionmaker))

    await bot.set_my_commands([
            BotCommand(command="start", description="Главное меню"),
        ],
        scope=BotCommandScopeDefault()
    )

    await create_all()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
