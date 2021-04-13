import win32com.client
import logging
from comtypes.automation import VARIANT
from ctypes import byref
from array import array

logger = logging.getLogger(__name__)


class AcadUtils:
    def __init__(self, acad):
        self.acad = acad
        self.doc = self.acad.doc
        self.shell = win32com.client.Dispatch("WScript.Shell")
        self.selected = None

    def change_focus_window(self):
        self.shell.AppActivate(self.acad.app.Caption)

    def select_drew_objects(self, text="Выберете объект"):
        self.change_focus_window()
        self.doc.Utility.prompt(text)
        try:
            self.doc.SelectionSets.Item("SS1").Delete()
        except AssertionError:
            logger.debug('Delete selection failed')

        self.selected = self.doc.SelectionSets.Add("SS1")
        self.selected.SelectOnScreen()

    def print_selected(self):
        for index in range(self.selected.Count):
            print(self.selected.Item(index))

    def get_point(self, message_text="Выберете точку"):
        self.change_focus_window()
        base_point = array("d", [0, 0, 0])
        return self.doc.Utility.GetPoint(base_point, message_text)

    def draw_polyline(self, points, width=0.0):
        amount_of_coordinates = 3
        polyline = self.doc.ModelSpace.AddPolyline(points)
        for index in range(int(len(points) / amount_of_coordinates)):
            polyline.SetWidth(index, width, width)

    def draw_table(self, table_coordinates, column_width, text_height, text):
        self.draw_polyline(table_coordinates["title"], 0.6)
        for row in table_coordinates["row"]["coordinates"]:
            self.draw_polyline(row)
        for index in range(len(table_coordinates["separators"])):
            separator = table_coordinates["separators"][index]
            column_initial_point = array("d", separator[0:3])
            self.draw_polyline(separator, 0.6)
            self.draw_text(column_initial_point, column_width[index], text_height, "MiddleCenter", text[index])

    @staticmethod
    def get_bounding_box(entity):
        min_point = VARIANT(array("d", array("d", [0, 0, 0])))
        max_point = VARIANT(array("d", array("d", [0, 0, 0])))
        ref_min_point = byref(min_point)
        ref_max_point = byref(max_point)
        entity.GetBoundingBox(ref_min_point, ref_max_point)
        return [array("d", list(*min_point)), array("d", list(*max_point))]

    @staticmethod
    def get_mtext_line_height(mode_space, width, text_height, text):
        text = mode_space.AddMText(array("d", array("d", [0, 0, 0])), width, text)
        text.Height = text_height
        bounding_box_coordinates = AcadUtils.get_bounding_box(text)
        text.Delete()
        return abs(bounding_box_coordinates[1][1] - bounding_box_coordinates[0][1])

    def draw_text(self, insertion_point, width, height, alignment, text):
        alignment_dict = {
            "TopLeft": 1,
            "TopCenter": 2,
            "TopRight": 3,
            "MiddleLeft": 4,
            "MiddleCenter": 5,
            "MiddleRight": 6,
            "BottomLeft": 7,
            "BottomCenter": 8,
            "BottomRight": 9,
        }
        text = self.doc.ModelSpace.AddMText(insertion_point, width, text)
        text.Height = height
        text.AttachmentPoint = alignment_dict[alignment]
        mtext_height = AcadUtils.get_mtext_line_height(self.doc.ModelSpace, width, height, text)







