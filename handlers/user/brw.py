from datetime import datetime, timedelta

from aiogram import types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from common.lexicon import BRWMessages as lxc, CommonMessages
from database.models import BRWTracker
from database.repository import BRWTrackerRepository
from keyboards import user as kb
from services.brw_manager import BRWTrackerManager
from states.user import UserCommonStates, UserBrwStates, UserBrwFillingTrackerStates
from utils.brw_utils import is_station_exists
from . import user_router


# кнопка Назад из меню трекеров
@user_router.callback_query(F.data == "back_button", StateFilter(UserBrwStates.brw_trackers_list))
async def back(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(CommonMessages.main_menu, reply_markup=kb.make_main_menu_keyboard())
    await state.update_data(previous_callback=callback)
    await state.set_state(UserCommonStates.main_menu)
    await callback.answer()


# кнопка Назад из меню редактирования трекера
@user_router.callback_query(F.data == "back_button", StateFilter(UserBrwStates.editing_brw_tracker))
async def back(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback.message.edit_text(lxc.trackers_list,
                                     reply_markup=await kb.make_brw_trackers_list_keyboard(callback.from_user.id, session))
    await state.clear()
    await state.update_data(previous_callback=callback)
    await state.set_state(UserBrwStates.brw_trackers_list)
    await callback.answer()


# кнопка Назад из меню редактирования параметра трекера
@user_router.callback_query(F.data == "back_button", StateFilter(UserBrwFillingTrackerStates))
async def back(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(lxc.edit_tracker, reply_markup=kb.make_edit_brw_tracker_keyboard(data))
    await state.update_data(previous_callback=callback)
    await state.set_state(UserBrwStates.editing_brw_tracker)
    await callback.answer()


# кнопка БЧ
@user_router.callback_query(F.data == "brw_button", StateFilter(UserCommonStates.main_menu))
async def brw_trackers_list(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback.message.edit_text(lxc.trackers_list,
                                     reply_markup=await kb.make_brw_trackers_list_keyboard(callback.from_user.id, session))
    await state.update_data(previous_callback=callback)
    await state.set_state(UserBrwStates.brw_trackers_list)
    await callback.answer()


# кнопка Добавить трекер
@user_router.callback_query(F.data == "edit_brw_tracker_button", StateFilter(UserBrwStates.brw_trackers_list))
async def add_new_brw_tracker(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(lxc.edit_tracker,
                                     reply_markup=kb.make_edit_brw_tracker_keyboard(await state.get_data()))
    await state.update_data(previous_callback=callback)
    await state.set_state(UserBrwStates.editing_brw_tracker)
    await callback.answer()


# Заполнение параметров трекера
# кнопка Добавить станцию отправления
@user_router.callback_query(F.data == "add_brw_departure_station_button", StateFilter(UserBrwStates.editing_brw_tracker))
async def add_brw_departure_station(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(lxc.input_departure_station, reply_markup=kb.make_back_button())
    await state.update_data(previous_callback=callback)
    await state.set_state(UserBrwFillingTrackerStates.adding_brw_departure_station)
    await callback.answer()

# кнопка Добавить станцию прибытия


@user_router.callback_query(F.data == "add_brw_arrival_station_button", StateFilter(UserBrwStates.editing_brw_tracker))
async def add_brw_arrival_station(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(lxc.input_arrival_station, reply_markup=kb.make_back_button())
    await state.update_data(previous_callback=callback)
    await state.set_state(UserBrwFillingTrackerStates.adding_brw_arrival_station)
    await callback.answer()

# кнопка Добавить дату отправления


@user_router.callback_query(F.data == "add_brw_departure_date_button", StateFilter(UserBrwStates.editing_brw_tracker))
async def add_brw_departure_date(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(lxc.input_departure_date, reply_markup=kb.make_back_button())
    await state.update_data(previous_callback=callback)
    await state.set_state(UserBrwFillingTrackerStates.adding_brw_departure_date)
    await callback.answer()

# кнопка Добавить номер поезда


@user_router.callback_query(F.data == "add_brw_train_number_button", StateFilter(UserBrwStates.editing_brw_tracker))
async def add_brw_train_number(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(lxc.input_train_number, reply_markup=kb.make_back_button())
    await state.update_data(previous_callback=callback)
    await state.set_state(UserBrwFillingTrackerStates.adding_brw_train_number)
    await callback.answer()


# хендлер, в который попадают все текстовые сообщения c добавлением параметров трекера
@user_router.message(F.text, StateFilter(UserBrwFillingTrackerStates))
async def input_text_to_fill_tracker_form(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    parts = current_state.split('_')
    key = "_".join(parts[-2:])

    data = await state.get_data()
    previous_callback: types.CallbackQuery = data.get("previous_callback")

    await state.update_data({key: message.text})
    # print(await state.get_data())
    await state.set_state(UserBrwStates.editing_brw_tracker)
    await previous_callback.message.edit_text(lxc.edit_tracker, reply_markup=kb.make_edit_brw_tracker_keyboard(await state.get_data()))

    await message.delete()


# кнопка подтверждения создания и запуска трекера
@user_router.callback_query(F.data == "run_brw_tracker_button", StateFilter(UserBrwStates.editing_brw_tracker))
async def confirm_brw_tracker(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    db_repo = BRWTrackerRepository(session)
    data: dict = await state.get_data()

    if not is_station_exists(data.get("departure_station")):
        await callback.answer(lxc.incorrect_departure_station, show_alert=True)
        return
    if not is_station_exists(data.get("arrival_station")):
        await callback.answer(lxc.incorrect_arrival_station, show_alert=True)
        return
    try:
        date = datetime.strptime(data.get("departure_date"), "%Y-%m-%d")
    except Exception as e:
        await callback.answer(lxc.incorrect_departure_date, show_alert=True)
        return
    else:
        now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if date < now or date > now + timedelta(days=50):
            await callback.answer(lxc.incorrect_departure_date, show_alert=True)
            return

    await callback.answer("Начинаем создавать мониторинг", show_alert=True)
    tracker = BRWTracker(
        departure_station=data.get("departure_station"),
        arrival_station=data.get("arrival_station"),
        departure_date=data.get("departure_date"),
        train_number=data.get("train_number"),
        is_turned_on=True,
        user_telegram_id=callback.from_user.id
    )
    tracker = await db_repo.add(tracker)
    tracker_manager = BRWTrackerManager(tracker, session)
    await callback.message.edit_text(
        lxc.trackers_list,
        reply_markup=await kb.make_brw_trackers_list_keyboard(callback.from_user.id, session)
    )

    await state.clear()
    await state.update_data(previous_callback=callback)
    await state.set_state(UserBrwStates.brw_trackers_list)
    await tracker_manager.monitor_places()


# кнопка отвечающая за переход в меню редактирования конкретного трекера по его id из бд
@user_router.callback_query(F.data.func(lambda data: data.isdigit()), StateFilter(UserBrwStates.brw_trackers_list))
async def edit_brw_tracker(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    tracker_id = int(callback.data)
    db_repo = BRWTrackerRepository(session)
    tracker = await db_repo.get_brw_tracker_by_id(tracker_id)
    tracker_state = "Запущен" if await db_repo.is_tracker_turned_on(tracker_id) else "Ожидает удаления"

    await state.update_data(departure_station=tracker.departure_station,
                            arrival_station=tracker.arrival_station,
                            departure_date=tracker.departure_date,
                            train_number=tracker.train_number,
                            is_turned_on=tracker.is_turned_on,
                            tracker_id=tracker.id,
                            previous_callback=callback)
    await state.set_state(UserBrwStates.editing_brw_tracker)
    await callback.message.edit_text(
        f"{lxc.edit_tracker}\n\nТекущий статус: {tracker_state}",
        reply_markup=kb.make_edit_brw_tracker_keyboard(await state.get_data())
    )


# кнопка удаления выбранного трекера
@user_router.callback_query(F.data == "delete_brw_tracker_button", StateFilter(UserBrwStates.editing_brw_tracker))
async def delete_brw_tracker(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    db_repo = BRWTrackerRepository(session)
    data = await state.get_data()
    tracker = await db_repo.get_brw_tracker_by_id(data.get("tracker_id"))
    await db_repo.set_value_by_params({"id": tracker.id}, {"is_turned_on": False})
    await callback.answer("Запрос на удаление трекера принят, ожидайте сообщения об успешном выполнении", show_alert=True)

    await state.clear()
    await state.update_data(previous_callback=callback)
    await state.set_state(UserBrwStates.brw_trackers_list)
    await callback.message.edit_text(
        lxc.trackers_list,
        reply_markup=await kb.make_brw_trackers_list_keyboard(callback.from_user.id, session)
    )
