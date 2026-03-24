from aiogram.fsm.state import State, StatesGroup


class DownloadStates(StatesGroup):
    awaiting_link = State()
