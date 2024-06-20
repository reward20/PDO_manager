from pathlib import Path
from typing import Tuple
from pydantic_settings import BaseSettings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

__all__ = [
    "settings",
    "reader_setting",
    "db_engine",
    "db_session",
]


class ProjectSettings(BaseSettings):
    DOS_FOLDER: Path = Path(r"data\dos_file")
    DOS_FILES_SUFFIX: str = ""

    MLE: str = "MLEXCEL"
    MLE_O: str = "MLEXCELO"
    SKLD: str = "SKLAD"

    DOS_FILES_NAMES: Tuple[str, ...] = (MLE, MLE_O, SKLD)

    YZ_FOLDER: Path = Path(r"data\yz_folder")
    YZ_NAMES_FILE: Tuple[str, ...] = ("dt", "sd", "tb", "yz")
    YZ_SUFFIX_FILE: str = ".csv"

    DIR_DATABASE: Path = Path(r"data\\DB")
    DIR_COPY: Path = Path(r"data\\Copy")
    X_DOS_FOLDER: Path = Path(r"X:\Для ПДО\Походня В.О\DOS_File")

    DIR_DATABASE.mkdir(parents=True, exist_ok=True)
    DIR_COPY.mkdir(parents=True, exist_ok=True)

    NAME_BASE: str = r"Маршрутные листы"
    SUFFIX_BASE: str = ".csv"

    NAME_MLE_DB: str = r"MLE_DB.db"
    MLE_engine: str = f"sqlite+pysqlite:///{DIR_DATABASE}\\{NAME_MLE_DB}"


class ReaderSettings(BaseSettings):

    MLEXCEL_CSV_NAME_COLUMNS: Tuple[str, ...] = (
        "mr_list", "order", "detail_num", "detail_name",
        "count", "mass_metal", "w_hours",
        "material", "mass_detail", "profile_full",
        "profile", "date_start", "det_in_workpiece"
    )

    SKLAD_CSV_NAME_COLUMNS: Tuple[str, ...] = (
        "detail_num", "mr_list", "complite", "count", "date_complite",
    )


settings = ProjectSettings()
reader_setting = ReaderSettings()
db_engine = create_engine(url=settings.MLE_engine)
db_session = sessionmaker(bind=db_engine)
