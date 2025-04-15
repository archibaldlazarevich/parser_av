from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool
from typing import AsyncGenerator
from config.config import DATABASE_URL
from models import Base


engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True,
    poolclass=NullPool,
)

async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncGenerator:
    async with async_session_maker() as session:
        yield session


async def create_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
