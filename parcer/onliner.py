# запрос на onliner на определенные данные
# https://ab.onliner.by/audi/q5/8r-restayling?location%5Bcountry%5D=248&engine_type%5B0%5D=gasoline&transmission%5B0%5D=automatic&price%5Bto%5D=17000&price%5Bcurrency%5D=USD

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
    url = f'https://ab.onliner.by/audi/q5/8r-restayling?location%5Bcountry%5D=248&engine_type%5B0%5D=gasoline&transmission%5B0%5D=automatic&price%5Bto%5D={price}&price%5Bcurrency%5D=USD'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=header) as resp:
            soup = bs4.BeautifulSoup(await resp.text(), 'lxml')
            print(soup)
            # data = soup.find('script', {'id': '__NEXT_DATA__'})
            # a = json.loads(data.text).get('props').get('initialState').get('listing').get('ads')
            # for i in a:
            #     print(i.get('ad_link'))
            #     print(i.get('price_usd')[:-2])
            #     print(i.get('price_byn')[:-2])
            #     print(i.get('list_time'))




asyncio.run(parser_audi_8r_kufar_by('17000'))