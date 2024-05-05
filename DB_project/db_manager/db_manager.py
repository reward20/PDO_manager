from dataclasses import dataclass
from pathlib import Path
from DB_project.Ml_readers import MLEXCEL_reader, MLEXCELO_reader, SKLAD_reader

from .db_writers import MLE_DB, MLE_O_DB, SKLAD_UP_DB
from .decorator import Control_file

from src import db_engine
from src.models import Mlexcel_model, Operation, Base

__all__ = [
    "DB_manager",
]


@Control_file
@dataclass
class DB_manager(object):
    path_MLEXCEL: Path
    path_MLEXCEL_O: Path
    path_SKLAD: Path

    def create_db(self):
        Base.metadata.create_all(db_engine)
        mle = MLE_DB(MLEXCEL_reader(self.path_MLEXCEL), Mlexcel_model)
        mle.rewrite_db()
        skl = SKLAD_UP_DB(SKLAD_reader(self.path_SKLAD), Mlexcel_model)
        skl.rewrite_db()
        mle_O = MLE_O_DB(MLEXCELO_reader(self.path_MLEXCEL_O), Operation)
        mle_O.rewrite_db()
