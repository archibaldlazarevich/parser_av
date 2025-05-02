from datetime import datetime

import aiohttp
import bs4
import asyncio
import fake_useragent
import json

from sqlalchemy import insert, Result, select, update

from src.database.create_db import get_db_session
from src.database.models import Cars

user = fake_useragent.UserAgent(
    browsers=["Google", "Chrome", "Firefox", "Edge", "Opera", "Safari"],
    os=["Windows", "Linux", "Ubuntu"],
    platforms=["desktop"],
).random
header = {"user-agent": user}

audi_url = (
    "https://auto.kufar.by/l/cars/audi-q5-i-8r-restajling"
    "?cre=v.or%3A1&crg=1&cur=USD&prc=r%3A{min_price}"
    "%2C{max_price}&rgd=r%3A2011%2C2022"
)
nissan_url = (
    "https://auto.kufar.by/l/cars/nissan-x-trail-iii"
    "?cre=v.or%3A1&crg=1&cur=USD&prc=r%3A{min_price}%2C{max_price}"
)
mits_url = (
    "https://auto.kufar.by/l/cars/mitsubishi-outlander?"
    "cre=v.or%3A1&crg=1&cur=USD&prc=r%3A{min_price}"
    "%2C{max_price}&rgd=r%3A2012%2C2022"
)
chevr_url = (
    "https://auto.kufar.by/l/r~minsk/cars/chevrolet-equinox-iii?"
    "cre=v.or%3A1&crg=1&cur=USD&prc=r%3A{min_price}%2C{max_price}"
)
volvo_url = (
    "https://auto.kufar.by/l/cars/volvo-xc60?cre=v.or"
    "%3A1&crg=1&cur=USD&prc=r%3A{min_price}%2C{max_price}"
)
mazda_url = (
    "https://auto.kufar.by/l/cars/mazda-cx-5?cre=v.or"
    "%3A1&crg=1&cur=USD&prc=r%3A{min_price}%2C{max_price}"
)
kia_sport_url = (
    "https://auto.kufar.by/l/cars/kia-sportage?cre="
    "v.or%3A1&crg=1&cur=USD&prc=r%3A{min_price}%2C{max_price}"
)
kia_sor_url = (
    "https://auto.kufar.by/l/cars/kia-sorento?cre="
    "v.or%3A1&crg=1&cur=USD&prc=r%3A{min_price}"
    "%2C{max_price}&rgd=r%3A2011%2C2022"
)
hyundai_url = (
    "https://auto.kufar.by/l/cars/hyundai-santa-fe-iii"
    "?cre=v.or%3A1&crg=1&cur=USD&prc=r%"
    "3A{min_price}%2C{max_price}"
)

toyota_url = (
    "https://auto.kufar.by/l/cars/toyota-rav4-iv-ca40"
    "?cre=v.or%3A1&crg=1&cur=USD&prc=r%3A{min_price}%2C{max_price}"
)

honda_url = (
    "https://auto.kufar.by/l/cars/honda-cr-v-iv"
    "?cre=v.or%3A1&crg=1&cur=USD&prc=r%3A{min_price}%2C{max_price}"
)

mercedes_url = (
    "https://auto.kufar.by/l/cars/mercedes-benz-m-klass-ii-w164-restajling"
    "?crca=r%3A1%2C211&cre=v.or%3A1&crg=1&cur=USD&prc=r%3A{min_price}%2C{max_price}"
)

urls_list = {
    audi_url: 1,
    nissan_url: 2,
    mits_url: 3,
    chevr_url: 4,
    volvo_url: 5,
    mazda_url: 6,
    kia_sor_url: 7,
    kia_sport_url: 8,
    hyundai_url: 9,
    toyota_url: 10,
    honda_url: 11,
    mercedes_url: 12,
}

model_dict = {
    1: "Audi_q5",
    2: "Nissan_x_trail",
    3: "Mitsubishi_outlander",
    4: "Chevrolet_equinox",
    5: "Volvo_cx60",
    6: "Mazda_cx5",
    7: "Kia_spotage",
    8: "Kia_sorento",
    9: "Hyundai_santa_fe",
    10: "Toyota_Rav4",
    11: "Honda_CRV",
    12: "Mercedes_Benz",
}


async def parser_kufar_by(
    session: aiohttp.ClientSession,
    url: str,
    name: str,
    min_price: int,
    max_price: int,
):
    async with session.get(
        url.format(min_price=min_price, max_price=max_price), headers=header
    ) as resp:
        soup = bs4.BeautifulSoup(await resp.text(), "lxml")
        data = soup.find("script", {"id": "__NEXT_DATA__"})
        a = (
            json.loads(data.text)
            .get("props")
            .get("initialState")
            .get("listing")
            .get("ads")
        )
        for i in a:
            # print(i)
            for data in i.get("ad_parameters"):
                if data["p"] == "mileage":
                    odometer = int(data["v"])
                if data["p"] == "regdate":
                    year = int(data["v"])
            name = name
            link = i.get("ad_link")
            price_usd = int(i.get("price_usd")[:-2])
            price_byn = int(i.get("price_byn")[:-2])
            date_pub = datetime.strptime(
                i.get("list_time"), "%Y-%m-%dT%H:%M:%SZ"
            )

            async with get_db_session() as session:
                data: Result[tuple[Cars]] = await session.execute(
                    select(Cars).where(Cars.link == link)
                )
                date_result = data.scalar()
                if date_result is not None:
                    if date_result.price_usd != price_usd:
                        await session.execute(
                            update(Cars)
                            .where(Cars.id == date_result.id)
                            .values(
                                price_blr=price_byn,
                                price_usd=price_usd,
                                date_add=datetime.today(),
                            )
                        )
                        await session.commit()
                else:
                    await session.execute(
                        insert(Cars).values(
                            name=name,
                            site="kufar.by",
                            link=link,
                            date_pub=date_pub,
                            price_usd=price_usd,
                            price_blr=price_byn,
                            odometer=odometer,
                            year=year,
                        )
                    )
                    await session.commit()


async def main(min_price, max_price):
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(80),
        connector=aiohttp.TCPConnector(limit=2),
    ) as session:
        task = [
            parser_kufar_by(
                session=session,
                url=key,
                name=model_dict[value],
                min_price=min_price,
                max_price=max_price,
            )
            for key, value in urls_list.items()
        ]
        return await asyncio.gather(*task)


if __name__ == "__main__":
    asyncio.run(main(min_price=12000, max_price=17000))
