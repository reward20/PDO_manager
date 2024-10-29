from collections import defaultdict
from decimal import Decimal
import pandas as pd

from src import YzViewer
from src.models import MrList, Order
from .point_yz import YzPoint


__all__ = [
    "OrderReport",
]


class OrderReport(YzViewer):

    def _get_mr_list(self, order: str) -> MrList:
        self.get_order_mrlist(order)

    def _get_order_detail(self, order: str, complite=False) -> dict[str, int]:

        order_detail = defaultdict(int)
        for mr_list in self.get_order_mrlist(order):
            if complite:
                if mr_list.complite == "D":
                    order_detail[mr_list.product_name] += mr_list.count
            else:
                order_detail[mr_list.product_name] += mr_list.count
        return order_detail

    def _houre_detail(self, order: str, complite=False):
        order_detail = defaultdict(int)
        result_houre = defaultdict(Decimal)
        for mr_list in self.get_order_mrlist(order):
            order_detail[mr_list.product_name] += mr_list.count
            result_houre[mr_list.product_name] += mr_list.w_hours

        for k, v in result_houre.items():
            result_houre[k] = round(v / order_detail[k], 3)

        return result_houre


    def _revision_dict(self, revison_dict: dict[str, int], yz_sk: list[str]) -> dict[str, int]:
        for yz in yz_sk:
            if yz in revison_dict.keys() and \
                   revison_dict.get(yz, 0) == 0:
                del revison_dict[yz]
        
    def _calc_dict(self, yz_det: dict[str, int], watch_dict: dict[str, int]) -> tuple[Decimal, Decimal]:
        list_procent = []
        for yz, count in watch_dict.items():
            list_procent.append( Decimal(yz_det[yz]-count) / Decimal(yz_det[yz]) )
        procent = round(Decimal(sum(list_procent) / len(list_procent))*100,2)
        return procent

    def _revision_detail_yz(self, yz_name: str,  w_detail: dict[str, int], c_detail: dict[str, int]) -> tuple[Decimal, Decimal]:
        # Детали в узлы
        all_yz_detail = self.collect_details(yz_name)
        work_detail_stat = all_yz_detail.copy()
        complite_detail_stat = all_yz_detail.copy()
        # Узлы входящие в мой узел
        yz_include = list([_yz for _yz , count in self.get_slave_parts(yz_name)])

        for det, det_count in all_yz_detail.items():
            count_work = w_detail.get(det, 0)
            count_comp = c_detail.get(det, 0)

            count_work = min(det_count, count_work)
            count_comp = min(det_count, count_work)

            work_detail_stat[det] -= count_work
            complite_detail_stat[det] -= count_comp

            w_detail[det] -= count_work
            c_detail[det] -= count_comp

        self._revision_dict(work_detail_stat, yz_include)
        self._revision_dict(complite_detail_stat, yz_include)
        
        work_proc = self._calc_dict(all_yz_detail, complite_detail_stat)
        ready_proc = self._calc_dict(all_yz_detail, work_detail_stat)

        return (work_proc, ready_proc)

    def _detail_complite(
        self,
        yz_name: str,
        yz_int: int,
        work_detail: dict[str, int],
        complite_detail: dict[str, int],
        num_pos: int,
    ) -> tuple[list, Decimal]:

        list_detail = []
        procent_detail = Decimal(0)
        all_detail = self.view_part_details(yz_name, yz_int)
        if not all_detail:
            return [], Decimal(0)


        for detail, _count in all_detail.items():
            _work_count = work_detail.get(detail, 0)
            _compl_count = complite_detail.get(detail, 0)

            if _work_count:
                if _work_count > _count:
                    work_detail[detail] -= _count
                    _work_count = _count
                else:
                    _work_count = work_detail[detail]
                    del work_detail[detail]

            if _compl_count:
                if _compl_count > _count:
                    complite_detail[detail] -= _count
                    _compl_count = _count
                else:
                    _compl_count = complite_detail[detail]
                    del complite_detail[detail]

            list_detail.append(
                (
                    num_pos, detail, _count, _work_count, _compl_count, 
                    round(Decimal(_work_count)/Decimal(_count)*Decimal(100.0), 2),
                    round(Decimal(_compl_count)/Decimal(_count)*Decimal(100.0), 2),
                )
            )
            procent_detail += (Decimal(_compl_count)/Decimal(_count)) * Decimal(100.0)
       
        return  list_detail, round((procent_detail / Decimal(len(list_detail))), 2)

    def _calculate_yz_order(
            self, yz_name: str, yz_int: int,
            work_detail: dict[str, int], complite_detail: dict[str, int],
            num_pos: int = 0) -> list[tuple]:

        yz_result: list = []
        _check_yz = list(self.view_part_yz(yz_name, yz_int).items())
        _procent_yz = []

        for _yz, _count in _check_yz:
            uz_res, _procent = self._calculate_yz_order(
                _yz, _count,
                work_detail,
                complite_detail,
                num_pos+1,
            )
            _procent_yz.append(_procent)
            yz_result.extend(uz_res)

        list_detail, detail_procent = self._detail_complite(
            yz_name, yz_int,
            work_detail,
            complite_detail,
            num_pos+1,
        )

        _procent_yz.append(detail_procent)
        result_procent = sum(_procent_yz) / len(_procent_yz)
        list_detail.extend(yz_result)
        yz_result = list_detail
        yz_result.insert(0, (num_pos, yz_name, yz_int, round(result_procent,2)))
        return (yz_result, result_procent)

    def order_report(self, order_name: str, yz_name: str, yz_int: int = 1):

        work_detail = self._get_order_detail(order_name)
        complite_detail = self._get_order_detail(order_name, complite=True)
        w_houre = self._houre_detail(order_name)

        return YzPoint(self._session_maker,
                yz_name,
                work_detail,
                complite_detail,
                count=yz_int,
                make_houre=w_houre
        )

        # list_result = self._calculate_yz_order(yz_name, yz_int, work_detail, complite_detail)
        # self._write_show_tree(list_result[0])
        # return list_result



        # all_yz_detail = self.collect_details(yz_name)
        # all_complite_detail = self._get_order_detail(order_name, complite=True)
        # all_detail = self._get_order_detail(order_name)

        # report_complite_detail = defaultdict(int)
        # need_to_word_detail = defaultdict(int)

        # for detail in all_yz_detail.keys():
        #     report_complite_detail[detail] = all_complite_detail.get(detail, 0)
        #     need_to_word_detail[detail] = all_detail.get(detail, 0)
        
        # report_complite_detail = pd.Series(report_complite_detail)
        # need_to_word_detail = pd.Series(need_to_word_detail)
        # all_yz_detail = pd.Series(all_yz_detail)

        # t = pd.concat(
        #     [all_yz_detail, need_to_word_detail, report_complite_detail],
        #     axis=1,
        # )
        # t.columns=["Требуется", "Запущено", 'Сделано']
        # t = t.sort_index()
        # t.to_excel(f"{order_name}_{yz_name}.xlsx")



