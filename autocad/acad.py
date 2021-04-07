from pyautocad import Autocad
import win32com.client
import logging
from array import array

logger = logging.getLogger(__name__)


class Acad:
    def __init__(self):
        self.acad = Autocad(create_if_not_exists=True)
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

    def draw_table(self, table_coordinates):
        self.draw_polyline(table_coordinates["title"], 0.6)
        for row in table_coordinates["row"]["coordinates"]:
            self.draw_polyline(row)
        for separator in table_coordinates["separators"]:
            self.draw_polyline(separator, 0.6)




