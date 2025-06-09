"""
Удаление моеделей для av бай
"""

import aiohttp
import asyncio
import fake_useragent
from src.database.func import get_all_av_urls, delete_cars

user = fake_useragent.UserAgent(
    browsers=["Google", "Chrome", "Firefox", "Edge", "Opera", "Safari"],
    os=["Windows", "Linux", "Ubuntu"],
    platforms=["desktop"],
).random

header = {"user-agent": user}


async def delete_av(session: aiohttp.ClientSession, url: str):
    async with session.get(url, headers=header) as resp:
        result = await resp.json()
        id_ = result.get("id")
        if not result.get("status") == "active":
            await delete_cars(id_=id_)


async def main():
    urls_list = await get_all_av_urls()
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(80),
        connector=aiohttp.TCPConnector(limit=2),
    ) as session:
        task = [delete_av(session=session, url=url) for url in urls_list]
        return await asyncio.gather(*task)
