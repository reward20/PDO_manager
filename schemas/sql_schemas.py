from datetime import date
from decimal import Decimal
from sqlalchemy import VARCHAR, CheckConstraint, Date, DECIMAL, CHAR, Column, INTEGER, BIGINT
from sqlalchemy.orm import DeclarativeBase, declared_attr

from typing import TYPE_CHECKING

__all__ = [
    "Base",
    "Mlexcel_model",
]


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()


class Mlexcel_model(Base):

    if TYPE_CHECKING:
        id: int
        mr_list: str
        order: str
        detail_num: str
        detail_count: str
        date_start: date
        mass_metall: Decimal
        mass_detail: Decimal
        w_hours: Decimal
        material: str
        profile_full: str
        profile: str
        det_in_workpiece: int
    else:
        id = Column(INTEGER, primary_key=True)
        mr_list = Column(CHAR(8), name="Маршрутный лист", nullable=False, unique=True)
        order = Column(CHAR(5), name="Заказ", nullable=False)
        detail_num = Column(VARCHAR(128), name="Номер детали", nullable=False)
        detail_name = Column(VARCHAR(128), name="Имя детали")
        detail_count = Column(INTEGER, nullable=False, name="Кол.")
        date_start = Column(Date, nullable=False, name="Дата запуска")
        mass_metall = Column(DECIMAL(scale=3), nullable=False, name="Расход. матер.")
        mass_detail = Column(DECIMAL(scale=3), nullable=False, name="Масса детали")
        w_hours = Column(DECIMAL(scale=3), nullable=False, name="Норм.часы")
        material = Column(VARCHAR(128), name="Материал")
        profile_full = Column(VARCHAR(128), name="Профиль заготовки")
        profile = Column(VARCHAR(64), name="Профиль")
        det_in_workpiece = Column(INTEGER, name="Дет. из заготовки")

    def __str__(self):
        return self.mr_list

    __table_args__ = (
        CheckConstraint("'Кол.' >= 0"),
        CheckConstraint("'Расход. матер.' >= 0"),
        CheckConstraint("'Масса детали' >= 0"),
        CheckConstraint("'Дет. из заготовки' > 0"),
    )
