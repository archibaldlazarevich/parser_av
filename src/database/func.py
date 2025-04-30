import datetime

from sqlalchemy import select, func

from src.database.create_db import get_db_session
from src.database.models import Cars


async def get_car_name() -> list:
    """
    Метод возвращает уникальные марки авто из бд
    :return: list
    """
    async with get_db_session() as session:
        result = await session.execute(select(Cars.name).distinct())
        car_name = [i[0] for i in result.all()]
    return car_name


async def get_all_cars() -> int:
    """
    Метод возвращает общее число автомобилей в бд
    :return: int
    """
    async with get_db_session() as session:
        data = await session.execute(select(func.count(Cars.id)))
    return data.scalar()


async def get_spec_cars_number(car_name: str) -> int:
    """
    Метод, возвращающий число автомобилей искомой марки в бд
    :param car_name: наименование марки авто
    :return: int
    """

    async with get_db_session() as session:
        data = await session.execute(
            select(func.count(Cars.id)).where(Cars.name == car_name)
        )
    return data.scalar()


async def get_all_spec_models(model: str) -> list:
    """
    Метод, возвращающий список всех автомобилей запрашиваемой модели
    :param model: модель автомобиля
    :return: str
    """
    async with get_db_session() as session:
        data = await session.execute(
            select(Cars.link).where(Cars.name == model)
        )
    return data.all()


async def get_update_models() -> list:
    """
    Метод, возвращающий список новых авто в зависимости от даты авторизации пользователя
    :return: list
    """

    star_tdata = datetime.datetime.today() - datetime.timedelta(minutes=45)
    async with get_db_session() as session:
        data = await session.execute(
            select(Cars.link).filter(
                Cars.date_add.between(star_tdata, datetime.datetime.today())
            )
        )
    return data.all()
