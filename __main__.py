# from sqlalchemy import select
# from sqlalchemy.orm import load_only

# from DB_project import DB_progect
# from DB_getter.db_getter import DB_getter
# from DB_module.models import Mlexcel_model
# from DB_module.config import db_engine

# from Excel_writer import Reader_DB
# from Excel_writer.Excel_writer.Base_program.base.Base import Base

# import pandas as pd

# from datetime import datetime
# import xlsxwriter as xlw
from datetime import datetime
import sys

from scripts.data_dos_create import DataBaseDosCreate
from src.db_getter import DB_getter
from src.db_getter.excel_writer import write_workbook

def decor(func, *args, **kwargs):
    def dec_func():
        begin = datetime.now()
        result = func(*args, **kwargs)
        write_workbook(result)
        end = datetime.now()
        print("Total time taken in : ", func.__name__, end - begin)
        return result
    return dec_func


if __name__ == "__main__":
    # DataBaseDosCreate.start()
    table = DB_getter(table="OP")
    # decor(table.select_pandas)()
    decor(table.read_sql)()

# if __name__ == "__main__":
#     time = datetime.now()
#     # project = DB_progect()
#     # project.start_project()
#     reader = Reader_DB()
#     # print(.column)
#     t = Base()
#     t.write_mr()
#     t.save_file(r"Data/hello.xlsx")



#     # workbook = xlw.Workbook(r"Data/hello.xlsx")

#     # prop = {
#     #     'font_name': "Time New Roman",
#     #     'font_size': 9,
#     #     'align': "left",
#     #     "valign": "vcenter",
#     #     "num_format": "d mmmm yyyy"
#     # }

#     # formating = workbook.add_format(prop)
#     # worksheet = workbook.add_worksheet("Sheet_1")
#     # worksheet.write_row(0, reader.column, formating)
#     # for x in reader:
#     #     worksheet.write_row(x[0], x[1].values, formating)
#     # workbook.close()
#     print(datetime.now() - time)
#     # stmt = select(Mlexcel_model.order).distinct()
#     # print(pd.read_sql(stmt, db_engine))
#     # # for x in DB_getter._execute_query(stmt):
#     # #     print(x.order, x.mr_list, x.date_start)
