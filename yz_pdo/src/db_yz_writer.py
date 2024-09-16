from typing import Any, Generator
from sqlalchemy import (
    select, update, delete, or_
)

from sqlalchemy.orm import (
    Session,
    sessionmaker,
)

from .models import (
    Product,
    YZ_include,
    Detail_include,
    Table_include,
)


__all__ = [
    "DBWriter",
    "DBViewer"
]


class DbConnect(object):
    
    def __init__(self, session_maker: sessionmaker[Session]):
        self._session_maker = session_maker

    def __enter__(self):
        self.session = self._session_maker()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()
        

class ProductExist(DbConnect):

    def exists_product(self, name: str) -> Product | None:
        exist_sub = (
            select(Product).
            where(Product.name == name).
            exists()
        )

        stmt_exist = (
            select(Product).
            where(exist_sub).
            where(Product.name == name)
        )
        result = self.session.scalar(stmt_exist)
        return result


class ProductExist_old(DbConnect):

    def exists_product(self, name: str) -> Product | None:
        exist_sub = (
            select(Product).
            where(Product.name == name).
            exists()
        )

        stmt_exist = (
            select(Product).
            where(exist_sub).
            where(Product.name == name)
        )

        with self.session as session:
            result = session.scalar(stmt_exist)
            if result:
                return result
            return None


class ProductCreate(ProductExist):

    def add_product(self, name) -> Product:
        product = self.exists_product(name=name)
        if product is None:
            product = Product(name=name)
            # self.session.add(product)
        return product


class ProductCreate_old(ProductExist):

    def add_product(self, name) -> Product:
        product = self.exists_product(name=name)
        if product is None:
            product = Product(name=name)
            with self.session.begin():
                self.session.add(product)
        return product


class ProductDelete_old(ProductExist):

    def delete_product(self, name: str) -> None:
        if self.exists_product(name) is None:
            raise ValueError(f"{name} is not found in table 'product'")
        else:
            stmt_delete = (
                delete(Product).
                where(Product.name == name)
            )
            with self.session.begin():
                self.session.execute(stmt_delete)


class ProductDelete(ProductExist):

    def delete_product(self, name: str) -> None:
        if self.exists_product(name) is None:
            raise ValueError(f"{name} is not found in table 'product'")
        else:
            stmt_delete = (
                delete(Product).
                where(Product.name == name)
            )
            self.session.execute(stmt_delete)


class ProductView(ProductExist):

    def get_product(self, name) -> Product:
        result = self.exists_product(name)
        if result is None:
            raise ValueError(f"{name} is not found in table 'product'")
        return result


class ProductWriter(ProductCreate, ProductDelete):
    pass


class DetailExist(ProductExist):
        
    def exist_detail(self, part_name: str, detail_name: str) -> Detail_include | None:
        part = self.exists_product(part_name)
        detail = self.exists_product(detail_name)

        if None in (part, detail):
            return None

        exist_sub = (
            select(Detail_include).
            where(Detail_include.part == part).
            where(Detail_include.detail == detail).
            exists()
        )

        stmt_exist = (
            select(Detail_include).
            where(exist_sub).
            where(Detail_include.part == part).
            where(Detail_include.detail == detail)
        )
        result = self.session.scalar(stmt_exist)
        return result


class DetailExist_old(ProductCreate, ProductExist):
        
    def exist_detail(self, part_name: str, detail_name: str) -> Detail_include | None:
        part = self.exists_product(part_name)
        detail = self.exists_product(detail_name)

        if None in (part, detail):
            return None

        exist_sub = (
            select(Detail_include).
            where(Detail_include.part == part).
            where(Detail_include.detail == detail).
            exists()
        )

        stmt_exist = (
            select(Detail_include).
            where(exist_sub).
            where(Detail_include.part == part).
            where(Detail_include.detail == detail)
        )

        with self.session as session:
            result = session.scalar(stmt_exist)
            if result:
                return result
            return None


class DetailCreator(DetailExist):

    def _update_detail(self, part: Product, detail: Product, count: int):
        with self.session.begin():
            update_stmt = (
                update(Detail_include).
                where(Detail_include.part == part).
                where(Detail_include.part == detail).
                values(count=count)
                .returning(Detail_include)
            )
            result = self.session.scalar(update_stmt)
            return result

    def add_detail(self, name_detail, name_part, count):
        result = self.exist_detail(name_part, name_detail)
        if result is None:
            part = self.add_product(name_part)
            detail = self.add_product(name_detail)
            detail_include = Detail_include(part=part, detail=detail, count=count)
            self.session.add(detail_include)
            return detail_include
        else:
            raise ValueError (f"Detail: {name_part} - {name_detail} is exists")
        

