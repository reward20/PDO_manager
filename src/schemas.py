from datetime import date, datetime
from decimal import Decimal
from pydantic import (
    BaseModel, PlainValidator, WithJsonSchema, 
    Field,
    ValidationError,
    field_validator,
    ConfigDict,
    model_validator,
    PositiveInt
)
import pandas as pd
from typing import  Annotated, Any, List, Tuple, Union
from pathlib import Path
from itertools import repeat

__all__ = [
    "CorrectDir",
    "Correct_Suffix",
    "ML_ex_correct",
    "ML_O_correct",
    "ML_Operation_Model",
    "ML_sum_Model",
    "SKLAD_correct",
    "ExcelOptionsSchem",
    "PartValidate",
    "DetailValidate",
    "TableValidate",
]

_Timestamp = Annotated[
    pd.Timestamp,
    PlainValidator(lambda x: pd.Timestamp(x)),
    WithJsonSchema({"type": 'date-time'})
]


class PartValidate(BaseModel):
    master_name: str = Field(max_length=32)
    slave_name: str = Field(max_length=32)
    count: PositiveInt


class DetailValidate(BaseModel):
    name_part: str = Field(max_length=32)
    name_detail: str = Field(max_length=128)
    count: PositiveInt


class TableValidate(BaseModel):
    name_part: str = Field(max_length=32)
    name_table: str = Field(max_length=32)
    count: PositiveInt


class CorrectDir(BaseModel):

    path: Path | list[Path]

    @field_validator("path")
    @classmethod
    def validate_path(cls, path_dir: Union[Path, str, list]):
        path_confirm = None
        if isinstance(path_dir, (tuple, list)):
            path_confirm = []
            for path in path_dir:
                path_confirm.append(CorrectDir.check_is_dir(path))
        else:
            path_confirm = CorrectDir.check_is_dir(path_dir)
        return path_confirm

    @classmethod
    def check_is_dir(cls, path_dir: Union[Path, str]) -> Path:
        path_dir = Path(path_dir)
        if not path_dir.exists():
            raise ValueError(f"{path_dir.absolute()} is not exits!")
        if not path_dir.is_dir():
            raise ValueError(f"{path_dir} is not dir!")
        return path_dir


class Correct_Suffix(BaseModel):

    suffix: str | List[str]

    @field_validator("suffix")
    @classmethod
    def valid_suffix(
            cls,
            suffix: str | Tuple[str, ...]
            ) -> Tuple[str, ...]:
        if isinstance(suffix, str):
            return (Correct_Suffix.valid_str_suffix(suffix),)
        elif isinstance(suffix, (tuple, list)):
            return Correct_Suffix.valid_tuple_suffix(suffix)

    @staticmethod
    def valid_str_suffix(suffix: str) -> str:
        if suffix.startswith(".") or not suffix:
            return suffix.lower()
        else:
            return ("." + suffix).lower()

    @staticmethod
    def valid_tuple_suffix(suffix: Tuple[str, ...]) -> Tuple[str, ...]:
        list_storage = list()
        for item in suffix:
            item = Correct_Suffix.valid_str_suffix(item)
            list_storage.append(item)
        return tuple(list_storage)


class ML_ex_correct(BaseModel):
    mr_list: str = Field(
        max_length=8,
        min_length=8,
        )
    order: str = Field(
        max_length=5,
        min_length=5,
        )
    detail_num: str = Field(max_length=128)
    detail_name: str = Field(max_length=128)
    count: int = Field(ge=0)
    w_hours: Decimal = Field(ge=0)
    date_start: date
    mass_metall: Decimal = Field(ge=0)
    mass_detail: Decimal = Field(ge=0)
    profile_full: str = Field(max_length=128)
    profile: str = Field(max_length=32)
    det_in_workpiece: int = Field(gt=0)
    material: str = Field(max_length=128)

    @field_validator("w_hours", "mass_metall", "mass_detail", mode="after")
    @classmethod
    def decimal_quantize(cls, decimal_v: Decimal):
        return decimal_v.quantize(Decimal("0.001"))

    @field_validator("w_hours", "mass_metall", "mass_detail", mode="before")
    @classmethod
    def decimal_requize(cls, decimal_v: str):
        return decimal_v.replace(",", ".")

    @field_validator("date_start", mode="before")
    @classmethod
    def date_requize(cls, date_v: str):
        return datetime.strptime(date_v, "%d/%m/%Y").date()

    @field_validator("count", mode="before")
    @classmethod
    def detail_count_validate(cls, count: str):
        if "#" in count:
            return count.split("#")[0]
        return count


