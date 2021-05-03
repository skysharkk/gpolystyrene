from PyQt6 import QtWidgets

from utils.myutils import show_error_window


class AddedElements:
    def __init__(self, el_ui_table, delete_btn):
        self.el_ui_table = el_ui_table
        self.delete_btn = delete_btn
        self.delete_btn.clicked.connect(self.delete_element)
        self.el_list = []

    def match_check(self, characteristic):
        for item in self.el_list:
            if item == characteristic:
                return True
        return False

    def add_el(self, get_characteristic):
        def add():
            characteristic = get_characteristic()
            if int(characteristic[0]) > 0:
                if not self.match_check(characteristic):
                    item = QtWidgets.QTreeWidgetItem(self.el_ui_table)
                    self.el_list.append(characteristic)
                    item.setText(0, characteristic[0])
                    item.setText(1, characteristic[1])

        return add

    def get_table_data(self):
        return self.el_list

    def get_selected_item(self):
        item = self.el_ui_table.currentItem()
        index = self.el_ui_table.indexOfTopLevelItem(item)
        return item, index

    def get_selected_item_value(self):
        item, item_index = self.get_selected_item()
        if item:
            return self.el_list[item_index]
        return None

    def delete_element(self):
        if len(self.el_list) > 0:
            item = self.get_selected_item()
            self.el_list.pop(item[1])
            self.el_ui_table.takeTopLevelItem(
                self.el_ui_table.indexOfTopLevelItem(item[0]))
