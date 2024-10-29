from decimal import Decimal
from sqlalchemy import (
    select, delete, update
)

from .db_connect import DbConnect
from .profile_writer import ProfilesCreate
from .material_writer import MaterialCreate

from src.models import (
    Product,
)


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


class ProductUpdate(DbConnect):

    def update_product(
            self,
            *,
            detail_num,
            detail_name,
            mass_metall,
            w_hours,
            material,
            mass_detail,
            profile_full,
            profile,
            det_in_workpiece,
        ) -> Product:
        stmt_update = (
            update(Product).
            where(Product.name == detail_num).
            values(
                title=detail_name,     
                h_work_one=w_hours,
                mass_metall=mass_metall,
                mass_detail=mass_detail,
                id_profile=profile.id,
                id_profile_full=profile_full.id,
                id_material=material.id_material,
                det_in_workpiece=det_in_workpiece
            )
        )
        self.session.execute(stmt_update)


class ProductCreate(ProductExist, ProductUpdate, ProfilesCreate, MaterialCreate):

    def add_product(self, name) -> Product:
        product = self.exists_product(name=name)
        if product is None:
            product = Product(name=name)
        return product
    
    def add_product_witdh(
            self,
            *,
            detail_num: str,
            detail_name: str,
            mass_metall: Decimal,
            w_hours: Decimal,
            material: str,
            mass_detail: Decimal,
            profile_full: str,
            profile: str,
            det_in_workpiece: int,
            ):
        product = self.exists_product(name=detail_num)
        new_profiles = self.add_profile(profile)
        new_profiles_full = self.add_profile(profile_full)
        new_material = self.add_material(material)
        if product is None:
            product = Product(
                name=detail_num,
                title=detail_name,     
                h_work_one=w_hours,
                mass_metall=mass_metall,
                mass_detail=mass_detail,
                profile=new_profiles,
                profile_full=new_profiles_full,
                material= new_material,
                det_in_workpiece=det_in_workpiece,
            )
        else:
            self.update_product(
                detail_num=detail_num,
                detail_name=detail_name,
                mass_metall=mass_metall,
                w_hours=w_hours,
                material=new_material,
                mass_detail=mass_detail,
                profile_full=new_profiles_full,
                profile=new_profiles,
                det_in_workpiece=det_in_workpiece,
            )
        return product
        

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

    def get_all_product(self):
        stmt_select = select(Product)
        return self.session.scalars(stmt_select)


    def get_product(self, name) -> Product:
        result = self.exists_product(name)
        if result is None:
            raise ValueError(f"{name} is not found in table 'product'")
        return result


class ProductWriter(ProductCreate, ProductDelete):
    pass
