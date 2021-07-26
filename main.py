from pprint import pprint

from PyQt6.QtWidgets import QApplication
from pyautocad import Autocad

from ui.uicomponents.uiaddposition import Positions
from ui.uicomponents.uibalance import Balance
from ui.uicomponents.uiscale import Scale
from ui.uicomponents.uiSelectElements import SelectElements
from ui.uimain import Ui
from ui.uicomponents.uiparameters import Parameters
from ui.uicomponents.uiaddedelements import AddedElements
from autocad.acad import AcadUtils
from autocad.AutocadTable import AcadTable
from ui.uicomponents.uiAcadselectedelements import AcadSelectedElements
from utils.myutils import get_rectangle_sizes, show_error_window

if __name__ == '__main__':
    import sys

    acad = Autocad(create_if_not_exists=True)
    app = QApplication(sys.argv)
    window = Ui()
    window.show()
    parameters = Parameters(
        window.lineEdit, window.comboBox, window.pushButton)
    added_elements = AddedElements(window.treeWidget, window.pushButton_2)
    select_elements_btn = SelectElements(window.pushButton_3)
    acad_utils = AcadUtils(acad)
    ui_table = AcadSelectedElements(
        window.tableWidget_2, window.pushButton_4, window.pushButton_7)
    scale = Scale(window.lineEdit_2)
    pos = Positions(window.pushButton_9, acad)

    def format_table_data(data):
        formatted_list = [
            ['Поз.', 'Обозначение', 'Наименование',
                'Кол.', u'Объем ед.м\u00b3', 'Примечание'],
            ['', '', 'Плиты пенополистирольные', '', '', ''],
        ]
        for item in data:
            formatted_list.append(item['row'])
        formatted_list.append(['', '', 'Плиты минераловатные', '', '', ''])
        formatted_list.append(['', '', '', '', '', ''])
        formatted_list.append(['', '', '', '', '', ''])
        formatted_list.append(['', '', '', '', '', ''])
        return formatted_list

    def create_table_data(params, list_data, acad_scale):
        result = []
        for item in list_data:
            sizes = get_rectangle_sizes(item.coord, acad_scale)
            thickness = params[0]
            result.append([params[1], [*sizes, int(thickness)], item])
        return result

    def select_items():
        params = added_elements.get_selected_item_value()
        scale_value = scale.get_value()
        if params and scale_value:
            acad_utils.select_drew_objects()
            data = acad_utils.get_selected_data()
            ui_table.add_data_to_table(
                create_table_data(params, data, scale_value))
            pos.set_action(ui_table.get_coordinates(), scale.get_value())
        else:
            show_error_window('Необходима выбрать толщину и тип утеплителя')

    def draw_table():
        point = acad_utils.get_point()
        column_width = [600, 2400, 2600, 400, 600, 800]
        formatted_data = format_table_data(ui_table.table_data)
        row_height = [600] * len(formatted_data)
        row_height[1:] = [320] * (len(formatted_data) - 1)
        table = AcadTable(point, scale.get_value(), column_width, row_height, formatted_data,
                          acad)
        table.create_table(60, 100/scale.get_value())

    def draw_balance(data, drawing_func, add_name_func):
        balance = Balance(data)
        balance.create_pack()

    def main():
        parameters.connect_action(
            added_elements.add_el(parameters.get_entered_data))
        select_elements_btn.connect_action(select_items)
        ui_table.draw_table_action(draw_table)
        sys.exit(app.exec())

    main()
