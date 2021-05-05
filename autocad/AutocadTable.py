from comtypes.client import Constants


class AcadTable:
    def __init__(
            self,
            initial_point,
            scale,
            column_width,
            row_height,
            data,
            acad
    ):
        self.initial_point = initial_point
        self.scale = scale
        self.column_width = column_width
        self.row_height = row_height
        self.data = data
        self.__model_space = acad.doc.ModelSpace
        self.__constants = Constants(acad.app)
        self.__table = None

    def apply_scale(self, sizes_list):
        for index in range(len(sizes_list)):
            sizes_list[index] /= self.scale

    def __add_table_to_ms(self):
        self.__table = self.__model_space.AddTable(
            self.initial_point,
            len(self.row_height) + 1,
            len(self.column_width),
            1,
            1
        )
        self.__table.DeleteRows(0, 1)

    def __change_table_sizes(self):
        self.apply_scale(self.row_height)
        self.apply_scale(self.column_width)

        for index in range(len(self.column_width)):
            self.__table.SetColumnWidth(index, self.column_width[index])

        for index in range(len(self.row_height)):
            self.__table.SetRowHeight(index, self.row_height[index])

    def __set_line_weight(self, position, align, weight):
        self.__table.SetGridLineWeight2(
            position[0], position[1], align, weight)

    def set_vertical_line_weight(self, position, weight):
        self.__set_line_weight(
            position,
            self.__constants.acVertLeft + self.__constants.acVertRight,
            weight
        )

    def set_vert_and_horz_line_weight(self, position, weight):
        self.__set_line_weight(
            position,
            self.__constants.acVertLeft +
            self.__constants.acVertRight + self.__constants.acHorzBottom +
            self.__constants.acHorzTop,
            weight
        )

    def create_table(self, line_weight, text_height):
        self.__add_table_to_ms()
        self.__change_table_sizes()
        for col_index in range(len(self.column_width)):
            for row_index in range(len(self.row_height)):
                self.__table.VertCellMargin = 0
                self.__table.HorzCellMargin = 0
                self.__table.SetTextHeight2(row_index, col_index, 1, text_height)
                if row_index == 0:
                    self.set_vert_and_horz_line_weight(
                        [row_index, col_index], line_weight)
                    self.__table.SetCellAlignment(row_index, col_index, self.__constants.acMiddleCenter)
                else:
                    self.set_vertical_line_weight(
                        [row_index, col_index], line_weight)
                    if col_index == 2:
                        self.__table.SetCellAlignment(row_index, col_index, self.__constants.acMiddleLeft)
                    else:
                        self.__table.SetCellAlignment(row_index, col_index, self.__constants.acMiddleCenter)
                if self.data[row_index][col_index] is not None:
                    self.__table.SetText(row_index, col_index, self.data[row_index][col_index])
