from pathlib import Path
from typing import Tuple

YZ_FOLDER: Path = Path(r"Data\dos_file")
BASE_FOLDER: Path = Path(r"Data\yz_folder")

FILES_NAMES_DOS: Tuple[str, ...] = ("MLEXCEL", "MLEXCELO", "SKLAD")
FILES_SUFFIX_DOS: str = ""

NAME_BASE: str = r"Маршрутные листы"
SUFFIX_BASE: str = ".csv"

YZ_NAMES_FILE: Tuple[str, ...] = ("dt", "sd", "tb", "yz")
YZ_SUFFIX_FILE: str = ".csv"
