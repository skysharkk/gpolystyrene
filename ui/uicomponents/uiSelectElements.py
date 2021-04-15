class SelectElements:
    def __init__(self, btn):
        self.btn = btn

    def connect_action(self, func):
        self.btn.clicked.connect(func)
