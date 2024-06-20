import pandas as pd
from sqlalchemy import select
from DB_module.config import db_engine
from .config import cl_setting, md_setting

__all__ = [
    "Reader_DB"
]


class Reader_DB(object):
    def __init__(self, table="Ml_ex"):
        stmt = select(md_setting[table].value)
        self.column = cl_setting[table].value
        self.table: pd.DataFrame = pd.read_sql(
            stmt,
            db_engine,
            index_col="id",
            columns=self.column,
        )
        self.iter = self.table.iterrows()

    def __iter__(self):
        return self

    def __next__(self):
        return self.iter.__next__()
