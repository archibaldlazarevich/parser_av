from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import src.telegram_bot.keyboards.reply as reply
from src.database.func import get_all_cars, get_spec_cars_number


class Number(StatesGroup):
    init_number = State()
    models_car = State()

all_data = ["Всего авто","Определённая марка"]

router_cars_number = Router()

async def send_cars(message: Message, state: FSMContext):
    """
    Функция для отправки клавиатуры с выбором марки авто
    :param message:
    :param state:
    :return:
    """
    repl_data = await state.get_value('models_car')
    await message.reply("Выберите интересующую марку", reply_markup= repl_data[1])

async def start_command(message: Message, state: FSMContext):
    """
    Старотовая функция для команды
    :param message:
    :param state:
    :return:
    """
    await state.clear()
    await state.set_state(Number.init_number)
    await message.reply(
        "Выберите необходимый пункт меню", reply_markup=reply.number
    )

@router_cars_number.message(Command("number"))
async def init_message(message: Message, state: FSMContext):
    await start_command(message= message, state= state)


@router_cars_number.message(F.text.not_in(all_data), Number.init_number)
async def check(message: Message, state: FSMContext):
    await message.reply(
        "Выберите данные из списка!!!", reply_markup=ReplyKeyboardRemove()
    )
    await start_command(message=message, state=state)


@router_cars_number.message(F.text == "Всего авто", Number.init_number)
async def get_all_cars_count(message: Message, state: FSMContext):
    await message.reply(
        f"Всего авто в базе данных {await get_all_cars()}",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.clear()


@router_cars_number.message(F.text == "Определённая марка", Number.init_number)
async def get_spec_cars(message: Message, state: FSMContext):
    reply_data = await reply.check_number()
    if reply_data:
        await state.set_state(Number.models_car)
        await state.update_data(models_car= reply_data)
        await send_cars(message= message, state= state)
    else:
        await message.reply('В данный момент база данных пуста.', reply_markup=ReplyKeyboardRemove())
        await state.clear()



@router_cars_number.message(Number.models_car)
async def get_spec_cars_answer(message: Message, state: FSMContext):
    repl_data = await state.get_value('models_car')
    if message.text in repl_data[0]:
        await state.clear()
        await message.reply(
            f"Всего авто {message.text} в базе данных {await get_spec_cars_number(message.text)}",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.reply('Введите данные из клавиатуры!!!', reply_markup=ReplyKeyboardRemove())
        await send_cars(message= message, state= state)
