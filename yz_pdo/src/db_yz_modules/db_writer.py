from .product_writer import ProductWriter
from .detail_writer import DetailWriter
from .yz_writer import YZWriter
from .table_writer import TableWriter


__all__ = [
    "DBWriter",
]


class DBWriter(ProductWriter, YZWriter, DetailWriter, TableWriter):
    pass
