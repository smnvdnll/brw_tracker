from aiogram.fsm.state import State, StatesGroup


class CommonStates(StatesGroup):
    choosing_carrier = State()