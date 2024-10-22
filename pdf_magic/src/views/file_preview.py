from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtGui import QPixmap

class FilePreview(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QGridLayout(self)

        self.file_label = QLabel("No file selected")
        layout.addWidget(self.file_label, 0, 0)

        self.file_image = QLabel()
        layout.addWidget(self.file_image, 1, 0)

        self.updateUI()

    def updateUI(self):
        # Update the UI based on the selected file
        pass