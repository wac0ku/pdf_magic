from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QPushButton

class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 300, 200)

        layout = QGridLayout(self)

        label = QLabel("Output folder:")
        layout.addWidget(label, 0, 0)

        self.output_folder = QLineEdit()
        layout.addWidget(self.output_folder, 0, 1)

        ok_button = QPushButton("OK", self)
        layout.addWidget(ok_button, 1, 1)
        ok_button.clicked.connect(self.close)