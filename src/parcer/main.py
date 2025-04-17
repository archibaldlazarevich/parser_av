from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler


import src.parcer.abw as abw
import src.parcer.av as av
import src.parcer.kufar as kufar
import asyncio


async def main():
    task = [
        abw.main(min_price=12000, max_price=17500),
        av.main(min_price=12000, max_price=17500),
        kufar.main(min_price=12000, max_price=17500),
    ]
    await asyncio.gather(*task)


async def scheduled_job():
    if 8 <= (datetime.now() + timedelta(hours=3)).hour < 23:
        await main()
    else:
        print("Вне рабочего времени, пропуск запуска")

async def scheduler_runner():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(scheduled_job, 'interval', minutes=45)
    scheduler.start()
    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    asyncio.run(scheduler_runner())

