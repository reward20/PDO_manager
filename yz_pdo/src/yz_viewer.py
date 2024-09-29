from .db_yz_modules.db_viewer import DBViewer
from collections import defaultdict

class YzViewer(DBViewer):

    def view_part_yz(self, name_part: str, count: int = 1) -> dict[str, int]:
        result = self.get_slave_parts(name_part)
        return self._calculate_result(result, count)

    def view_part_details(self, name_part: str, count: int = 1) -> dict[str, int]:
        result = self.get_include_details(name_part)
        return self._calculate_result(result, count)

    def view_part_tables(self, name_part: str, count: int = 1) -> dict[str, int]:
        result = self.get_tables_include(name_part)
        return self._calculate_result(result, count)

    def view_tree_yz(self, name_part: str, count_y: int = 1) -> tuple[tuple[int, str, int]]:
        list_tree_yz = self._view_tree_yz(name_part, count_y)
        self._show_tree(list_tree_yz)

    def _view_tree_yz(self, name_part: str, count_y: int = 1) -> tuple[tuple[int, str, int]]:
        self.get_product(name_part)
        list_tree_yz = []
        list_check_yz: list[tuple[int, str, int]] = []
        list_check_yz.append((0, name_part, count_y))
        while list_check_yz:
            check_yz = list_check_yz.pop(0)
            pos, check_name, count = check_yz
            list_tree_yz.append((check_yz))
            dict_result = self.view_part_yz(check_name, count)
            temp_list = []
            for name, count_yz in dict_result.items():
                temp_list.append((pos+1, name, count_yz))
            list_check_yz = temp_list + list_check_yz
        return list_tree_yz

    def view_tree_detail(self, name_part: str, count_d: int = 1) -> None:
        list_tree_yz = self._view_tree_yz(name_part=name_part, count_y=count_d)
        list_tree_detail = []
        for pos, yz, count in list_tree_yz:
            list_tree_detail.append((pos, yz, count))
            dict_detail = self.view_part_details(yz, count)
            for detail, count_dict in dict_detail.items():
                list_tree_detail.append((pos+1, detail, count_dict))
        self._show_tree(list_tree_detail)

    def view_tree_tables(self, name_part: str, count_t: int = 1) -> None:
        list_tree_yz = self._view_tree_yz(name_part=name_part, count_y=count_t)
        list_table_detail = []

        check_pos = -1
        temp_list = []
        for pos, yz, count in list_tree_yz:
            dict_detail = self.view_part_tables(yz, count)

            if check_pos >= pos:
                delete_width = min(len(list_table_detail), check_pos - pos + 1)
                for i in range(delete_width):
                    list_table_detail.pop()
            check_pos = pos
            list_table_detail.append((pos, yz, count))

            if dict_detail:
                for detail, count_dict in dict_detail.items():
                    list_table_detail.append((pos+1, detail, count_dict))
                temp_list.extend(list_table_detail)
                list_table_detail = []
        if not temp_list:
            print(f"In {name_part} tables not found")
        else:
            self._show_tree(temp_list)
        # return temp_list

    def view_include_yz(self, name_part: str) -> None:
        self._show_tree(self._view_include_yz(name_part))

    def _view_include_yz(self, name_part: str) -> tuple[tuple[int, str, int]]:
        self.get_product(name_part)
        complite_list = []
        list_all = [
            [
                [0, name_part, 1],
            ]
        ]

        while list_all:
            list_temp = list_all.pop(0)
            pos, check_part, count = list_temp[-1]
            master_list = list(self.get_master_parts(check_part))

            if not master_list:
                complite_list.append(list_temp)
                continue

            for master, count_d in master_list:
                add_list = list_temp.copy()
                add_list = self._correct_count(add_list, count_d)
                add_list.append([pos+1, master, 1])
                list_all.append(add_list)

        result = []
        for result_list in complite_list:
            result.extend(result_list)
        result.reverse()
        return self._calculate_possition_include(result)

    def view_include_detail(self, name_detail: str) -> tuple[tuple[int, str, int]]:
        master_list = list(self.get_parts_detail(name_detail))
        list_include_detail = self._collect_yz_and_detail(name_detail, master_list)
        self._show_tree(list_include_detail)
        # return list_include_detail

    def view_include_table(self, name_table: str) -> tuple[tuple[int, str, int]]:
        master_list = list(self.get_parts_table(name_table))
        list_include_detail = self._collect_yz_and_detail(name_table, master_list)
        self._show_tree(list_include_detail)
        # return list_include_detail
    
    def _collect_yz_and_detail(self, name_product: str, master_list: list[tuple[str, int]]) -> tuple[tuple[int, str, int]]:
        self.get_product(name_product)
        list_masters = []
        list_detail = []

        for master_name, count in master_list:
            list_masters.append(master_name)
            list_detail.append([0, name_product, count])

        del master_list
        list_include_detail = []

        for master_name in list_masters:
            list_yz = self._view_include_yz(master_name)
            temp_detail_list = self._input_detail(list_yz, list_detail.pop(0))
            list_include_detail.extend(temp_detail_list)
        return list_include_detail

    def collect_parts(self, name_part: str, count: int = 1) -> dict[str, int]:
        self.get_product(name_part)
        parts_collection = defaultdict(int)
        list_part = [(name_part, count), ]
        while list_part:
            check_part, count_y = list_part.pop(0)
            parts_collection[check_part] += count_y
            for yz, count_i in self.view_part_yz(check_part, count_y).items():
                list_part.append((yz, count_i))
        return parts_collection

    def collect_details(self, name_part: str, count: int = 1) -> dict[str, int]:
        detail_collection = defaultdict(int)
        parts_collection = self.collect_parts(name_part, count)
        for yz, count_yz in parts_collection.items():
            detail_collection[yz] += count_yz
            for detail, count_dt in self.view_part_details(yz, count_yz).items():
                detail_collection[detail] += count_dt
        return detail_collection 

    def collect_tables(self, name_part: str, count: int = 1) -> dict[str, int]:
        table_collection = defaultdict(int)
        parts_collection = self.collect_parts(name_part, count)
        for yz, count_yz in parts_collection.items():
            for table, count_tb in self.view_part_tables(yz, count_yz).items():
                table_collection[table] += count_tb
        return table_collection

    @staticmethod
    def _input_detail(list_yz: list[tuple[int, str, int]], detail: list[int, str, int]):

        def input_detail() -> None:
            nonlocal pos
            nonlocal count_yz
            nonlocal detail
            nonlocal list_detail
            detail_inp = detail.copy()
            detail_inp[2] = detail_inp[2] * count_yz
            detail_inp[0] = pos + 1
            list_detail.append(tuple(detail_inp))
        
        count = False
        list_detail = []
        for yz in list_yz:
            if yz[0] == 0:
                if count:
                    input_detail()
                count = True
            pos = yz[0]
            count_yz = yz[2]
            list_detail.append(yz)
        else:
            input_detail()

        return list_detail

    @staticmethod
    def _calculate_possition_include(result: list[tuple[int, str, int]]) -> list[tuple[int, str, int]]:
        calculate_list = []
        calc_pos = 0
        temp_pos = 0
        for pos, product, count in result:
            if pos > calc_pos or calc_pos == temp_pos:
                calc_pos = pos
                temp_pos = 0
            else:
                temp_pos = calc_pos - pos
            calculate_list.append((temp_pos, product, count))
        return calculate_list

    @staticmethod
    def _correct_count(list_correct: list[list[int, str, int]], count: int) -> list[list[int, str, int]]:
        for lst in list_correct:
            lst[2] = count * lst[2]
        return list_correct

    @staticmethod
    def _calculate_result(result: list[tuple[str, int]], count: int) -> dict[str, int]:
        dict_result = defaultdict(int)
        for detail, det_count in result:
            dict_result[detail] += count * det_count
        return dict_result
    
    @staticmethod
    def _show_tree(tree_list: list[tuple[int, str, int]]) -> None:
        for pos, *data in tree_list:
            for count in range(pos):
                print("|  ", end="")
            print(f"|_{" ".join([str(x) for x in data])}")

    @staticmethod
    def _write_show_tree(tree_list: list[tuple[int, str, int]]) -> None:
        with open(file="tree.txt", mode="w", encoding="cp1251") as wr:
            for pos, *data in tree_list:
                for count in range(pos):
                    wr.write("|  ")
                wr.write(f"|_{" | ".join([str(x) for x in data])} |\n")