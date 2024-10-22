from PyQt5.QtWidgets import QDialog, QLabel, QPushButton

class ErrorDialog(QDialog):
    def __init__(self, error_message):
        super().__init__()
        self.initUI(error_message)

    def initUI(self, error_message):
        self.setWindowTitle("Error")
        self.setGeometry(100, 100, 300, 100)

        error_label = QLabel(error_message, self)
        error_label.move(20, 20)

        ok_button = QPushButton("OK", self)
        ok_button.move(120, 60)
        ok_button.clicked.connect(self.close)