from aiogram.fsm.state import State, StatesGroup

class ElementsOfDiskriminant(StatesGroup):
    element_a = State()
    element_b = State()
    element_c = State()
    eval_result = State()