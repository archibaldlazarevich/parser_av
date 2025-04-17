import asyncio
from src.database.create_db import create_db

if __name__ == '__main__':
    asyncio.run(create_db())