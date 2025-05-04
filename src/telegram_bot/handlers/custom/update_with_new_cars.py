from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import insert, delete, update, select
from aiogram import Bot


from config.config import BOT_TOKEN
from src.database.create_db import get_db_session
from src.database.func import get_update_models, get_users_id

from src.database.models import Users


class UpdateCars(StatesGroup):
    init_model = State()


# bot = Bot(token=BOT_TOKEN)

router_update = Router()

# scheduler = AsyncIOScheduler()


@router_update.message(Command("update"))
async def get_all_model_car(message: Message, state: FSMContext):
    await state.set_state(UpdateCars.init_model)
    async with get_db_session() as session:
        result = await session.execute(
            select(Users.chat_id).where(
                Users.chat_id == message.chat.id,
            )
        )
        result = result.scalar()
    if result is not None:
        await message.reply(
            f"Процесс просмотра новых объявлений уже запущен, как только появятся обновления, данные отправятся вам",
        )
    else:
        await message.reply(
            f"Новые объявления и обновленные старые объявления будут присылаться по мере поступления",
        )
        async with get_db_session() as session:
            await session.execute(
                insert(Users).values(
                    chat_id=message.chat.id, date=datetime.today()
                )
            )
            await session.commit()


@router_update.message(Command("cancel"))
async def cancel_get_all_model_car(message: Message):
    async with get_db_session() as session:
        result = await session.execute(
            select(Users.chat_id).where(
                Users.chat_id == message.chat.id,
            )
        )
        result = result.scalar()
    if result is not None:
        async with get_db_session() as session:
            await session.execute(
                delete(Users).where(Users.chat_id == message.chat.id)
            )
            await session.commit()
            await message.reply(
                "Поступление новых данных остановлено. \nДля возобновления введите команду: \n/update",
            )
    else:
        await message.reply(
            "Вы не включили функцию доставки новых и обновленных старых объявлений"
        )
