from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextBrowser
from PyQt5.QtCore import Qt

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Über")
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Über PDF Magic")
        self.layout.addWidget(self.label)

        self.text_browser = QTextBrowser()
        self.text_browser.setHtml("<p>PDF Magic ist eine kostenlose PDF-Bearbeitungsanwendung.</p>"
                                 "<p>Entwickelt von [Ihr Name]</p>")
        self.layout.addWidget(self.text_browser)