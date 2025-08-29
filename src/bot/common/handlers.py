from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
import sqlalchemy.exc

from .callbacks import CarriersCallback
from .enum import Carrier
from .states import CommonStates
from .keyboards import make_main_kb
from .lexicon import Messages as MessagesCommon
from src.bot.brw.keyboards import make_trackers_kb
from src.bot.brw.lexicon import Messages as MessagesBrw
from src.database.models import User
from src.database.repository import UserRepository


user_router = Router()


@user_router.message(CommandStart())
async def start_handler(message: Message, users_repo: UserRepository, state: FSMContext):
    if message.from_user:
        try:
            await users_repo.add(User(id=message.from_user.id))
        except sqlalchemy.exc.IntegrityError:
            pass

    await state.set_state(CommonStates.choosing_carrier)
    await message.answer(MessagesCommon.START, reply_markup=make_main_kb())


@user_router.callback_query(CarriersCallback.filter())
async def carriers_handler(call: CallbackQuery, callback_data: CarriersCallback):
    if not isinstance(call.message, Message):
        return

    carrier = callback_data.carrier
    if carrier == Carrier.BRW:
        await call.message.edit_text(MessagesBrw.LIST_TRACKERS, reply_markup=make_trackers_kb())
        await call.answer()
