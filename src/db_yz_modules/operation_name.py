from sqlalchemy import delete, select

from src.models import Operation_Name
from .db_connect import DbConnect


__all__ = [
    "OpNameView",
    "OpNameWriter",
]


class OpNameExist(DbConnect):

    def exist_op_name(self, op_name: str) -> Operation_Name | None:

        exist_sub = (
            select(Operation_Name).
            where(Operation_Name.name == op_name).
            exists()
        )

        stmt_exist = (
            select(Operation_Name).
            where(exist_sub).
            where(Operation_Name.name == op_name)
        )
        result = self.session.scalar(stmt_exist)
        return result


class OpNameCreate(OpNameExist):

    def add_op_name(self, op_name: str) -> Operation_Name:
        result = self.exist_op_name(op_name)
        if result is not None:
            return result
        result = Operation_Name(name=op_name)
        self.session.add(result)
        return result


class OpNameDelete(OpNameExist):

    def delete_op_name(self, op_name: str) -> None:
        if self.exist_op_name(op_name) is None:
            raise ValueError(f"Oper_name '{op_name} 'is not found in table '{Operation_Name.__tablename__}'")
        else:
            stmt_delete = (
                delete(Operation_Name).
                where(Operation_Name.name == op_name)
            )
            self.session.execute(stmt_delete)


class OpNameView(OpNameExist):

    def get_op_name(self, op_name) -> Operation_Name:
        result = self.exist_op_name(op_name)
        if result is None:
            raise ValueError(f"Profile '{op_name}' is not found in table '{Operation_Name.__tablename__}'")
        return result


class OpNameWriter(OpNameCreate, OpNameDelete):
    pass
