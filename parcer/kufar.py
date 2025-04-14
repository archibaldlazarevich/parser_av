# запрос в куфар на определенные данные
# https://auto.kufar.by/l/cars/audi-q5-i-8r-restajling?cre=v.or%3A1&crg=1&cur=USD&prc=r%3A0%2C17000

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


async def parser_audi_8r_kufar_by(price: str):
    url = f'https://auto.kufar.by/l/cars/audi-q5-i-8r-restajling?cre=v.or%3A1&crg=1&cur=USD&prc=r%3A0%2C{price}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=header) as resp:
            soup = bs4.BeautifulSoup(await resp.text(), 'lxml')
            data = soup.find('script', {'id': '__NEXT_DATA__'})
            a = json.loads(data.text).get('props').get('initialState').get('listing').get('ads')
            for i in a:
                print(i.get('ad_link'))
                print(i.get('price_usd')[:-2])
                print(i.get('price_byn')[:-2])
                print(i.get('list_time'))




asyncio.run(parser_audi_8r_kufar_by('17000'))