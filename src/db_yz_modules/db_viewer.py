from .detail_writer import DetailView
from .table_writer import TableView
from .yz_writer import YZView
from .operation_writer import OperationView
from .mr_list_writer import MrListView
from .order_write import OrderView

__all__ = [
    "DBViewer",
]

class DBViewer(TableView, DetailView, YZView,
               OperationView, MrListView, OrderView):
    pass
