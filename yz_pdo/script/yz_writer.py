from yz_pdo.config import session, settings, engine
from time import time
from yz_pdo.src import (
    PotrGetter,
    PotrebHandler,
    DBWriter,
    Base,
)


__all__ = [
    "script_yz_write_potr"
]


def script_yz_write_potr():
    potreb_files = PotrGetter(settings.FOLDER_INPUT, settings.FILE_TYPE)
    port_files = potreb_files.files_dict
    for files in port_files.values():
        file_mapped = {
            "pr1_file": files[".pr1"],
            "se1_file": files[".se1"],
            "sp1_file": files[".sp1"]
        }
        potreb_handler = PotrebHandler(**file_mapped)

        Base.metadata.create_all(engine)
        time_t = time()
        set_yz = set()
        with DBWriter(session) as db_writer:
            for part in potreb_handler.yz_include:
                if part["master_name"] not in set_yz:
                    db_writer.delete_yz_parts(part["master_name"])
                    # db_writer.delete_table_parts(part[1])
                set_yz.add(part["master_name"])
                db_writer.delete_detail_parts(part["slave_name"])
                db_writer.delete_detail_parts(part["master_name"])
                db_writer.delete_table_parts(part["slave_name"])
                db_writer.delete_table_parts(part["master_name"])
                db_writer.add_yz(**part)
            for detail in potreb_handler.detail_include:
                db_writer.add_detail(**detail)
            for table in potreb_handler.table_include:
                db_writer.add_table(**table)
        print(time() - time_t)
