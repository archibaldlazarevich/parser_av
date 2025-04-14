# запрос в ав бай на определенные данные
# https://cars.av.by/filter?brands[0][brand]=6&brands[0][model]=2093&brands[0][generation]=94&price_usd[max]=17000&transmission_type[0]=1&transmission_type[1]=3&transmission_type[2]=4&engine_type[0]=1

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

async def parser_audi_8r_av_by(price: str):
    url = f'https://cars.av.by/filter?brands[0][brand]=6&brands[0][model]=2093&brands[0][generation]=94&price_usd[max]={price}&transmission_type[0]=1&transmission_type[1]=3&transmission_type[2]=4&engine_type[0]=1'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=header) as resp:
            soup = bs4.BeautifulSoup(await resp.text(), 'lxml')
            data = soup.find('script', {'id': '__NEXT_DATA__'})
            a = json.loads(data.text).get('props').get('initialState').get('filter').get('main').get('adverts')
            for i in a:
                print(i.get('price').get('usd').get('amount'))
                print(i.get('publishedAt'))
                print(i.get('publicUrl'))

asyncio.run(parser_audi_8r_av_by('17000'))

# def simple(price: str):
#     url = f'https://cars.av.by/filter?brands[0][brand]=6&brands[0][model]=2093&brands[0][generation]=94&price_usd[max]={price}&transmission_type[0]=1&transmission_type[1]=3&transmission_type[2]=4&engine_type[0]=1'
#     result = requests.get(url = url, headers=header)
#     soup = bs4.BeautifulSoup(result.text, 'lxml')
#     data = soup.find('script', {'id': '__NEXT_DATA__'})
#     a = json.loads(data.text).get('props').get('initialState').get('filter').get('main').get('adverts')
#     for i in a:
#         print(i.get('price').get('usd').get('amount'))
#         print(i.get('publishedAt'))
#         print(i.get('publicUrl'))
# start_2 = time.time()
# simple('17000')
# print('2:', time.time() - start_2)

