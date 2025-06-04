import asyncio
from datetime import datetime

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config.config import BOT_TOKEN
from src.database.func import get_update_models, get_users_id

bot = Bot(token=BOT_TOKEN)
scheduler = AsyncIOScheduler()

async def send_hourly_message():
    if 8 <= datetime.now().hour < 23:
        result = await get_update_models()
        users = await get_users_id()
        if len(users) != 0:
            for chat_id in users:
                if len(result) != 0:
                    for car in result:
                        await bot.send_message(chat_id[0], car[0])



async def scheduler_start():
    await asyncio.sleep(5)
    scheduler.add_job(
        send_hourly_message, trigger="interval", minutes=45
    )
    scheduler.start()
    await asyncio.Event().wait()


if __name__ == '__main__':
    asyncio.run(scheduler_start())
