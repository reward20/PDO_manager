from dataclasses import dataclass
from sqlalchemy import delete, insert, update
from typing import TYPE_CHECKING, Type, Union

from config import db_engine
from ..models import Base, Mlexcel_model, Operation
from .ml_readers import MlexcelReader, MlexcelOReader, SkladReader

__all__ = [
    "MleDb",
    "SkldDb",
    "MleODb",
]


@dataclass
class MleDb(object):
    reader: Union[MlexcelReader, MlexcelOReader, SkladReader]
    model: Union[Type[Mlexcel_model], Type[Operation]]

    def __post_init__(self):
        Base.metadata.create_all(db_engine)

    def rewrite_db(self):
        with db_engine.connect() as connect:
            connect.execute(delete(self.model))
            stmt = insert(self.model)
            connect.execute(stmt, [x for x in self.reader])
            connect.commit()


class SkldDb(MleDb):
    if TYPE_CHECKING:
        model: Type[Mlexcel_model]
        reader: SkladReader

    def rewrite_db(self):
        with db_engine.connect() as connect:
            for line in self.reader:
                stmt = (
                    update(self.model)
                    .where(self.model.mr_list == line["mr_list"])
                    .values(
                        complite=line["complite"],
                        date_complite=line["date_complite"]
                    )
                )
                connect.execute(stmt)
            connect.commit()


class MleODb(MleDb):

    def rewrite_db(self):
        def generator_line():
            dublic_set = set()
            for line in self.reader:
                if (line["detail_num"], line["operation_num"]) not in dublic_set:
                    dublic_set.add((line["detail_num"], line["operation_num"]))
                    yield line

        with db_engine.connect() as connect:
            connect.execute(delete(self.model))
            stmt = insert(self.model)
            connect.execute(stmt, [x for x in generator_line()])
            connect.commit()
