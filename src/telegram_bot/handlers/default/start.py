from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from config.config import DEFAULT_COMMANDS

router_start = Router()



@router_start.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    commands = "\n".join(
        [f"/{command[0]} - {command[1]}" for command in DEFAULT_COMMANDS]
    )
    await message.reply(
        f"Бот для получения информации о новых объявлений "
        f"на сайтах по продажам авто\n"
        f"{commands}", reply_markup=ReplyKeyboardRemove()
    )
