from itertools import count
from pathlib import Path
from typing import Any, Iterable, Tuple
import xlsxwriter as xls
from dataclasses import dataclass

from src.schemas import CorrectDir
# from src.schemas import CorrectDir

@dataclass
class Formater(object):
    # number = {

    # }

    # f_number = {

    # }

    text_center = {
        "bold": 1,
        "border": 1,
        "align": "center",
        "valign": "vcenter",
        "fg_color": "yellow",
    }

    text_basic = {
        "bold": 0,
        "border": 0,
        "align": "left",
        "valign": "vcenter",
    }


class ExcelBookWriter(object):
    def __init__(self, filename: str | None = None, save_path: Path | Tuple[Path] | None = None) -> None:

        self.filename = "default.xlsx"
        self.save_path = (Path(__file__).parent,)
        self.book = xls.Workbook()

        if filename is not None:
            self.filename = filename + ".xlsx"

        if save_path is not None:
            self.save_path = CorrectDir(path=save_path).path

    def write_pivot_table(
        self,
        worksheet: xls.workbook.Worksheet,
        data: Iterable[list[Any]],
        *,
        start_row: int = 0,
        start_colomn: int = 0,
        columns: list[str] | None = None,
        format: dict[str, Any] | None = None,
    ):
        end_row = 0 #sum(1 for x in data)
        end_column = 0
        worksheet.add_table()




    def write_data(
        self,
        namesheet: str,
        data: Iterable[list[Any]],
        *,
        start_row: int = 0,
        start_colomn: int = 0,
        columns: list[str] | None = None,
        pivot: bool = False,
        filter: bool = False,
        format: dict[str, Any] | None = None
    ) -> None:
    
        worksheet = self._get_worksheet(namesheet)

    
    def _get_worksheet(self, namesheet: str) -> xls.workbook.Worksheet:
        sheet = self.book.get_worksheet_by_name(namesheet)
        if sheet is None:
            sheet = self.book.add_worksheet(name=namesheet)
        return sheet

    def _add_format():
        pass

    def _add_():
        pass
    def save():
        pass





def write_workbook(iter: Iterable):
    workbook = xls.Workbook("hello.xlsx")
    worksheet = workbook.add_worksheet()

    row = 0
    row_c = 0
    col = 0
    set_x = None
    merge_format = workbook.add_format(Formater.text_center)
    list_t = list(iter)
    print(list_t[0])
    worksheet.add_table(0, 0, len(list_t), len(list_t[0])-1, {"data": list_t})
    print(list_t[0])
    workbook.close()
    return None

    for row, item in enumerate(iter):
        if set_x is None:
            set_x = item[1]
            row_c += 1
        elif not (set_x == item[1]):
            set_x = item[1]
            if row_c > 1:
                worksheet.merge_range(row-row_c, 0, row-1, 0, set_x, merge_format)
                row_c = 1
        else:
            row_c += 1
    else:
        if row_c > 1:
            worksheet.merge_range(row-row_c-1, 0, row, 0, set_x, merge_format)

        worksheet.write_row(row, col, item[1:])
    workbook.close()


if __name__ == "__main__":
    print(len(range(10)))
    # ExcelBookWriter()

# workbook = xls.Workbook("hello.xlsx")
# worksheet = workbook.add_worksheet()
# merge_format = workbook.add_format(
#     {
#         "bold": 1,
#         "border": 1,
#         "align": "center",
#         "valign": "vcenter",
#         "fg_color": "yellow",
#     }
# )
# worksheet.merge_range(1,1,5,5,"fasfsdsdffsdsdf", merge_format)
# workbook.close()
