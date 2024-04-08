from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union, Generator, List, Iterator
from pydantic import validate_call
from schemas.schemas import Dir_file

__all__ = [
    "AbstractFinder"
]


class AbstractFinder(ABC):

    @staticmethod
    def get_files(*, path_dir: Union[str, Path]) -> Iterator[Path]:
        path_dir = Dir_file(path=path_dir).path
        return (x for x in path_dir.iterdir() if x.is_file())

    @staticmethod
    @validate_call
    def valid_file(*, path: Path, suffix: Union[str, List[str]]) -> Iterator[Path]:
        generator = AbstractFinder.get_files(path_dir=path)
        if isinstance(suffix, list):
            return (x for x in generator if x.suffix in suffix)
        elif isinstance(suffix, str):
            return (x for x in generator if x.suffix == suffix)
