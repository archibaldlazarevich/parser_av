import datetime

from sqlalchemy import select, func, and_, delete, insert, update, Result

from src.database.create_db import get_db_session
from src.database.models import Cars, Users


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
    :return: list
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


async def get_aver_year(car_name: str) -> int:
    """
    Метод, возвращаюший средний год выпуска авто из бд по названию
    :param car_name: название автомобиля
    :return: int
    """
    async with get_db_session() as session:
        data = await session.execute(
            select(func.round(func.avg(Cars.year))).where(
                Cars.name == car_name
            )
        )
    return int(data.scalar())


async def get_aver_cost(car_name: str) -> int:
    """
    Метод, возвращающий среднюю стоимость авто
    :param car_name: название автомобиля
    :return: int
    """
    async with get_db_session() as session:
        data = await session.execute(
            select(func.round(func.avg(Cars.price_usd))).where(
                Cars.name == car_name
            )
        )
    return int(data.scalar())


async def get_car_year(car_name: str) -> list:
    """
    Мето, возвращающий список годов выпуска авто
    :param car_name: нименование автомобиля
    :return: list
    """

    async with get_db_session() as session:
        data = await session.execute(
            select(Cars.year)
            .where(Cars.name == car_name)
            .distinct()
            .order_by(Cars.year)
        )
        car_year = [i[0] for i in data.all()]
    return car_year


async def get_aver_cost_by_year(car_name: str, year: int) -> int:
    """
    Метод, возвращающий среднюю цену на авто по году выпуска
    :param car_name: наименование автомобиля
    :param year: год автомобиля
    :return: int
    """

    async with get_db_session() as session:
        data = await session.execute(
            select(func.round(func.avg(Cars.price_usd))).filter(
                and_(Cars.name == car_name, Cars.year == year)
            )
        )
    return int(data.scalar())


async def get_users_id() -> list | None:
    """
    Метод возвращаюший список id пользователей подписанных на обновления
    :return: list
    """
    async with get_db_session() as session:
        data = await session.execute(select(Users.chat_id))
        data_all = data.all()
    return data_all


async def get_all_av_urls():
    """
    Метод, возвращающий список доступных ссылок на модели
    :return:
    """
    async with get_db_session() as session_db:
        urls = await session_db.execute(
            select(Cars.link).where(Cars.site == "av.by")
        )
        urls_list = [
            f"https://api.av.by/offers/{i[0].split('/')[-1]}"
            for i in urls.all()
        ]
    return urls_list


async def delete_cars(id_: int):
    """
    Метод, удаляющий сущность недейсвтующей ссылки
    :param id_:
    :return:
    """
    async with get_db_session() as session_db:
        await session_db.execute(delete(Cars).where(Cars.link.contains(id_)))
        await session_db.commit()


async def parser_abw(result: dict):
    """
    Метод добавляющий новые данные в базу данных при парсинге abw
    :param result:
    :return:
    """
    async with get_db_session() as session:
        data: Result[tuple[Cars]] = await session.execute(
            select(Cars).where(Cars.link == result[2])
        )
        date_result = data.scalar()
        if date_result is not None:
            if date_result.price_usd != result[6]:
                await session.execute(
                    update(Cars)
                    .where(Cars.id == date_result.id)
                    .values(
                        price_blr=result[5],
                        price_usd=result[6],
                        date_add=datetime.datetime.now(),
                    )
                )
                await session.commit()
        else:
            await session.execute(
                insert(Cars).values(
                    name=result[1],
                    site="abw.by",
                    link=result[2],
                    date_pub=result[4],
                    price_usd=result[6],
                    price_blr=result[5],
                    odometer=result[3],
                    year=result[8],
                )
            )
            await session.commit()


async def parser_av(
        name: str,
        year: int,
        link: str,
        date_pub: datetime.datetime.now,
        price_byn: int,
        price_usd: int,
        odometer: int,
):
    """
    Метод добавляющий новые данные в базу данных при парсинге av
    :param name: Название модели
    :param year: год производства авто
    :param link: сслыка на объявление
    :param date_pub: дата публикации
    :param price_byn: цена в BYN
    :param price_usd: цена в USD
    :param odometer: показатель одометра
    :return:
    """
    async with get_db_session() as session:
        data: Result[tuple[Cars]] = await session.execute(
            select(Cars).where(Cars.link == link)
        )
        date_result = data.scalar()
        if date_result is not None:
            if date_result.price_usd != price_usd:
                await session.execute(
                    update(Cars)
                    .where(Cars.id == date_result.id)
                    .values(
                        price_blr=price_byn,
                        price_usd=price_usd,
                        date_add=datetime.datetime.now(),
                    )
                )
                await session.commit()
        else:
            await session.execute(
                insert(Cars).values(
                    name=name,
                    site="av.by",
                    link=link,
                    date_pub=date_pub,
                    price_usd=price_usd,
                    price_blr=price_byn,
                    odometer=odometer,
                    year=year,
                )
            )
            await session.commit()


async def parser_kufar(
        name: str,
        year: int,
        link: str,
        date_pub: datetime.datetime.now,
        price_byn: int,
        price_usd: int,
        odometer: int,
):
    """
    Метод добавляющий новые данные в базу данных при парсинге kufar
    :param name: Название модели
    :param year: год производства авто
    :param link: сслыка на объявление
    :param date_pub: дата публикации
    :param price_byn: цена в BYN
    :param price_usd: цена в USD
    :param odometer: показатель одометра
    :return:
    """

    async with get_db_session() as session:
        data: Result[tuple[Cars]] = await session.execute(
            select(Cars).where(Cars.link == link)
        )
        date_result = data.scalar()
        if date_result is not None:
            if date_result.price_usd != price_usd:
                await session.execute(
                    update(Cars)
                    .where(Cars.id == date_result.id)
                    .values(
                        price_blr=price_byn,
                        price_usd=price_usd,
                        date_add=datetime.datetime.now(),
                    )
                )
                await session.commit()
        else:
            await session.execute(
                insert(Cars).values(
                    name=name,
                    site="kufar.by",
                    link=link,
                    date_pub=date_pub,
                    price_usd=price_usd,
                    price_blr=price_byn,
                    odometer=odometer,
                    year=year,
                )
            )
            await session.commit()


async def check_update(id_: int):
    """
    Проверка на подписку
    :param id_:
    :return:
    """
    async with get_db_session() as session:
        result = await session.execute(
            select(Users.chat_id).where(
                Users.chat_id == id_,
            )
        )
    return result.scalar()


async def update_insert(id_: int):
    """
    Функция подпискиина обновления
    :param id_:
    :return:
    """
    async with get_db_session() as session:
        await session.execute(
            insert(Users).values(
                chat_id=id_, date=datetime.datetime.now()
            )
        )
        await session.commit()

async def delete_update(id_: int):
    """
    Функци отмены подписки
    :param id_:
    :return:
    """
    async with get_db_session() as session:
        await session.execute(
            delete(Users).where(Users.chat_id == id_)
        )
        await session.commit()