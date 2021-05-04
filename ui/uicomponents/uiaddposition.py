from autocad.acad import AcadUtils
from array import array


class Positions:
    def __init__(self, add_btn, acad):
        self.add_btn = add_btn
        self.acad = acad
        self.data = None
        self.scale = None

    @staticmethod
    def get_point_of_center(coordinates):
        x = ((coordinates.min_x + coordinates.max_x) / 2)
        y = ((coordinates.min_y + coordinates.max_y) / 2)
        return array("d", [x, y, 0])

    def set_action(self, data, scale):
        self.data = data
        self.scale = scale
        self.add_btn.clicked.connect(self.add_positions)

    def add_positions(self):
        utils = AcadUtils(self.acad)
        for index, pos in enumerate(self.data):
            for item in pos:
                utils.draw_text(
                    Positions.get_point_of_center(item),
                    240/self.scale,
                    120/self.scale,
                    "MiddleCenter",
                    str(index + 1)
                )
