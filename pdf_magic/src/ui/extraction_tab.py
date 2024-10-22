from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QSpinBox, QPushButton
from PyQt5.QtCore import Qt

class ExtractionTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.label = QLabel("Extraktionseinstellungen")
        self.layout.addWidget(self.label)

        self.format_combo_box = QComboBox()
        self.format_combo_box.addItem("PDF")
        self.format_combo_box.addItem("DOCX")
        self.format_combo_box.addItem("TXT")
        self.layout.addWidget(self.format_combo_box)

        self.page_spin_box = QSpinBox()
        self.page_spin_box.setMinimum(1)
        self.page_spin_box.setMaximum(100)
        self.page_spin_box.setValue(1)
        self.layout.addWidget(self.page_spin_box)

        self.extract_button = QPushButton("Extrahieren")
        self.layout.addWidget(self.extract_button)