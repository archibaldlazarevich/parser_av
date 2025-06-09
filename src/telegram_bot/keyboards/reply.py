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


async def check_number() -> (list, ReplyKeyboardMarkup):
    """
    Функция возвращает клавиатуру из автомобилей
    :return:
    """
    car_name = await get_car_name()
    if car_name:
        all_data = [car for car in car_name]
        keyboard = ReplyKeyboardBuilder()
        for car in all_data:
            keyboard.add(KeyboardButton(text=car))
        markup =  keyboard.adjust(1).as_markup(resize_keyboard=True)
        return all_data, markup
    return False


async def check_year(car_name: str) -> (list, ReplyKeyboardMarkup):
    """
    Функция возвращает клавиатуру из годов впуска автомобилей
    :param car_name:
    :return:
    """
    car_year = await get_car_year(car_name=car_name)
    if car_year:
        all_data = [str(year) for year in car_year]
        keyboard = ReplyKeyboardBuilder()
        for year in all_data:
            keyboard.add(KeyboardButton(text=year))
        markup = keyboard.adjust(1).as_markup(resize_keyboard=True)
        return all_data, markup
    return False