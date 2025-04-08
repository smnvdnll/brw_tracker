from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from database.repository import BRWTrackerRepository


def make_main_menu_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="БЧ",
        callback_data="brw_button"
    ))
    return kb.as_markup()


async def make_brw_trackers_list_keyboard(tg_id: int, session: AsyncSession) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    db_repo = BRWTrackerRepository(session)
    trackers = await db_repo.get_brw_trackers_by_user_id(tg_id)

    for tracker in trackers:
        tracker_state = "🟢" if tracker.is_turned_on else "🗑️"
        kb.add(InlineKeyboardButton(
            text=f"{tracker_state} {tracker.departure_station} -> {tracker.arrival_station}, {tracker.train_number}, {tracker.departure_date}",
            callback_data=f"{tracker.id}"
        ))
    kb.add(InlineKeyboardButton(
        text="Добавить",
        callback_data="edit_brw_tracker_button"
    ))
    make_back_button(kb)
    kb.adjust(1)
    return kb.as_markup()


def make_edit_brw_tracker_keyboard(user_data: dict):
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text=user_data.get("departure_station", "Откуда"),
        callback_data="add_brw_departure_station_button"
    ))
    kb.add(InlineKeyboardButton(text="→", callback_data="swap_brw_stations_button"))
    kb.add(InlineKeyboardButton(
        text=user_data.get("arrival_station", "Куда"),
        callback_data="add_brw_arrival_station_button"
    ))
    kb.add(InlineKeyboardButton(
        text=user_data.get("departure_date", "Дата"),
        callback_data="add_brw_departure_date_button"
    ))
    kb.add(InlineKeyboardButton(
        text=user_data.get("train_number", "Номер поезда"),
        callback_data="add_brw_train_number_button"
    ))
    kb.add(InlineKeyboardButton(
        text="Запустить",
        callback_data="run_brw_tracker_button"
    ))
    if user_data.get("is_turned_on"):
        kb.add(InlineKeyboardButton(
            text="Удалить",
            callback_data="delete_brw_tracker_button"
        ))
    make_back_button(kb)
    kb.adjust(3, 1, 1, 2)
    return kb.as_markup()


def make_back_button(keyboard: InlineKeyboardBuilder = None):
    if not keyboard:
        keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(
        text="‹ Назад",
        callback_data="back_button"
    ))
    return keyboard.as_markup()
