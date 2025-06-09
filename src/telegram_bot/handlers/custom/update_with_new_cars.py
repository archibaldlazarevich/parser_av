from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from src.database.func import check_update, update_insert, delete_update


router_update = Router()


@router_update.message(Command("update"))
async def get_all_model_car(message: Message, state: FSMContext):
    await state.clear()
    result = await check_update(id_ = message.chat.id)
    if result:
        await message.reply(
            f"Процесс просмотра новых объявлений уже запущен, как только появятся обновления, данные отправятся вам",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.reply(
            f"Новые объявления и обновленные старые объявления будут присылаться по мере поступления",
            reply_markup=ReplyKeyboardRemove()
        )
        await update_insert(id_ = message.chat.id)


@router_update.message(Command("cancel"))
async def cancel_get_all_model_car(message: Message, state: FSMContext):
    await state.clear()
    result = await check_update(id_ = message.chat.id)
    if result:
        await delete_update(id_ = message.chat.id)
        await message.reply(
            "Поступление новых данных остановлено. \nДля возобновления введите команду: \n/update",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.reply(
            "Вы не включили функцию доставки новых и обновленных старых объявлений",
            reply_markup=ReplyKeyboardRemove()
        )
