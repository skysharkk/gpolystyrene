import win32com.client
import logging
from comtypes.automation import VARIANT
from ctypes import byref
from array import array
from collections import namedtuple
from copy import copy

from utils.myutils import create_array_of_double, two_dimension_list_to_list

logger = logging.getLogger(__name__)


class AcadUtils:
    def __init__(self, acad):
        self.acad = acad
        self.doc = self.acad.doc
        self.shell = win32com.client.Dispatch("WScript.Shell")
        self.__selected_data = None

    def change_focus_window(self):
        self.shell.AppActivate(self.acad.app.Caption)

    def select_drew_objects(self, text="Выберете объект"):
        self.change_focus_window()
        self.doc.Utility.prompt(text)
        try:
            if self.doc.SelectionSets.Count > 0:
                self.doc.SelectionSets.Item("SS1").Delete()
        except AssertionError:
            logger.debug('Delete selection failed')
        finally:
            selected = self.doc.SelectionSets.Add("SS1")
            selected.SelectOnScreen()
            self.__selected_data = self.get_param_of_selected_el(selected)

    def get_selected_data(self):
        copied_data = [*self.__selected_data]
        self.__selected_data = None
        return copied_data

    @staticmethod
    def get_param_of_selected_el(selected_elements):
        Data = namedtuple("Data", ["coord", "area"])
        result = []
        for index in range(selected_elements.Count):
            el = selected_elements.Item(index)
            result.append(Data(el.Coordinates, el.Area))
        return result

    def get_point(self, message_text="Выберете точку"):
        self.change_focus_window()
        base_point = array("d", [0, 0, 0])
        return array('d', self.doc.Utility.GetPoint(base_point, message_text))

    def draw_polyline(self, points, width=0.0):
        amount_of_coordinates = 3
        polyline = self.doc.ModelSpace.AddPolyline(points)
        for index in range(int(len(points) / amount_of_coordinates)):
            polyline.SetWidth(index, width, width)

    @staticmethod
    def get_bounding_box(entity):
        min_point = VARIANT(array("d", array("d", [0, 0, 0])))
        max_point = VARIANT(array("d", array("d", [0, 0, 0])))
        ref_min_point = byref(min_point)
        ref_max_point = byref(max_point)
        entity.GetBoundingBox(ref_min_point, ref_max_point)
        return [array("d", list(*min_point)), array("d", list(*max_point))]

    @staticmethod
    def get_mtext_line_height(text_obj):
        bounding_box_coordinates = AcadUtils.get_bounding_box(text_obj)
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
        text_obj = self.doc.ModelSpace.AddMText(insertion_point, width, text)
        text_obj.Height = height
        text_obj.AttachmentPoint = alignment_dict[alignment]
        mtext_height = AcadUtils.get_mtext_line_height(text_obj)
        new_x = insertion_point[0] - (width / 2)
        new_y = insertion_point[1] + (mtext_height / 2)
        text_obj.Move(insertion_point, array("d", [new_x, new_y, 0]))

    @staticmethod
    def create_point(coordinates, size, coordinate_position):
        copy_coordinates = copy(coordinates)
        copy_coordinates[coordinate_position] += size
        return copy_coordinates

    def draw_rectangle(self, initial_point, width, height):
        ms = self.doc.ModelSpace
        points = [list(initial_point)]
        sizes = [width, -height, -width, height]
        amount_iterates = 4
        for i in range(amount_iterates):
            if i % 2 == 0:
                new_point = AcadUtils.create_point(points[i], sizes[i], 0)
                points.append(new_point)
            else:
                new_point = AcadUtils.create_point(points[i], sizes[i], 1)
                points.append(new_point)
        points = create_array_of_double(two_dimension_list_to_list(points))
        ms.AddPolyline(points)
        return points
