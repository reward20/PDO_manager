from pathlib import Path
from typing import Union, List, Iterator

from schemas import Correct_Dir, Correct_Suffix
from dataclasses import dataclass

__all__ = [
    "Getter_files"
]


@dataclass
class Getter_files(object):
    path_dir: Union[str, Path]
    suffix: Union[str, List[str]] = ""

    def __post_init__(self):
        self.path_dir = Correct_Dir(path=self.path_dir).path
        self.suffix = Correct_Suffix(suffix=self.suffix).suffix

    @staticmethod
    def _find_file(*, path_dir: Path) -> Iterator[Path]:
        return (x for x in path_dir.iterdir() if x.is_file())

    @staticmethod
    def _get_files(*, path: Path, suffix: List[str]) -> Iterator[Path]:
        generator = Getter_files._find_file(path_dir=path)
        return (file for file in generator if file.suffix in suffix)

    def search_files(self) -> Iterator[Path]:
        return Getter_files._get_files(path=self.path_dir, suffix=self.suffix)
