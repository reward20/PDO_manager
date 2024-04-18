from datetime import date, datetime
from decimal import Decimal
from typing import Tuple, Union

from pydantic import BaseModel, Field, field_validator, ValidationError, ConfigDict
from pathlib import Path

__all__ = [
    "Correct_Dir",
    "Correct_Suffix",
    "ML_ex_correct",
    "ML_O_correct"
]


class Correct_Dir(BaseModel):
    path: Union[Path, str]

    @field_validator("path")
    @classmethod
    def check_is_dir(cls, path_dir: Union[Path, str]) -> Path:

        path_dir = Path(path_dir)
        if not path_dir.exists():
            raise ValueError(f"{path_dir} is not exits!")
        if not path_dir.is_dir():
            raise ValueError(f"{path_dir} is not dir!")
        return path_dir


class Correct_Suffix(BaseModel):
    suffix: Union[str, Tuple[str, ...]]

    @field_validator("suffix")
    @classmethod
    def valid_suffix(
            cls,
            suffix: Union[str, Tuple[str, ...]]
            ) -> Union[str, Tuple[str, ...]]:
        if isinstance(suffix, str):
            return Correct_Suffix.valid_str_suffix(suffix)
        elif isinstance(suffix, tuple):
            return Correct_Suffix.valid_tuple_suffix(suffix)

    @staticmethod
    def valid_str_suffix(suffix: str) -> Tuple:
        if suffix.startswith(".") or not suffix:
            return tuple([suffix])
        else:
            return tuple(["." + suffix])

    @staticmethod
    def valid_tuple_suffix(suffix: Tuple[str]) -> Tuple[str]:
        list_storage = list()
        for item in suffix:
            if item.startswith(".") or not item:
                list_storage.append(item)
            elif item:
                list_storage.append("." + item)
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
    detail_count: int = Field(ge=0)
    w_hours: Decimal = Field(ge=0)
    date_start: date
    mass_metal: Decimal = Field(ge=0)
    mass_detail: Decimal = Field(ge=0)
    profile_full: str = Field(max_length=128)
    profile: str = Field(max_length=32)
    det_in_workpiece: int = Field(gt=0)
    material: str = Field(max_length=128)

    @field_validator("w_hours", "mass_metal", "mass_detail", mode="after")
    @classmethod
    def decimal_quantize(cls, decimal_v: Decimal):
        return decimal_v.quantize(Decimal("0.001"))

    @field_validator("w_hours", "mass_metal", "mass_detail", mode="before")
    @classmethod
    def decimal_requize(cls, decimal_v: str):
        return decimal_v.replace(",", ".")

    @field_validator("date_start", mode="before")
    @classmethod
    def date_requize(cls, date_v: str):
        return datetime.strptime(date_v, "%d/%m/%Y").date()

    @field_validator("detail_count", mode="before")
    @classmethod
    def detail_count_validate(cls, count: str):
        if "#" in count:
            return count.split("#")[0]
        return count


class ML_O_correct(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)

    detail_num: str = Field(max_length=128, min_length=2)
    operation_num: int
    operation_name: str = Field(max_length=128, min_length=1)

    @field_validator("operation_num", mode="after")
    @classmethod
    def num_operation_validate(cls, num: int):
        if not num > 99 and num < 1000:
            ValidationError(
                f"Operation number most be greater than 99 and less 1000, received {num}"
                )
        return num
