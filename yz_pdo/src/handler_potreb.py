from pathlib import Path
import re
from typing import Any, Generator, Iterable
from .schemas import PartValidate, DetailValidate, TableValidate

__all__ = [
    "PotrebHandler",
]

class ReadFile(object):

    @staticmethod
    def read_file(read_file: Path) -> Iterable[str]:
        with open(read_file, mode="r", encoding="cp866") as lines:
            for line in lines:
                yield line


class ReadFile_old(object):

    def __init__(self, file: Path):
        self.file = file

    def read_file(self) -> Iterable[str]:
        with open(self.file, mode="r", encoding="cp866") as lines:
            for line in lines:
                yield line


class ValidateLine(object):

    PATTERN_LIST = re.compile('"([^,]*)"')

    @classmethod
    def _line_handler(cls, line: str, pattern: re.Pattern | None = None) -> list[str]:
        if pattern is not None:
            return pattern.findall(line)
        else:
            return cls.PATTERN_LIST.findall(line)

    @staticmethod
    def _valid_count(line: str) -> int:
        line = line.strip()
        if line.isdigit():
            return int(line)
        else:
            raise ValueError(f"{line} is not digit")


class ReaderDetailInclude(ValidateLine, ReadFile):

    def __init__(self, pr1_file: Path):
        self.pr1_file = pr1_file

    """
        read PR1 file
    """
    PATTERN_TABLE = re.compile("^[12]$")
    DETAIL: int = 3
    TABLE: int = 4

    def get_details(self):
        for detail in self._get_detail_data_line(condition=self.DETAIL):
            yield detail[1:]

    def get_tables(self):
        for table in self._get_detail_data_line(condition=self.TABLE):
            yield table[2:]

    def _get_detail_data_line(self, condition: int) -> Generator[list[str|int], Any, Any]:
        check_count = False
        list_line = []
        count = 0
        for count_line, line in enumerate(self.read_file(self.pr1_file), start=1):

            if check_count:
                try:
                    count = self.__class__._valid_count(line)
                    list_line.append(count)
                    yield list_line
                except ValueError as e:
                    raise ValueError(f"in file line № {count_line}: {e}")
                check_count = False
            else:
                list_line = self.__class__._line_handler(line)
                if len(list_line) == condition:
                    is_table = bool(condition - 3)
                    if self.__class__._is_table(list_line) is is_table:
                        check_count = bool(list_line)

    @classmethod
    def _is_table(cls, line_list: list[str]) -> bool:
        return bool(cls.PATTERN_TABLE.search(line_list[1]))


class ReaderPartInclude(ValidateLine, ReadFile):
    """
        read SE1 file
    """

    def __init__(self, se1_file: Path):
        self.se1_file = se1_file


    def _get_part_data_line(self):
        check_count = False
        list_line = []

        for count_line, line in enumerate(self.read_file(self.se1_file), start=1):
            if check_count:
                try:
                    count = self._valid_count(line)
                    list_line.append(count)
                    yield list_line
                except ValueError as e:
                    raise ValueError(f"in file: {self.se1_file.absolute()} line № {count_line}: {e}")
                check_count = False
            else:
                list_line = self._line_handler(line)
                if len(list_line) == 2:
                    check_count = True


    def get_part_include(self):
        for line in self._get_part_data_line():
            yield line


class ReaderStandartRename(ValidateLine, ReadFile):
    """
        read SP1 file
    """
    def __init__(self, sp1_file: Path):
        self.sp1_file = sp1_file

    PATTERN_STANDART_LIST = re.compile('(?:"(.+)")')

    def get_standart_name(self):
        regit = re.compile(r"^У[0-9]+\.")
        for standart in self._get_standart_data_line():
            if regit.search(standart[0]):
                continue
            yield standart

    def _get_standart_data_line(self):
        unique_name = set()
        name_dict = {}
        check_name = False

        for count_line, line in enumerate(self.read_file(self.sp1_file), start=1):
            if check_name:
                try:
                    name = line.strip()
                    if name in unique_name:
                        raise ValueError(f"{list_line[0]} and {name_dict[name]} have the same name {name}")
                    unique_name.add(name)
                    name_dict[name] = list_line[0]
                    list_line.append(name)
                    yield list_line
                except ValueError as e:
                    raise ValueError(f"in file: {self.sp1_file.absolute()} line № {count_line}: {e}")
                check_name = False
            else:
                list_line = self.__class__._line_handler(line, self.PATTERN_STANDART_LIST)
                if list_line:
                    check_name = True


