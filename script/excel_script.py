from src.db_dos_modules.calculation import CaclulationGraph
from src.db_dos_modules.db_getter import PDOExcelDataHandler
from src.excel_writer import ExcelBookWriter
from config import session, excel_setting

__all__ = [
    "excel_base_create"
]


def excel_pdo_create():

    excel_data = PDOExcelDataHandler(session)

    pdo_excel = ExcelBookWriter(
        excel_setting.EXCEL_NAME_PDO,
        excel_setting.SAVE_PATHS_PDO
    )

    order_data, mr_list_data = excel_data.get_value_order_mr_list()

    pdo_excel.write_sheet_new(
        "Мр_листы",
        mr_list_data,
        options=excel_setting.OPTIONS_PDO_MR_LIST,
    )
    del mr_list_data

    pdo_excel.write_sheet_new(
        "Заказы",
        order_data,
        options=excel_setting.OPTIONS_PDO_ORDER,
    )
    del order_data

    pdo_excel.write_sheet_new(
        "Операции",
        excel_data.get_value_operation(),
        options=excel_setting.OPTIONS_PDO_OPERATIONS,
    )
    
    pdo_excel.write_sheet_new(
        "Детали",
        excel_data.get_value_detail(),
        options=excel_setting.OPTIONS_PDO_DETAILS,
    )
    frame_calculation = excel_data.get_frame_calculation()
    pdo_excel.write_sheet_new(
        "Калькул.",
        excel_data.get_value_by_frame(frame_calculation),
        options=excel_setting.OPTIONS_PDO_CALCULATION,
    )

    graph = CaclulationGraph()
    image = graph.create_graphs(frame_calculation)
    pdo_excel.insert_image(
        excel_setting.CALC_ROW_IMAGE, 
        excel_setting.CALC_COL_IMAGE,
        "Калькул.",
        image
    )
    pdo_excel.save_book()

def excel_mp_create():
    excel_data = PDOExcelDataHandler(session)

    mp_excel = ExcelBookWriter(
        excel_setting.EXCEL_NAME_MP,
        excel_setting.SAVE_PATHS_MP,
    )

    mp_data = excel_data.get_value_mp_ml()

    mp_excel.write_sheet_new(
        "MLEXCEL",
        mp_data,
        options=excel_setting.OPTIONS_MP_EXCEL,
    )

    mp_excel.save_book()

def excel_mtoil_create():
    
    excel_data = PDOExcelDataHandler(session)
    mtoil_excel = ExcelBookWriter(
        excel_setting.EXCEL_NAME_MTOIL,
        excel_setting.SAVE_PATHS_MTOIL,
    )

    mtoil_data = excel_data.get_value_mtoil()
    mtoil_excel.write_sheet_new(
        "Потребность",
        mtoil_data,
        options=excel_setting.OPTIONS_MTOIL_EXCEL,
    )
    mtoil_excel.save_book()

def excel_base_create():
    excel_pdo_create()
    excel_mp_create()
    excel_mtoil_create()
