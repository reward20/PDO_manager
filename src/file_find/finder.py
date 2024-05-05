from pathlib import Path
from typing import Tuple, Union, List, Iterator

from src.schemas import Correct_Dir, Correct_Suffix
from dataclasses import dataclass

__all__ = [
    "Getter_files"
]


@dataclass
class Getter_files(object):
    path_dir: Union[str, Path]
    suffix: Union[str, List[str]] = ""

    def __post_init__(self):
        self.path_dir: Path = Correct_Dir(path=self.path_dir).path
        self.suffix: Tuple[str, ...] = Correct_Suffix(suffix=self.suffix).suffix

    @staticmethod
    def __find_file(*, path_dir: Path) -> Iterator[Path]:
        return (x for x in path_dir.iterdir() if x.is_file())

    @staticmethod
    def __get_files(*, path: Path, suffix: List[str]) -> Iterator[Path]:
        generator = Getter_files.__find_file(path_dir=path)
        return (file for file in generator if file.suffix in suffix)

    def files(self) -> Iterator[Path]:
        return Getter_files.__get_files(path=self.path_dir, suffix=self.suffix)

    def get_file(self, name):
        for file in self.files():
            if file.name == name:
                return file
        else:
            raise ValueError(f"{name} is not Found")

    def __iter__(self):
        return self.files()
