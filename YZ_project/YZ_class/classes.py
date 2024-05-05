from decimal import Decimal, ROUND_HALF_UP
import decimal
from typing import List

__all__ = [
    "Detail",
    "Manager_DB"
    
]

class Manager_DB(object):
    ...


class Detail_DB(object):
    ...


class YZ_detail(object):
    def __init__(self, *, name: str, count: int, level: int = 1):
        self.name:str = name
        self.count: int = count
        self.level = level
        self.create_procent: Decimal = Decimal(value="0.00")
        self.in_process_count: int = 0
        self.w_hours: Decimal = Decimal(value="0.00") #.quantize(Decimal("1.000"), ROUND_HALF_UP)
        self.detail_list: List[Detail] = []
        self.yz_list: List[YZ_detail] = []


class Detail(object):
    
    def __init__(self, *, name: str, count: int):
        self.name:str = name
        self.count: int = count
        self.create_count: int = 0
        self.in_process_count: int = 0
        self.w_hours: Decimal = Decimal(value="0").quantize(Decimal("1.000"), ROUND_HALF_UP)

    def query_count(self, manager: Manager_DB):
        """create query for Manager_bd and get how more detail in process
        and how more detail is create
        """
        pass
