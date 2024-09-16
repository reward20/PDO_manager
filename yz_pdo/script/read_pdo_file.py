from yz_pdo.src import PdoGetter, DosHandler
from yz_pdo.config import settings


def script_pdo_read():
    pdo_getter = PdoGetter(settings.X_DOS_FOLDER, settings.DOS_FILES_SUFFIX)
    files = pdo_getter.files_dict
    dos_reader = DosHandler(**files)
    for f, i in enumerate(dos_reader._read_ml_file(), start=1):
        for k, v in i.items():
            print(k,": ", v)
        break