from aiogram import types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from . import user_router
from common.lexicon import CommonMessages as lxc
from database.models import User
from database.repository import UserRepository
import keyboards.user as kb
from states import user as states


@user_router.message(CommandStart())
async def start_message(message: types.Message, state: FSMContext, session: AsyncSession):
    await message.delete()
    await message.answer(lxc.main_menu, reply_markup=kb.make_main_menu_keyboard())
    await state.set_state(states.UserCommonStates.main_menu)

    user = User(telegram_id=message.from_user.id)
    db_repo = UserRepository(session)
    await db_repo.add(user)

    data: dict = await state.get_data()
    previous_callback: types.CallbackQuery = data.get("previous_callback")
    if (previous_callback):
        await previous_callback.message.delete()

    # print(f"Storage: {state.storage}")
    # print(f"Key: {state.key}")


@user_router.message(F.text == "/fill")
async def fill(message: types.Message, state: FSMContext):
    await state.update_data(
        departure_station="Пинск",
        arrival_station="Минск",
        departure_date="2025-02-08",
        train_number="860Б",
        is_turned_on=True)
    await message.delete()


@user_router.message(F.text == "/data")
async def get_data(message: types.Message, state: FSMContext):
    data = await state.get_data()
    print("---------------------------------")
    print(data)
    print("---------------------------------")
    await message.delete()


@user_router.message(F.text == "/allargs")
async def get_all_args(message: types.Message, state: FSMContext, **kwargs):
    print("---------------------------------")
    print(kwargs)
    print("---------------------------------")
    await message.delete()
