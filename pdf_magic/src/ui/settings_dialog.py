from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Einstellungen")
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Einstellungen")
        self.layout.addWidget(self.label)

        self.api_key_line_edit = QLineEdit()
        self.layout.addWidget(self.api_key_line_edit)

        self.save_button = QPushButton("Speichern")
        self.layout.addWidget(self.save_button)