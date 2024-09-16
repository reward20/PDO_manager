from datetime import date
from decimal import Decimal
from sqlalchemy import select

from yz_pdo.src.models import MrList
from .product_writer import ProductView, ProductCreate


class MrListExist(ProductView):

    def exist_mr_list(self, mr_list: str) -> MrList | None:

        exist_sub = (
            select(MrList).
            where(MrList.mr_list == mr_list).
            exists()
        )

        stmt_exist = (
            select(MrList).
            where(exist_sub).
            where(MrList.mr_list == mr_list)
        )

        result = self.session.scalar(stmt_exist)
        return result


class MrListUpdate():
    pass


class MrListCreate(MrListExist, ProductCreate):

    def add_mr_list(
        self,
        mr_list: str,
        order: str,
        detail_num: str,
        detail_name: str,
        count: int,
        w_hours: Decimal,
        date_start: date,
        mass_metall: Decimal,
        mass_detail: Decimal,
        profile: str,
        profile_full: str,
        det_in_workpiece: str,
        material: str,
        ):
        
        return yz_include


class MrListUpdate(MrListCreate):
    pass


class MrListView(MrListCreate):
    pass


class MrListDelete(MrListCreate):
    pass


class MrListWriter(MrListUpdate, MrListDelete):
    pass
