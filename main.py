from PyQt6.QtWidgets import QApplication
from ui.uimain import Ui
from ui.uicomponents.uiparameters import Parameters
from ui.uicomponents.uiaddedelements import AddedElements
from autocad.acad import Acad
from autocad.table import Table


if __name__ == '__main__':
    import sys


    def main():
        app = QApplication(sys.argv)
        window = Ui()
        window.show()
        parameters = Parameters(window.lineEdit, window.comboBox, window.pushButton)
        added_elements = AddedElements(window.treeWidget, window.pushButton_2)
        parameters.connect_action(added_elements.add_el(parameters.get_entered_data))
        autocad = Acad()
        # table = Table(autocad.get_point(), 4, 40)
        # table_data = table.create_table()
        # autocad.draw_table(table_data)
        sys.exit(app.exec())

    main()

