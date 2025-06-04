from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

import src.parcer.abw as abw
import src.parcer.av as av
import src.parcer.kufar as kufar
import src.parcer.delete_av as delete_av
import asyncio

count = 0
scheduler = AsyncIOScheduler()

async def main():
    task = [
        abw.main(min_price=12000, max_price=17500),# Вписать необходимые суммы в usd
        av.main(min_price=12000, max_price=17500),
        kufar.main(min_price=12000, max_price=17500),
        delete_av.main(),
    ]
    await asyncio.gather(*task)


async def scheduled_job():
    global count
    if 8 <= datetime.now().hour < 23:
        await main()
        count += 1
    if count == 3:
        scheduler.modify_job(job_id='parcer', trigger=IntervalTrigger(minutes=45))


async def scheduler_runner():
    scheduler.add_job(scheduled_job, "interval", minutes=2, id='parcer')
    scheduler.start()
    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == "__main__":
    asyncio.run(scheduler_runner())
