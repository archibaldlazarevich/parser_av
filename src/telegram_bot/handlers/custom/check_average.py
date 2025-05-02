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

car = {}


@router_cars_counter.message(Command("average"))
async def init_message(message: Message, state: FSMContext):
    await state.set_state(Counter.init)
    await message.reply(
        "Выберите необходимый пункт меню", reply_markup=reply.year_reply
    )


@router_cars_counter.message(F.text == "Средний год авто", Counter.init)
async def aver_year(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Counter.average_year)
    await message.reply(
        "Выберите интересующую марку", reply_markup=await reply.check_number()
    )


@router_cars_counter.message(Counter.average_year)
async def aver_year_answer(message: Message, state: FSMContext):
    await state.clear()
    await message.reply(
        f"Средний возраст {message.text} {await get_aver_year(car_name=message.text)}",
        reply_markup=ReplyKeyboardRemove(),
    )


@router_cars_counter.message(F.text == "Средняя цена авто", Counter.init)
async def aver_price(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Counter.average_cost)
    await message.reply(
        "Выберите интересующую марку", reply_markup=await reply.check_number()
    )


@router_cars_counter.message(Counter.average_cost)
async def aver_price_answer(message: Message, state: FSMContext):
    await state.clear()
    await message.reply(
        f"Средняя цена на {message.text} в usd составляет :{await get_aver_cost(car_name=message.text)}",
        reply_markup=ReplyKeyboardRemove(),
    )


@router_cars_counter.message(F.text == "Средняя цена по году", Counter.init)
async def aver_year_price(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Counter.average_year_cost)
    await message.reply(
        "Выберите интересующую марку", reply_markup=await reply.check_number()
    )


@router_cars_counter.message(Counter.average_year_cost)
async def aver_year_price_func(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Counter.average_year_cost_answer)
    car[1] = message.text
    await message.reply(
        f"Выберите год выпуска для подсчета",
        reply_markup=await reply.check_year(car_name=message.text),
    )


@router_cars_counter.message(Counter.average_year_cost_answer)
async def aver_year_price_answer(message: Message, state: FSMContext):
    await state.clear()
    await message.reply(
        f"Средний ценник на {car[1]} {message.text} года выпуска в usd составляет:"
        f"{await get_aver_cost_by_year(car_name= car[1], year= int(message.text))}",
        reply_markup=ReplyKeyboardRemove(),
    )
