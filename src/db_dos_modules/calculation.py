from collections import defaultdict
from typing import Any
from matplotlib.ticker import NullLocator
import pandas as pd
from io import BytesIO
from sqlalchemy import (
    select, or_
)
import locale
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np

from src.schemas import CalculationSchem
from src.models import MrList
from config import engine
from src.db_yz_modules import DBViewer


class CaclulationGraph(object):
    
    def __init__(self):
        self.line_type = ['dashed','solid', 'dashdot', 'dotted']
        self.dotted_style = ["o", "^", "p", "D"]
        self._dott_int = 0
        self._line_int = 0


    @property
    def dott_int(self):
        self.dott_int = self._dott_int + 1 
        return self._dott_int
    
    @dott_int.setter
    def dott_int(self, vall: int):
        if vall % len(self.dotted_style) == 0:
            self.line_int += 1
        self._dott_int = vall % len(self.dotted_style)
        return self._dott_int



    @property
    def line_int(self):
        return self._line_int

    @line_int.setter
    def line_int(self, vall: int):
        self._line_int = vall % len(self.line_type)
        return self._line_int

    def _get_data_plot(self, x: list[Any], y: list[Any]):
        if not len(x) == len(y):
            raise ValueError("data list dont have same len ")
        x = np.asarray(x)
        y = np.asarray(y)
        return x, y

    def _create_procent_graph(
            self,
            data: tuple[tuple[str, list, list], ...]
        ):
        fig = plt.figure(figsize = (5, 5), dpi=200)
        ax = fig.subplots()
        for order, x, y in data:
            params = {
                "markersize": 6,
                "linewidth": 1.5,
                "linestyle": self.line_type[self.line_int],
                "marker": self.dotted_style[self.dott_int],
                'label': order,
                "markerfacecolor": (1,1,1),
                "color": "black",
            }
            self._ploter(ax, x , y, params)

            ax.set_title("Выполнение заказов")
            ax.set_ylabel("Выполнено, %")
            ax.legend(handlelength=5, fontsize=6)
            ax.set_ylim([0,110])
            ax.tick_params(axis = "x", labelrotation = 45, labelsize = 7)
         
            ax.minorticks_on()
            ax.xaxis.set_minor_locator(NullLocator())
            ax.grid()
            ax.yaxis.grid(which = "major" , linewidth = 1, color = "black")
            ax.xaxis.grid(which = "major" , linewidth = 1, color = "black")
            ax.grid(which = "minor", linewidth = 0.6, color = "gray")
            ax.set_aspect(0.1)
        image = BytesIO()
        fig.savefig(image, format="png", dpi=200, bbox_inches='tight')
        fig.clf()
        image.seek(0)
        return image

    def _ploter(self, ax: plt.Axes, data1: np.asarray, data2: np.asarray, param_dict: dict):
        out, = ax.plot(data1, data2, **param_dict)
        return out
    
    def create_graphs(self, frame: pd.DataFrame):
        list_with_all = list()
        frame_grand = frame[frame["Тип"] == "Норм часов, ч."]
        frame_grand = frame_grand[["Месяц", "Заказ", "Процент выполнения"]]
        list_order = frame_grand["Заказ"].unique()
        list_order.sort()
        
        for order in list_order:
            temp_frame = frame_grand[frame_grand["Заказ"] == order]
            temp_frame = temp_frame.sort_values(by="Месяц")
            list_date = temp_frame["Месяц"].dt.strftime("%B %Y").to_list()
            list_value = temp_frame["Процент выполнения"].to_list()
            
            list_with_all.append((order, list_date, list_value))
        image = self._create_procent_graph(list_with_all)
        return image
        

class DbFrameCalculation(DBViewer):

    def _get_frame_orders_mr_list(self, orders: tuple[str, ...]) -> pd.DataFrame:
        with self as db:
            data = defaultdict(list)
            pd_Frame = pd.DataFrame()
            for order_name in orders:
                for mr_list in self.get_order_mrlist(order_name):
                    obj = CalculationSchem(
                        order_name=mr_list.order_name,
                        mr_list=mr_list.mr_list,
                        product=mr_list.product_name,
                        count=mr_list.count,
                        w_hours=mr_list.w_hours,
                        date_start=mr_list.date_start,
                        date_complite=mr_list.date_complite,
                        complite=mr_list.complite
                    )
                    
                    for name, val in obj.model_dump().items():
                        data[name].append(val)

            frame = pd.DataFrame.from_dict(data)
            pd_Frame = pd.concat([pd_Frame, frame])
            return pd_Frame

    def _validate_frame(self, data_frame: pd.DataFrame):
        data_frame["date_start"] = data_frame["date_start"].dt.to_period('M')
        data_frame["date_complite"] = data_frame["date_complite"].dt.to_period('M')
        
        def complite(line):
            if not line.loc["complite"] == "D":
                line.loc["date_complite"] = pd.NaT
            return line
        return data_frame.apply(complite, axis=1)

    def _frame_order(self, orders: tuple[str, ...]) -> pd.DataFrame:
        frame = self._get_frame_orders_mr_list(orders)
        frame = self._validate_frame(frame)
        return frame


