from zipfile import ZipFile, ZIP_DEFLATED

from src.port_getter import PdoGetter
from config import settings
from datetime import datetime
from shutil import move


class ZipStore(PdoGetter):

    def stored_into_zip(self):
        if not settings.DOS_STORED:
            return None

        file_name = datetime.today().strftime("%Y_%m_%d")
        for file_z in settings.DOS_ZIP_STORED.iterdir():
            if not (file_z.is_file() and file_z.suffix == ".zip"):
                continue
            if file_z.stem == file_name:
                file_z.unlink()
                break

        with ZipFile(
            file = f"{settings.DOS_ZIP_STORED / file_name}.zip",
            mode="a", compression=ZIP_DEFLATED,
            compresslevel=7,
        ) as zip_file:

            for file in self.files_dict.values():
                zip_file.write(file, f"{file.name}")
                file.unlink()
