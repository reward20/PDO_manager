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
from datetime import datetime, time

from scripts.data_dos_create import DataBaseDosCreate
from scripts.dos_create_excel_files import DataExcelTransfer
from src.db_getter import DB_getter
from src.db_getter.excel_writer import ExcelBookWriter
from src.formater import Formater
from src.models import Operation

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
            Formater.format_int,
            Formater.text_basic,
            Formater.format_int,
            Formater.text_basic,
            Formater.format_number,
            Formater.format_number,
        ]

        options = {
            "data": result,
            "data_format": data_format,
            "headers": ["№", "Деталь", "№ опер", "Операция", "t настройки","t изготов",],
            "autofilter": True,
            "pivot": True,

            "columns_wight": [5, 30, 6, 22, 8, 8],
            "headers_format": [Formater.text_center],
            "headers_height": 30,
            "start_row": 0,
            "start_column": 0,
            "end_row": None,
            "end_column": None,
        }

        Book.write_sheet_new(namesheet="coop", options=options)
        Book.save_book()
        # write_workbook(result)
        end = datetime.now()
        print("Total time taken in : ", func.__name__, end - begin)
    return dec_func

if __name__ == "__main__":
    # from sqlalchemy import select

#     query = select([ 
#     Operation.first_name, 
#     STUDENTS.c.last_name, 
#     db.func.sum(STUDENTS.c.score) 
# ]).group_by(STUDENTS.c.first_name, STUDENTS.c.last_name) 

    time_me = datetime.now()
    DataBaseDosCreate.start()
    DataExcelTransfer.pdo_excel_write()
    DataExcelTransfer.mtoil_excel_write()
    DataExcelTransfer.mp_excel_write()
    print(datetime.now() - time_me)
