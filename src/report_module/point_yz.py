import pandas as pd
from collections import defaultdict
from decimal import Decimal

from src.yz_viewer import YzViewer
from sqlalchemy.orm import (
    Session,
    sessionmaker,
)


class YzPoint(YzViewer):

    def __init__(
            self,
            session_maker: sessionmaker[Session],
            name: str,
            detail_make: dict[str, int],
            detail_comp: dict[str, int],
            parent: object | None = None,
            count: int = 1,
            yz_queve: list[str] = [],
            make_houre: dict[str, float] = dict(),
            level: int = 0,
        ):
        super().__init__(session_maker)
        self.parent: YzPoint = parent
        self.name = name
        self.count = count
        self.yz_queve = yz_queve
        self.detail_make = detail_make
        self.detail_comp = detail_comp
        self.w_detail_houre = make_houre
        self.level = level

        self.title = ""
        self._detail: pd.DataFrame = self._calc_detail(detail_make, detail_comp)
        self.detail_count = self._detail["need"].sum()
        self.details_procent_work: Decimal = self._detail_procent_work()
        self.details_procent_complite: Decimal = self._detail_procent_complite()
        self.yz_include: list[tuple[str, int]] = self._yz_get_calc()
        self.dict_include_yz: dict[str, YzPoint] = self._make_child_yz()
        self.yz_procent_work: Decimal = self._yz_calc_work()
        self.yz_procent_complite: Decimal = self._yz_calc_complite()
        self.yz_procent_assembly: Decimal = self._yz_calc_assembly()

        self.work_hours = self._w_houre()
        self.complite_hours = self._c_houre()



    def _review_dicts(self, detail_need: dict[str, int], detail_view: dict[str, int]):

        detail_result = defaultdict(int)
        for detail, count in detail_need.items():
            have_details = detail_view.get(detail , 0)
    
            if have_details == 0:
                detail_result[detail] += 0
                continue

            if count >= have_details:
                count = have_details
                del detail_view[detail]
            else:
                detail_view[detail] -= count
            detail_result[detail] += count
        return detail_result

    def _calc_detail(self, detail_make: dict[str, int], detail_comp: dict[str, int]) -> pd.DataFrame:
        with self as obj:
            detail_need = obj.view_part_details(self.name, self.count)
            detail_in_work = self._review_dicts(detail_need, detail_make)
            detail_ready = self._review_dicts(detail_need, detail_comp)

            dict_result = {
                "need": pd.Series(detail_need),
                "at_work": pd.Series(detail_in_work),
                "complite": pd.Series(detail_ready),
            }
            detail_table = pd.DataFrame(dict_result)
            detail_table = detail_table.fillna(0)
            detail_table = detail_table.reset_index()
            detail_table = detail_table.rename(columns={"index": "detail"})
            return detail_table

    def _detail_procent_work(self):
        # calculate procent detail in work
        with self as obj:

            list_procent = list()
            for num, row in self._detail.iterrows():
                list_procent.append(row["at_work"] / row["need"])
            if len(list_procent) == 0:
                return Decimal(0)
            else:
                procent = Decimal(sum(list_procent) / len(list_procent) * 100.0)
                procent = round(procent, 2)
                return procent

    def _detail_procent_complite(self):
        # calculate proccent detail ready
        list_procent = list()
        for num, row in self._detail.iterrows():
            list_procent.append(row["complite"] / row["need"])
        if len(list_procent) == 0:
            return Decimal(0)
        else:
            procent = Decimal(sum(list_procent) / len(list_procent) * 100.0)
            procent = round(procent, 2)
            return procent

    def _yz_get_calc(self) -> list[tuple[str, int]]:
        # get include yz_part
        with self as obj:
            dict_yz = obj.view_part_yz(self.name, self.count)
            list_yz = []

            if self.yz_queve:
                for name_yz in self.yz_queve:
                    if name_yz in dict_yz:
                        count = dict_yz.pop(name_yz)
                        list_yz.append((name_yz, count))

            for yz, count in dict_yz.items():
                list_yz.append((yz, count))
            return list_yz

    def _make_child_yz(self):
        # create child parts
        list_result = dict()
        for name, count in self.yz_include:
            list_result[name] = YzPoint(
                    self._session_maker,
                    name,
                    self.detail_make,
                    self.detail_comp,
                    self,
                    count,
                    level=self.level + 1,
                    make_houre = self.w_detail_houre 
            )
        return list_result

    def _yz_calc_work(self) -> Decimal:
        list_ready = list()
        for name, count in self.yz_include:
            child = self.dict_include_yz[name]
            list_ready.append(child.yz_procent_work)
        # for name, child in self.dict_include_yz.items():
        #     list_ready.append(child.yz_procent_work)
        list_ready.append(self.details_procent_work)
        if len(list_ready) == 0:
            return Decimal(0)
        else:
            ready = Decimal(sum(list_ready) / len(list_ready))
            return round(ready, 2)

    def _yz_calc_complite(self) -> Decimal:
        # calculate procent complite with child parts
        list_ready = list()
        for name, count in self.yz_include:
            child = self.dict_include_yz[name]
        # for name, child in self.dict_include_yz.items():
            list_ready.append(child.yz_procent_complite)
        list_ready.append(self.details_procent_complite)
        if len(list_ready) == 0:
            return Decimal(0)
        else:
            ready = Decimal(sum(list_ready) / len(list_ready))
            return round(ready, 2)

    def _yz_calc_assembly(self):
        # calculate procent assembly with child parts
        ready = self.detail_comp.get(self.name, 0)
        if ready:
            if self.count <= ready:
                self.detail_comp[self.name] -= self.count
                return self._make_assembly()
            else:
                del self.detail_comp[self.name]
                return round(Decimal(ready/self.count)*100, 2)
        else:
            list_ready = list()
            for name, count in self.yz_include:
                child = self.dict_include_yz[name]
            # for name, child in self.dict_include_yz.items():
                list_ready.append(child.yz_procent_assembly)
            list_ready.append(Decimal(0))
            ready = Decimal(sum(list_ready) / len(list_ready))
            return round(ready, 2)

    def _make_assembly(self):
        # if yz assembly, then all child assembly too
        self.yz_procent_work = round(Decimal(100.0), 2)
        self.yz_procent_assembly = round(Decimal(100.0), 2)
        self.yz_procent_complite = round(Decimal(100.0), 2)
        for child in self.dict_include_yz.values():
            child._make_assembly()
        return round(Decimal(100.0), 2)

    def _w_houre(self):
        sum_houre = 0
        for num, row in self._detail.iterrows():
            hour_one = self.w_detail_houre.get(row["detail"], 0.0)
            sum_houre += Decimal(row["at_work"] * hour_one)
        return sum_houre
    
    def _c_houre(self):
        sum_houre = 0
        for num, row in self._detail.iterrows():
            hour_one = self.w_detail_houre.get(row["detail"], 0.0)
            sum_houre += Decimal(row["complite"] * hour_one)
        return sum_houre

    def show_yz_info(self) -> dict[str, int]:

        self_info = {
            "yz_name": self.name,
            "yz_title": self.title,
            "procent_work": float(self.yz_procent_work),
            "procent_complite": float(self.yz_procent_complite),
            "procent_assembly": float(self.yz_procent_assembly)
        }
        return self_info

    def show_detail(self):
        return self._detail

    def show_all_detail(self) -> pd.DataFrame:
        return_detail = self._detail
        for name, count in self.yz_include:
            child = self.dict_include_yz[name]
            return_detail = pd.concat([return_detail, child.show_all_detail()]).groupby(by=["detail"]).sum()
            return_detail = return_detail.reset_index()
        return return_detail

    def show_include_yz_info(self):
        dict_yz_info = defaultdict(list)

        for name, count in self.yz_include:
            child = self.dict_include_yz[name]
            yz_info = child.show_yz_info()
            for key, value in yz_info.items():
                dict_yz_info[key].append(value)
        return dict_yz_info


        # for child_yz in self.dict_include_yz.

    def get_all_info(self):
        dict_result = defaultdict(list)
        dict_result["Наименование"].append(f"{'   '*self.level}|_{self.name}")
        dict_result["Название"].append(self.title)
        dict_result["Кол. шт."].append(self.count)
        dict_result["Деталей, шт."].append(self.detail_count)
        dict_result["% Запущено"].append(float(self.details_procent_work))
        dict_result["Норм_часов зап."].append(float(self.work_hours))
        dict_result["% Сдано"].append(float(self.details_procent_complite))
        dict_result["Норм_часов сдано."].append(float(self.complite_hours))
        dict_result["Готов к сборке, %"].append(float(self.yz_procent_complite))
        dict_result["Собран, %"].append(float(self.yz_procent_assembly))

        for child in self.dict_include_yz.values():
            for k, v in child.get_all_info().items():
                dict_result[k].extend(v)

        return dict_result


    # def show_yz_info(self, pos: int = 0):
    #     print(f"{' '*pos}|_{self.name}|{self.yz_procent_complite}|{self.yz_procent_assembly}")
    #     for child in self.dict_include_yz.values():
    #         print(f"{' '*(pos+1)}|_{child.name}|{child.yz_procent_complite}|{child.yz_procent_assembly}")

    def show_yz_info_widht(self, pos: int = 0):
        print(f"{'| '*pos}|_{self.name}|{self.yz_procent_complite}|{self.yz_procent_assembly}|")
        for child in self.dict_include_yz.values():
            child.show_yz_info_widht(pos=pos+1)


    
