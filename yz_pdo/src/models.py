from sqlalchemy import (
    INTEGER,
    VARCHAR,
    CheckConstraint,
    ForeignKey,
    Date
)
from datetime import date
from decimal import Decimal

from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    relationship,
    Mapped,
    mapped_column,
)

from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy

__all__ = [
    "Base",
    "Product",
    "YZ_include",
    "Detail_include",
    "Table_include",
]


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(self) -> str:
        return self.__name__.lower()


class Product(Base):

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(128), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(VARCHAR(64), default="")
    h_work_one: Mapped[Decimal] = mapped_column(default=Decimal(0.000))
    mass_metall: Mapped[Decimal] = mapped_column(default=Decimal(0.000))
    mass_detail_one: Mapped[Decimal] = mapped_column(default=Decimal(0.000))
    id_profile: Mapped[int | None] = mapped_column(ForeignKey("profiles.id", name="fk_profile"))
    id_profile_full: Mapped[int | None] = mapped_column(ForeignKey("profiles.id", name="fk_profile_full"))
    id_material: Mapped[int | None] = mapped_column(ForeignKey("materials.id_material", name="fk_material"))
    det_in_workpiece: Mapped[int] = mapped_column(default=1)

    _profile: Mapped["Profiles"] = relationship(lazy="select", foreign_keys=id_profile, viewonly=True,)
    _profile_full: Mapped["Profiles"] = relationship(lazy="select", foreign_keys=id_profile_full, viewonly=True,)
    _material: Mapped["Materials"] = relationship(lazy="select", viewonly=True)

    profile: AssociationProxy[str] = association_proxy("_profile", "name")
    profile_full: AssociationProxy[str] = association_proxy("_profile_full", "name")
    material: AssociationProxy[str] = association_proxy("_material", "name")

    _parts_masters: Mapped[list["YZ_include"]] = relationship(
        "YZ_include",
        primaryjoin="YZ_include.slave_part_id == Product.id",
        lazy="select",
        viewonly=True,
    )
    _masters: AssociationProxy[list[str]] = association_proxy("_parts_masters", "master_name")
    _count_parts_masters: AssociationProxy[list[int]] = association_proxy("_parts_masters", "count")
    
    @property
    def part_masters(self):
        for master, master_count in zip(self._masters, self._count_parts_masters):
            yield master, master_count

    _parts_slave: Mapped[list["YZ_include"]] = relationship(
        "YZ_include",
        primaryjoin="YZ_include.master_part_id == Product.id",
        lazy="dynamic",
        viewonly=True,
    )
    _slaves: AssociationProxy[list[str]] = association_proxy("_parts_slave", "slave_name")
    _count_parts_slaves: AssociationProxy[list[int]] = association_proxy("_parts_slave", "count")

    @property
    def part_slaves(self):
        for slave, slave_count in zip(self._slaves, self._count_parts_slaves):
            yield slave, slave_count

    _details_include: Mapped[list["Detail_include"]] = relationship(
        "Detail_include",
        primaryjoin="Detail_include.part_id == Product.id",
        lazy="dynamic",
        viewonly=True,
    )
    _details: AssociationProxy[list[str]] = association_proxy("_details_include", "detail_name")
    _count_details: AssociationProxy[list[int]] = association_proxy("_details_include", "count")

    @property
    def details(self):
        for detail, detail_count in zip(self._details, self._count_details):
            yield detail, detail_count

    _parts_for_detail: Mapped[list["Detail_include"]] = relationship(
        "Detail_include",
        primaryjoin="Detail_include.detail_id == Product.id",
        lazy="dynamic",
        viewonly=True,
    )
    _part_for_detail: AssociationProxy[list[str]] = association_proxy("_parts_for_detail", "part_name")
    _count_part_for_detail: AssociationProxy[list[int]] = association_proxy("_parts_for_detail", "count")

    @property
    def parts_for_details(self):
        for master, detail_count in zip(self._part_for_detail, self._count_part_for_detail):
            yield master, detail_count

    _tables_include: Mapped[list["Table_include"]] = relationship(
        primaryjoin="Table_include.part_id == Product.id",
        lazy="dynamic",
        viewonly=True
    )
    _tables: AssociationProxy[list[str]] = association_proxy("_tables_include", "table_name")
    _count_tables: AssociationProxy[list[int]] = association_proxy("_tables_include", "count")

    @property
    def tables(self):
        for table, table_count in zip(self._tables, self._count_tables):
            yield table, table_count

    _parts_table: Mapped[list["Table_include"]] = relationship(
        primaryjoin="Table_include.table_id == Product.id",
        lazy="dynamic",
        viewonly=True
    )
    _master_tables: AssociationProxy[list[str]] = association_proxy("_parts_table", "part_name")
    _count_table_in_part: AssociationProxy[list[int]] = association_proxy("_parts_table", "count")
    
    @property
    def parts_table(self):
        for part, table_count in zip(self._master_tables, self._count_table_in_part):
            yield part, table_count

    def __init__(self, name: str):
        self.name = name


