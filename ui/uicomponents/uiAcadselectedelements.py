from PyQt6 import QtWidgets


class AcadSelectedElements:
    def __init__(self, table, delete_btn, export_btn):
        self.table = table
        self.delete_btn = delete_btn
        self.export_btn = export_btn
        self.table_data = []

    def add_element(self, data):
        table_item = QtWidgets.QTreeWidgetItem(self.table)
        for index in range(len(data)):
            table_item.setText(index, data[index])
        self.table_data.append(data)

    def export_table(self):
        pass

    def delete_el(self):
        pass
