from typing import Type, Union
from shutil import copy
from src.files_getter import FilesGetter
from src.dos_handler.ml_readers import (
    MlexcelOReader,
    MlexcelReader,
    SkladReader,
)
from src.dos_handler.db_writers import (
    MleDb,
    MleODb,
    SkldDb,
)

from src.models import Mlexcel_model, Operation
from src.dos_handler.files_recopy import RecopyFile
from config import settings


class DataBaseDosCreate(object):

    @staticmethod
    def _get_reader(name: str) -> Union[
        Type[MlexcelOReader],
        Type[MlexcelReader],
        Type[SkladReader],
    ]:
        reader_dict: dict[
            str,
            Type[MlexcelReader] | Type[MlexcelOReader] | Type[SkladReader]
        ] = {
            settings.MLE: MlexcelReader,
            settings.MLE_O: MlexcelOReader,
            settings.SKLD: SkladReader,
        }

        try:
            return reader_dict[name]
        except ValueError:
            raise ValueError(f"{name} for file_reader not supported")

    @staticmethod
    def _get_db_writer(name: str) -> Union[
        Type[MleDb],
        Type[MleODb],
        Type[SkldDb],
    ]:
        db_writer_dict: dict[
            str,
            Type[MleDb] | Type[MleODb] | Type[SkldDb]
        ] = {
            settings.MLE: MleDb,
            settings.MLE_O: MleODb,
            settings.SKLD: SkldDb,
        }
        try:
            return db_writer_dict[name]
        except KeyError:
            raise ValueError(f"{name} for db_writer not supproted")

    @staticmethod
    def _get_db_model(name: str) -> Union[
        Type[Mlexcel_model],
        Type[Operation],
    ]:
        db_model: dict[
            str,
            Type[Mlexcel_model] | Type[Operation]
        ] = {
            settings.MLE: Mlexcel_model,
            settings.MLE_O: Operation,
            settings.SKLD: Mlexcel_model,
        }
        try:
            return db_model[name]
        except KeyError:
            raise ValueError(f"{name} for db_models not support")

    @staticmethod
    def start():
        x_files = FilesGetter(
            path_dir=settings.X_DOS_FOLDER,
            suffix=settings.DOS_FILES_SUFFIX
        )

        dos_files = FilesGetter(
            path_dir=settings.DOS_FOLDER,
            suffix=settings.DOS_FILES_SUFFIX
        )

        # check if all files exist
        for name_file in settings.DOS_FILES_NAMES:
            x_files.get_file(name_file)

        for name_file in settings.DOS_FILES_NAMES:
            x_file = x_files.get_file(name_file)
            RecopyFile(check_file=x_file).recopy_dos_file()
            copy(x_file, settings.DOS_FOLDER / x_file.name)
            file = dos_files.get_file(name_file)
            reader = DataBaseDosCreate._get_reader(name_file)
            reader = reader(file)
            model = DataBaseDosCreate._get_db_model(name_file)
            db_writer = DataBaseDosCreate._get_db_writer(name_file)
            db_writer = db_writer(reader=reader, model=model)
            db_writer.rewrite_db()
