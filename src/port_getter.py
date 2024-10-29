from pathlib import Path
from collections import defaultdict
from .files_getter import FilesGetter
from config import settings
from shutil import move

__all__ = [
    "PotrGetter",
    "PdoGetter",
]


class PotrGetter(FilesGetter):
    """
    Get potreb files for handler
    """

    def __init__(self, path_dir: Path, suffix: str | tuple[str] = ""):
        super().__init__(path_dir, suffix)
        self._files = defaultdict(dict)

    def _update_files(self):
        folders: list[Path] = []
        folders.append(self.path_dir)
        while folders:
            check_folder = folders.pop(0)
            temp_dict = self._review_files(check_folder)
            self._files.update(temp_dict)
            folders.extend(self.get_folders(path_dir=check_folder))

    def _review_files(self, check_folder: Path):
        temp_file_dict = defaultdict(dict)
        files = self.get_files(path_dir=check_folder)
        files = [(file.stem, file) for file in files]
        files = self._view_dublicates_name(files)

        for name, file in files:
            temp_file_dict[name][file.suffix.lower()] = file
        
        correct_file_dict =  self._check_suffix_files_dict(temp_file_dict)
        return correct_file_dict

    def _check_suffix_files_dict(self, check_dict: dict[dict[str, Path]]) -> dict[dict[str, Path]]:
        return_dict = defaultdict(dict)
        for name, dict_suffix in check_dict.items():
            dict_keys = dict_suffix.keys()
            for key_suffix in self.suffix:
                if key_suffix not in dict_keys:
                    break
            else:
                return_dict[name].update(check_dict[name])
        return return_dict

    def _view_dublicates_name(self, files: list[tuple[str, Path]]) -> list[tuple[str, Path]]:
        name_set = self._files.keys()
        new_files = []
        for name, file in files:
            name = self._check_name(name, name_set)
            new_files.append((name, file))
        return new_files

    def _check_name(self, name: str, set_list: set) -> str:
        if name not in set_list:
            return name
        i = 1
        while name+f"_{i}" in set_list:
            i += 1
        return name+f"_{i}"

    @property
    def files_dict(self) -> dict[str, dict[str, Path]]:
        self._update_files()
        return self._files


class PdoGetter(FilesGetter):
    """
    Get PDO files
    """

    def __init__(self, path_dir: Path, suffix: str | tuple[str] = ""):
        super().__init__(path_dir, suffix)
        self._files = defaultdict(dict)
        self._update_files()

    def _validate_pdo_file(self, files: list[Path]):
        error_message = []
        files_name = list([x.stem.upper() for x in files])
        for name_file in settings.DOS_FILES_NAMES:
            if name_file not in files_name:
                error_message.append(name_file)
        if error_message:
            raise ValueError (f"In {self.path_dir} not found files by name: {error_message}")

    def _update_files(self):
        files = list(self.files)
        self._validate_pdo_file(files)

        for file in files:
            if file.stem.upper() in settings.DOS_FILES_NAMES:
                # self._files[file.stem] = self._move_file(file, settings.DOS_FOLDER)
                self._files[file.stem] = file
        self._move_dos_files()

    def _move_dos_files(self):
        if not settings.DOS_MOVING:
            return None
        for name, file in self._files.items():
            self._files[name] = self._move_file(file, settings.DOS_FOLDER)

    def _move_file(self, file: Path, folder: Path):
        return move(file, folder / file.name)

    @property
    def files_dict(self) -> dict[str,  Path]:
        return self._files


