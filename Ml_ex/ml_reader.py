from dataclasses import dataclass
import csv
from pathlib import Path
from typing import Iterable
from schemas import ML_ex_correct
from src.config import settings

__all__ = [
    "MLEXCEL_reader",
]


@dataclass
class MLEXCEL_reader(object):
    MLEXCEL_path: Path

    def read_file(self) -> Iterable[ML_ex_correct]:
        with open(
                self.MLEXCEL_path,
                mode="r",
                encoding="cp866",
                newline=""
                ) as csvfile:

            csv_reader = csv.reader(csvfile, delimiter='^')
            for row in csv_reader:
                fields = dict(zip(settings.MLEXCEL_CSV_NAME_COLUMNS, row))
                obj = ML_ex_correct(**fields)
                yield obj


# class MLEXCELO(object):
#     pass


# class SKLAD(object):
#     pass
