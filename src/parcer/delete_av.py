"""
Удаление моеделей для av бай
"""
import aiohttp
import asyncio
import fake_useragent

from sqlalchemy import select, delete

from src.database.create_db import get_db_session
from src.database.models import Cars

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
            async with get_db_session() as session_db:
                await session_db.execute(
                    delete(Cars).where(Cars.link.contains(id_))
                )
                await session_db.commit()


async def main():
    async with get_db_session() as session_db:
        urls = await session_db.execute(
            select(Cars.link).where(Cars.site == "av.by")
        )
        urls_list = [
            f"https://api.av.by/offers/{i[0].split('/')[-1]}"
            for i in urls.all()
        ]
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(80),
        connector=aiohttp.TCPConnector(limit=2),
    ) as session:
        task = [delete_av(session=session, url=url) for url in urls_list]
        return await asyncio.gather(*task)


# if __name__ == "__main__":
#     asyncio.run(main())
