from PyQt5.QtCore import QObject

class MainController(QObject):
    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        self.conversion_controller = None
        self.extraction_controller = None
        self.settings_controller = None

    def set_conversion_controller(self, controller):
        self.conversion_controller = controller

    def set_extraction_controller(self, controller):
        self.extraction_controller = controller

    def set_settings_controller(self, controller):
        self.settings_controller = controller

    def show_conversion_tab(self):
        self.view.show_conversion_tab()

    def show_extraction_tab(self):
        self.view.show_extraction_tab()

    def show_settings_tab(self):
        self.view.show_settings_tab()