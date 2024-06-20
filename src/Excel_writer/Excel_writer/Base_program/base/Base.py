from pathlib import Path
import xlsxwriter as xls
from io import BytesIO
from Excel_writer.Excel_writer.Formating import Cl_type

from Excel_writer.Reader import Reader_DB
from DB_module.config import db_engine, db_settings


class Base(object):

    def __init__(self):
        self.byte_obj = BytesIO()
        self.reader = Reader_DB()
        self.ex_file = xls.Workbook(self.byte_obj)

    def write_mr(self):
        sheets = self.ex_file.add_worksheet("MLEXCEL")
        row = 0
        for line in self.reader:
            sheets.write_row(row=row, col=0, data=line[1], cell_format=None)
            row += 1
        for col, column in enumerate(self.reader.column):
            sheets.set_column(
                first_col=col,
                last_col=col,
                width=15,
                cell_format=self.ex_file.add_format(Cl_type[column]),
            )
        sheets.add_table(0, 0, row-1, len(self.reader.column)-1, {
            "columns": [{"header": x} for x in self.reader.column]
        })

    def save_file(self, ex_path: Path):
        self.ex_file.close()
        with open(ex_path, "wb") as f:
            f.write(self.byte_obj.getbuffer())
        self.byte_obj.close()

    def return_book(self):
        pass
