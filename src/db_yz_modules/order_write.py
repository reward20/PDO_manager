from typing import Any, Generator
from sqlalchemy import delete, select

from src.models import MrList, Order
from .db_connect import DbConnect


__all__ = [
    "OrderWriter",
    "OrderView",
]


class OrderExist(DbConnect):

    def exist_order(self, order_name: str) -> Order | None:

        exist_sub = (
            select(Order).
            where(Order.name == order_name).
            exists()
        )

        stmt_exist = (
            select(Order).
            where(exist_sub).
            where(Order.name == order_name)
        )

        result = self.session.scalar(stmt_exist)
        return result


class OrderCreate(OrderExist):

    def add_order(self, order_name: str) -> Order:
        result = self.exist_order(order_name)
        if result is not None:
            return result
        new_line = Order(name=order_name)
        self.session.add(new_line)
        return new_line


class OrderDelete(OrderExist):

    def delete_order(self, order_name: str) -> None:
        if self.exist_order(order_name) is None:
            raise ValueError(f"Order '{order_name} 'is not found in table '{Order.__tablename__}'")
        else:
            stmt_delete = (
                delete(Order).
                where(Order.name == order_name)
            )
            self.session.execute(stmt_delete)


class OrderView(OrderExist):

    def get_order(self, order_name) -> Order:
        result = self.exist_order(order_name)
        if result is None:
            raise ValueError(f"order '{order_name}' is not found in table '{Order.__tablename__}'")
        return result
    
    def get_order_mrlist(self, order_name: str) -> Generator[MrList, Any, Any]:
        order = self.get_order(order_name)
        for mr_list in order.mrlist:
            yield mr_list


class OrderWriter(OrderCreate, OrderDelete):
    pass
