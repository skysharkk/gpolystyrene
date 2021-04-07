

class SelectedElements:
    def __init__(self, window, acad):
        self.btn = window.pushButton_3
        self.btn.clicked.connect(self.select_elements)

    def select_elements(self):
        acad = Autocad(create_if_not_exists=True)