class PotrebHandler(
    ReaderPartInclude,
    ReaderDetailInclude,
    ReaderStandartRename,
    ):

    DETAIL_INDEX = 0
    # YZ_MAIN = 0
    # YZ_SLAVE = 1

    def __init__(self, *,  pr1_file: Path, se1_file: Path, sp1_file: Path):
        self.pr1_file = pr1_file
        self.se1_file = se1_file
        self.sp1_file = sp1_file

    @property
    def yz_include(self) -> Generator[dict[str, str | int], Any, Any]:
        for yz_main, yz_slave, count in self.get_part_include():
            yz_validate = PartValidate(
                master_name=yz_main,
                slave_name=yz_slave,
                count=count,
            )
            yield yz_validate.model_dump()

    @property
    def detail_include(self) -> Generator[dict[str, str | int], Any, Any]:
        standart_dict = self._get_standart_dict()
        clear_standart_detail = self._handler_standart(standart_dict)
        yz_set = self._get_yz_set()
        clear_yz_detail = self._clear_yz_in_detail(
            details=clear_standart_detail,
            yz_set=yz_set,
        )
        for detail in clear_yz_detail:
            detail = DetailValidate(
                name_detail=detail[0],
                name_part=detail[1],
                count=detail[2]
                )
            yield detail.model_dump()

    @property
    def table_include(self) -> Generator[dict[str, str | int], Any, Any]:
        for table in self.get_tables():
            # detail = TableValidate(
            #     name_detail=detail[0],
            #     name_part=detail[1],
            #     count=detail[2]
            #     )
            # yield detail.model_dump()
            table = TableValidate(
                name_table=table[0],
                name_part=table[1],
                count=table[2]
            )
            yield table.model_dump()

    def _get_standart_dict(self):
        standart_dict = {}
        for old_name, new_name in self.get_standart_name():
            standart_dict[old_name] = new_name
        return standart_dict
    
    def _handler_standart(self, standart_dict: dict[str, Any]):
        for detail_list in self.get_details():
            detail = detail_list[self.DETAIL_INDEX]
            if detail in standart_dict:
                detail_list[self.DETAIL_INDEX] = standart_dict.get(detail)
            yield detail_list

    def _get_yz_set(self):
        yz_set = set()
        for yz_list in self.yz_include:
            yz_set.add(yz_list["master_name"])
            yz_set.add(yz_list["slave_name"])
        return yz_set

    def _clear_yz_in_detail(
            self,
            *,
            details: list[list[str | int]],
            yz_set: set[str]
        ) -> Generator[list[str], Any, None]:
        
        for details_list in details:
            if details_list[self.DETAIL_INDEX] in yz_set:
                continue
            else:
                yield details_list
        

class ReaderDetailInclude_old(ValidateLine, ReadFile_old):
    """
        read PR1 file
    """
    PATTERN_TABLE = re.compile("^[12]$")
    DETAIL: int = 3
    TABLE: int = 4

    def get_details(self):
        for detail in self._get_data_line(condition=self.DETAIL):
            yield detail[1:]

    def get_tables(self):
        for table in self._get_data_line(condition=self.TABLE):
            yield table[2:]

    def _get_data_line(self, condition: int) -> Generator[list[str|int], Any, Any]:
        check_count = False
        list_line = []
        count = 0
        for count_line, line in enumerate(self.read_file(), start=1):

            if check_count:
                try:
                    count = self.__class__._valid_count(line)
                    list_line.append(count)
                    yield list_line
                except ValueError as e:
                    raise ValueError(f"in file line № {count_line}: {e}")
                check_count = False
            else:
                list_line = self.__class__._line_handler(line)
                if len(list_line) == condition:
                    is_table = bool(condition - 3)
                    if self.__class__._is_table(list_line) is is_table:
                        check_count = bool(list_line)

    @classmethod
    def _is_table(cls, line_list: list[str]) -> bool:
        return bool(cls.PATTERN_TABLE.search(line_list[1]))


