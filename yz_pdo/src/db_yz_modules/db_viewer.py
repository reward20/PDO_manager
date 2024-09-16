from .detail_writer import DetailView
from .table_writer import TableView
from .yz_writer import YZView

__all__ = [
    "DBViewer",
]

class DBViewer(TableView, DetailView, YZView):
    pass
