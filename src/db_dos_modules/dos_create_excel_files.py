from decimal import Decimal
from typing import Callable, Any
from sqlalchemy import Sequence
from config import excel_setting
from .db_getter import DB_getter
from src.excel_writer import ExcelBookWriter
import pandas as pd


__all__ = [
    "DataExcelTransfer",
]

class DataExcelTransfer(object):
    def __init__(self):
        pass

    @staticmethod
    def _get_data(table="ML") -> Sequence:
        bd = DB_getter(table=table)
        bd.read_orm_sql()
        return bd.read_orm_sql()

    @staticmethod
    def logic_data(result: Sequence, columns: tuple[str, ...], fucn_bis_log: Callable | None = None) -> list[Any]:
        data = []
        for item in result:
            list_temp = []
            for col in columns:
                list_temp.append(item._get_by_key_impl_mapping(col))
            if fucn_bis_log is not None:
                list_temp = fucn_bis_log(list_temp, item)
            data.append(list_temp)
        return data

    @staticmethod
    def mp_excel_write():
        result = DataExcelTransfer._get_data(table="ML")
        data = DataExcelTransfer.logic_data(result, excel_setting.BD_COLUMN_MP)
        options = excel_setting.OPTIONS_EX_MP
        options["data"] = data
        book = ExcelBookWriter(
            excel_setting.EXCEL_NAME_MP,
            excel_setting.SAVE_PATHS_MP
        )
        book.write_sheet_new("MLEXCEL", options=options)
        book.save_book()

    @staticmethod
    def _mtoil_bis_logic(list_data: list[Any], item):
        count = item._get_by_key_impl_mapping("count")
        one_metal = item._get_by_key_impl_mapping("mass_metal")
        list_data.append(count * one_metal)
        return list_data

    @staticmethod
    def mtoil_excel_write():
        result = DataExcelTransfer._get_data(table="ML")
        data = DataExcelTransfer.logic_data(
            result,
            excel_setting.BD_COLUMN_MTOIL,
            DataExcelTransfer._mtoil_bis_logic
        )
        options = excel_setting.OPTIONS_EX_MTOIL
        options["data"] = data
        book = ExcelBookWriter(
            excel_setting.EXCEL_NAME_MTOIL,
            save_path=excel_setting.SAVE_PATHS_MTOIL
        )
        book.write_sheet_new("MLEXCEL", options=options)
        book.save_book()

    @staticmethod
    def pdo_excel_write():

        def create_order_list(table: pd.DataFrame):

            table_complite = table[table["complite"] == "D"] \
                .groupby("order")[["count", "w_hours"]] \
                .sum(min_count=0)\
                .reset_index()
            table_complite = table_complite.rename(columns={"count": "make_detail", "w_hours": "make_w_hours"})
            table = table.groupby("order")[["count", "w_hours"]]\
                .sum()\
                .reset_index()
            table = table.merge(table_complite, how="left", left_on="order", right_on="order")\
                .fillna(0)
            table["complite_procent"] = table["make_w_hours"] / table["w_hours"]

            table = table[["order", "count", "w_hours", "make_detail", "make_w_hours", "complite_procent"]]
            options = excel_setting.OPTIONS_PDO_ORDER
            options["data"] = table.to_numpy()
            book.write_sheet_new("Заказы", options=options)

        def create_mr_list(table: pd.DataFrame):
            options = excel_setting.OPTIONS_PDO_MR_LIST
            options["data"] = table[
                    [
                        'order', 'mr_list', 'w_hours',
                        'detail_num', 'count', 'date_start',
                        'complite', 'date_complite', 'detail_name',
                        'mass_metal', 'mass_detail', 'material',
                        'profile_full', 'profile', 'det_in_workpiece'
                    ]
                ]\
                .to_numpy()
            book.write_sheet_new("Мр листы", options=options)

        def create_operation_list():
            table_op = DataExcelTransfer._get_data(table="OP")
            table_op = pd.DataFrame(table_op).drop(columns=["id"])
            table_op = table_op.drop_duplicates(subset=["detail_num", "operation_num"])
            options = excel_setting.OPTIONS_PDO_OPERATIONS
            options["data"] = table_op.to_numpy()
            book.write_sheet_new("Операции", options=options)

        def create_detail_list(table: pd.DataFrame):
            table = table[
                [
                    "detail_num",
                    "detail_name",
                    "material",
                    "profile_full",
                    "det_in_workpiece",
                    "mass_metal",
                    "mass_detail",
                ]
            ]
            table = table.drop_duplicates(subset=["detail_num"])
            options = excel_setting.OPTIONS_PDO_DETAILS
            options["data"] = table.to_numpy()
            book.write_sheet_new("Детали", options=options)

        table = DataExcelTransfer._get_data(table="ML")
        table = pd.DataFrame(table)
        table = table.drop(["id", "w_hours"], axis=1)
        w_hourse_table = DataExcelTransfer._get_data(table="WH")
        w_hourse_table = pd.DataFrame(w_hourse_table)
        w_hourse_table = w_hourse_table.drop(["id", "order"], axis=1)
        table = table.merge(
            w_hourse_table,
            how="left",
            left_on="mr_list",
            right_on="mr_list"
        )
        del w_hourse_table
        book = ExcelBookWriter(
            filename=excel_setting.EXCEL_NAME_PDO,
            save_path=excel_setting.SAVE_PATHS_PDO
        )
        create_mr_list(table)
        create_order_list(table)
        create_operation_list()
        create_detail_list(table)
        book.save_book()