class MOWHourse(BaseModel):
    mr_list: str = Field(
        max_length=8,
        min_length=8,
        )
    w_hours: Decimal = Field(ge=0)


class ML_Operation_Model(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    detail_num: str = Field(max_length=128, min_length=2)
    operation_num: int
    operation_name: str = Field(max_length=128, min_length=1)
    t_single: Decimal = Field(ge=0)
    t_install: Decimal = Field(ge=0)

    @field_validator("operation_num", mode="after")
    @classmethod
    def num_operation_validate(cls, num: int):
        if not num > 99 and num < 1000:
            ValidationError(
                f"Operation number most be greater than 99 and less 1000, received {num}"
            )
        return num
    

class ML_sum_Model(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    mr_list: str = Field(
        max_length=8,
        min_length=8,
    )
    t_all: Decimal = Field(ge=0)


class ML_O_correct(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    mr_list: str = Field(
        max_length=8,
        min_length=8,
    )
    order: str = Field(
        max_length=5,
        min_length=5,
    )
    detail_num: str = Field(max_length=128, min_length=2)
    operation_num: int
    operation_name: str = Field(max_length=128, min_length=1)
    t_single: Decimal = Field(ge=0)
    t_install: Decimal = Field(ge=0)
    t_all: Decimal = Field(ge=0)


    @field_validator("operation_num", mode="after")
    @classmethod
    def num_operation_validate(cls, num: int):
        if not num > 99 and num < 1000:
            ValidationError(
                f"Operation number most be greater than 99 and less 1000, received {num}"
            )
        return num


class SKLAD_correct(BaseModel):
    detail_num: str = Field(max_length=128, min_length=2)
    mr_list: str = Field(
        max_length=8,
        min_length=8,
        )
    count: int = Field(ge=0)
    complite: str
    date_complite: date

    @field_validator("date_complite", mode="before")
    @classmethod
    def date_requize(cls, date_v: str):
        return datetime.strptime(date_v, "%d/%m/%y").date()


class ExcelOptionsSchem(BaseModel):
    data: list[list[Any]]
    data_format: list[dict[str, Any]] | None = None
    headers: tuple[str, ...] | None = None
    headers_format: list[dict[str, Any]] | None = None
    autofilter: bool = False
    pivot: bool = False

    columns_wight: list[int] | None = None
    headers_height: int | None = None

    start_row: int = 0
    start_column: int = 0
    end_row: int | None = None
    end_column: int | None = None

    @model_validator(mode="after")
    def validate_format(self):
        data = self.data
        data_format = self.data_format
        headers_format = self.headers_format
        headers = self.headers
        columns_wight = self.columns_wight
        size_column = len(data[0])
        size_row = len(data)
        self.end_column = self.start_column + size_column - 1
        self.end_row = self.start_row + size_row
        self.autofilter = True if self.pivot else self.autofilter

        def check_variable(value_check: list[Any] | None, name: str):
            if value_check is not None:
                if len(value_check) == 1:
                    list_format: list[Any] = []
                    for count in range(size_column):
                        list_format.append(value_check[0])
                    return list_format

                elif len(value_check) != size_column:
                    raise ValueError(f"size '{name}' not equal size 'data' columns")
                return value_check
            else:
                return list(repeat(None, size_column))

        if headers is not None:
            if len(headers) != size_column:
                raise ValueError("size 'headers' not equal size 'data' columns")
            self.headers_format = check_variable(headers_format, "headers_format")
        else:
            self.headers_format = list(repeat(None, size_column))
            self.headers_height = None
            self.end_row -= 1

        self.data_format = check_variable(data_format, "data_format")
        self.columns_wight = check_variable(columns_wight, "columns_wight")
        return self


class CalculationSchem(BaseModel):

    order_name: str = Field(
        max_length=5,
        min_length=5,
    )
    mr_list: str = Field(
        max_length=8,
        min_length=8,
    )
    product: str
    count: int
    w_hours: float
    date_start: _Timestamp
    date_complite: _Timestamp
    complite: str | None

    # @field_validator("date_complite","date_start", mode="after")
    # @classmethod
    # def date_requize(cls, date_v: date | None) -> pd.Timestamp:
    #     return pd.to_datetime(date_v)
    
    @field_validator("complite", mode="after")
    @classmethod
    def str_requize(cls, str_line: str | None) -> str:
        if str_line is None:
            return ""
        return str_line
