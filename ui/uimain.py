from PyQt6 import uic, QtWidgets

Form, _ = uic.loadUiType('ui/polystyrene.ui')


class Ui(QtWidgets.QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
