import pandas as pd
import sys

from config import session
from src.report_module import OrderReport


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    with OrderReport(session) as order:
        data = order.order_report("32110", "МС7-1984Ф11.000.000")
        data = data.get_all_info()
        # print(view.collect_tables("МС65А80Ф1-11.000.000"))
        # print(data.get_all_info())
        pd.DataFrame(data).to_excel("32110.xlsx")