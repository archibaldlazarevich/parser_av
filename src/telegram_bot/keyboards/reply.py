from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from src.database.func import get_car_name, get_car_year

number = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Всего авто")],
        [KeyboardButton(text="Определённая марка")],
    ],
    resize_keyboard=True,
)


year_reply = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Средний год авто")],
        [KeyboardButton(text="Средняя цена авто")],
        [KeyboardButton(text="Средняя цена по году")],
    ],
    resize_keyboard=True,
)


async def check_number():
    car_name = await get_car_name()
    keyboard = ReplyKeyboardBuilder()
    for car in car_name:
        keyboard.add(KeyboardButton(text=car))
    return keyboard.adjust(1).as_markup(resize_keyboard=True)


async def check_year(car_name: str):
    car_year = await get_car_year(car_name=car_name)
    keyboard = ReplyKeyboardBuilder()
    for year in car_year:
        keyboard.add(KeyboardButton(text=str(year)))
    return keyboard.adjust(1).as_markup(resize_keyboard=True)
