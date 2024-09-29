from yz_pdo import script_yz_write_potr, script_pdo_read
from time import time
from yz_pdo.src.report_module.point_yz import YzPoint
from yz_pdo.src.report_module import OrderReport


import pandas as pd

if __name__ == "__main__":
    now = time()
    script_pdo_read()
    # script_yz_write_potr()
    print(time() - now)


# if __name__ == "__main__":
#     from yz_pdo.config import session
#     order_report = OrderReport(session)
#     with order_report as writer:
#         t = writer.order_report("32110", "МС7-1984Ф11.000.000")
#     print(t.dict_include_yz.keys())
#     data = t.dict_include_yz["МС7-1984Ф11.100.000"].show_all_detail().sort_index()
#     data.to_excel("MS7.xlsx")

#     lsit = [
#         {"frik": 1, "frog": 2},
#         {"lirp": 3, "flor": 1}
#     ]

#     pd.Series(data)
#     print(pd.DataFrame.from_dict(lsit, orient='index'))


    # from yz_pdo.config import session
    # # # print([1,2,3][0:2])
    # order_report = OrderReport(session)
    # with order_report as writer:
    #     writer.order_report("32110", "МС7-1984Ф11.000.000")
            # print(i)
        # print("\n\n\n")
        # print(writer.view_part_details("ГФ1982.45.000*A"))

# from yz_pdo.config import settings, session
# from yz_pdo.src.yz_viewer import YzViewer

# if __name__ == "__main__":
#     with YzViewer(session) as view:
#         for i, v in enumerate(view.get_order_mrlist(32126)):
#             print(v.mr_list, v.product_name, v.count)
#             if i == 1000:
#                 break
                
            
