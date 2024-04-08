from typing import Tuple, Union

from pydantic import BaseModel, field_validator
from pathlib import Path


__all__ = [
    "Correct_Dir",
    "Correct_Suffix"
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
    def valid_suffix(cls, suffix: Union[str, Tuple[str, ...]]) -> Union[str, Tuple[str, ...]]:
        if isinstance(suffix, str):
            return Correct_Suffix.valid_str_suffix(suffix)
        elif isinstance(suffix, tuple):
            return Correct_Suffix.valid_tuple_suffix(suffix)
    
    @staticmethod
    def valid_str_suffix(suffix: str) -> str:
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

if __name__ == "__main__":
    print(Correct_Suffix(suffix = "").suffix)
