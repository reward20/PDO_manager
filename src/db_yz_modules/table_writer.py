from sqlalchemy import (
    select, update, delete, or_
)

from .product_writer import ProductCreate, ProductView


from src.models import (
    Table_include,
)


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


class TableWriter(TableCreate, TableDelete):
    pass

