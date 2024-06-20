from shutil import copy
from pathlib import Path
from typing import Union

from config import settings
from src.files_getter import FilesGetter


__all__ = [
    "RecopyFile",
]


class RecopyFile(object):

    def __init__(self, check_file: Path):
        self.check_file: Path = check_file

    @staticmethod
    def _check_new_size_file(coping_file: Path, reserv_files: Path) -> bool:
        """_summary_

        Args:
            coping_file (Path): copying file
            reserv_files (Path): reserv_file

        Returns:
            bool: True if size is diffrent
        """
        def get_size(file: Path) -> float:
            size = file.stat().st_size
            return size

        copy_file_t_creat = get_size(coping_file)
        reserv_file_t_creation = get_size(reserv_files)
        # if file_copy create today, then file is not new
        return not (copy_file_t_creat == reserv_file_t_creation)

    @staticmethod
    def _compare_date_create(coping_file: Path, reserv_files: Path) -> bool:
        # Return True if date is different

        def get_date(file: Path) -> float:
            return file.stat().st_birthtime

        copy_file_date_creat = get_date(coping_file)
        reserv_file_date_creation = get_date(reserv_files)

        return not (copy_file_date_creat == reserv_file_date_creation)

    def recopy_dos_file(self) -> None:

        def get_file(file_name: str, dir_manager: FilesGetter) -> Union[None, Path]:
            try:
                file = dir_manager.get_file(file_name)
            except ValueError:
                return None
            else:
                return file

        dir_dos_files = FilesGetter(settings.DOS_FOLDER, settings.DOS_FILES_SUFFIX)
        dir_copy_files = FilesGetter(settings.DIR_COPY, settings.DOS_FILES_SUFFIX)

        exist_file = get_file(self.check_file.stem, dir_dos_files)
        copy_file = get_file(self.check_file.stem, dir_copy_files)

        if exist_file is None:
            copy(self.check_file, settings.DOS_FOLDER / self.check_file.name)
            return None

        if copy_file is None:
            copy(exist_file, settings.DIR_COPY / self.check_file.name)
        elif RecopyFile._compare_date_create(copy_file, exist_file) and\
                RecopyFile._check_new_size_file(copy_file, exist_file):
            copy(exist_file, settings.DIR_COPY / self.check_file.name)

        # coping file from X in local storage
        copy(self.check_file, settings.DOS_FOLDER / self.check_file.name)
