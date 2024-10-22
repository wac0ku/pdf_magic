from PyQt5.QtWidgets import QDialog, QTextBrowser

class HelpDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Help")
        self.setGeometry(100, 100, 400, 300)

        text_browser = QTextBrowser(self)
        text_browser.setHtml("This is the help dialog.")