import os
from typing import cast

from dotenv import find_dotenv, load_dotenv

if not find_dotenv():
    exit("Переменные окружения не найдены, т.к. отсутствует файл .env")
else:
    load_dotenv()

DATABASE_URL: str = cast(str, os.getenv("DATABASE_URL"))
BOT_TOKEN: str = cast(str, os.getenv("BOT_TOKEN"))

DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Справка"),
    ("number", "Количество автомобилей в базе"),
    ("models", "Список объявлений определенной модели авто"),
    ("update", "Получение новых объявлений"),
    ("cancel", "Остановить получение новых сообщений"),
)
