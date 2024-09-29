from yz_pdo.src import DosDbWriter
from yz_pdo.config import settings, session, engine
from yz_pdo.src import (
    Base,
)


def script_pdo_read():
    Base.metadata.create_all(engine)
    dos_writer = DosDbWriter(
        session_maker=session,
        path_dir=settings.X_DOS_FOLDER,
        suffix=settings.DOS_FILES_SUFFIX,
    )
    
    with dos_writer as writer:
        writer.write_dos_in_db()
