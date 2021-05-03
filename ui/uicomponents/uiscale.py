from utils.myutils import show_error_window


class Scale:
    def __init__(self, input_field):
        self.input_field = input_field

    def get_value(self):
        try:
            return int(self.input_field.displayText())
        except ValueError:
            show_error_window('Введено неверное значение масштаба')
