import os
from PyQt5.QtCore import QRunnable, pyqtSlot
from PyQt5.QtCore import QObject, pyqtSignal
import fitz  # PyMuPDF
from utils.error_handler import ErrorHandler
import json

class MetadataExtractorWorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    result = pyqtSignal(dict, str)  # Emits metadata dict and output file path

class MetadataExtractorWorker(QRunnable):
    def __init__(self, pdf_path, output_dir):
        super(MetadataExtractorWorker, self).__init__()
        self.pdf_path = pdf_path
        self.output_dir = output_dir
        self.signals = MetadataExtractorWorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            doc = fitz.open(self.pdf_path)
            metadata = self.extract_metadata(doc)
            doc.close()

            # Create output filename
            base_name = os.path.splitext(os.path.basename(self.pdf_path))[0]
            output_path = os.path.join(self.output_dir, f"{base_name}_metadata.json")

            # Save metadata to file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=4)

            self.signals.result.emit(metadata, output_path)
            self.signals.finished.emit()

        except Exception as e:
            error_message = f"Error extracting metadata from {self.pdf_path}: {str(e)}"
            ErrorHandler.handle_error(error_message)
            self.signals.error.emit(error_message)

    def extract_metadata(self, doc):
        metadata = {
            "title": doc.metadata.get("title", ""),
            "author": doc.metadata.get("author", ""),
            "subject": doc.metadata.get("subject", ""),
            "keywords": doc.metadata.get("keywords", ""),
            "creator": doc.metadata.get("creator", ""),
            "producer": doc.metadata.get("producer", ""),
            "creation_date": doc.metadata.get("creationDate", ""),
            "modification_date": doc.metadata.get("modDate", ""),
            "number_of_pages": len(doc),
            "file_size": os.path.getsize(self.pdf_path),
        }
        return metadata
