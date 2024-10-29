from typing import Any
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from .formater import Formater

__all__ = [
    "settings",
    "engine",
    "session",
    "excel_setting",
]


class ProjectSettings(BaseSettings):

    # YZ settings
    FILE_TYPE: tuple[str, ...] = (".sp1", ".pr1", ".se1")
    FOLDER_YZ: Path = Path(r"data\\yz_data")
    FOLDER_INPUT: Path = FOLDER_YZ / r"input_potreb"
    FOLDER_OUTPUT: Path = FOLDER_YZ / r"store_potreb"
    
    FOLDER_INPUT.mkdir(parents=True, exist_ok=True)
    FOLDER_OUTPUT.mkdir(parents=True, exist_ok=True)

    # PDO settings
    FOLDER_DATABASE: Path = Path(r"data\\DB")
    DOS_FOLDER: Path = Path(r"data\\dos_file")
    DOS_ZIP_STORED: Path = Path(r"data\\dos_zip")
    # DIR_COPY: Path = Path(r"data\\dos_file")
    X_DOS_FOLDER: Path = DOS_FOLDER
    # X_DOS_FOLDER: Path = Path(r"X:\Для ПДО\Походня В.О\DOS_File")

    FOLDER_DATABASE.mkdir(parents=True, exist_ok=True)
    DOS_FOLDER.mkdir(parents=True, exist_ok=True)
    # DIR_COPY.mkdir(parents=True, exist_ok=True)
    DOS_ZIP_STORED.mkdir(parents=True, exist_ok=True)
    
    DOS_MOVING = False
    DOS_STORED = False

    MLE: str = "MLEXCEL"
    MLE_O: str = "MLEXCELO"
    SKLD: str = "SKLAD"
    DOS_FILES_NAMES: tuple[str, ...] = (MLE, MLE_O, SKLD)
    DOS_FILES_SUFFIX: tuple[str] = ("", )
    DB_NAME: str = "MLE_DB.db"
    DATABASE: str = f"sqlite+pysqlite:///{FOLDER_DATABASE}\\{DB_NAME}"

    MLEXCEL_CSV_NAME_COLUMNS: tuple[str, ...] = (
        "mr_list", "order", "detail_num", "detail_name",
        "count", "mass_metall", "w_hours",
        "material", "mass_detail", "profile_full",
        "profile", "date_start", "det_in_workpiece"
    )

    SKLAD_CSV_NAME_COLUMNS: tuple[str, ...] = (
        "detail_num", "mr_list", "complite", "count", "date_complite",
    )

    MLEXCELO_CSV_NAME_COLUMNS: tuple[str, ...] = (
        "mr_list", "order", "detail_num", "detail_name",
        "oper_num", "operation_name", "t_install", "t_single", "t_sum",
    )

    if DOS_FOLDER == X_DOS_FOLDER:
        DOS_MOVING: bool = False
        DOS_STORED: bool = False

