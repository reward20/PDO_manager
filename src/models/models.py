
from datetime import date
from decimal import Decimal
from sqlalchemy import BOOLEAN, VARCHAR, CheckConstraint, Date, DECIMAL, CHAR, Column, INTEGER, BIGINT, ForeignKey, Integer
from .base import Base
from sqlalchemy.orm import relationship

from typing import TYPE_CHECKING

__all__ = [
    "Mlexcel_model",
    "ML_O_Model",
    "Techology",
    "Operation",
]



class Mlexcel_model(Base):
    __tablename__ = "ml_excel"
    if TYPE_CHECKING:
        id: int
        mr_list: str
        order: str
        detail_num: str
        detail_count: str
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
        mr_list = Column(CHAR(8), nullable=False, unique=True)
        order = Column(CHAR(5), nullable=False)
        detail_num = Column(VARCHAR(128), nullable=False)
        detail_name = Column(VARCHAR(128))
        detail_count = Column(INTEGER, nullable=False)
        date_start = Column(Date, nullable=False)
        mass_metal = Column(DECIMAL(scale=3), nullable=False)
        mass_detail = Column(DECIMAL(scale=3), nullable=False)
        w_hours = Column(DECIMAL(scale=3), nullable=False)
        material = Column(VARCHAR(128))
        profile_full = Column(VARCHAR(128))
        profile = Column(VARCHAR(64))
        det_in_workpiece = Column(INTEGER)

    def __str__(self):
        return self.mr_list

    __table_args__ = (
        CheckConstraint("detail_count >= 0"),
        CheckConstraint("mass_metal >= 0"),
        CheckConstraint("mass_detail >= 0"),
        CheckConstraint("det_in_workpiece > 0"),
    )


class Operation(Base):
    id = Column(INTEGER, primary_key=True)
    operation_name = Column(VARCHAR(128), nullable=False)
    detail_num = relationship(
        argument="Techology",
        )


class Techology(Base):

    # if TYPE_CHECKING:
    #     id: int
    #     detail_num: str
    #     operation_num: str
    #     operation_name: Operation
    # else:
    id = Column(INTEGER, primary_key=True)
    detail_num = Column(
        VARCHAR(128),
        nullable=False,
        )
    operation_num = Column(
        INTEGER,
        nullable=False,
        )
    # operation_name = Column(
    #     VARCHAR(128),
    #     nullable=False,
    #     )
    operation_id = Column(
        ForeignKey(
            Operation.id,
            onupdate="CASCADE",
            ondelete="CASCADE",
            ),
        index=True,
        nullable=False,
        )
    operation_name = relationship(
        Operation,
        back_populates="detail_num",
        )

    __table_args__ = (
        CheckConstraint("length(detail_num) > 2"),
        CheckConstraint("length(operation_num) = 3"),
    )







# class Order(Base):
#     id = Column(INTEGER, primary_key=True)
#     order_num = Column(CHAR(5), nullable=False)
#     count_name_detail = Column(INTEGER, nullable=False, default=0)
#     count_detail = Column(INTEGER, nullable=False, default=0)
#     w_hours = Column(DECIMAL, nullable=False, default=0)
#     procent_complite = Column(DECIMAL, nullable=False, default=0)


# class Mr_list(Base):
#     id = Column(INTEGER, primary_key=True)
#     mr_list = Column(CHAR(8), nullable=False)
#     # order_id
#     # detail_id
#     count = Column(INTEGER, nullable=False)
#     w_hours = Column(DECIMAL, nullable=False, default=0)
#     date_start = Column(Date, nullable=False)
#     complite = Column(BOOLEAN, nullable=False, default=False)
#     date_complite = Column(Date, default=None)


# class Detail(Base):
#     id = Column(INTEGER, primary_key=True)
#     detail_num = Column(VARCHAR(128), nullable=False, unique=True)
#     detail_name = Column(VARCHAR(128), default="")
#     mass_metal = Column(DECIMAL, nullable=False, default=0)
#     mass_detail = Column(DECIMAL, nullable=False, default=0)
#     det_in_workpiece = Column(INTEGER, nullable=False, default=0)
#     profile_id = Column(INTEGER, nullable=False)
#     profile_full_id = Column(INTEGER, nullable=False)
#     material_id = Column(INTEGER, nullable=False)
#     techology_id = relationship(
#                     argument="Detail_tech",
#                     )


# class Detail_tech(Base):
#     id = Column(INTEGER, primary_key=True)
#     detail_id = Column(ForeignKey(Detail.id), nullable=False, index=True)
#     operation_num = Column(INTEGER, nullable=False)
#     operation_id = Column(ForeignKey("Operation_data.id"), nullable=False)
# # relationship add





# class Material(Base):
#     id = Column(INTEGER, primary_key=True)
#     material_name = Column(VARCHAR(128))
# # relationship add


# class Profile_full(Base):
#     id = Column(INTEGER, primary_key=True)
#     profile_full = Column(VARCHAR(128))
# # relationship add


# class Profile(Base):
#     id = Column(INTEGER, primary_key=True)
#     profile_type = Column(VARCHAR(24))
# # relationship add