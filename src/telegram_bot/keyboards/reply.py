from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from src.database.func import get_car_name

number = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Всего авто')],
        [KeyboardButton(text='Определённая марка')]
    ],
    resize_keyboard=True
)

async def check_number():
    car_name = await get_car_name()
    keyboard = ReplyKeyboardBuilder()
    for car in car_name:
        keyboard.add(KeyboardButton(text=car))
    return keyboard.adjust(1).as_markup(resize_keyboard=True)