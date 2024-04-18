from pathlib import Path
from typing import Tuple

from pydantic_settings import BaseSettings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

__all__ = [
    "settings",
    "db_engine",
    "db_session",
]


class Settings(BaseSettings):
    DOS_FOLDER: Path = Path(r"Data\dos_file")
    FILES_NAMES_DOS: Tuple[str, ...] = ("MLEXCEL", "MLEXCELO", "SKLAD")
    FILES_SUFFIX_DOS: str = ""

    YZ_FOLDER: Path = Path(r"Data\yz_folder")
    YZ_NAMES_FILE: Tuple[str, ...] = ("dt", "sd", "tb", "yz")
    YZ_SUFFIX_FILE: str = ".csv"

    MLEXCEL_CSV_NAME_COLUMNS: Tuple[str, ...] = (
        "mr_list", "order", "detail_num", "detail_name",
        "detail_count", "mass_metal", "w_hours",
        "material", "mass_detail", "profile_full",
        "profile", "date_start", "det_in_workpiece"
        )

    DIR_DATABASE: str = r"Data\\DB"
    NAME_MLE_DB: str = r"MLE_DB.db"
    MLE_engine: str = f"sqlite+pysqlite:///{DIR_DATABASE}\\{NAME_MLE_DB}"
    # MLE_engine: str = "sqlite+pysqlite:///:memory:"

    NAME_BASE: str = r"Маршрутные листы"
    SUFFIX_BASE: str = ".csv"


settings = Settings()
db_engine = create_engine(url=settings.MLE_engine)
db_session = sessionmaker(bind=db_engine)
