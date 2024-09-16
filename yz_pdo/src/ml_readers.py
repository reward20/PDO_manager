import csv
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable
from .schemas import (
    ML_ex_correct,
    ML_O_correct,
    SKLAD_correct,
    ML_Operation_Model,
    ML_sum_Model,
)
from yz_pdo.config import settings

__all__ = [
    "DosReader",
]

class MlexcelReader(object):

    def __init__(self, MLEXCEL: Path):
        self.file_ml_path = MLEXCEL

    def _read_ml_file(self) -> Iterable[dict[str, Any]]:
        with open(
                self.file_ml_path,
                mode="r",
                encoding="cp866",
                newline="",
        ) as csvfile:
            csv_reader = csv.reader(csvfile, delimiter='^')
            for row in csv_reader:
                fields = dict(
                    zip(settings.MLEXCEL_CSV_NAME_COLUMNS, row)
                )
                obj = ML_ex_correct(**fields)  # type: ignore
                yield obj.model_dump()


class MlexcelOReader(object):

    def __init__(self, MLEXCELO: Path):
        self.file_ml_o_path = MLEXCELO

    def _read_operation_file(self) -> Iterable[dict[str, Any]]:
        with open(
            self.file_ml_o_path,
            mode="r",
            encoding="cp866"
        ) as file:
            operation_info: dict[str, Any] = {
                "detail_num": "",
                "operation_num": "",
                "operation_name": "",
                "t_install": Decimal("0.000"),
                "t_single": Decimal("0.000"),
            }
            for line in file:
                if line[0] == "@":
                    list_split = line.split("^")
                    detail_num = list_split[2]
                    operation_info["detail_num"] = detail_num
                elif line[0] == "N":
                    oper_row = line.split(":")
                    operation_num = oper_row[0][1:]
                    operation_info.update({"operation_num": operation_num})

                    oper_line = oper_row[1].split("^")
                    operation_name = oper_line[0]
                    t_install = oper_line[1].replace(",", ".")
                    t_single = oper_line[2].replace(",", ".")

                    operation_info["operation_name"] = operation_name
                    operation_info["t_install"] = Decimal(value=t_install)
                    operation_info["t_single"] = Decimal(value=t_single)
                    yield operation_info
                    obj = ML_Operation_Model(**operation_info)
                    yield obj.model_dump()


    def _read_ml_o_file(self) -> Iterable[dict]:
        with open(
            self.file_ml_o_path,
            mode="r",
            encoding="cp866"
        ) as file:

            detail_info: dict[str, Any] = {
                "mr_list": "",
                "t_all": Decimal("0.000"),
            }

            for line in file:
                if line[0] == "@":
                    list_split = line.split("^")
                    detail_info["mr_list"] = list_split[0][1:]
                elif line[0] == "N":
                    oper_row = line.split(":")
                    oper_line = oper_row[1].split("^")
                    t_all = oper_line[3].replace(",", ".")
                    detail_info["t_all"] = Decimal(value=t_all)

                    obj = ML_sum_Model(**detail_info)
                    yield obj.model_dump()


    def _read_ml_o_file_old(self) -> Iterable[dict]:
        with open(
                self.file_ml_o_path,
                mode="r",
                encoding="cp866"
            ) as file:

            detail_info: Dict[str, Any] = {
                "mr_list": "",
                "order": "",
                "detail_num": "",
                "operation_num": "",
                "operation_name": "",
                "t_install": Decimal("0.000"),
                "t_single": Decimal("0.000"),
                "t_all": Decimal("0.000"),
            }


            for line in file:
                if line[0] == "@":
                    list_split = line.split("^")
                    mr_list = list_split[0][1:]
                    order = list_split[1]
                    detail_num = list_split[2]
                    detail_info["detail_num"] = detail_num
                elif line[0] == "N":
                    oper_row = line.split(":")
                    operation_num = oper_row[0][1:]
                    detail_info.update({"operation_num": operation_num})

                    oper_line = oper_row[1].split("^")
                    operation_name = oper_line[0]
                    t_install = oper_line[1].replace(",", ".")
                    t_single = oper_line[2].replace(",", ".")
                    t_all = oper_line[3].replace(",", ".")

                    detail_info["mr_list"] = mr_list
                    detail_info["order"] = order
                    detail_info["operation_name"] = operation_name
                    detail_info["t_install"] = Decimal(value=t_install)
                    detail_info["t_single"] = Decimal(value=t_single)
                    detail_info["t_all"] = Decimal(value=t_all)

                    obj = ML_O_correct(**detail_info)
                    yield obj.model_dump()


class SkladReader(object):

    def __init__(self, SKLAD: Path):
        self.file_skl_path = SKLAD

    def _read_skl_file(self) -> Iterable[dict[str, Any]]: 
        with open(
            self.file_skl_path,
            "r", encoding="cp866",
            newline="\r\n"
        ) as file:
            for read_line in file:
                line = read_line.rstrip().split("^")
                fields = dict(zip(settings.SKLAD_CSV_NAME_COLUMNS, line))
                obj = SKLAD_correct(**fields)
                return_dict = obj.model_dump(include=("mr_list", "complite", "date_complite"))
                yield return_dict


    def read_skl_file_old(self) -> Iterable[dict]:
        with open(
            self.file_ml_path,
            "r", encoding="cp866",
            newline="\r\n"
        ) as file:
            for read_line in file:
                line = read_line.rstrip().split("^")
                fields = dict(zip(settings.SKLAD_CSV_NAME_COLUMNS, line))
                obj = SKLAD_correct(**fields)
                return_dict = obj.model_dump()
                yield return_dict


class DosHandler(MlexcelReader, MlexcelOReader, SkladReader):

    def __init__(
            self,
            *,
            MLEXCEL: Path,
            MLEXCELO: Path,
            SKLAD: Path
        ):

        self.file_ml_path = MLEXCEL
        self.file_ml_o_path = MLEXCELO
        self.file_skl_path = SKLAD

    def _read_ml_o_file(self) -> Iterable[dict[str, Any]]:

        iter_list = iter(super()._read_ml_o_file())
        iter_first = iter_list.__next__()

        for iter_one in iter_list:
            if iter_one["mr_list"] != iter_first["mr_list"]:
                yield iter_first
                iter_first = iter_one
            else:
                iter_first["t_all"] += iter_one["t_all"]
        else:
            yield iter_first


class DosDbWriter(DosHandler):
    pass