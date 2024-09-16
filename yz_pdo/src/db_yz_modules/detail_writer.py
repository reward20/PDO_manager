from sqlalchemy import (
    select, update, delete, or_
)

from .product_writer import ProductExist, ProductView

from yz_pdo.src.models import (
    Product,
    Detail_include,
)


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
