import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.telegram import TelegramAPIServer
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.client.session.aiohttp import AiohttpSession

from src.telegram_bot.handlers.custom.update_with_new_cars import router_update
from src.telegram_bot.handlers.default.start import router_start
from src.telegram_bot.handlers.default.help import router_help
from src.telegram_bot.handlers.custom.check_cars_number import (
    router_cars_number,
)
from src.telegram_bot.handlers.custom.get_all_cars_by_model import (
    router_cars_model,
)
from src.telegram_bot.handlers.custom.check_average import (
    router_cars_counter,
)

from config.config import BOT_TOKEN, DEFAULT_COMMANDS

bot = Bot(
    token=BOT_TOKEN,
)
dp = Dispatcher()


async def set_commands():
    commands = [
        BotCommand(command=command[0], description=command[1])
        for command in DEFAULT_COMMANDS
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def start_bot():
    await set_commands()


async def main():
    dp.include_routers(
        router_help,
        router_start,
        router_cars_number,
        router_cars_model,
        router_update,
        router_cars_counter,
    )
    dp.startup.register(start_bot)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(
            bot, allowed_updates=dp.resolve_used_update_types()
        )
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
