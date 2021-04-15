from PyQt6 import QtWidgets


class AcadSelectedElements:
    def __init__(self, table):
        self.table = table
        self.row_count = 0
        self.table_data = []

        """
        table_data 
        []
        """

    def insert_row(self):
        self.table.insertRow(self.row_count)
        self.row_count += 1

    def add_element(self, el_data, position):
        item = QtWidgets.QTableWidgetItem(str(el_data))
        self.table.setItem(position[0], position[1], item)

    def add_data(self):
        pass

    def export_table(self):
        pass

    def delete_row(self):
        pass
