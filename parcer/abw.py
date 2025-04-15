# запрос в аbw.by на определенные данные
# https://abw.by/cars/brand_audi/model_q5/generation_i-8r-rest/price_:17000/engine_benzin/transmission_at#classified-listing-adverts

import aiohttp
import bs4
import asyncio
import fake_useragent

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
mits_url_3 = ("https://abw.by/cars/brand_mitsubishi/model_outlander/"
              "generation_iii-rest-2/price_{min_price}:{max_price}/"
              "engine_benzin/transmission_at#classified-listing-adverts")
chevr_url = ("https://abw.by/cars/brand_chevrolet/model_equinox/"
             "generation_iii/price_{min_price}:{max_price}/engine_benzin/"
             "transmission_at#classified-listing-adverts")
volvo_url = ("https://abw.by/cars/brand_volvo/model_xc60/price_{min_price}"
             ":{max_price}/engine_benzin/transmission_at#"
             "classified-listing-adverts")
mazda_url = ("https://abw.by/cars/brand_mazda/model_cx-5/price_{min_price}:"
             "{max_price}/engine_benzin/transmission_at#c"
             "lassified-listing-adverts")
kia_sport_url = ("https://abw.by/cars/brand_kia/model_sportage/"
                 "price_{min_price}:"
                 "{max_price}/engine_benzin/transmission_at#"
                 "classified-listing-adverts")
kia_sor_url = ("https://abw.by/cars/brand_kia/model_sorento/"
               "price_{min_price}:"
               "{max_price}/engine_benzin/transmission_at#c"
               "lassified-listing-adverts")

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
]


async def parser_abw_by(
    session: aiohttp.ClientSession, url: str, min_price: int, max_price: int
):
    async with session.get(
        url.format(min_price=min_price, max_price=max_price), headers=header
    ) as resp:
        soup = bs4.BeautifulSoup(await resp.text(), "lxml")
        data = soup.find_all(
            ["div", "span"],
            {"class": ["top__left", "price-usd", "bottom__additional"]},
        )
        for i in data:
            if i.find("a", {"class": "top__title"}):
                print(
                    f"abw.by{i.find('a', {'class': 'top__title'}).get('href')}"
                )
            elif i.find("span", {"class": "bottom__city"}):
                print(i.contents[1].text)
            else:
                print(int("".join(i.contents[1].split()[:2])))


async def main(min_price, max_price):
    async with aiohttp.ClientSession(
        # timeout=aiohttp.ClientTimeout(60),
        # connector=aiohttp.TCPConnector(limit=10),
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
