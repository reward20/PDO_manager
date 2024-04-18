from dataclasses import dataclass
import csv
from pathlib import Path
from typing import Iterable
from src.schemas import ML_ex_correct, ML_O_correct
from src.config import settings

__all__ = [
    "MLEXCEL_reader",
    "MLEXCELO_parcer",
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

@dataclass
class MLEXCELO_parcer(object):
    MLEXCELO_path: Path

    def read_file(self) -> Iterable[ML_O_correct]:
        with open(
                self.MLEXCELO_path,
                mode="r",
                encoding="cp866"
                ) as file:

            detail_info = {
                "detail_num": None,
                "operation_num": None,
                "operation_name": None,
            }

            for line in file:
                if line[0] == "@":
                    detail_num = line.split("^")[2]
                    detail_info.update({"detail_num": detail_num})
                elif line[0] == "N":
                    oper_row = line.split(":")
                    operation_num = oper_row[0][1:]
                    detail_info.update({"operation_num": operation_num})

                    oper_line = oper_row[1].split("^")
                    operation_name = oper_line[0]
                    detail_info.update({"operation_name": operation_name})
                    yield ML_O_correct(**detail_info)
