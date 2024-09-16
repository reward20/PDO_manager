from yz_pdo import script_yz_write_potr, script_pdo_read


# if __name__ == "__main__":
#     script_yz_write_potr()


# if __name__ == "__main__":
#     script_pdo_read()

from yz_pdo.config import settings, session
# from .yz_pdo.src.yz_viewer import YzViewer
from yz_pdo.src.yz_viewer import YzViewer

if __name__ == "__main__":
#     f_test = {"file": "i", "count": 10}
#     t = {}
#     t["file"] = f_test["file"]
#     t["count"] = f_test["count"]
#     f_test["file"] = "asdfsd"
#     f_test["count"] = "asdfsd"
#     print(t,f_test)

    # script_pdo_read()


    with YzViewer(session) as view:
        print(view.view_include_detail("ШАЙБА 7019-0397 ГОСТ 13438-68"))

