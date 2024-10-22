from PyQt5.QtWidgets import QToolBar, QAction
from PyQt5.QtGui import QIcon

class Toolbar(QToolBar):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.addAction(QIcon("icons/open.png"), "Open")
        self.addAction(QIcon("icons/save.png"), "Save")
        self.addAction(QIcon("icons/convert.png"), "Convert")
        self.addAction(QIcon("icons/extract.png"), "Extract")