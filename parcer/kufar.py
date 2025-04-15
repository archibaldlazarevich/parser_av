# запрос в куфар на определенные данные
# https://auto.kufar.by/l/cars/audi-q5-i-8r-restajling?cre=v.or%3A1&crg=1&cur=USD&prc=r%3A0%2C17000

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

audi_url = ("https://auto.kufar.by/l/cars/audi-q5-i-8r-restajling"
            "?cre=v.or%3A1&crg=1&cur=USD&prc=r%3A{min_price}%2C{max_price}")
nissan_url = ("https://auto.kufar.by/l/cars/nissan-x-trail-iii"
              "?cre=v.or%3A1&crg=1&cur=USD&prc=r%3A{min_price}%2C{max_price}")
mits_url = ("https://auto.kufar.by/l/cars/mitsubishi-outlander?"
            "cre=v.or%3A1&crg=1&cur=USD&prc=r%3A{min_price}"
            "%2C{max_price}&rgd=r%3A2012%2C2022")
chevr_url = ("https://auto.kufar.by/l/cars/chevrolet-equinox-iii?"
             "cre=v.or%3A1&crg=1&cur=USD&prc=r%3A{min_price}%2C{max_price}")
volvo_url = ("https://auto.kufar.by/l/cars/volvo-xc60?cre=v.or"
             "%3A1&crg=1&cur=USD&prc=r%3A{min_price}%2C{max_price}")
mazda_url = ("https://auto.kufar.by/l/cars/mazda-cx-5?cre=v.or"
             "%3A1&crg=1&cur=USD&prc=r%3A{min_price}%2C{max_price}")
kia_sport_url = ("https://auto.kufar.by/l/cars/kia-sportage?cre="
                 "v.or%3A1&crg=1&cur=USD&prc=r%3A{min_price}%2C{max_price}")
kia_sor_url = ("https://auto.kufar.by/l/cars/kia-sorento?cre="
               "v.or%3A1&crg=1&cur=USD&prc=r%3A{min_price}"
               "%2C{max_price}&rgd=r%3A2011%2C2022")

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


async def parser_kufar_by(
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
            .get("listing")
            .get("ads")
        )
        for i in a:
            print(i.get("ad_link"))
            print(i.get("price_usd")[:-2])
            print(i.get("price_byn")[:-2])
            print(i.get("list_time"))


async def main(min_price, max_price):
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(60),
        connector=aiohttp.TCPConnector(limit=3),
    ) as session:
        task = [
            parser_kufar_by(
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
