from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from config.config import DEFAULT_COMMANDS
from src.telegram_bot.middlewares.middlewares import TestMiddleware

router_start = Router()

router_start.message.outer_middleware(TestMiddleware())


@router_start.message(CommandStart())
async def cmd_start(message: Message) -> None:
    commands = "\n".join(
        [f"/{command[0]} - {command[1]}" for command in DEFAULT_COMMANDS]
    )
    await message.reply(
        f"Бот для получения информации о новых объявлений "
        f"на сайтах по продажам авто\n"
        f"{commands}"
    )
