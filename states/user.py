from aiogram.fsm.state import State, StatesGroup


class UserCommonStates(StatesGroup):
    main_menu = State()


class UserBrwStates(StatesGroup):
    brw_trackers_list = State()
    editing_brw_tracker = State()
    deleting_brw_tracker = State()


class UserBrwFillingTrackerStates(StatesGroup):
    adding_brw_departure_station = State()
    adding_brw_arrival_station = State()
    adding_brw_departure_date = State()
    adding_brw_train_number = State()