class ReaderPartInclude_old(ValidateLine, ReadFile_old):
    """
        read SE1 file
    """


    def _get_data_line(self):
        check_count = False
        list_line = []

        for count_line, line in enumerate(self.read_file(), start=1):
            if check_count:
                try:
                    count = self.__class__._valid_count(line)
                    list_line.append(count)
                    yield list_line
                except ValueError as e:
                    raise ValueError(f"in file line № {count_line}: {e}")
                check_count = False
            else:
                list_line = self.__class__._line_handler(line)
                if len(list_line) == 2:
                    check_count = True


    def get_part_include(self):
        for line in self._get_data_line():
            yield line


class ReaderStandartRename_old(ValidateLine, ReadFile_old):
    """
        read SP1 file
    """


    PATTERN_LIST = re.compile('(?:"(.+)")')

    def get_standart_name(self):
        for standart in self._get_data_line():
            yield standart

    def _get_data_line(self):
        unique_name = set()
        name_dict = {}
        check_name = False

        for count_line, line in enumerate(self.read_file(), start=1):
            if check_name:
                try:
                    name = line.strip()
                    if name in unique_name:
                        raise ValueError(f"{list_line[0]} and {name_dict[name]} have the same name {name}")
                    unique_name.add(name)
                    name_dict[name] = list_line[0]
                    list_line.append(name)
                    yield list_line
                except ValueError as e:
                    raise ValueError(f"in file: {self.file.absolute()} line № {count_line}: {e}")
                check_name = False
            else:
                list_line = self.__class__._line_handler(line)
                if list_line:
                    check_name = True


class PotrebHandler_old(object):

    DETAIL_INDEX = 0
    YZ_MAIN = 0
    YZ_SLAVE = 1

    def __init__(self, *, yz_list: Iterable[list[str | int]],
                 detail_list: Iterable[list[str | int]],
                 standart_list: Iterable[list[str]],
                 tables_list: Iterable[list[str]]):
        self._yz_include = list(yz_list)
        self._detail_include = list(detail_list)
        self._standart = list(standart_list)
        self._tables = list(tables_list)

    def get_yz_include(self):
        for yz_main, yz_slave, count in self._yz_include:
            yield [yz_slave, yz_main, count]

    def get_detail_include(self):
        standart_dict = self._get_standart_dict()
        clear_standart_detail = self._handler_standart(
            details=self._detail_include,
            standart_dict=standart_dict
            )
        yz_set = self._get_yz_set()
        clear_yz_detail = self._clear_yz_in_detail(
            details=clear_standart_detail,
            yz_set=yz_set,
        )
        for detail in clear_yz_detail:
            yield detail

    def get_table_include(self):
        for table in self._tables:
            yield table

    def _get_standart_dict(self):
        standart_dict = {}
        for old_name, new_name in self._standart:
            standart_dict[old_name] = new_name
        return standart_dict
    
    def _handler_standart(self, *, details: list[list[str]], standart_dict: dict[str, Any]):
        for detail_list in details:
            detail = detail_list[self.DETAIL_INDEX]
            if detail in standart_dict:
                detail_list[self.DETAIL_INDEX] = standart_dict.get(detail)
            yield detail_list

    def _get_yz_set(self):
        yz_set = set()
        for yz_list in self._yz_include:
            yz_set.add(yz_list[self.YZ_MAIN])
            yz_set.add(yz_list[self.YZ_SLAVE])
        return yz_set

    def _clear_yz_in_detail(
            self,
            *,
            details: list[list[str | int]],
            yz_set: set[str]
        ) -> Generator[list[str], Any, None]:
        
        for details_list in details:
            if details_list[self.DETAIL_INDEX] in yz_set:
                continue
            else:
                yield details_list
        
 
