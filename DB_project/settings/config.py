from typing import Tuple
from pydantic_settings import BaseSettings

__all__ = [
    "settings",
]


class Settings(BaseSettings):
    # FILES_NAMES_DOS: Tuple[str, ...] = ("MLEXCEL", "MLEXCELO", "SKLAD")
    # FILES_SUFFIX_DOS: str = ""

    MLEXCEL_CSV_NAME_COLUMNS: Tuple[str, ...] = (
        "mr_list", "order", "detail_num", "detail_name",
        "count", "mass_metal", "w_hours",
        "material", "mass_detail", "profile_full",
        "profile", "date_start", "det_in_workpiece"
    )

    SKLAD_CSV_NAME_COLUMNS: Tuple[str, ...] = (
        "detail_num", "mr_list", "complite", "count", "date_complite",
    )


settings = Settings()
