from dataclasses import dataclass
from sqlalchemy import delete, insert, update
from DB_project.Ml_readers import MLEXCEL_reader, MLEXCELO_reader, SKLAD_reader
from typing import TYPE_CHECKING, Type, Union

from src.models import Mlexcel_model, Operation
from src import db_engine


@dataclass
class MLE_DB(object):
    reader: Union[MLEXCEL_reader, MLEXCELO_reader, SKLAD_reader]
    model: Union[Type[Mlexcel_model], Type[Operation]]

    def rewrite_db(self):
        with db_engine.connect() as connect:
            connect.execute(delete(self.model))
            stmt = insert(self.model)
            connect.execute(stmt, [x for x in self.reader])
            connect.commit()


class SKLAD_UP_DB(MLE_DB):
    if TYPE_CHECKING:
        model: Type[Mlexcel_model]
        reader: SKLAD_reader

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


class MLE_O_DB(MLE_DB):

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
