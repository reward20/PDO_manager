from collections import defaultdict
from typing import Any, Generator
from sqlalchemy import Select, select, Sequence
import pandas as pd

from .calculation import CalculateFrames
from config import excel_setting
from src.db_yz_modules import DBViewer


__all__ = [
    "DB_getter",
]



class PdoDBGetter(DBViewer):

    def _pdo_mr_list(self):
        with self as db:
            for list in db.get_all_mrlist():
                mr_list = [
                    list.order_name,
                    list.mr_list,
                    list.product_name,
                    list.product.title,
                    list.count,
                    list.w_hours,
                    list.date_start,
                    list.complite,
                    list.date_complite,
                    list.product.material_name,
                    list.product.mass_metall,
                    list.product.mass_detail,
                    list.product.profile_full_name,
                    list.product.profile_name,
                    list.product.det_in_workpiece,
                ]
                yield mr_list

    def _pdo_detail(self):
        with self as db:
            for product in db.get_all_product():
                list_ = [
                    product.name,
                    product.title,
                    product.material_name,
                    product.mass_metall,
                    product.mass_detail,
                    product.det_in_workpiece,
                    product.profile_name,
                    product.profile_full_name,
                ]
                yield list_

    def _pdo_oper(self):
        with self as db:
            for operation in db.get_all_operations():
                list_ = [
                    operation.detail_name,
                    operation.num_operation,
                    operation.operation_name,
                    operation.t_install,
                    operation.t_single,
                ]
                yield list_

    def _mp_ml(self):
        with self as db:
            for list in db.get_all_mrlist():
                mr_list = [
                    list.mr_list,
                    list.order_name,
                    list.product_name,
                    list.product.title,
                    list.count,
                    list.product.mass_metall,
                    list.product.h_work_one,
                    list.product.material_name,
                    list.product.mass_detail,
                ]
                yield mr_list

    def _mtoil_ml(self):
        with self as db:
            for list in db.get_all_mrlist():
                mr_list = [
                    list.mr_list,
                    list.order_name,
                    list.product_name,
                    list.product.title,
                    list.product.material_name,
                    list.product.profile_full_name,
                    list.product.profile_name,
                    list.product.mass_metall,
                    list.product.det_in_workpiece,
                    list.count,
                ]
                yield mr_list





class PDOExcelDataHandler(PdoDBGetter, CalculateFrames):

    def _create_frame(self, get_func, headers: list[str]):
        dict_frame = defaultdict(list)

        for line in get_func():
            for val, name in zip(line, headers):
                dict_frame[name].append(val)
        return pd.DataFrame.from_dict(dict_frame)

    def get_value_order_mr_list(self) -> tuple[list, list]:
        frame = self._create_frame(self._pdo_mr_list, excel_setting.mr_list_headers)
        order_frame = frame[["Заказ", "Мр_лист", "№ детали", "Количество", "Норм-часы", "Тип сдачи"]]
        _unique = (
            order_frame[["Заказ","№ детали"]]
            .groupby(by="Заказ")
            .nunique()
            .rename({"№ детали": "Кол. наим."}, axis=1)
        )

        _detail_all = (
            order_frame[["Заказ","Количество"]]
            .groupby(by="Заказ")
            .sum()
            .rename({"Количество": "Всего деталей"})
        )
        
        _hours_all = (
            order_frame[["Заказ","Норм-часы"]]
            .groupby(by="Заказ")
            .sum()
            .rename({"Норм-часы": "Всего н/ч"}, axis=1)
        )

        _detail_compl = (
            order_frame[order_frame["Тип сдачи"] == "D"][["Заказ","Количество"]]
            .groupby(by="Заказ")
            .sum()
            .rename({"Количество": "Сделано деталей"}, axis=1)
        )
        
        _hours_compl = (
            order_frame[order_frame["Тип сдачи"] == "D"][["Заказ","Норм-часы"]]
            .groupby(by="Заказ")
            .sum()
            .rename({"Норм-часы": "Сделано н/ч"}, axis=1)
        )

        order_frame = pd.concat(
            [
                _unique, _detail_all, _hours_all,
                _detail_compl, _hours_compl
            ],
            axis=1
        ).reset_index().fillna(0)
        order_frame["Выполнено"] = order_frame["Сделано н/ч"] / order_frame["Всего н/ч"]
        order_frame["Выполнено"] = order_frame["Выполнено"].round(2)
        return order_frame.values, frame.values

    def get_value_detail(self) -> list:
        frame = self._create_frame(self._pdo_detail, excel_setting.detail_headers)
        return frame.values

    def get_value_operation(self) -> list:
        frame = self._create_frame(self._pdo_oper, excel_setting.operation_headers)
        return frame.values

    def get_frame_calculation(self) -> pd.DataFrame:
        return self._get_calculation_data(
            excel_setting.CALCULATION_ORDER,
            excel_setting.CALCULATION_MONTH,
        )

    def get_value_mp_ml(self) -> list:
        frame = self._create_frame(self._mp_ml, excel_setting.ml_ex_headers)
        return frame.values

    def get_value_mtoil(self) -> list:
        frame = self._create_frame(self._mtoil_ml, excel_setting.mtoil_ex_headers)
        frame["Расход на партию"] = frame["Металла на ед."] * frame["Размер партии"]
        frame["Расход на партию"] = frame["Расход на партию"].round(3)
        return frame.values



    def get_value_by_frame(self, frame: pd.DataFrame) -> list:
        return frame.values
