
from datetime import date
from decimal import Decimal
from sqlalchemy import (
    VARCHAR,
    CheckConstraint,
    Date,
    DECIMAL,
    CHAR,
    Column,
    INTEGER,
)
from .base import Base
from typing import TYPE_CHECKING

__all__ = [
    "Mlexcel_model",
    "Operation",
]


class Mlexcel_model(Base):

    __tablename__ = "ml_excel"

    if TYPE_CHECKING:
        id: int
        mr_list: str
        order: str
        detail_num: str
        count: int
        date_start: date
        mass_metal: Decimal
        mass_detail: Decimal
        w_hours: Decimal
        material: str
        profile_full: str
        profile: str
        det_in_workpiece: int
    else:
        id = Column(INTEGER, primary_key=True)
        order = Column(CHAR(5), nullable=False)
        mr_list = Column(CHAR(8), nullable=False, unique=True)
        detail_num = Column(VARCHAR(128), nullable=False)
        count = Column(INTEGER, nullable=False)
        w_hours = Column(DECIMAL(scale=3), nullable=False)
        date_start = Column(Date, nullable=False)
        complite = Column(CHAR(1), nullable=True)
        date_complite = Column(Date, nullable=True)
        detail_name = Column(VARCHAR(128))
        mass_metal = Column(DECIMAL(scale=3), nullable=False)
        mass_detail = Column(DECIMAL(scale=3), nullable=False)
        material = Column(VARCHAR(128))
        profile_full = Column(VARCHAR(128))
        profile = Column(VARCHAR(64))
        det_in_workpiece = Column(INTEGER)

    def __str__(self):
        return self.mr_list

    __table_args__ = (
        CheckConstraint("count >= 0"),
        CheckConstraint("mass_metal >= 0"),
        CheckConstraint("mass_detail >= 0"),
        CheckConstraint("det_in_workpiece > 0"),
    )


class Operation(Base):

    if TYPE_CHECKING:
        id: int
        detail_num: str
        operation_num: str
        operation_name: str
        t_install: Decimal
        t_single: Decimal
    else:
        id = Column(INTEGER, primary_key=True)
        detail_num = Column(
            VARCHAR(128),
            nullable=False,
            )
        operation_num = Column(
            INTEGER,
            nullable=False,
            )
        operation_name = Column(
            VARCHAR(128),
            nullable=False,
            )
        # Время на стройку
        t_install = Column(
            DECIMAL,
            nullable=False,
            default=Decimal("0.000")
            )

        # Время на одну операцию
        t_single = Column(
            DECIMAL,
            nullable=False,
            default=Decimal("0.000")
            )

        __table_args__ = (
            CheckConstraint("length(detail_num) > 2"),
            CheckConstraint("length(operation_num) = 3"),
        )
