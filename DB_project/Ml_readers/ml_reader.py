import csv
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, Iterable
from src.schemas import ML_ex_correct, ML_O_correct, SKLAD_correct
from DB_project.settings import settings

__all__ = [
    "MLEXCEL_reader",
    "MLEXCELO_reader",
    "SKLAD_reader",
]


@dataclass
class MLEXCEL_reader(object):
    file_path: Path

    def read_file(self) -> Iterable[Dict]:
        with open(
                self.file_path,
                mode="r",
                encoding="cp866",
                newline=""
                ) as csvfile:
            csv_reader = csv.reader(csvfile, delimiter='^')
            for row in csv_reader:
                fields = dict(zip(settings.MLEXCEL_CSV_NAME_COLUMNS, row))
                obj = ML_ex_correct(**fields)
                yield obj.model_dump()

    def __iter__(self):
        return self.read_file()


class MLEXCELO_reader(MLEXCEL_reader):

    def read_file(self) -> Iterable[Dict]:
        with open(
                self.file_path,
                mode="r",
                encoding="cp866"
                ) as file:

            detail_info: Dict[str, Any] = {
                "detail_num": "",
                "operation_num": "",
                "operation_name": "",
                "t_install": Decimal("0.000"),
                "t_single": Decimal("0.000"),
            }

            for line in file:
                if line[0] == "@":
                    detail_num = line.split("^")[2]
                    detail_info["detail_num"] = detail_num
                elif line[0] == "N":
                    oper_row = line.split(":")
                    operation_num = oper_row[0][1:]
                    detail_info.update({"operation_num": operation_num})

                    oper_line = oper_row[1].split("^")
                    operation_name = oper_line[0]
                    t_install = oper_line[1].replace(",", ".")
                    t_single = oper_line[2].replace(",", ".")

                    detail_info["operation_name"] = operation_name
                    detail_info["t_install"] = Decimal(value=t_install)
                    detail_info["t_single"] = Decimal(value=t_single)

                    obj = ML_O_correct(**detail_info)
                    yield obj.model_dump()


class SKLAD_reader(MLEXCEL_reader):

    def read_file(self) -> Iterable[Dict]:
        with open(
            self.file_path,
            "r", encoding="cp866",
            newline="\r\n"
        ) as file:
            for read_line in file:
                line = read_line.rstrip().split("^")
                fields = dict(zip(settings.SKLAD_CSV_NAME_COLUMNS, line))
                obj = SKLAD_correct(**fields)
                return_dict = obj.model_dump()
                yield return_dict