class DetailCreator_old(DetailExist):

    def _update_detail(self, part: Product, detail: Product, count: int):
        with self.session.begin():
            update_stmt = (
                update(Detail_include).
                where(Detail_include.part == part).
                where(Detail_include.part == detail).
                values(count=count)
                .returning(Detail_include)
            )
            result = self.session.scalar(update_stmt)
            return result

    def add_detail(self, name_detail, name_part, count):
        result = self.exist_detail(name_part, name_detail)
        if result is None:
            part = self.add_product(name_part)
            detail = self.add_product(name_detail)
            detail_include = Detail_include(part=part, detail=detail, count=count)
            with self.session.begin():
                self.session.add(detail_include)
                return detail_include
        else:
            raise ValueError (f"Detail: {name_part} - {name_detail} is exists")


class DetailDelete_old(DetailExist, ProductView):
    
    def delete_detail_parts(self, name_part):
        result = self.exists_product(name_part)
        if result is not None:
            stmt_delete = (
                delete(Detail_include).
                where(Detail_include.part_name == name_part)
            )
            with self.session.begin():
                self.session.execute(stmt_delete)

    def delete_detail(self, name_part, name_detail):
        result = self.exist_detail(name_part, name_detail)
        if result is None:
            raise ValueError(f"delete operation aborter: {name_part} - {name_detail} is not exist in {Detail_include.__tablename__}")
        else:
            stmt_delete = (
                delete(Detail_include).
                where(Detail_include.part_name == name_part).
                where(Detail_include.detail_name == name_detail)
            )
            with self.session.begin():
                self.session.execute(stmt_delete)


class DetailDelete(DetailExist, ProductView):
    
    def delete_detail_parts(self, name_part):
        result = self.exists_product(name_part)
        if result is not None:
            stmt_delete = (
                delete(Detail_include).
                where(Detail_include.part_name == name_part)
            )
            self.session.execute(stmt_delete)

    def delete_detail(self, name_part, name_detail):
        result = self.exist_detail(name_part, name_detail)
        if result is None:
            raise ValueError(f"delete operation aborter: {name_part} - {name_detail} is not exist in {Detail_include.__tablename__}")
        else:
            stmt_delete = (
                delete(Detail_include).
                where(Detail_include.part_name == name_part).
                where(Detail_include.detail_name == name_detail)
            )
            self.session.execute(stmt_delete)


class DetailView(DetailExist, ProductView):

    def get_include_details(self, name_part: str):
        result = self.get_product(name_part)
        for res in result.details:
            yield res

    def get_parts_detail(self, name_detail: str):
        result = self.get_product(name_detail)
        for res in result.parts_for_details:
            yield res

    def get_all_detail(self, name_detail: str):
        detail = self.get_product(name_detail)
        stmt = (
            select(Detail_include).
            where(
                or_(
                    Detail_include.part == detail,
                    Detail_include.detail == detail
                )
            )
        )

        results = self.session.scalars(stmt)

        for result in results:
            yield (result.part_name, result.detail_name, result.count)

    def get_detail(self, name_part, name_detail) -> Detail_include:
        result = self.exist_detail(name_part, name_detail)
        if result is not None:
            return result.part_name, result.detail_name, result.count
        else:
            raise ValueError(f"{name_part} - {name_detail} is not fount in {Detail_include.__tablename__}")


class DetailWriter(DetailCreator, DetailDelete):
    pass


class YZExist_old(ProductCreate):

    def exist_yz(self, master_name: str, slave_name: str) -> YZ_include:

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

        with self.session as session:
            result = session.scalar(stmt_exist)
            if result:
                return result
            return None


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


class YZCreate_old(YZExist):
    
    def add_yz(self, slave_name: str, master_name: str,  count: int):
        master_part = self.add_product(master_name)
        slave_part = self.add_product(slave_name)
        result = self.exist_yz(master_name, slave_name)
        if result is not None:
            raise ValueError(f"{master_name} - {slave_name} is exist in yz_include")
        yz_include = YZ_include(master=master_part, slave=slave_part, count=count)
        with self.session.begin():
            self.session.add(yz_include)
        return yz_include


