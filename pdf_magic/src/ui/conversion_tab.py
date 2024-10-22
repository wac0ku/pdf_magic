from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QSpinBox, QPushButton
from PyQt5.QtCore import Qt

class ConversionTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.label = QLabel("Konvertierungseinstellungen")
        self.layout.addWidget(self.label)

        self.format_combo_box = QComboBox()
        self.format_combo_box.addItem("PDF")
        self.format_combo_box.addItem("DOCX")
        self.format_combo_box.addItem("TXT")
        self.layout.addWidget(self.format_combo_box)

        self.resolution_spin_box = QSpinBox()
        self.resolution_spin_box.setMinimum(72)
        self.resolution_spin_box.setMaximum(300)
        self.resolution_spin_box.setValue(150)
        self.layout.addWidget(self.resolution_spin_box)

        self.convert_button = QPushButton("Konvertieren")
        self.layout.addWidget(self.convert_button)