class ExcelScriptConfig(BaseSettings):
    EXCEL_NAME_PDO: str = "PDO_Base"
    EXCEL_NAME_MP: str = "MLEXCEL"
    EXCEL_NAME_MTOIL: str = "MTOIL"

    OPTIONS_EX_MP: dict[str, Any] = {
        "data": None,
        "data_format": [
            Formater.format_int,
            Formater.text_center,
            Formater.text_basic,
            Formater.text_basic,
            Formater.format_int,
            Formater.format_number,
            Formater.format_number,
            Formater.text_basic,
            Formater.format_number,
        ],
        "headers": (
            "Маршрутный лист",
            "Заказ",
            "№ детали",
            "Название детали",
            "Количество",
            "Норма расхода на ед",
            "Норм/часы",
            "Материал",
            "Масса детали",
        ),
        "autofilter": False,
        "pivot": False,

        "columns_wight": (17, 8, 22, 17, 10, 18, 11, 25, 12),
        "headers_format": [Formater.text_center,],
        "headers_height": 15,
        "start_row": 0,
        "start_column": 0,
        "end_row": None,
        "end_column": None,
    }

    BD_COLUMN_MP: tuple[str, ...] = (
        "mr_list",
        "order",
        "detail_num",
        "detail_name",
        "count",
        "mass_metal",
        "w_hours",
        "material",
        "mass_detail",
    )

    OPTIONS_EX_MTOIL: dict[str, Any] = {
        "data": None,
        "data_format": [
            Formater.text_basic,
            Formater.text_center,
            Formater.text_basic,
            Formater.text_basic,
            Formater.text_basic,
            Formater.text_basic,
            Formater.text_basic,
            Formater.format_number,
            Formater.format_int,
            Formater.format_int,
            Formater.format_number,
        ],
        "headers": (
            "Маршрутный лист",
            "Заказ",
            "№ детали",
            "Название детали",
            "Материал",
            "Профиль заготовки",
            "Профиль",
            "Норма расхода на ед",
            "Деталей из заготовки",
            "Размер партии",
            "Расход на партию",
        ),
        "autofilter": True,
        "pivot": True,

        "columns_wight": [13, 7, 23, 15, 22, 14, 11, 14, 13, 12, 12],
        "headers_format": [Formater.text_center,],
        "headers_height": 41,
        "start_row": 0,
        "start_column": 0,
        "end_row": None,
        "end_column": None,
    }

    BD_COLUMN_MTOIL: tuple[str, ...] = (
        "mr_list",
        "order",
        "detail_num",
        "detail_name",
        "material",
        "profile_full",
        "profile",
        "mass_metal",
        "det_in_workpiece",
        "count",
    )

    OPTIONS_PDO_ORDER: dict[str, Any] = {
        "data": None,
        "data_format": [
            Formater.text_center,
            Formater.format_int,
            Formater.format_number,
            Formater.format_int,
            Formater.format_number,
            Formater.format_procent,
        ],
        "headers": (
            "Заказ",
            "Всего деталей шт.",
            "Всего н/ч",
            "Сделано деталей шт.",
            "Сделано н/ч",
            "Выполнено, %"
        ),
        "autofilter": True,
        "pivot": True,
        "columns_wight": (7, 14, 12, 15, 14, 11),
        "headers_format": [Formater.text_center,],
        "headers_height": 40,
        "start_row": 0,
        "start_column": 0,
        "end_row": None,
        "end_column": None,
    }

    OPTIONS_PDO_MR_LIST: dict[str, Any] = {
            "data": None,
            "data_format": [
                Formater.text_center,
                Formater.text_basic,
                Formater.format_number,
                Formater.text_basic,
                Formater.format_int,
                Formater.format_date,
                Formater.text_center,
                Formater.format_date,
                Formater.text_basic,
                Formater.format_number,
                Formater.format_number,
                Formater.text_basic,
                Formater.text_basic,
                Formater.text_basic,
                Formater.format_int,
            ],
            "headers": (
                "Заказ",
                "Мр_лист",
                "Норм-часы",
                "№ детали",
                "Количество",
                "Дата запуска",
                "Тип дачи",
                "Дата сдачи",
                "Название детали",
                "Расход металла на ед",
                "Масса детали",
                "Материал",
                "Профиль заготовки",
                "Профиль",
                "Дет. из заготовки",
            ),
            "autofilter": True,
            "pivot": True,
            "columns_wight": (7, 9, 7, 22, 12, 11, 8, 10, 20, 15, 10, 23, 18, 12, 13),
            "headers_format": [Formater.text_center,],
            "headers_height": 37,
            "start_row": 0,
            "start_column": 0,
            "end_row": None,
            "end_column": None,
    }

    OPTIONS_PDO_OPERATIONS: dict[str, Any] = {
            "data": None,
            "data_format": [
                Formater.text_basic,
                Formater.format_int,
                Formater.text_basic,
                Formater.format_number,
                Formater.format_number,
            ],
            "headers": (
                "№ детали",
                "№ операции",
                "Назв. операции",
                "Время настройки",
                "Время изготовления"
            ),
            "autofilter": True,
            "pivot": True,
            "columns_wight": (32, 13, 14, 12, 12),
            "headers_format": [Formater.text_center,],
            "headers_height": 30,
            "start_row": 0,
            "start_column": 0,
            "end_row": None,
            "end_column": None,
    }

    OPTIONS_PDO_DETAILS: dict[str, Any] = {
            "data": None,
            "data_format": [
                Formater.text_basic,
                Formater.text_basic,
                Formater.text_basic,
                Formater.text_basic,
                Formater.format_int,
                Formater.format_number,
                Formater.format_number,
            ],
            "headers": (
                "№ детали",
                "Назв. детали",
                "Материал",
                "Профиль",
                "Дет. из заготов.",
                "Металла на ед.",
                "Масса детали",
            ),
            "autofilter": True,
            "pivot": True,
            "columns_wight": (32, 13, 25, 19, 10, 10, 10),
            "headers_format": [Formater.text_center,],
            "headers_height": 30,
            "start_row": 0,
            "start_column": 0,
            "end_row": None,
            "end_column": None,
    }

    # BD_COLUMN_PDO = ()
    SAVE_PATHS_PDO: tuple[Path, ...] = (
        Path(r"X:\Для ПДО\Петлицкий"),
        Path(r"D:\Project\Explore\Базы"),
        Path(r"D:\Project\PDO_project"),
    )
    SAVE_PATHS_MP: tuple[Path, ...] = (
        Path(r"D:\Project\PDO_project"),
    )
    SAVE_PATHS_MTOIL: tuple[Path, ...] = (
        Path(r"D:\Project\PDO_project"),
    )


settings = ProjectSettings()
engine = create_engine(url=settings.DATABASE)
session = sessionmaker(bind=engine)
excel_setting = ExcelScriptConfig()
