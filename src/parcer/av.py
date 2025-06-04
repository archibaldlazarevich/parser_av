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

audi_url = ( # просто ссылку вставить из настроенного поиска на сайте и заменить цены на price_{min_price}:{max_price}
    "https://cars.av.by/filter?brands[0][brand]=6&brands[0]"
    "[model]=2093&brands[0][generation]="
    "94&price_usd[min]={min_price}"
    "&price_usd[max]={max_price}&transmission_type[0]=1&"
    "transmission_type[1]=3&transmission_type[2]=4&engine_type[0]=1"
)
nissan_url = (
    "https://cars.av.by/filter?brands[0][brand]=892&brands[0]"
    "[model]=964&brands[0][generation]=1849&"
    "price_usd[min]={min_price}"
    "&price_usd[max]={max_price}&transmission_type"
    "[0]=1&transmission_type[1]=3&"
    "transmission_type[2]=4&engine_type[0]=1"
)
mits_url = (
    "https://cars.av.by/filter?brands[0][brand]=834&brands[0]"
    "[model]=875&price_usd[min]={min_price}"
    "&price_usd[max]={max_price}"
    "&transmission_type[0]=1&transmission_type[1]=3"
    "&transmission_type[2]=4&engine_type[0]=1"
)
chevr_url = (
    "https://cars.av.by/filter?brands[0][brand]=41&brands[0]"
    "[model]=1596&brands[0][generation]=3266&"
    "price_usd[min]={min_price}&price_usd[max]={max_price}&"
    "transmission_type[0]=1&transmission_type[1]=3&"
    "transmission_type[2]=4&engine_type[0]=1&place_region[0]=1005"
)
volvo_url = (
    "https://cars.av.by/filter?brands[0][brand]=1238&brands[0]"
    "[model]=2098&brands[0][generation]=2781&price_usd[min]={min_price}"
    "&price_usd[max]={max_price}&transmission_type[0]=1"
    "&transmission_type[1]=3&transmission_type[2]=4&engine_type[0]=1"
)
mazda_url = (
    "https://cars.av.by/filter?brands[0][brand]=634&brands[0]"
    "[model]=2397&price_usd[min]={min_price}&price_usd[max]={max_price}"
    "&transmission_type[0]=1&transmission_type[1]=3"
    "&transmission_type[2]=4&engine_type[0]=1"
)
kia_sport_url = (
    "https://cars.av.by/filter?brands[0]"
    "[brand]=545&brands[0][model]=569&price_usd[min]={min_price}"
    "&price_usd[max]={max_price}&transmission_type[0]=1"
    "&transmission_type[1]=3"
    "&transmission_type[2]=4&engine_type[0]=1"
)
kia_sor_url = (
    "https://cars.av.by/filter?brands[0][brand]=545&brands[0]"
    "[model]=567&year[min]=2011&price_usd[min]={min_price}"
    "&price_usd[max]={max_price}&transmission_type[0]=1"
    "&transmission_type[1]=3&transmission_type[2]=4"
    "&engine_type[0]=1"
)

hyundai_url = (
    "https://cars.av.by/filter?brands[0][brand]=433&brands[0]"
    "[model]=453&brands[0][generation]=973&"
    "price_usd[min]={min_price}&"
    "price_usd[max]={max_price}&engine_type[0]=1"
)

toyota_url = (
    "https://cars.av.by/filter?brands[0]"
    "[brand]=1181&brands[0][model]=1209&"
    "brands[0][generation]=2462&price_usd[min]={min_price}"
    "&price_usd[max]={max_price}"
    "&transmission_type[0]=1&transmission_type[1]=3"
    "&transmission_type[2]=4&engine_type[0]=1"
)

honda_url = (
    "https://cars.av.by/filter?brands[0]"
    "[brand]=383&brands[0][model]=393&brands[0]"
    "[generation]=816&price_usd[min]={min_price}&price_usd[max]={max_price}&"
    "transmission_type[0]=1&transmission_type[1]=3&"
    "transmission_type[2]=4&engine_type[0]=1"
)

mercedes_url = (
    "https://cars.av.by/filter?brands[0]"
    "[brand]=683&brands[0][model]=789&brands[0]"
    "[generation]=4661&price_usd[min]={min_price}&price_usd[max]={max_price}"
    "&engine_capacity[max]=3600&transmission_type[0]=1&transmission_type[1]=3&"
    "transmission_type[2]=4&engine_type[0]=1"
)

urls_list = [
    audi_url,
    nissan_url,
    mits_url,
    chevr_url,
    volvo_url,
    mazda_url,
    kia_sor_url,
    kia_sport_url,
    hyundai_url,
    toyota_url,
    honda_url,
    mercedes_url,
]

all_urls = []

for number in range(1, 11):
    urls = [url + f"&page={number}" for url in urls_list]
    all_urls.extend(urls)

model_dict = {
    2093: "Audi_q5", # 2093 - код автомобиля из API AV.by, так же есть в ссылке из поиска авто пример - [model]=2093
    964: "Nissan_x_trail",
    875: "Mitsubishi_outlander",
    1596: "Chevrolet_equinox",
    2098: "Volvo_cx60",
    2397: "Mazda_cx5",
    569: "Kia_spotage",
    567: "Kia_sorento",
    453: "Hyundai_santa_fe",
    1209: "Toyota_Rav4",
    393: "Honda_CRV",
    789: "Mercedes_Benz",
}


async def parser_av_by(
    session: aiohttp.ClientSession, url: str, min_price: int, max_price: int
):
    """
    Функция парсера av.by
    :param session:
    :param url: ссылка для парсинга
    :param min_price: минимальная цена в usd
    :param max_price: максимальная цена в usd
    :return:
    """
    async with session.get(
        url.format(min_price=min_price, max_price=max_price, page=number),
        headers=header,
    ) as resp:
        soup = bs4.BeautifulSoup(await resp.text(), "lxml")
        data = soup.find("script", {"id": "__NEXT_DATA__"})
        a = (
            json.loads(data.text)
            .get("props")
            .get("initialState")
            .get("filter")
            .get("main")
            .get("adverts")
        )
        if not a is None:
            for i in a:
                price_usd = i.get("price").get("usd").get("amount")
                price_byn = i.get("price").get("byn").get("amount")
                date_pub = datetime.strptime(
                    i.get("publishedAt"), "%Y-%m-%dT%H:%M:%S+0000"
                )
                link = i.get("publicUrl")
                year = i.get("year")
                name = model_dict[i.get("metadata").get("modelId")]
                for prop in i.get("properties"):
                    if prop["name"] == "mileage_km":
                        odometer = prop.get("value")

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
                                site="av.by",
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
            parser_av_by(
                session=session,
                url=url,
                min_price=min_price,
                max_price=max_price,
            )
            for url in all_urls
        ]
        return await asyncio.gather(*task)


# if __name__ == "__main__":
#     asyncio.run(main(min_price=12000, max_price=17000))