class CalculateFrames(DbFrameCalculation):

    def _russian_name_month(self, int_month: int):
        locale.setlocale(locale.LC_ALL,"ru")
        month_list = []
        Perod_M = pd.Timestamp.now().to_period(freq="M") - int_month + 1
        for period in pd.period_range(start=Perod_M, periods=int_month, freq="M"):
            month_list.insert(0, (period, period.strftime("%B %Y")))
        return month_list

    def _caclculate_data(self, frame: pd.DataFrame, int_month: int) -> list:

        data_dict = defaultdict(list)

        def _calculate_unique_name(
                order: str,
                month: pd.Period,
                month_name: str,
                temp_frame: pd.DataFrame,
            ):

            result_dict = dict()
            result_dict["order"] = order
            result_dict["month"] = month_name
            result_dict["types_op"] = "Наименований, шт"
            result_dict["in_work"] = (
                temp_frame[temp_frame["date_start"] == month]\
                ["product"].
                unique().
                size
            )

            result_dict["full_in_work"] = (
                temp_frame[temp_frame["date_start"] <= month]\
                ["product"].
                unique().
                size
            )

            result_dict["pass_the_month"] = (
                temp_frame[temp_frame["date_complite"] == month]\
                ["product"].
                unique().
                size
            )

            result_dict["full_pass"] = (
                temp_frame[temp_frame["date_complite"] <= month]\
                ["product"].
                unique().
                size
            )

            full_in_work = (
                temp_frame[temp_frame["date_start"] <= first_month]\
                ["product"].
                unique().
                size
            )

            result_dict["procent_ready"] = round(
                result_dict["full_pass"] / full_in_work * 100,
                2
            )
            return result_dict

        def _calculate_detail(
                order: str,
                month: pd.Period,
                month_name: str,
                temp_frame: pd.DataFrame,
            ):

            result_dict = dict()
            result_dict["order"] = order
            result_dict["month"] = month_name
            result_dict["types_op"] = "Деталей, шт"
            result_dict["in_work"] = (
                temp_frame[temp_frame["date_start"] == month]\
                ["count"].
                sum()
            )

            result_dict["full_in_work"] = (
                temp_frame[temp_frame["date_start"] <= month]\
                ["count"].
                sum()
            )

            result_dict["pass_the_month"] = (
                temp_frame[temp_frame["date_complite"] == month]\
                ["count"].
                sum()
            )

            result_dict["full_pass"] = (
                temp_frame[temp_frame["date_complite"] <= month]\
                ["count"].
                sum()
            )

            full_in_work = (
                temp_frame[temp_frame["date_start"] <= first_month]\
                ["count"].
                sum()
            )


            result_dict["procent_ready"] = round(
                result_dict["full_pass"] / full_in_work * 100,
                2
            )
            return result_dict

        def _calculate_w_howrs(
                order: str,
                month: pd.Period,
                month_name: str,
                temp_frame: pd.DataFrame,
            ):

            result_dict = dict()
            result_dict["order"] = order
            result_dict["month"] = month_name
            result_dict["types_op"] = "Норм часов, ч."
            result_dict["in_work"] = round(
                (
                temp_frame[temp_frame["date_start"] == month]\
                ["w_hours"].
                sum()
                ),
                3
            )

            result_dict["full_in_work"] = round(
                (
                temp_frame[temp_frame["date_start"] <= month]\
                ["w_hours"].
                sum()
                ),
                3,
            )

            result_dict["pass_the_month"] = round(
                (
                temp_frame[temp_frame["date_complite"] == month]\
                ["w_hours"].
                sum()
                ),
                3,
            )

            result_dict["full_pass"] = round(
                (
                temp_frame[temp_frame["date_complite"] <= month]\
                ["w_hours"].
                sum()
                ),
                3,
            )

            
            full_in_work = (
                temp_frame[temp_frame["date_start"] <= first_month]\
                ["w_hours"].
                sum()
            )

            result_dict["procent_ready"] = round(
                result_dict["full_pass"] / full_in_work * 100,
                2
            )
            return result_dict

        def _add_to_dict( *, order, month, types_op,
                in_work, full_in_work, pass_the_month,
                full_pass, procent_ready,
        ):
            nonlocal data_dict
            data_dict["Месяц"].append(month)
            data_dict["Заказ"].append(order)
            data_dict["Тип"].append(types_op)
            data_dict["Дозапуск"].append(in_work)
            data_dict["Полный запуск"].append(full_in_work)
            data_dict["Сдано за месяц"].append(pass_the_month)
            data_dict["Сдано всего"].append(full_pass)
            data_dict["Процент выполнения"].append(procent_ready)

        order_list = frame["order_name"].unique()
        order_list.sort()
        month_list = self._russian_name_month(int_month)
        first_month = month_list[0][0]
        for month, month_name in month_list:
            month_name = month.to_timestamp(freq="M")
            for order_name in order_list:
                temp_frame = frame[frame["order_name"] == order_name]

                if (temp_frame["date_start"] <= month).any() == False:
                    continue

                name_dict = _calculate_unique_name(
                    order_name, month, month_name, temp_frame,
                )
                detail_dict = _calculate_detail(
                    order_name, month, month_name, temp_frame,
                )
                hours_dict = _calculate_w_howrs(
                    order_name, month, month_name, temp_frame,
                )

                _add_to_dict(**name_dict)
                _add_to_dict(**detail_dict)
                _add_to_dict(**hours_dict)

        return pd.DataFrame.from_dict(data_dict)

    def _get_calculation_data(self, order: list[str], int_month: int = 6) -> pd.DataFrame:
        data=self._get_frame_orders_mr_list(order)
        data = self._validate_frame(data)
        return self._caclculate_data(data, int_month)
    