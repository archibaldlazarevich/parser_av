from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import src.telegram_bot.keyboards.reply as reply
from src.database.func import get_all_cars, get_spec_cars_number

import datetime

class Number(StatesGroup):
    init_number = State()
    models_car = State()

router_cars_number = Router()

@router_cars_number.message(Command('number'))
async def init_message(message: Message, state: FSMContext):
    await state.set_state(Number.init_number)
    await message.reply('Выберите необходимы пункт меню',
                        reply_markup=reply.number)

@router_cars_number.message(F.text == 'Всего авто', Number.init_number)
async def get_all_cars_count(message: Message, state: FSMContext):
    await message.reply(f'Всего авто в базе данных {await get_all_cars()}', reply_markup=ReplyKeyboardRemove())
    await message.delete_reply_markup()
    await state.clear()

@router_cars_number.message(F.text == 'Определённая марка', Number.init_number)
async def get_spec_cars(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Number.models_car)
    await message.reply('Выберите интересующую марку', reply_markup=await reply.check_number())

@router_cars_number.message(Number.models_car)
async def get_spec_cars_answer(message: Message, state: FSMContext):
    await message.reply(f'Всего авто {message.text} в базе данных {await get_spec_cars_number(message.text)}', reply_markup=ReplyKeyboardRemove())
    await state.clear()