import locale
import dateparser
import aiohttp
import bs4
import asyncio
import fake_useragent
from typing import Annotated
from datetime import datetime, timedelta

from scrapy.utils.project import data_path
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.create_db import get_db_session
from src.database.models import Cars
from sqlalchemy import insert, select, Result, update


user = fake_useragent.UserAgent(
    browsers=["Google", "Chrome", "Firefox", "Edge", "Opera", "Safari"],
    os=["Windows", "Linux", "Ubuntu"],
    platforms=["desktop"],
).random
header = {"user-agent": user}

audi_url = (
    "https://abw.by/cars/brand_audi/model_q5/generation_i-8r-rest"
    "/price_{min_price}:{max_price}/engine_benzin/transmission_at"
    "#classified-listing-adverts"
)
nissan_url = (
    "https://abw.by/cars/brand_nissan/model_x-trail"
    "/generation_iii/price_{min_price}:{max_price}/engine_benzin/"
    "transmission_at#classified-listing-adverts"
)
mits_url_1 = (
    "https://abw.by/cars/brand_mitsubishi/model_outlander/"
    "generation_iii/price_{min_price}:{max_price}/engine_benzin/"
    "transmission_at#classified-listing-adverts"
)
mits_url_2 = (
    "https://abw.by/cars/brand_mitsubishi/model_outlander/"
    "generation_iii-rest/price_{min_price}:{max_price}/engine_benzin/"
    "transmission_at#classified-listing-adverts"
)
mits_url_3 = (
    "https://abw.by/cars/brand_mitsubishi/model_outlander/"
    "generation_iii-rest-2/price_{min_price}:{max_price}/"
    "engine_benzin/transmission_at#classified-listing-adverts"
)
chevr_url = (
    "https://abw.by/cars/brand_chevrolet/model_equinox/"
    "generation_iii/price_{min_price}:{max_price}/engine_benzin/"
    "transmission_at#classified-listing-adverts"
)
volvo_url = (
    "https://abw.by/cars/brand_volvo/model_xc60/generation_i/price_{min_price}"
    ":{max_price}/engine_benzin/transmission_at#"
    "classified-listing-adverts"
)
mazda_url = (
    "https://abw.by/cars/brand_mazda/model_cx-5/price_{min_price}:"
    "{max_price}/engine_benzin/transmission_at#c"
    "lassified-listing-adverts"
)
kia_sport_url = (
    "https://abw.by/cars/brand_kia/model_sportage/"
    "price_{min_price}:"
    "{max_price}/engine_benzin/transmission_at#"
    "classified-listing-adverts"
)
kia_sor_url = (
    "https://abw.by/cars/brand_kia/model_sorento/"
    "price_{min_price}:"
    "{max_price}/engine_benzin/transmission_at#c"
    "lassified-listing-adverts"
)

hyundai_url = (
    "https://abw.by/cars/brand_hyundai/model_santa-fe/"
    "generation_iii/price_{min_price}:{max_price}/"
    "engine_benzin/transmission_at#classified-listing-adverts"
)

toyota_url = (
    "https://abw.by/cars/brand_toyota/"
    "model_rav-4/generation_iv-xa40/"
    "price_{min_price}:{max_price}/engine_benzin/transmission_at?"
    "sort=new#classified-listing-adverts"
)

honda_url = (
    "https://abw.by/cars/brand_honda/"
    "model_cr-v/generation_iv/"
    "price_{min_price}:{max_price}/engine_benzin/"
    "transmission_at?sort=new#classified-listing-adverts"
)

urls_list = [
    audi_url,
    nissan_url,
    mits_url_1,
    mits_url_2,
    mits_url_3,
    chevr_url,
    volvo_url,
    mazda_url,
    kia_sor_url,
    kia_sport_url,
    hyundai_url,
    toyota_url,
    honda_url,
]

