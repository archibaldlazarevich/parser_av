from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from src.telegram_bot.middlewares.middlewares import TestMiddleware

router_start = Router()

router_start.message.outer_middleware(TestMiddleware())

@router_start.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.reply('Бот для получения информации о новых объявлений на сайтах')
