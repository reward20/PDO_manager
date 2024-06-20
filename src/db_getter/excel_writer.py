from pathlib import Path
from typing import Any, Iterable, Tuple
import xlsxwriter as xls
from dataclasses import dataclass
from io import BytesIO
from itertools import zip_longest, repeat

from src.schemas import CorrectDir


@dataclass
class Formater(object):

    format_number = {
        'num_format': '#,##0.00',
        "align": "right",
        "valign": "vcenter",
        "font_name": "Times New Roman",
        "font_size": 12,
    }

    format_int = {
        'num_format': r"#,##0",
        "align": "right",
        "valign": "vcenter",
        "font_name": "Times New Roman",
        "font_size": 12,
    }

    format_date = {
        "num_format": "DD.MM.YYYY",
        "align": "vcenter",
        "valign": "vcenter",
        "font_name": "Times New Roman",
        "font_size": 12,
    }

    text_center = {
        "align": "center",
        "valign": "vcenter",
        "font_name": "Times New Roman",
        "font_size": 12,
    }

    text_basic = {
        "align": "right",
        "valign": "vcenter",
        "font_name": "Times New Roman",
        "font_size": 12,
    }


class ExcelBookWriter(object):

    def __init__(self, filename: str | None = None, save_path: Path | Tuple[Path] | None = None) -> None: # good

        self.filename = "default.xlsx"
        self.save_path = (Path(__name__).parent,)

        if filename is not None:
            self.filename = filename + ".xlsx"

        if save_path is not None:
            self.save_path = CorrectDir(path=save_path).path
            if not isinstance(self.save_path, (tuple, list)):
                self.save_path = (self.save_path, )

        self._bookIO = BytesIO()
        self.workbook = xls.Workbook(self._bookIO, {"in_memory": True})


    def write_sheet_new(
        self,
        namesheet: str,
        data: Iterable[list[Any]],
        *,
        options: dict[str, Any] = {},
    ):

        start_row = options.get("start_row", 0)
        start_column = options.get("start_column", 0)
        options["last_row"] = len(data)
        options["last_column"] = len(iter(data).__next__())
        worksheet = self._get_worksheet(namesheet)


    def write_data_in_table(self, worksheet, data, options = {}):

        start_row = options.get("start_row", 0)
        start_column = options.get("start_column", 0)
        last_row = options.get("last_row", 0)
        last_column = options.get("last_column", 0)
        autofilter = options.get("filter", False)
        columns = []

        headers = options.get("headers", None)
        if headers is None:
            header_row = False
        else:
            header_row = True
            last_row += 1
            last_column += 1

        pivot = options.get("pivot", False)
        if pivot:
            style = "Table Style Medium 9"
        else:
            style = None


        if header_row:
            headers_format = options.get("headers_format", None)
            for num, header_name in enumerate(headers):
                store_options = {}
                store_options["header"] = header_name
                store_options["header_format"] = headers_format
                columns.append({"header": header_name})




        local_options = {
            "data": data,
            "autofilter": autofilter,
            "header_row": header_row,
            "style": style,
        }



        worksheet.add_table(start_row, start_column, last_row, last_column, local_options)



    def write_sheet(
        self,
        namesheet: str,
        data: Iterable[list[Any]],
        *,
        options: dict[str, Any] = {},
    ) -> tuple[int, int]:

        start_row = options.get("start_row", 0)
        start_column = options.get("start_column", 0)
        # columns = options.get("columns", None)
        # filter = options.get("filter", False)
        # format = options.get("format", None)
        autofilter = options.get("filter", False)
        pivot = options.get("pivot", False)

        worksheet = self._get_worksheet(namesheet)
        last_row, last_column = self._write_data_in_sheets(worksheet, data, options=options)
        self._set_format(worksheet, options=options)
        options["last_row"] = last_row
        options["last_column"] = last_column
        if autofilter:
            worksheet.autofilter(start_row, start_column, last_row, last_column)
        self._add_pivot(worksheet, options)

        # if pivot:
        #     self._add_pivot(worksheet, start_row, start_column, last_row, last_column, columns)
        # elif filter:
        #     worksheet.autofilter(start_row, start_column, last_row, last_column)

    def _get_worksheet(self, namesheet: str) -> xls.workbook.Worksheet:
        worksheet = self.workbook.get_worksheet_by_name(namesheet)
        if worksheet is None:
            worksheet = self.workbook.add_worksheet(name=namesheet)
        return worksheet

    def _write_data_in_sheets(
        self,
        worksheet: xls.workbook.Worksheet,
        data: Iterable[list[Any]],
        *,
        options: dict[str, Any] = {},
    ) -> tuple[int, int]:

        data_first_column = options.get("start_column", 0)
        data_first_row = options.get("start_row", 0)
        headers = options.get("headers", None)

        if headers is not None:
            line_data = iter(data).__next__()
            if not line_data:
                raise ValueError("data is empty")
            if not isinstance(headers, (list, tuple)):
                raise ValueError(f"headers is not iterable object, headers is {type(headers)}")
            if len(headers) != len(line_data):
                raise ValueError("len(column) not equal len data row!")

            worksheet.write_row(
                row=data_first_row,
                col=data_first_column,
                data=headers,
            )
            data_first_row += 1

        for row, line in enumerate(data):
            for col, val in enumerate(line):
                worksheet.write(
                    row+data_first_row,
                    data_first_column+col,
                    val,
                )
        return (row+data_first_row, data_first_column+col)

    def _set_format(self, sheet: xls.workbook.Worksheet, options={}):
        headers_format = options.get("headers_format", None)
        header_height = options.get("headers_height", None)
        columns_format = options.get("data_format", None)
        columns_wight = options.get("columns_wight", None)
        start_column = options.get("start_column", 0)
        start_row = options.get("start_row", 0)

        h_form = self.workbook.add_format(headers_format)
        sheet.set_row(start_row, height=header_height, cell_format=h_form)

        if columns_format is not None:
            for c_form in columns_format:
                c_form = self.workbook.add_format(c_form)
                sheet.set_column(
                    start_column,
                    start_column,
                    cell_format=c_form,
                )
        if columns_wight is not None:
            for col, c_wight in enumerate(columns_wight):
                sheet.set_column(
                    start_column+col,
                    start_column+col,
                    width=c_wight,
                )

    def _add_filter(self, worksheet: xls.workbook.Worksheet, options={}):
        filter = options.get("filter", False)
        if not filter:
            return None

        first_row = options.get("start_row", 0)
        first_col = options.get("start_column", 0)
        last_row = options["last_row"]
        last_col = options["last_column"]

        worksheet.autofilter(first_row, first_col, last_row, last_col)

    def _add_pivot(self, sheet: xls.workbook.Worksheet, options={}):
        pivot = options.get("pivot", False)
        if not pivot:
            return None

        headers = options.get("headers", None)
        headers_row = False
        filter = options.get("filter", False)
        columns = None
        if headers is None:
            columns = []
            for name_column in headers:
                columns.append({"header": name_column})
            headers_row = True

        pivot_options = {
            "autofilter": filter,
            "header_row": headers_row,
            "columns": columns,
        }


        if not pivot:
            return None

        first_row = options.get("start_row", 0)
        first_col = options.get("start_column", 0)
        last_row = options["last_row"]
        last_col = options["last_column"]
        sheet.add_table(first_row, first_col, last_row, last_col)


    def save_book(self):

        def _save_in_paths(
                list_path: tuple[Path],
                filename: str,
                value: bytes
                ) -> None:
            for path in list_path:
                with open(path / filename, "wb") as ex_file:
                    ex_file.write(value)

        self.workbook.close()
        self._bookIO.seek(0)
        _save_in_paths(self.save_path, self.filename, self._bookIO.getvalue())
        self._bookIO.close()

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
