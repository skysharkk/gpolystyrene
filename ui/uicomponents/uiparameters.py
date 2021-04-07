class Parameters:
    def __init__(self, input_depth, type_list, btn):
        self.type_list = type_list
        self.input_depth = input_depth
        self.btn = btn
        self.data = None

    def get_entered_data(self):
        depth = self.input_depth.displayText()
        poly_type = self.type_list.currentText()
        self.data = [
            depth if len(depth) > 0 else '0',
            poly_type
        ]
        return self.data

    def connect_action(self, func):
        self.btn.clicked.connect(func)
