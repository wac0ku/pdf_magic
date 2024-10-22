from PyQt5.QtCore import QObject, pyqtSignal
from enum import Enum

class ConversionType(Enum):
    PDF_TO_DOCX = "PDF zu DOCX"
    PDF_TO_IMAGE = "PDF zu Bild"
    IMAGE_TO_PDF = "Bild zu PDF"
    TEXT_EXTRACTION = "Textextraktion"

class ConversionStatus(Enum):
    PENDING = "Ausstehend"
    IN_PROGRESS = "In Bearbeitung"
    COMPLETED = "Abgeschlossen"
    FAILED = "Fehlgeschlagen"

class ConversionModel(QObject):
    conversion_added = pyqtSignal(object)
    conversion_updated = pyqtSignal(object)
    conversion_removed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._conversions = {}  # Dictionary to store conversion tasks

    def add_conversion(self, file_path, conversion_type):
        conversion = {
            'file_path': file_path,
            'type': conversion_type,
            'status': ConversionStatus.PENDING,
            'progress': 0,
            'output_path': None,
            'error_message': None
        }
        task_id = self._generate_task_id(file_path, conversion_type)
        self._conversions[task_id] = conversion
        self.conversion_added.emit(conversion)
        return task_id

    def update_conversion(self, task_id, **kwargs):
        if task_id in self._conversions:
            self._conversions[task_id].update(kwargs)
            self.conversion_updated.emit(self._conversions[task_id])

    def remove_conversion(self, task_id):
        if task_id in self._conversions:
            del self._conversions[task_id]
            self.conversion_removed.emit(task_id)

    def get_conversion(self, task_id):
        return self._conversions.get(task_id)

    def get_all_conversions(self):
        return list(self._conversions.values())

    def _generate_task_id(self, file_path, conversion_type):
        import hashlib
        return hashlib.md5(f"{file_path}{conversion_type}".encode()).hexdigest()