from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from .tab_widget import TabWidget
from .toolbar import Toolbar
from .menu_bar import MenuBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("PDF Magic")
        self.setGeometry(100, 100, 1000, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

        self.toolbar = Toolbar()
        self.addToolBar(self.toolbar)

        self.tab_widget = TabWidget()
        layout.addWidget(self.tab_widget)