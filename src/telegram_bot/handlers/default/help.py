from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from config.config import DEFAULT_COMMANDS

router_help = Router()

@router_help.message(Command('help'))
async def get_help(message:Message):
    commands = '\n'.join([f'/{command[0]} - {command[1]}' for command in DEFAULT_COMMANDS])
    await message.answer('Этот бот - по просмотру новых объявлений автомобилей.\n'
                         'Команды, которые выполняет данный бот:\n'
                         f'{commands}')
