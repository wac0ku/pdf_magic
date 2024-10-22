from PyQt5.QtWidgets import QMenuBar, QAction

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        file_menu = self.addMenu("File")
        file_menu.addAction("Open")
        file_menu.addAction("Save")
        file_menu.addAction("Exit")

        edit_menu = self.addMenu("Edit")
        edit_menu.addAction("Undo")
        edit_menu.addAction("Redo")

        tools_menu = self.addMenu("Tools")
        tools_menu.addAction("Convert")
        tools_menu.addAction("Extract")

        help_menu = self.addMenu("Help")
        help_menu.addAction("About")