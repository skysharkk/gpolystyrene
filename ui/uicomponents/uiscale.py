class Scale:
    def __init__(self, input_field):
        self.input_field = input_field

    def get_value(self):
        return int(self.input_field.displayText())
