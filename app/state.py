from aiogram.fsm.state import StatesGroup, State



class get_msg(StatesGroup):
    get_photo = State()
    get_rod = State()
    get_era = State()
    get_company = State()
    get_name = State()
    final = State() 
