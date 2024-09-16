from pathlib import Path
from zipfile import (
    ZipFile,
    ZIP_DEFLATED,
)
from src.files_getter import FilesGetter
from collections import defaultdict
from collections.abc import Iterable   
from shutil import move

from sqlalchemy import create_engine

from config import settings, session
from src.handler_potreb import PotrebHandler
from src.models import Base
from src.yz_viewer import YzViewer

from src.db_yz_writer import (
    DBWriter,
    DBViewer,
)



from sqlalchemy import (
    create_engine,
)
from sqlalchemy.orm import(
    sessionmaker,
)

from time import time

from src.port_getter import PotrGetter



class PotrGetter_old(object):

    def __init__(self, path_object: Path):
        self._path = path_object
        self._files = defaultdict(dict)

    def update_files(self):
        folders = []
        folders.append(self._path.path_dir)
        while folders:
            self._path.path_dir = folders.pop(0)
            temp_dict = self._review_files()
            self._files.update(temp_dict)
            folders.extend(self._path.get_folders())

    def _review_files(self):
        temp_file_dict = defaultdict(dict)
        files = self._path.get_files()
        files = [(file.stem, file) for file in files]
        files = self._view_dublicates_name(files)

        for name, file in files:
            temp_file_dict[name][file.suffix.lower()] = file
        
        correct_file_dict =  self._check_suffix_files_dict(temp_file_dict)
        return correct_file_dict

    def _check_suffix_files_dict(self, check_dict: dict[dict[str, Path]]) -> dict[dict[str, Path]]:
        return_dict = defaultdict(dict)
        for name, dict_suffix in check_dict.items():
            dict_keys = dict_suffix.keys()
            for key_suffix in self._path.suffix:
                if key_suffix not in dict_keys:
                    break
            else:
                return_dict[name].update(check_dict[name])
        return return_dict

    def _view_dublicates_name(self, files: list[tuple[str, Path]]) -> list[tuple[str, Path]]:
        name_set = self._files.keys()
        new_files = []
        for name, file in files:
            name = self._check_name(name, name_set)
            new_files.append((name, file))
        return new_files

    def _check_name(self, name: str, set_list: set) -> str:
        if name not in set_list:
            return name
        i = 1
        while name+f"_{i}" in set_list:
            i += 1
        return name+f"_{i}"
    
    @property
    def file_getter(self) -> FilesGetter:
        return self._path
    
    @file_getter.setter
    def set_file_getter(self, path_object: FilesGetter):
        self._path = path_object
        self.update_files()

    @property
    def files_dict(self) -> dict[str, dict[str, Path]]:
        if not self._files:
            self.update_files()
        return self._files


class PotrebProcess(object):

    @staticmethod
    def main():
        
        files.ge


        pack_files = PotrebProcess._wrap_potreb(files)
        PotrebProcess._processing_file(pack_files)
        # PotrebProcess._ziping_file(pack_files)

    @staticmethod
    def _wrap_potreb(files: Iterable[Path]):
        wrap_dict = defaultdict(list)
        for file in files:
            wrap_dict[file.stem].append(file)
        for key, value in list(wrap_dict.items()):
            if len(value) != 3:
                del wrap_dict[key]
        return wrap_dict

    @staticmethod
    def _ziping_file(pack_file: dict[str, list[Path]]):
        for potr_name, files_list in pack_file.items():
            if Path(settings.FOLDER_OUTPUT/ f"{potr_name}.zip").exists():
                raise FileExistsError(f"{potr_name}.zip is exist")

            with ZipFile(
                file=settings.FOLDER_OUTPUT/ f"{potr_name}.zip",
                mode="w",
                compression= ZIP_DEFLATED,
                compresslevel=9,
                allowZip64=False,
                ) as zfile:
                for file in files_list:
                    zfile.write(file, arcname=file.name)
                    file.unlink()

    @staticmethod
    def _processing_file(pack_file: dict[str, list[Path]]):
        for list_file in pack_file.values():
            table_file = {file.suffix: file for file in list_file}

            PotrFileHandler.start_handler(
                SP1_file=table_file[".SP1"],
                PR1_file=table_file[".PR1"],
                SE1_file=table_file[".SE1"],
            )


if __name__ == "__main__":
    
    # engine = create_engine("sqlite+pysqlite:///test.db")
    # session = sessionmaker(engine)
    with YzViewer(session) as view:
        # list_t = [
        #     (2,"Galon", 1),
        #     (1,"Frion", 1),
        #     (0,"Neon", 1),
        #     (1,"Pion", 1),
        #     (0,"Neon", 1),
        #     (3,"Pion", 1),
        #     (2,"Neon", 1),
        #     (1,"Neon", 1),
        #     (0,"Neon", 1),
        # ]
        # t = view._calculate_possition_include(list_t)
        # t = view.collect_tables("МС7-1984Ф11.000.000")
        # view.view_tree_detail("МС7-1984Ф11.100.000")
        # view.view_tree_detail("МС7-1984Ф11.000.000")
        # view.view_include_detail("ПРУЖИНА 2.5*28*110 ОСТ 2Д81-5-73")
        print(view.collect_details("МС7-1984Ф11.851.000",1))

        # t = view.view_part_details("МС7-1984Ф11.100.000")
        # kt = defaultdict(int)
        # kt["МС7-1984Ф11.У"] += 5
        # import pandas as pd
        # # # t = pd.DataFrame.from_dict(data=t, orient="index").sort_index()
        # # # t.to_excel("МС7-1984Ф11.000.000.xlsx")
        # t = pd.DataFrame.from_dict(data=t, orient="index", columns = ["count"]).sort_index()
        # # t.to_excel("МС7-1984Ф11.000.000.xlsx")
        # for key, val in t.iterrows():
        #     print(f"|{key:>30}:{val["count"]:^5}|")
        # print(t.count())
        # print(t)


# ///////////////////////////////////////////////
    # with DBViewer(session_maker=session) as db_view:
    #     name = "Y4"
    #     parts = db_view.get_parts_table(name)
    #     for item in parts:
    #         print(item)
