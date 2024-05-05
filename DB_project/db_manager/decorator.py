from shutil import copy
from typing import Any
from pathlib import Path
from src.settings import settings
from src.file_find import Getter_files
from datetime import datetime, date

__all__ = [
    "Control_file",
]


class Control_file(object):
    def __init__(self, cls) -> None:
        self.obj = cls

    def __call__(self, *args: Any, **kwds: Path) -> Any:
        for k, v in kwds.items():
            files_middle = Getter_files(settings.DOS_FOLDER, v.suffix)
            files_coping = Getter_files(settings.DIR_COPY, v.suffix)
            try:
                middle_f = files_middle.get_file(v.stem)
            except ValueError:
                kwds[k] = copy(v, settings.DOS_FOLDER / v.name)
                continue
            else:
                try:
                    copy_f = files_coping.get_file(v.stem)
                    time_create = copy_f.stat().st_birthtime
                    time_create = datetime.fromtimestamp(time_create).date()
                except ValueError:
                    copy(middle_f, settings.DIR_COPY / middle_f.name)
                else:
                    if time_create < date.today():
                        copy(middle_f, settings.DIR_COPY / middle_f.name)
                kwds[k] = copy(v, settings.DOS_FOLDER / v.name)
        return self.obj(*args, **kwds)
