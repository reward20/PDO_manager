from sqlalchemy import delete, select

from src.models import Materials
from .db_connect import DbConnect


__all__ = [
    "MaterialView",
    "MaterialWriter",
]


class MaterialExist(DbConnect):

    def exist_material(self, material_name: str) -> Materials | None:

        exist_sub = (
            select(Materials).
            where(Materials.name == material_name).
            exists()
        )

        stmt_exist = (
            select(Materials).
            where(exist_sub).
            where(Materials.name == material_name)
        )

        result = self.session.scalar(stmt_exist)
        return result


class MaterialCreate(MaterialExist):

    def add_material(self, material_name: str) -> Materials:
        result = self.exist_material(material_name)
        if result is not None:
            return result
        new_line = Materials(name=material_name)
        self.session.add(new_line)
        return new_line


class MaterialDelete(MaterialExist):

    def deleta_material(self, material_name: str) -> None:
        if self.exist_material(material_name) is None:
            raise ValueError(f"Material '{material_name} 'is not found in table '{Materials.__tablename__}'")
        else:
            stmt_delete = (
                delete(Materials).
                where(Materials.name == material_name)
            )
            self.session.execute(stmt_delete)


class MaterialView(MaterialExist):

    def get_material(self, material_name) -> Materials:
        result = self.exist_material(material_name)
        if result is None:
            raise ValueError(f"Material '{material_name}' is not found in table '{Materials.__tablename__}'")
        return result


class MaterialWriter(MaterialCreate, MaterialDelete):
    pass
