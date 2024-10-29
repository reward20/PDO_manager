from pathlib import Path
from typing import Iterator
from .schemas import CorrectDir, Correct_Suffix

__all__ = [
    "FilesGetter"
]

class FilesGetter(object):

    def __init__(self, path_dir: Path, suffix: str | tuple[str] = ""):
        self.path_dir: Path = path_dir
        self.suffix: tuple[str] = suffix
        self._validate = bool(self.suffix)

    @property
    def path_dir(self) -> Path:
        return self._path_dir

    @path_dir.setter
    def path_dir(self, dir: Path):
        self._path_dir = CorrectDir(path=dir).path

    @property
    def suffix(self):
        return self._suffix
    
    @suffix.setter
    def suffix(self, suffix: str | tuple[str]):
        self._suffix = Correct_Suffix(suffix=suffix).suffix

    @staticmethod
    def _get_files(*, path_dir: Path) -> Iterator[Path]:
        return (file for file in path_dir.iterdir() if file.is_file())

    @staticmethod
    def _get_validate_files(*, path_dir: Path, suffix: tuple[str]):
        files = FilesGetter._get_files(path_dir=path_dir)
        return (file for file in files if file.suffix.lower() in suffix)


    def get_files(self, *, path_dir: Path = None, suffix: tuple[str] | None = None) -> Iterator[Path]:
        if path_dir is None:
            path_dir = self.path_dir
        
        if suffix is None:
            suffix = self.suffix
        
        if self._validate:
            return self._get_validate_files(
                path_dir=path_dir,
                suffix=suffix
            )
        else:
            return self._get_files(path_dir=path_dir)

    @property
    def files(self):
        return self.get_files(
            path_dir=self.path_dir,
            suffix=self.suffix
        )
 

    def get_file_by_name(self, name: str):
        for file in self.get_all_files():
            if file.name == name:
                return file
        else:
            raise ValueError(f"{name} is not Found")

    def get_folders(self, *, path_dir: Path | None = None) -> Iterator[Path]:
        if path_dir is None:
            path_dir = self.path_dir
        return (folder for folder in path_dir.iterdir() if folder.is_dir())

    def get_all_files(self) -> Iterator[Path]:
        list_folder = [self.path_dir, ]
        while list_folder:
            check_dir = list_folder.pop()
            list_folder.extend(self.get_folders(path_dir=check_dir))
            if self._validate:
                files = FilesGetter._get_validate_files(path_dir=check_dir, suffix=self.suffix)
            else:
                files = FilesGetter._get_files(path_dir=check_dir)
            for file in files:
                yield file

    def __iter__(self):
        return self.files
