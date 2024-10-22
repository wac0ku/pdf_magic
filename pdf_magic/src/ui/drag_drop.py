from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, 
                             QListWidget, QListWidgetItem, QHBoxLayout, QSpacerItem, 
                             QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QIcon, QColor, QPalette, QFont
from utils.logger import logger
import os

class DropArea(QWidget):
    files_dropped = pyqtSignal(list)

    def __init__(self, accepted_extensions=None, parent=None):
        super().__init__(parent)
        self.accepted_extensions = accepted_extensions or ['.pdf', '.docx', '.txt', '.jpg', '.png']
        self.files = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Icon und Haupttext
        icon_layout = QHBoxLayout()
        self.icon_label = QLabel(self)
        self.set_icon("drag_drop", size=48)
        icon_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        icon_layout.addWidget(self.icon_label)
        icon_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(icon_layout)

        self.text_label = QLabel("Dateien hier hineinziehen oder auswählen", self)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet("""
            font-size: 16px;
            color: #606770;
            font-weight: 500;
        """)
        layout.addWidget(self.text_label)

        # Dateiliste
        self.file_list = QListWidget(self)
        self.file_list.setDragDropMode(QListWidget.InternalMove)
        self.file_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #dddfe2;
                border-radius: 8px;
                background-color: #f5f6f7;
                padding: 10px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #dddfe2;
            }
            QListWidget::item:last {
                border-bottom: none;
            }
            QListWidget::item:hover {
                background-color: #e4e6eb;
            }
        """)
        layout.addWidget(self.file_list)

        # Dateiauswahl-Button
        self.select_button = QPushButton("Dateien auswählen", self)
        self.select_button.clicked.connect(self.select_files)
        self.select_button.setCursor(Qt.PointingHandCursor)
        self.select_button.setStyleSheet("""
            QPushButton {
                background-color: #1877f2;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #166fe5;
            }
            QPushButton:pressed {
                background-color: #1464d1;
            }
        """)
        layout.addWidget(self.select_button)

        self.setAcceptDrops(True)
        self.setStyleSheet("""
            DropArea {
                background-color: #ffffff;
                border: 2px dashed #dddfe2;
                border-radius: 8px;
            }
            DropArea:hover {
                background-color: #f0f2f5;
            }
        """)

    def set_icon(self, icon_name, size=64):
        try:
            icon = QIcon(f":/icons/{icon_name}.png")
            if not icon.isNull():
                pixmap = icon.pixmap(QSize(size, size))
                self.icon_label.setPixmap(pixmap)
            else:
                logger.warning(f"Icon nicht gefunden: {icon_name}")
        except Exception as e:
            logger.error(f"Fehler beim Setzen des Icons: {str(e)}")

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        new_files = [url.toLocalFile() for url in event.mimeData().urls() if self.is_valid_file(url.toLocalFile())]
        if new_files:
            self.add_files(new_files)
            event.acceptProposedAction()

    def is_valid_file(self, file_path):
        _, ext = os.path.splitext(file_path)
        return ext.lower() in self.accepted_extensions

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Dateien auswählen", "", 
            f"Akzeptierte Dateien (*{' *'.join(self.accepted_extensions)})"
        )
        if files:
            self.add_files(files)

    def add_files(self, new_files):
        for file in new_files:
            if file not in self.files:
                self.files.append(file)
                item = QListWidgetItem(os.path.basename(file))
                item.setIcon(QIcon(":/icons/file.png"))
                self.file_list.addItem(item)
        self.update_ui()
        self.files_dropped.emit(self.files)

    def update_ui(self):
        count = len(self.files)
        if count == 0:
            self.text_label.setText("Dateien hier hineinziehen oder auswählen")
        else:
            self.text_label.setText(f"{count} Datei{'en' if count > 1 else ''} ausgewählt")

    def clear_files(self):
        self.files.clear()
        self.file_list.clear()
        self.update_ui()

    def remove_file(self, index):
        if 0 <= index < len(self.files):
            del self.files[index]
            self.file_list.takeItem(index)
            self.update_ui()

    def get_files(self):
        return self.files