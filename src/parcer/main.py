import time

import src.parcer.abw as abw
import src.parcer.av as av
import src.parcer.kufar as kufar
import asyncio

async def main():
    task = [
        abw.main(min_price=12000, max_price=18000),
        av.main(min_price=12000, max_price=18000),
        kufar.main(min_price=12000, max_price=18000),
    ]
    await asyncio.gather(*task)


if __name__ == '__main__':
    while True:
        asyncio.run(main())
        time.sleep(300)