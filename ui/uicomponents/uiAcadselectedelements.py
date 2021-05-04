from PyQt6 import QtWidgets
from utils.myutils import compare_list_or_tuple, get_corner_coordinates, is_elem_exist_in_collection
from utils.myutils import round_half_up
from utils.myutils import show_error_window


class AcadSelectedElements:
    def __init__(self, table, delete_btn, draw_table_btn):
        self.dict_type = {
            "ППТ-15-А-Р": "СТБ1437",
            "Эффективный утеплитель λ ≤ 0,034 Вт/(м·°C)": "Эффективный утеплитель λ ≤ 0,034 Вт/(м·°C)"
        }
        self.dict_name = {
            "ППТ-15-А-Р": "ППТ-15-А-Р",
            "Эффективный утеплитель λ ≤ 0,034 Вт/(м·°C)": ""
        }
        self.delete_btn = delete_btn
        self.draw_table_btn = draw_table_btn
        self.table = table
        self.table_data = []
        self.delete_btn.clicked.connect(self.delete_row)

    def insert_row(self):
        self.table.insertRow(len(self.table_data) - 1)

    def add_elements_to_cell(self, el_data, position):
        item = QtWidgets.QTableWidgetItem(str(el_data))
        self.table.setItem(position[0], position[1], item)

    def add_data_to_row(self, row_data, row_index):
        for index, item in enumerate(row_data):
            self.add_elements_to_cell(item, [row_index, index])

    def change_amount(self, row_index):
        item_value = int(self.table.item(row_index, 3).text())
        self.add_elements_to_cell(item_value + 1, [row_index, 3])

    def is_object_exist(self, obj_coordinates):
        for el in self.table_data:
            if is_elem_exist_in_collection(obj_coordinates, el["acad_data"][2]):
                show_error_window("Одна из позиций уже был выбран!")
                return True
        return False

    def find_if_exist(self, acad_data_el):
        if len(self.table_data) > 0:
            for el_index, el in enumerate(self.table_data):
                if compare_list_or_tuple(acad_data_el[1], el["acad_data"][1]) \
                        and acad_data_el[0] == el["acad_data"][0]:
                    return el_index
        return -1

    def insert_data(self, item_data):
        ppt_type = item_data[0]
        sizes = item_data[1]
        volume = round_half_up((sizes[0] * sizes[1] * sizes[2]) / 1000000000, 2, False)
        self.table_data.append({
            "row": [
                len(self.table_data) + 1,
                self.dict_type[ppt_type],
                f"{self.dict_name[ppt_type]} {sizes[0]}x{sizes[1]}x{sizes[2]}",
                1,
                volume,
                "м\u00b3"
            ],
            "acad_data": [item_data[0], item_data[1], [item_data[2]]]
        })

    def add_data_to_table(self, acad_data):
        for el in acad_data:
            if not self.is_object_exist(el[2].coord):
                is_exist = self.find_if_exist(el)
                if is_exist != -1:
                    self.table_data[is_exist]["row"][3] += 1
                    self.table_data[is_exist]["acad_data"][2].append(el[2])
                    self.change_amount(is_exist)
                else:
                    self.insert_data(el)
                    self.insert_row()
                    self.add_data_to_row(self.table_data[-1]["row"], len(self.table_data) - 1)
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStretchLastSection(True)

    def export_table(self):
        pass

    def change_position(self):
        for index, item in enumerate(self.table_data):
            item["row"][0] = index + 1
            self.add_elements_to_cell(item["row"][0], [index, 0])

    def draw_table_action(self, func):
        self.draw_table_btn.clicked.connect(func)

    def delete_row(self):
        row = self.table.currentRow()
        self.table.removeRow(row)
        self.table_data.pop(row)
        self.change_position()

    def get_coordinates(self):
        result = []
        for item in self.table_data:
            position = []
            for data in item["acad_data"][2]:
                position.append(get_corner_coordinates(data.coord))
            result.append(position)
        return result
