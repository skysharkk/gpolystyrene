from collections import namedtuple
from array import array
from autocad.acad import AcadUtils
from utils import greedypacker
from pyautocad import Autocad


class Balance:
    def __init__(self, data):
        """
                :param data: [[[sizes], type, count], [[sizes], type, count], [[sizes], type, count], ...]
                [sizes] = ['width', 'height', 'thickness']
        """
        self.data = data
        self.__converted_data = {}
        self.__container_sizes = (2000, 1000)
        self.__possible_types = ["ППТ-15-А-Р",
                                 "Эффективный утеплитель λ ≤ 0,034 Вт/(м·°C)"]
        self.__packed_items = {}

    def __convert__data(self):
        Item = namedtuple("Item", ["sizes", "count"])
        for item in self.data:
            poly_type = item[1]
            thickness = item[0][2]
            sizes = item[0][:2]
            count = item[2]
            if self.__converted_data.get(poly_type) is None:
                self.__converted_data[poly_type] = {}
            if self.__converted_data[poly_type].get(thickness) is None:
                self.__converted_data[poly_type][thickness] = []
            self.__converted_data[poly_type][thickness].append(
                Item(sizes, count))

    @staticmethod
    def create_packer_item(sizes):
        return greedypacker.Item(*sizes)

    def __packing_items(self, items):
        greedy_items = []
        width, height = self.__container_sizes
        bin_manager = greedypacker.BinManager(
            width,
            height,
            pack_algo='shelf',
            heuristic='best_area_fit',
            wastemap=True,
            rotation=True
        )
        for item in items:
            for _ in range(item.count):
                greedy_items.append(Balance.create_packer_item(item.sizes))
        bin_manager.add_items(*greedy_items)
        bin_manager.execute()
        return bin_manager.bins

    def create_pack(self):
        self.__convert__data()
        types = self.__converted_data.keys()
        for poly_type in types:
            thickness_list = self.__converted_data[poly_type].keys()
            self.__packed_items[poly_type] = {}
            for thickness in thickness_list:
                self.__packed_items[poly_type][thickness] = self.__packing_items(
                    self.__converted_data[poly_type][thickness]
                )

    def draw_packs(self, drawing_func, add_name_func):
        initial_x = 0
        initial_y = 0
        types = self.__packed_items.keys()
        for poly_type in types:
            thickness_list = self.__packed_items[poly_type].keys()
            for thickness in thickness_list:
                for greedy_bin in self.__packed_items[poly_type][thickness]:
                    add_name_func(
                        array("d", [initial_x, initial_y, 0]), 0, 120, "MiddleCenter", poly_type)
                    initial_y -= 240
                    add_name_func(
                        array("d", [initial_x, initial_y, 0]), 0, 120, "MiddleCenter", str(thickness))
                    initial_y -= 240
                    drawing_func(
                        array("d", [initial_x, initial_y, 0]), *self.__container_sizes)
                    for item in greedy_bin.items:
                        drawing_func(
                            array("d", [initial_x + item.x, initial_y - item.y, 0]), item.width, item.height)
                    initial_y -= (240 + self.__container_sizes[1])


acad = Autocad(create_if_not_exists=True)
acad_utils = AcadUtils(acad)


bal = Balance(
    [
        [[300, 400, 180], "ППТ-15-А-Р", 2],
        [[800, 900, 160], "ППТ-15-А-Р", 4],
        [[360, 500, 180], "ППТ-15-А-Р", 2],
        [[500, 600, 180], "ППТ-15-А-Р", 5],
        [[500, 600, 140], "Эффективный утеплитель λ ≤ 0,034 Вт/(м·°C)", 1],
    ]
)

bal.create_pack()
bal.draw_packs(acad_utils.draw_rectangle, acad_utils.draw_text)
