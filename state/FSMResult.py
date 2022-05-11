from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMResult(StatesGroup):
    chooseResult = State()
    result = State()