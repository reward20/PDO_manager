from datetime import date
from decimal import Decimal
from sqlalchemy import delete, select, update

from yz_pdo.src.models import MrList
from .product_writer import ProductCreate
from .order_write import OrderCreate
from .db_connect import DbConnect


class MrListExist(DbConnect):

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


class MrListUpdate(MrListExist):

    def update_mrlist_w_hours(self, *, mr_list: str, t_all: Decimal) -> MrList:
        if self.exist_mr_list(mr_list) is None:
            raise ValueError(f"mr_list {mr_list} is not found in {MrList.__tablename__}")

        update_stmt = (
            update(MrList).
            where(MrList.mr_list == mr_list).
            values(w_hours=t_all)
        )

        self.session.execute(update_stmt)

    def update_mrlist_complite(self, *, mr_list: str, complite: str, date_complite: date):

        if self.exist_mr_list(mr_list) is None:
            raise ValueError(f"mr_list {mr_list} is not found in {MrList.__tablename__}")

        update_stmt = (
            update(MrList).
            where(MrList.mr_list == mr_list).
            values(complite=complite, date_complite=date_complite)
        )
        self.session.execute(update_stmt)


class MrListCreate(MrListExist, ProductCreate, OrderCreate):

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
        # mrlist = self.exist_mr_list(mr_list)
        # if mrlist is not None:
        #     return mrlist

        product = self.add_product_witdh(
            detail_num=detail_num,
            detail_name=detail_name,
            w_hours=w_hours,
            mass_metall=mass_metall,
            mass_detail=mass_detail,
            profile=profile,
            profile_full=profile_full,
            det_in_workpiece=det_in_workpiece,
            material=material,
        )

        order_line = self.add_order(order)
        mr_list_line = MrList(
            mr_list=mr_list,
            order=order_line,
            product=product,
            count=count,
            date_start=date_start,
        )
        self.session.add(mr_list_line)
        self.session.flush()
        return mr_list_line
        

class MrListView(MrListCreate):
    
    def get_mrlist(self, mr_list: str) -> MrList:
        result = self.exist_mr_list(mr_list)
        if result is None:
            raise ValueError(f"mr_list '{mr_list}' is not found in table '{MrList.__tablename__}'")
        return result


class MrListDelete(MrListCreate):
    
    def clear_mrlist_table(self) -> None:
        stmt_delete = delete(MrList)
        self.session.execute(stmt_delete)

    def delete_mrlist(self, mr_list: str) -> None:
        if self.exist_order(mr_list) is None:
            raise ValueError(f"Order '{mr_list} 'is not found in table '{MrList.__tablename__}'")
        else:
            stmt_delete = (
                delete(MrList).
                where(MrList.mr_list == mr_list)
            )
            self.session.execute(stmt_delete)


class MrListWriter(MrListUpdate, MrListDelete):
    pass
