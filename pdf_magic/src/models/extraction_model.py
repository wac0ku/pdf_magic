from enum import Enum
from PyQt5.QtCore import QObject, pyqtSignal
import uuid

class ExtractionType(Enum):
    TEXT = 1
    METADATA = 2

class ExtractionStatus(Enum):
    PENDING = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    FAILED = 4
    CANCELED = 5

class ExtractionModel(QObject):
    extraction_added = pyqtSignal(str)
    extraction_updated = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.extractions = {}

    def add_extraction(self, file_path, extraction_type):
        extraction_id = str(uuid.uuid4())
        self.extractions[extraction_id] = {
            'file_path': file_path,
            'extraction_type': extraction_type,
            'status': ExtractionStatus.PENDING,
            'progress': 0,
            'result': None,
            'error_message': None
        }
        self.extraction_added.emit(extraction_id)
        return extraction_id

    def update_extraction(self, extraction_id, **kwargs):
        if extraction_id in self.extractions:
            self.extractions[extraction_id].update(kwargs)
            self.extraction_updated.emit(extraction_id)
        else:
            raise ValueError(f"Extraction with id {extraction_id} not found")

    def get_extraction(self, extraction_id):
        return self.extractions.get(extraction_id)

    def get_all_extractions(self):
        return self.extractions

    def remove_extraction(self, extraction_id):
        if extraction_id in self.extractions:
            del self.extractions[extraction_id]
        else:
            raise ValueError(f"Extraction with id {extraction_id} not found")

    def clear_completed_extractions(self):
        self.extractions = {k: v for k, v in self.extractions.items() 
                            if v['status'] != ExtractionStatus.COMPLETED}

    def get_extractions_by_status(self, status):
        return {k: v for k, v in self.extractions.items() if v['status'] == status}

    def get_extractions_by_type(self, extraction_type):
        return {k: v for k, v in self.extractions.items() if v['extraction_type'] == extraction_type}

    def cancel_extraction(self, extraction_id):
        if extraction_id in self.extractions:
            self.update_extraction(extraction_id, status=ExtractionStatus.CANCELED)
        else:
            raise ValueError(f"Extraction with id {extraction_id} not found")

    def add_log_entry(self, extraction_id, message):
        if extraction_id in self.extractions:
            if 'log' not in self.extractions[extraction_id]:
                self.extractions[extraction_id]['log'] = []
            self.extractions[extraction_id]['log'].append(message)
            self.extraction_updated.emit(extraction_id)
        else:
            raise ValueError(f"Extraction with id {extraction_id} not found")

    def get_log(self, extraction_id):
        if extraction_id in self.extractions:
            return self.extractions[extraction_id].get('log', [])
        else:
            raise ValueError(f"Extraction with id {extraction_id} not found")