class YZDelete_old(YZExist, ProductView):
    
    def delete_yz_parts(self, name_part):
        part = self.exists_product(name_part)
        stmt_delete = (
            delete(YZ_include).
            where(
                YZ_include.master == part,
            )
        )
        with self.session.begin():
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
        with self.session.begin():
            self.session.execute(stmt_delete)


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


class TableExist_old(ProductView):

    def exist_table(self, name_part, name_table):
        part = self.exists_product(name_part)
        table = self.exists_product(name_table)

        if None in (part, table):
            return None

        stmt_exist = (
            select(Table_include).
            where(Table_include.part == part).
            where(Table_include.table == table)
        ).exists()

        stmt = (
            select(Table_include).
            where(stmt_exist).
            where(Table_include.part == part).
            where(Table_include.table == table)
        )
        with self.session.begin():
            return self.session.scalar(stmt)


class TableExist(ProductView):

    def exist_table(self, name_part, name_table):

        part = self.exists_product(name_part)
        table = self.exists_product(name_table)

        if None in (part, table):
            return None

        stmt_exist = (
            select(Table_include).
            where(Table_include.part == part).
            where(Table_include.table == table)
        ).exists()

        stmt = (
            select(Table_include).
            where(stmt_exist).
            where(Table_include.part == part).
            where(Table_include.table == table)
        )
        return self.session.scalar(stmt)


class TableCreate(ProductCreate, TableExist):

    def add_table(self, name_table, name_part, count):
        result = self.exist_table(name_part, name_table)
        if result is not None:
            raise ValueError (f"Table: {name_part} - {name_table} is exists")
        else:
            part = self.add_product(name_part)
            table = self.add_product(name_table)
            table_include = Table_include(part=part, table=table, count=count)
            self.session.add(table_include)
            return table_include


class TableCreate_old(ProductCreate, TableExist):

    def add_table(self, name_table, name_part, count):
        result = self.exist_table(name_part, name_table)
        if result is not None:
            raise ValueError (f"Table: {name_part} - {name_table} is exists")
        else:
            part = self.add_product(name_part)
            table = self.add_product(name_table)
            table_include = Table_include(part=part, table=table, count=count)
            with self.session.begin():
                self.session.add(table_include)
                return table_include


class TableView(TableExist):

    def get_parts_table(self, name_table):
        table = self.get_product(name_table)
        for part in table.parts_table:
            yield(part)

    def get_tables_include(self, name_part):
        part = self.get_product(name_part)
        for table in part.tables:
            yield(table)

    def get_table(self, name_part, name_table):
        result = self.exist_table(name_part, name_table)
        if result is None:
            raise ValueError (f"Table: {name_part} - {name_table} is exists")
        else:
            return result


class TableDelete(TableView):

    def delete_table(self, name_part, name_table):
        result = self.get_table(name_part, name_table)
        if result is not None:
            stmt_delete = (
                delete(Table_include).
                where(Table_include.part_name == name_part).
                where(Table_include.table_name == name_table)
            )
            self.session.execute(stmt_delete)

    
    def delete_table_parts(self, name_part):
        part = self.exists_product(name_part)
        if part is not None:
            stmt_delete = (
                delete(Table_include).
                where(Table_include.part == part)
            )
            self.session.execute(stmt_delete)


class TableDelete_old(TableView):

    def delete_table(self, name_part, name_table):
        result = self.get_table(name_part, name_table)
        if result is not None:
            stmt_delete = (
                delete(Table_include).
                where(Table_include.part_name == name_part).
                where(Table_include.table_name == name_table)
            )
            with self.session.begin():
                self.session.execute(stmt_delete)

    
    def delete_table_parts(self, name_part):
        part = self.exists_product(name_part)
        if part is not None:
            stmt_delete = (
                delete(Table_include).
                where(Table_include.part == part)
            )
            with self.session.begin():
                self.session.execute(stmt_delete)


class TableWriter(TableCreate, TableDelete):
    pass


class DBWriter(ProductWriter, YZWriter, DetailWriter, TableWriter):
    pass


class DBViewer(TableView, DetailView, YZView):
    pass

