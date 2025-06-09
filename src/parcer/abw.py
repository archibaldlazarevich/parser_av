"""
Парсер сайта abw
"""

import dateparser
import aiohttp
import bs4
import asyncio
import fake_useragent
from datetime import datetime, timedelta

from src.database.create_db import get_db_session
from src.database.func import parser_abw
from src.database.models import Cars
from sqlalchemy import insert, select, Result, update


user = fake_useragent.UserAgent(
    browsers=["Google", "Chrome", "Firefox", "Edge", "Opera", "Safari"],
    os=["Windows", "Linux", "Ubuntu"],
    platforms=["desktop"],
).random
header = {"user-agent": user}

audi_url = (  # просто ссылку вставить из настроенного поиска на сайте и заменить цены на price_{min_price}:{max_price}
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
    "transmission_at#/region_minskaia-oblast/city_minsk#classified-listing-adverts"
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

mercedes_url = (
    "https://abw.by/cars/brand_mercedes/"
    "model_m-klasse/generation_ii-w164-rest/"
    "price_{min_price}:{max_price}/volume_:4.0/"
    "engine_benzin/transmission_at#classified-listing-adverts"
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
    mercedes_url,
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
    "m-klasse": "Mercedes_Benz",
}


async def parser_abw_by(
    session: aiohttp.ClientSession,
    url: str,
    min_price: int,
    max_price: int,
):
    """ "
    Функция парсера abw.by
    :param session:
    :param url: ссылка для парсинга
    :param min_price: минимальная цена в usd
    :param max_price: максимальная цена в usd
    :return:
    """
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
                data_car = i.find("a", {"class": "top__title"})
                data_link = data_car.get("href").split("/")
                if ',' in  data_car.text.split()[-1]:
                    result[8] = ''
                else:
                    result[8] = int(data_car.text.split()[-1])
                model = data_link[4]
                data_gas = i.find("ul", {"class": "top__params"}).text
                if "бензин" in data_gas:
                    result[7] = 1
                else:
                    result[7] = 0
                if model in model_dict:
                    name = model_dict[model]
                    result[1] = name
                    link_ = f"https://abw.by{'/'.join(data_link)}"
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
                    # locale.setlocale(locale.LC_ALL, ("ru_RU", "UTF-8"))
                    # date_pub = datetime.strptime(date_init.lower(), "%d %B %Y") # убрал, т.к работат на русском сервере и там системно такие же настройки
                    date_pub = dateparser.parse(
                        date_init.lower(), languages=["ru"]
                    )
                else:
                    date_pub = datetime.today()
                result[4] = date_pub
            elif i.attrs["class"] == ["price-byn"]:
                price_byn = int("".join(i.text[:-2].split()))
                result[5] = price_byn
            elif i.attrs["class"] == ["price-usd"]:
                price_usd = int("".join(i.contents[1].split()[:2]))
                result[6] = price_usd

            if len(result) == 8:
                if result[7] == 1:
                    await parser_abw(result=result)
                    result.clear()
                else:
                    result.clear()


async def main(min_price, max_price):
    """
    Функция запуска парсера для сайта www.abw.by
    :param min_price: минимальная цена
    :param max_price: максимальная цена
    :return:
    """
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
