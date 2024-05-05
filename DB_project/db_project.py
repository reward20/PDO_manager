from .db_manager import DB_manager
from src import Getter_files
from src import settings

__all__ = [
    "DB_progect",
]


class DB_progect(object):
    @staticmethod
    def start_project():
        files = Getter_files(
            path_dir=settings.X_DOS_FOLDER,
            suffix=settings.FILES_SUFFIX_DOS
        )

        manager = DB_manager(
            path_MLEXCEL=files.get_file("MLEXCEL"),
            path_MLEXCEL_O=files.get_file("MLEXCELO"),
            path_SKLAD=files.get_file("SKLAD"),
        )

        manager.create_db()
