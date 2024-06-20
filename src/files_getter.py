from pathlib import Path
from typing import List, Iterator

from src.schemas import CorrectDir, Correct_Suffix


__all__ = [
    "FilesGetter"
]


class FilesGetter(object):

    def __init__(self, path_dir: Path, suffix: str | List[str] = ""):
        self.path_dir: Path = CorrectDir(path=path_dir).path
        self.suffix: List[str] = Correct_Suffix(suffix=suffix).suffix

    @staticmethod
    def _find_file(*, path_dir: Path) -> Iterator[Path]:
        return (x for x in path_dir.iterdir() if x.is_file())

    @staticmethod
    def _get_files(*, path: Path, suffix: List[str]) -> Iterator[Path]:
        generator = FilesGetter._find_file(path_dir=path)
        return (file for file in generator if file.suffix in suffix)

    def files(self) -> Iterator[Path]:
        return FilesGetter._get_files(path=self.path_dir, suffix=self.suffix)

    def get_file(self, name: str):
        for file in self.files():
            if file.name == name:
                return file
        else:
            raise ValueError(f"{name} is not Found")

    def __iter__(self):
        return self.files()
