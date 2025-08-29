from aiogram.filters.callback_data import CallbackData

from .enum import Carrier


class CarriersCallback(CallbackData, prefix="carriers"):
    carrier: Carrier