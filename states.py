from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    waiting_for_report = State()
    waiting_for_rating = State()
