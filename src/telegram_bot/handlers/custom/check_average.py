from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import src.telegram_bot.keyboards.reply as reply
from src.database.func import (
    get_aver_year,
    get_aver_cost,
    get_aver_cost_by_year,
)

class Counter(StatesGroup):
    init = State()
    average_year = State()
    average_cost = State()
    average_year_cost = State()
    average_year_cost_answer = State()


router_cars_counter = Router()


async def send_cars(message: Message, state: FSMContext):
    """
    Функция для отправки клавиатуры с выбором марки авто
    :param message:
    :param state:
    :return:
    """
    repl_data = await state.get_value('init')
    await message.reply("Выберите интересующую марку", reply_markup= repl_data[1])


async def send_year(message: Message, state: FSMContext):
    """
    Функция для отправки клавиатуры с выбором марки авто
    :param message:
    :param state:
    :return:
    """
    repl_data = await state.get_value('average_year_cost_answer')
    await message.reply(
        f"Выберите год выпуска для подсчета",
        reply_markup= repl_data[1])

@router_cars_counter.message(Command("average"))
async def init_message(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Counter.init)
    await message.reply(
        "Выберите необходимый пункт меню", reply_markup=reply.year_reply
    )


@router_cars_counter.message(F.text == "Средний год авто", Counter.init)
async def aver_year(message: Message, state: FSMContext):
    reply_data = await reply.check_number()
    if reply_data:
        await state.set_state(Counter.average_year)
        await state.update_data(init= reply_data)
        await send_cars(message= message, state= state)
    else:
        await message.reply('В данный момент база данных пуста.', reply_markup=ReplyKeyboardRemove())
        await state.clear()

@router_cars_counter.message(Counter.average_year)
async def aver_year_answer(message: Message, state: FSMContext):
    repl_data = await state.get_value('init')
    if message.text in repl_data[0]:
        await state.clear()
        await message.reply(
            f"Средний возраст {message.text} {await get_aver_year(car_name=message.text)}",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.reply('Введите данные из клавиатуры!!!', reply_markup=ReplyKeyboardRemove())
        await send_cars(message= message, state= state)


@router_cars_counter.message(F.text == "Средняя цена авто", Counter.init)
async def aver_price(message: Message, state: FSMContext):
    reply_data = await reply.check_number()
    if reply_data:
        await state.set_state(Counter.average_cost)
        await state.update_data(init= reply_data)
        await send_cars(message= message, state= state)
    else:
        await message.reply('В данный момент база данных пуста.', reply_markup=ReplyKeyboardRemove())
        await state.clear()


@router_cars_counter.message(Counter.average_cost)
async def aver_price_answer(message: Message, state: FSMContext):
    repl_data = await state.get_value('init')
    if message.text in repl_data[0]:
        await state.clear()
        await message.reply(
            f"Средняя цена на {message.text} в usd составляет :{await get_aver_cost(car_name=message.text)}",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.reply('Введите данные из клавиатуры!!!', reply_markup=ReplyKeyboardRemove())
        await send_cars(message= message, state= state)


@router_cars_counter.message(F.text == "Средняя цена по году", Counter.init)
async def aver_year_price(message: Message, state: FSMContext):
    reply_data = await reply.check_number()
    if reply_data:
        await state.set_state(Counter.average_year_cost)
        await state.update_data(init=reply_data)
        await send_cars(message=message, state=state)
    else:
        await message.reply('В данный момент база данных пуста.', reply_markup=ReplyKeyboardRemove())
        await state.clear()


@router_cars_counter.message(Counter.average_year_cost)
async def aver_year_price_func(message: Message, state: FSMContext):
    repl_data = await state.get_value('init')
    if message.text in repl_data[0]:
        new_data = await reply.check_year(car_name=message.text)
        if new_data:
            await state.update_data(init = message.text)
            await state.set_state(Counter.average_year_cost_answer)
            await state.update_data(average_year_cost_answer = new_data)
            await send_year(message= message, state= state)
        else:
            await message.reply('Данных по году выпуска для данного автомобиля нет в базе данных.', reply_markup=ReplyKeyboardRemove())
    else:
        await message.reply('Введите данные из клавиатуры!!!', reply_markup=ReplyKeyboardRemove())
        await send_cars(message=message, state=state)


@router_cars_counter.message(Counter.average_year_cost_answer)
async def aver_year_price_answer(message: Message, state: FSMContext):
    repl_data = await state.get_value('average_year_cost_answer')
    if message.text in repl_data[0]:
        car_data = await state.get_value('init')
        aver_cost = await get_aver_cost_by_year(car_name= car_data, year= int(message.text))
        await state.clear()
        if aver_cost:
            await message.reply(
                f"Средний ценник на {car_data}, {message.text} года выпуска в usd составляет:"
                f"{aver_cost}",reply_markup=ReplyKeyboardRemove(),
        )
        else:
            await message.reply('На данную марку автомобиля невозвможно посчитать среднюю стоимость.', reply_markup=ReplyKeyboardRemove())
    else:
        await message.reply('Введите данные из клавиатуры!!!', reply_markup=ReplyKeyboardRemove())
        await send_year(message=message, state=state)
