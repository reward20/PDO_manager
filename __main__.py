# from sqlalchemy import select
# from sqlalchemy.orm import load_only

# from DB_project import DB_progect
# from DB_getter.db_getter import DB_getter
# from DB_module.models import Mlexcel_model
# from DB_module.config import db_engine

# from Excel_writer import Reader_DB
# from Excel_writer.Excel_writer.Base_program.base.Base import Base

import pandas as pd

# from datetime import datetime
# import xlsxwriter as xlw
from datetime import datetime

from scripts.data_dos_create import DataBaseDosCreate
from src.db_getter import DB_getter
from src.db_getter.excel_writer import ExcelBookWriter, Formater

import xlsxwriter as xlsx

def timeit(func, *args, **kwargs):
    def deroc_fun():
        begin = datetime.now()
        func(*args, **kwargs)
        end = datetime.now()
        print("Total time taken in : ", func.__name__, end - begin)
    return deroc_fun

def decor(func, *args, **kwargs):
    def dec_func():
        begin = datetime.now()
        result = func(*args, **kwargs)
        Book = ExcelBookWriter()
        data_format = [
            Formater.text_basic,
            Formater.text_basic,
            Formater.text_basic,
            Formater.text_basic,
            Formater.text_basic,
            Formater.text_basic,
        ]

        options = {
            # "filter": True,
            "headers": [f"ranger{x}" for x in range(6)],
            "headers_format": Formater.text_center,
            "data_format": data_format,
            "columns_wight": [4, 30, 6, 22, 8, 8],
            "pivot": True,
        }

        Book.write_sheet(namesheet="coop", data=result, options=options)
        Book.save_book()
        # write_workbook(result)
        end = datetime.now()
        print("Total time taken in : ", func.__name__, end - begin)
    return dec_func


if __name__ == "__main__":
    print(len(None))
    # DataBaseDosCreate.start()
    # table = DB_getter(table="OP")
    # # timeit(table.select_pandas)()
    # decor(table.read_sql)()
    # pd.ExcelWriter()
