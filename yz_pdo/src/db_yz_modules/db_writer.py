from .detail_writer import DetailWriter
from .yz_writer import YZWriter
from .table_writer import TableWriter
from .operation_writer import OperationWriter
from .mr_list_writer import MrListWriter

__all__ = [
    "DBWriter",
]


class DBWriter(MrListWriter, OperationWriter,
               YZWriter, DetailWriter, TableWriter):
    pass
