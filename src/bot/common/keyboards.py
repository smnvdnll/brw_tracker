from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callbacks import CarriersCallback
from .enum import Carrier
from .lexicon import Buttons


def make_main_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text=Buttons.BRW,
        callback_data=CarriersCallback(carrier=Carrier.BRW).pack()
        )
    )
    return kb.as_markup()


