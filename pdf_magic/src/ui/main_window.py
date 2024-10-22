from PyQt5.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget, QMenuBar, QMenu, QAction
from PyQt5.QtCore import Qt
from .conversion_tab import ConversionTab
from .extraction_tab import ExtractionTab
from .settings_dialog import SettingsDialog
from .about_dialog import AboutDialog
from utils.logger import logger

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("PDF Magic")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.conversion_tab = ConversionTab()
        self.extraction_tab = ExtractionTab()

        self.tab_widget.addTab(self.conversion_tab, "Konvertierung")
        self.tab_widget.addTab(self.extraction_tab, "Extraktion")

        self.create_menu_bar()

        logger.info("Main window UI initialized")

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("Datei")
        edit_menu = menu_bar.addMenu("Bearbeiten")
        help_menu = menu_bar.addMenu("Hilfe")

        settings_action = QAction("Einstellungen", self)
        settings_action.triggered.connect(self.open_settings_dialog)
        edit_menu.addAction(settings_action)

        about_action = QAction("Über", self)
        about_action.triggered.connect(self.open_about_dialog)
        help_menu.addAction(about_action)

    def open_settings_dialog(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec_()

    def open_about_dialog(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec_()