from pathlib import Path
from typing import Any, Tuple
import xlsxwriter as xls
from io import BytesIO
from itertools import zip_longest
from src.schemas import CorrectDir, ExcelOptionsSchem

__all__ = [
    "ExcelBookWriter",
]


class ExcelBookWriter(object):

    def __init__(self, filename: str | None = None, save_path: Path | Tuple[Path, ...] | None = None) -> None: # good

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
        data: list,
        *,
        options: dict[str, Any] = {},
    ):
        options["data"] = data
        options = ExcelOptionsSchem(**options).model_dump()
        worksheet = self._get_worksheet(namesheet)
        self.write_data_in_table(worksheet, options)
        self._set_format(worksheet, options)

    def _get_worksheet(self, namesheet: str) -> xls.workbook.Worksheet:
        worksheet = self.workbook.get_worksheet_by_name(namesheet)
        if worksheet is None:
            worksheet = self.workbook.add_worksheet(name=namesheet)
        return worksheet

    def write_data_in_table(self, worksheet: xls.workbook.Worksheet, options: dict[str, Any]):

        data = options["data"]
        data_format = options["data_format"]
        headers = options["headers"]
        headers_format = options["headers_format"]
        autofilter = options["autofilter"]
        pivot = options["pivot"]
        start_row = options["start_row"]
        start_column = options["start_column"]
        end_row = options["end_row"]
        end_column = options["end_column"]

        style = "Table Style Light 15" if pivot else None
        header_row = True if headers is not None else False

        for col, val in enumerate(data_format):
            data_format[col] = self.workbook.add_format(val)

        for col, val in enumerate(headers_format):
            headers_format[col] = self.workbook.add_format(val)

        store_options = []

        def handler_list(value):
            if value is None:
                return [None]
            return value

        for head, h_format, d_format in zip_longest(
            handler_list(headers),
            handler_list(headers_format),
            handler_list(data_format),
        ):
            store_options.append({
                "header": head,
                "header_format": h_format,
                "format": d_format
            })

        local_options = {
            "data": data,
            "autofilter": autofilter,
            "header_row": header_row,
            "style": style,
            "columns": store_options,
        }
        worksheet.add_table(start_row, start_column, end_row, end_column, local_options)

    def _set_format(self, sheet: xls.workbook.Worksheet, options={}):
        # headers_format = options.get("headers_format", None)
        header_height = options.get("headers_height", None)
        # columns_format = options.get("data_format", None)
        columns_wight = options.get("columns_wight", None)
        start_column = options.get("start_column", 0)
        start_row = options.get("start_row", 0)

        if options.get("headers", False):
            sheet.set_row(start_row, height=header_height)

        if columns_wight is not None:
            for col, c_wight in enumerate(columns_wight):
                sheet.set_column(
                    start_column+col,
                    start_column+col,
                    width=c_wight,
                )

    def insert_image(self, row, col, namesheet, picture: BytesIO):
        worksheet = self._get_worksheet(namesheet)
        # worksheet.insert_image(row, col, {"image_data": picture})
        worksheet.images.append(
            [
                row,
                col,
                "pict",
                0,
                0,
                1,
                1,
                None,
                None,
                2,
                picture,
                None,
                False
            ]
        )

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
