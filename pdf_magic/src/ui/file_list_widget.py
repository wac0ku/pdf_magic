from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class FileListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setFont(QFont("Arial", 12))
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def add_file(self, file_path):
        item = QListWidgetItem(file_path)
        item.setData(Qt.UserRole, file_path)
        self.addItem(item)

    def get_selected_files(self):
        selected_items = self.selectedItems()
        return [item.data(Qt.UserRole) for item in selected_items]