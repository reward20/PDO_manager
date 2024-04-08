from typing import List, Union, Any

from pydantic import BaseModel, field_validator
from pathlib import Path


__all__ = [
    "Dir_file"
]


class Dir_file(BaseModel):
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
