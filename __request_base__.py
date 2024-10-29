from pathlib import Path
import pandas as pd
import sys
from shutil import rmtree

from config import session
from src.db_yz_modules.db_viewer import DBViewer
from src.yz_viewer import YzViewer


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    with YzViewer(session) as view:
        # print(view.collect_tables("МС65А80Ф1-11.000.000"))
        data = view.collect_details("У372.503.000").items()
    #     pd.DataFrame(data).to_excel("32476.xlsx")
        f = 1
        for k, v in data:
            print(f"{f}|{k:<30}|{v:^5}|")
            f+=1

    # with DBViewer(session) as db:
    #     for i in db.get_operation("ЛИТЕЙНАЯ"):
    #         print(i.detail_name)
    

# if __name__ == "__main__":
#     from yz_pdo.config import session
#     order_report = OrderReport(session)
#     with order_report as writer:
#         t = writer.order_report("32110", "МС7-1984Ф11.000.000")

#     row = 0
#     with pd.ExcelWriter("32110.xlsx") as exc:
#         frame_1 = pd.Series(t.show_yz_info()).to_frame().transpose()
#         frame_1.to_excel(exc, startrow=row, index=False)
#         row += frame_1.shape[0]+2
#         frame_1 = pd.DataFrame(t.show_include_yz_info())
#         frame_1.to_excel(exc, startrow=row, index=False)
#         row += frame_1.shape[0]+2
#         frame_1 = pd.DataFrame(t._detail)
#         frame_1.to_excel(exc, startrow=row, index=False)
#         row += frame_1.shape[0]+2
#         for name, count in t.yz_include:
#             child = t.dict_include_yz[name]
#             frame_1 = pd.Series(child.show_yz_info()).to_frame().transpose()
#             frame_1.to_excel(exc, startrow=row, index=False)
#             row += frame_1.shape[0]+2
#             frame_1 = pd.DataFrame(child.show_include_yz_info())
#             frame_1.to_excel(exc, startrow=row, index=False)
#             row += frame_1.shape[0]+2
#             frame_1 = pd.DataFrame(child.show_all_detail())
#             frame_1.to_excel(exc, startrow=row, index=False)
#             row += frame_1.shape[0]+2