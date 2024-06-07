from aiogram.fsm.state import StatesGroup , State

class Newmember(StatesGroup):
    Name = State()
    Number = State()
    Avatar = State()


class Change(StatesGroup):
    Namenew = State()
    Numbernew = State()
    Avatarnew = State()