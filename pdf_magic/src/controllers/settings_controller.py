# pdf_magic/controllers/settings_controller.py

from PyQt5.QtCore import QObject, pyqtSlot

class SettingsController(QObject):
    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view

    @pyqtSlot(str)
    def update_output_directory(self, directory):
        self.model.set_output_directory(directory)

    @pyqtSlot()
    def save_settings(self):
        self.model.save_settings()