# запрос в аbw.by на определенные данные
# https://abw.by/cars/brand_audi/model_q5/generation_i-8r-rest/price_:17000/engine_benzin/transmission_at#classified-listing-adverts

import aiohttp
import bs4
import asyncio
import fake_useragent
import json

user = fake_useragent.UserAgent(
    browsers=['Google', 'Chrome', 'Firefox', 'Edge', 'Opera', 'Safari'],
    os=['Windows', 'Linux', 'Ubuntu'],
    platforms=['desktop']
).random
header = {'user-agent': user}


async def parser_audi_8r_abw_by(price: str):
    url = f'https://abw.by/cars/brand_audi/model_q5/generation_i-8r-rest/price_:{price}/engine_benzin/transmission_at#classified-listing-adverts'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=header) as resp:
            soup = bs4.BeautifulSoup(await resp.text(), 'lxml')
            data = soup.find_all(['div', 'span'], {'class': ['top__left', 'price-usd', 'bottom__additional']})
            for i in data:
                if i.find('a', {'class': 'top__title'}):
                    print(f'abw.by{i.find('a', {'class': 'top__title'}).get('href')}')
                elif i.find('span', {'class': 'bottom__city'}):
                    print(i.contents[1].text)
                else:
                    print(int(''.join(i.contents[1].split()[:2])))



asyncio.run(parser_audi_8r_abw_by('17000'))