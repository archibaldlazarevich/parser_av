# запрос в ав бай на определенные данные
# https://cars.av.by/filter?brands[0][brand]=6&brands[0][model]=2093&brands[0][generation]=94&price_usd[max]=17000&transmission_type[0]=1&transmission_type[1]=3&transmission_type[2]=4&engine_type[0]=1

import aiohttp
import bs4
import asyncio
import fake_useragent
import json

user = fake_useragent.UserAgent(
    browsers=["Google", "Chrome", "Firefox", "Edge", "Opera", "Safari"],
    os=["Windows", "Linux", "Ubuntu"],
    platforms=["desktop"],
).random

header = {"user-agent": user}

audi_url = (
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
    "[model]=1596&brands[0][generation]=3266&price_usd[min]={min_price}"
    "&price_usd[max]={max_price}&transmission_type[0]=1"
    "&transmission_type[1]=3&transmission_type[2]=4&engine_type[0]=1"
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

urls_list = [
    audi_url,
    nissan_url,
    mits_url,
    chevr_url,
    volvo_url,
    mazda_url,
    kia_sor_url,
    kia_sport_url,
]


async def parser_av_by(
    session: aiohttp.ClientSession, url: str, min_price: int, max_price: int
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
            .get("filter")
            .get("main")
            .get("adverts")
        )
        for i in a:
            print(i.get("price").get("usd").get("amount"))
            print(i.get("publishedAt"))
            print(i.get("publicUrl"))


async def main(min_price, max_price):
    async with aiohttp.ClientSession(
        # timeout=aiohttp.ClientTimeout(60),
        # connector=aiohttp.TCPConnector(limit=10),
    ) as session:
        task = [
            parser_av_by(
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