class Materials(Base):
    id_material: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(64), nullable=False, unique=True)
    product: Mapped[list[Product]] = relationship()


class Profiles(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(64), unique=True)
    product: Mapped[list[Product]] = relationship(
        primaryjoin= "Product.id_profile == Profiles.id or Product.id_profile_full == Profiles.id",
        viewonly=True
    )


class MrList(Base):
    mr_list: Mapped[str] = mapped_column(VARCHAR(8), primary_key=True)
    id_order: Mapped[int] = mapped_column(ForeignKey("order.id", name="mr_order"))
    id_product: Mapped[int] = mapped_column(ForeignKey("product.id", name="mr_product"))
    count: Mapped[int] = mapped_column()
    w_hours: Mapped[Decimal] = mapped_column(default=Decimal(0.000))
    date_start: Mapped[date] = mapped_column()
    complite: Mapped[str | None] = mapped_column(VARCHAR(1))
    date_complite: Mapped[date | None] = mapped_column()

    _product: Mapped[Product] = relationship(viewonly=True)
    _order: Mapped["Order"] = relationship(viewonly=True)

    product: AssociationProxy[str] = association_proxy("_product", "name")
    order: AssociationProxy[str] = association_proxy("_order", "order")


class Order(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(5))
    product: Mapped[list[MrList]] = relationship(viewonly=True)


class Operation(Base):
    id_detail: Mapped[int] = mapped_column(ForeignKey("product.id", name="oper_det"), primary_key=True)
    num_operation: Mapped[str] = mapped_column(VARCHAR(3), primary_key=True)
    id_operation: Mapped[int] = mapped_column(ForeignKey("operation_name.id", name="oper_name"))
    t_install: Mapped[Decimal] = mapped_column(default=Decimal(0.000))
    t_single: Mapped[Decimal] = mapped_column(default=Decimal(0.000))

    _detail: Mapped[Product] = relationship(viewonly=True)
    _name_operation: Mapped["Operation_Name"] = relationship(viewonly=True)

    detail: AssociationProxy[str] = association_proxy("_detail", "name")
    operation: AssociationProxy[str] = association_proxy("_name_operation", "name")


class Operation_Name(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(64), unique=True)
    detail: Mapped[list[Operation]] = relationship(viewonly=True)


class YZ_include(Base):
    master_part_id: Mapped[int] = mapped_column(ForeignKey("product.id"), primary_key=True)
    slave_part_id: Mapped[int] = mapped_column(ForeignKey("product.id"), primary_key=True)
    count: Mapped[int] = mapped_column(nullable=False)

    master: Mapped["Product"] = relationship("Product", foreign_keys=master_part_id)
    slave: Mapped["Product"] = relationship("Product", foreign_keys=slave_part_id)

    master_name: AssociationProxy[str] = association_proxy("master", "name")
    slave_name: AssociationProxy[str] = association_proxy("slave", "name")

    __table_args__ = (
        CheckConstraint("count > 0"),
    )


class Detail_include(Base):
    part_id: Mapped[int] = mapped_column(ForeignKey("product.id"), primary_key=True)
    detail_id: Mapped[int] = mapped_column(ForeignKey("product.id"), primary_key=True)
    count: Mapped[int] = mapped_column(nullable=False)

    part: Mapped["Product"] = relationship("Product", foreign_keys=part_id)
    detail: Mapped["Product"] = relationship("Product", foreign_keys=detail_id)

    part_name: AssociationProxy[str] = association_proxy("part", "name")
    detail_name: AssociationProxy[str] = association_proxy("detail", "name")

    __table_args__ = (
        CheckConstraint("count > 0"),
    )


class Table_include(Base):
    part_id: Mapped[int] = mapped_column(ForeignKey("product.id"), primary_key=True)
    table_id: Mapped[int] = mapped_column(ForeignKey("product.id"), primary_key=True)
    count: Mapped[int] = mapped_column(nullable=False)

    part: Mapped["Product"] = relationship("Product", foreign_keys=part_id)
    table: Mapped["Product"] = relationship("Product", foreign_keys=table_id)

    part_name: AssociationProxy[str] = association_proxy("part", "name")
    table_name: AssociationProxy[str] = association_proxy("table", "name")

    __table_args__ = (
        CheckConstraint("count > 0"),
    )
