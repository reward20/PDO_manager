import xlwings as xw
import pandas as pd
import numpy as np
import xlsxwriter as xlw
from DB_getter import DB_getter


class ML_ex(object):
    


if __name__ == "__main__":

    workbook = xlw.Workbook(r"Data/hello.xlsx")
    worksheet = workbook.add_worksheet("Sheet_1")
    worksheet.write(1, 1, "21412412424")
    workbook.close()

    # df = pd.DataFrame(
    #     data=np.random.rand(100, 5),
    #     columns=[f"Trial {i}" for i in range(1, 6)]
    #     )
    # xw.view(df)
