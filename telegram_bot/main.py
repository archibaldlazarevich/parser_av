import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault
from sqlalchemy.util import await_only
from handlers.default.start import router_start
from handlers.default.help import router_help

from config.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def set_commands():
    commands = [
        BotCommand(command='start', description='Запустить бота!'),
        BotCommand(command='help', description='Справка'),
        BotCommand(command='model', description='Выбрать интересующую модель')
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

async def start_bot():
    await set_commands()

async def main():
    dp.include_routers(
        router_help,
        router_start,
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