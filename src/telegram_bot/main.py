import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault
from sqlalchemy.util import await_only
from src.telegram_bot.handlers.default.start import router_start
from src.telegram_bot.handlers.default.help import router_help
from src.telegram_bot.handlers.custom.check_cars_number import router_cars_number
from src.telegram_bot.handlers.custom.get_all_cars_by_model import router_cars_model

from config.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def set_commands():
    commands = [
        BotCommand(command='start', description='Запустить бота!'),
        BotCommand(command='help', description='Справка'),
        BotCommand(command='number', description='Количество автомобилей в базе'),
        BotCommand(command='models', description='Список моделей авто'),
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
    )
    dp.startup.register(start_bot)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')