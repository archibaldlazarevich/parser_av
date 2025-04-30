from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler


import src.parcer.abw as abw
import src.parcer.av as av
import src.parcer.kufar as kufar
import src.parcer.delete_av as delete_av
import asyncio


async def main():
    task = [
        # abw.main(min_price=12000, max_price=17500),
        av.main(min_price=12000, max_price=17500),
        # kufar.main(min_price=12000, max_price=17500),
        # delete_av.main(),
    ]
    await asyncio.gather(*task)


async def scheduled_job():
    # if 8 <= datetime.now().hour < 23:
    await main()


async def scheduler_runner():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(scheduled_job, "interval", minutes=1)
    scheduler.start()
    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == "__main__":
    asyncio.run(scheduler_runner())