model_dict = {
    "q5": "Audi_q5",
    "x-trail": "Nissan_x_trail",
    "outlander": "Mitsubishi_outlander",
    "equinox": "Chevrolet_equinox",
    "xc60": "Volvo_cx60",
    "cx-5": "Mazda_cx5",
    "sportage": "Kia_spotage",
    "sorento": "Kia_sorento",
    "santa-fe": "Hyundai_santa_fe",
    "rav-4": "Toyota_Rav4",
    "cr-v": "Honda_CRV",
}


async def parser_abw_by(
    session: aiohttp.ClientSession,
    url: str,
    min_price: int,
    max_price: int,
):

    async with session.get(
        url.format(min_price=min_price, max_price=max_price), headers=header
    ) as resp:
        soup = bs4.BeautifulSoup(await resp.text(), "lxml")
        data_site = soup.find_all(
            ["div", "span"],
            {
                "class": [
                    "top__left",
                    "price-usd",
                    "price-byn",
                    "bottom__additional",
                ]
            },
        )
        result = {}
        for i in data_site:
            if i.attrs["class"] == ["top__left"]:
                data = (
                    i.find(
                        "a", {"class": "top__title"}
                           ).get("href").split("/")
                )
                model = data[4]
                if model in model_dict:
                    name = model_dict[model]
                    result[1] = name
                    link_ = f"https://abw.by{'/'.join(data)}"
                    result[2] = link_
                    odometer = int(
                        "".join(
                            i.find("ul", {"class": "top__params"})
                            .contents[1]
                            .text.split()[:-1]
                        )
                    )
                    result[3] = odometer
            elif i.find("span", {"class": "bottom__city"}):
                date_init = i.contents[1].text
                if "вчера" in date_init.lower():
                    date = date_init.split()
                    date_delta = datetime.strftime(
                        (datetime.today() - timedelta(days=1)), "%Y-%m-%d"
                    )
                    date_pub = datetime.strptime(
                        date_delta + date[2], "%Y-%m-%d%H:%M"
                    )
                elif "сегодня" in date_init.lower():
                    date = date_init.split()[2].split(":")
                    date_pub = datetime.today() - (
                        timedelta(minutes=int(date[1]))
                        + timedelta(hours=int(date[0]))
                    )
                elif "назад" not in date_init.lower():
                    #locale.setlocale(locale.LC_ALL, ("ru_RU", "UTF-8"))
                    #date_pub = datetime.strptime(date_init.lower(), "%d %B %Y")
                    date_pub = dateparser.parse(date_init.lower(), languages=['ru'])
                else:
                    date_pub = datetime.today()
                result[4] = date_pub
            elif i.attrs["class"] == ["price-byn"]:
                price_byn = int("".join(i.text[:-2].split()))
                result[5] = price_byn
            elif i.attrs["class"] == ["price-usd"]:
                price_usd = int("".join(i.contents[1].split()[:2]))
                result[6] = price_usd

            if len(result) == 6:
                async with get_db_session() as session:
                    data: Result[tuple[Cars]] = await session.execute(
                        select(Cars).where(Cars.link == result[2])
                    )
                    date_result = data.scalar()
                    if date_result is not None:
                        if date_result.price_blr != result[5]:
                            await session.execute(
                                update(Cars)
                                .where(Cars.id == date_result.id)
                                .values(
                                    price_blr=result[5],
                                    price_usd=result[6],
                                    date_add=datetime.today(),
                                )
                            )
                            await session.commit()
                    else:
                        await session.execute(
                            insert(Cars).values(
                                name=result[1],
                                site="abw.by",
                                link=result[2],
                                date_pub=result[4],
                                price_usd=result[6],
                                price_blr=result[5],
                                odometer=result[3],
                            )
                        )
                        await session.commit()
                result.clear()


async def main(min_price, max_price):
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(80),
        connector=aiohttp.TCPConnector(limit=2),
    ) as session:
        task = [
            parser_abw_by(
                session=session,
                url=url,
                min_price=min_price,
                max_price=max_price,
            )
            for url in urls_list
        ]
        return await asyncio.gather(*task)


if __name__ == "__main__":
    asyncio.run(main(min_price=12000, max_price=17000))
