from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import Select, select
import pandas as pd
from sqlalchemy.orm import defer
from config import db_session, db_engine, settings
from src.models import Mlexcel_model, Operation


from enum import Enum

__all__ = [
    "DB_getter",
]


class tables(Enum):
    ML = Mlexcel_model
    OP = Operation


class DB_getter():

    def __init__(self, table: str = "ML"):
        try:
            self.table: Mlexcel_model = tables[table].value
        except KeyError:
            raise ValueError(
                f"Table expected 'ML' or 'OP', transferred '{table}'!"
            )

    @staticmethod
    def _execute_select_orm(stmt: Select):
        with db_session() as session:
            result = session.scalars(stmt).all()
            return result
            # for user_obj in result.scalars():
            #     yield user_obj

    @staticmethod
    def _execute_select(stmt: Select):
        with db_engine.connect() as con:
            result = con.execute(stmt)
            return result.all()

    def read_sql(self):
        stmt = select(self.table)
        return DB_getter._execute_select(stmt)

    def select_pandas(self):
        table = pd.read_sql_table(self.table.__tablename__, db_engine)
        table = table.reset_index(drop=True)
        # table.set_index([
        #     "detail_num", "operation_num"], inplace=True)
        table.to_excel("hello_2.xlsx", engine='auto')
        # return table.iterrows()
