from decimal import Decimal
from typing import Iterable
from sqlalchemy import delete, select

from src.models import Operation
from .product_writer import ProductExist, ProductCreate
from .operation_name import OpNameExist, OpNameCreate


__all__ = [
    "OperationView",
    "OperationWriter",
]


class OperationExist(ProductExist, OpNameExist):

    def exist_operation(self, product: str, operation_name: str) -> Operation | None:

        product = self.exists_product(product)
        operation_name = self.exist_op_name(operation_name)


        if None in (product, operation_name):
            return None

        exist_sub = (
            select(Operation).
            where(Operation.detail == product).
            where(Operation.operation == operation_name).
            exists()
        )

        stmt_exist = (
            select(Operation).
            where(exist_sub).
            where(Operation.detail == product).
            where(Operation.operation == operation_name)
        )

        result = self.session.scalar(stmt_exist)
        return result


class OperationCreate(ProductCreate, OpNameCreate, OperationExist):

    def add_operation(self, *, detail_num: str, operation_name: str, operation_num: str,
                      t_install: Decimal, t_single: Decimal) -> Operation:

        # result = self.exist_operation(detail_num, operation_name)
        # if result is not None:
        #     return result
        
        detail_num = self.add_product(detail_num)
        operation = self.add_op_name(operation_name)

        result = Operation(
            detail=detail_num,
            num_operation=operation_num,
            operation=operation,
            t_install=t_install,
            t_single=t_single,
        )
        self.session.add(result)
        return result


class OperationDelete(OperationExist):

    def delete_op_name(self, op_name: str) -> None:
        if self.exist_operation(op_name) is None:
            raise ValueError(f"Oper_name '{op_name} 'is not found in table '{Operation.__tablename__}'")
        else:
            stmt_delete = (
                delete(Operation).
                where(Operation.name == op_name)
            )
            self.session.execute(stmt_delete)


class OperationView(OperationExist):

    def get_operation(self, opetation_name: str) -> Iterable[Operation]:
        operation = self.exist_op_name(opetation_name)
        if operation is  None:
            raise ValueError(f"Operation '{opetation_name}' is not exist in table '{Operation.__tablename__}'")

        stmt_select = (
            select(Operation).
            where(Operation.operation == operation)
        )
        for line_result in self.session.scalars(stmt_select):
            yield line_result

    def get_all_operations(self):
        stmt_select = select(Operation)
        return self.session.scalars(stmt_select)



class OperationDelete(ProductExist):
    
    def clear_operation_table(self):
        stmt_delete = delete(Operation)
        self.session.execute(stmt_delete)

    def delete_operations(self, product: str) -> None:
        product = self.exists_product(product)
        if product is None:
            return None
        
        stmt_delete = (
            delete(Operation).
            where(Operation.detail==product)
        )
        self.session.executre(stmt_delete)



class OperationWriter(OperationDelete, OperationCreate):
    pass
