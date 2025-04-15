import datetime
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.types import Date, Integer


class Base(DeclarativeBase):
    pass


class Cars(Base):
    __tablename__ = "cars"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    site: Mapped[str] = mapped_column(String(20), nullable=False)
    link: Mapped[str] = mapped_column(String(), nullable=False)
    date_pub: Mapped[datetime.datetime] = mapped_column(Date, nullable=False)
    date_add: Mapped[datetime.datetime] = mapped_column(
        Date, default=datetime.date, nullable=False
    )
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    odometer: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self) -> str:
        return (
            f"Car (id={self.id!r}, name={self.name!r}, "
            f"site={self.site!r}, link={self.link!r}, "
            f"date_pub={self.date_pub!r}, "
            f"date_add={self.date_add!r}, price={self.price!r})"
        )
