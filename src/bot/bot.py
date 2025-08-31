import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from src.bot.brw.handlers import brw_router
from src.settings import settings
from src.database.engine import create_all, sessionmaker
from .common.handlers import user_router
from .common.middlewares import CallbackLoggerMiddleware, DatabaseMiddleware



async def main():
    logging.basicConfig(level=logging.DEBUG)

    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(user_router)
    dp.include_router(brw_router)
    dp.update.middleware(DatabaseMiddleware(session_pool=sessionmaker))
    dp.callback_query.middleware(CallbackLoggerMiddleware())

    await bot.set_my_commands([
            BotCommand(command="start", description="Главное меню"),
        ],
        scope=BotCommandScopeDefault()
    )

    await bot.delete_webhook(drop_pending_updates=True)

    await create_all()
    await dp.start_polling(bot)

def run_bot():
    asyncio.run(main())
