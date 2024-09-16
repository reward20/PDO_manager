from sqlalchemy import (
    select, delete, or_
)

from .product_writer import ProductCreate, ProductView


from yz_pdo.src.models import (
    YZ_include,
)


class YZExist(ProductCreate):

    def exist_yz(self, master_name: str, slave_name: str) -> YZ_include | None:

        master_part = self.exists_product(master_name)
        slave_part = self.exists_product(slave_name)

        if None in (master_part, slave_part):
            return None

        exist_sub = (
            select(YZ_include).
            where(YZ_include.master == master_part).
            where(YZ_include.slave == slave_part).
            exists()
        )

        stmt_exist = (
            select(YZ_include).
            where(exist_sub).
            where(YZ_include.master == master_part).
            where(YZ_include.slave == slave_part)
        )

        result = self.session.scalar(stmt_exist)
        return result


class YZCreate(YZExist):
    
    def add_yz(self, slave_name: str, master_name: str,  count: int):
        master_part = self.add_product(master_name)
        slave_part = self.add_product(slave_name)
        result = self.exist_yz(master_name, slave_name)
        if result is not None:
            raise ValueError(f"{master_name} - {slave_name} is exist in yz_include")
        yz_include = YZ_include(master=master_part, slave=slave_part, count=count)
        self.session.add(yz_include)
        return yz_include


class YZDelete(YZExist, ProductView):
    
    def delete_yz_parts(self, name_part):
        part = self.exists_product(name_part)
        stmt_delete = (
            delete(YZ_include).
            where(
                YZ_include.master == part,
            )
        )
        self.session.execute(stmt_delete)

    def delete_yz(self,  master_name, slave_name):
        result = self.exist_yz(master_name, slave_name)
        if result is None:
            raise ValueError(f"delete operation aborter: {master_name} - {slave_name} is not exist in {YZ_include.__tablename__}")
        stmt_delete = (
            delete(YZ_include).
            where(YZ_include.master_name == master_name).
            where(YZ_include.slave_name == slave_name)
        )
        self.session.execute(stmt_delete)


class YZView(YZExist, ProductView):

    def get_master_parts(self, name_part):
        result = self.get_product(name_part)
        for part in result.part_masters:
            yield part

    def get_slave_parts(self, name_part):
        result = self.get_product(name_part)
        for part in result.part_slaves:
            yield part

    def get_all_yz(self, name_part):
        part = self.get_product(name_part)
        stmt = (
            select(YZ_include).
            where(
                or_(
                    YZ_include.master == part,
                    YZ_include.slave == part
                )
            )
        )

        results = self.session.scalars(stmt)

        for result in results:
            yield (result.master_name, result.slave_name, result.count)

    def get_yz(self, name_part, slave_part) -> tuple[str]:
        result = self.exist_yz(name_part, slave_part)
        if result is not None:
            return result.master_name, result.slave_name, result.count
        else:
            raise ValueError(f"{name_part} - {slave_part} is not fount in {YZ_include.__tablename__}")


class YZWriter(YZCreate, YZDelete):
    pass
