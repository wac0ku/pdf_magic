from PyQt5.QtWidgets import QPushButton, QLineEdit, QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class CustomButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.initUI()

    def initUI(self):
        self.setFont(QFont("Arial", 12))
        self.setCursor(Qt.PointingHandCursor)

class CustomLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setFont(QFont("Arial", 12))

class DropArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.label = QLabel("Dateien hierhin ziehen oder klicken, um hochzuladen")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

class ProgressBarWithLabel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.progress_bar = QProgressBar(self)
        self.label = QLabel("")
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.label)