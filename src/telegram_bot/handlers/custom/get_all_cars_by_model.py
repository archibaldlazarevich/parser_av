from aiogram import Router, F
from aiogram.types import Message,  ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import src.telegram_bot.keyboards.reply as reply
from src.database.func import (
    get_all_spec_models,
)


class AllCars(StatesGroup):
    init_model = State()


async def send_cars(message: Message, state: FSMContext):
    """
    Функция для отправки клавиатуры с выбором марки авто
    :param message:
    :param state:
    :return:
    """
    repl_data = await state.get_value('init_model')
    await message.reply("Выберите интересующую марку", reply_markup= repl_data[1])

router_cars_model = Router()


@router_cars_model.message(Command("models"))
async def get_all_model_car(message: Message, state: FSMContext):
    await state.clear()
    repl_data = await reply.check_number()
    if repl_data:
        await state.set_state(AllCars.init_model)
        await state.update_data(init_model= repl_data)
        await send_cars(message= message, state= state)
    else:
        await message.reply('В данный момент база данных пуста.', reply_markup=ReplyKeyboardRemove())
        await state.clear()


@router_cars_model.message(AllCars.init_model)
async def get_all_models(message: Message, state: FSMContext):
    repl_data = await state.get_value('init_model')
    if message.text in repl_data[0]:
        await state.clear()
        result = await get_all_spec_models(model=message.text)
        for model in result:
            await message.reply(text=model[0], reply_markup=ReplyKeyboardRemove())
    else:
        await message.reply('Введите данные из клавиатуры!!!', reply_markup=ReplyKeyboardRemove())
        await send_cars(message= message, state= state)
