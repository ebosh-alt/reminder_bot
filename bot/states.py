from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    input_fio = State()
    input_country = State()
    input_number = State()


