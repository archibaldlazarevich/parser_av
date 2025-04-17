from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import src.telegram_bot.keyboards.reply as reply
from src.database.func import (
    get_all_cars,
    get_spec_cars_number,
    get_all_spec_models,
)


class AllCars(StatesGroup):
    init_model = State()


router_cars_model = Router()


@router_cars_model.message(Command("models"))
async def get_all_model_car(message: Message, state: FSMContext):
    await state.set_state(AllCars.init_model)
    await message.reply(
        "Выберите интересующую модель", reply_markup=await reply.check_number()
    )


@router_cars_model.message(AllCars.init_model)
async def get_all_models(message: Message, state: FSMContext):
    await state.clear()
    result = await get_all_spec_models(model=message.text)
    for model in result:
        await message.reply(text=model[0], reply_markup=ReplyKeyboardRemove())
