from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from ...database.repository import UserRepository

user_router = Router()


@user_router.message(CommandStart())
async def start_handler(message: Message, users: UserRepository):
    await message.answer("Welcome! I'm your bot.")