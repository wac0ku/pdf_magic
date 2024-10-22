from PyQt5.QtCore import QObject, pyqtSignal
import os
from datetime import datetime

class File:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.size = os.path.getsize(path)
        self.created_at = datetime.fromtimestamp(os.path.getctime(path))
        self.modified_at = datetime.fromtimestamp(os.path.getmtime(path))
        self.type = self._get_file_type()

    def _get_file_type(self):
        _, ext = os.path.splitext(self.name)
        ext = ext.lower()
        if ext == '.pdf':
            return 'PDF'
        elif ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']:
            return 'Image'
        elif ext == '.docx':
            return 'DOCX'
        else:
            return 'Unknown'

    def __str__(self):
        return f"{self.name} ({self.size} Bytes, {self.type})"

class FileModel(QObject):
    file_added = pyqtSignal(object)
    file_removed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.files = {}

    def add_file(self, file_path):
        if file_path not in self.files:
            file = File(file_path)
            self.files[file_path] = file
            self.file_added.emit(file)

    def remove_file(self, file_path):
        if file_path in self.files:
            del self.files[file_path]
            self.file_removed.emit(file_path)

    def get_file(self, file_path):
        return self.files.get(file_path)

    def get_all_files(self):
        return list(self.files.values())

    def get_files_by_type(self, file_type):
        return [file for file in self.files.values() if file.type == file_type]

    def clear_files(self):
        self.files.clear()

    def is_valid_file(self, file_path):
        _, ext = os.path.splitext(file_path)
        return ext.lower() in ['.pdf', '.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.docx']