from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    waiting_for_add_url = State()
    waiting_for_remove_url = State()
