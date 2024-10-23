from .base_controller import BaseController
from PyQt5.QtCore import QObject, pyqtSlot
from models.extraction_model import ExtractionModel
from workers.text_extractor_worker import TextExtractorWorker
from workers.metadata_extractor_worker import MetadataExtractorWorker
from utils.file_handler import FileHandler
from utils.logger import logger

class ExtractionController(BaseController):
    def __init__(self, model: ExtractionModel, view, thread_pool, file_handler: FileHandler):
        super().__init__(thread_pool, file_handler)
        self.model = model
        self.view = view
        self.setup_connections()

    def setup_connections(self):
        """Richtet die Signal-Verbindungen ein"""
        self.view.start_text_extraction_signal.connect(self.start_text_extraction)
        self.view.start_metadata_extraction_signal.connect(self.start_metadata_extraction)
        self.view.cancel_extraction_signal.connect(self.cancel_current_task)
        self.view.file_dropped_signal.connect(self.handle_file_drop)

    @pyqtSlot(str)
    def start_text_extraction(self, input_path: str):
        """Startet die Textextraktion"""
        try:
            if not self.file_handler.is_pdf_file(input_path):
                raise ValueError("Only PDF files are supported for text extraction")

            worker = TextExtractorWorker(self.model.pdf_processor)
            worker.setup(input_path)
            
            # Signale verbinden
            worker.signals.started.connect(self.on_extraction_started)
            worker.signals.result.connect(self.view.show_extracted_text)
            worker.signals.finished.connect(self.on_extraction_finished)
            worker.signals.error.connect(self.view.show_error)
            
            self._start_worker(worker)
            logger.info(f"Started text extraction: {input_path}")
            
        except Exception as e:
            logger.error(f"Error starting text extraction: {str(e)}")
            self.view.show_error(str(e))

    @pyqtSlot(str)
    def start_metadata_extraction(self, input_path: str):
        """Startet die Metadatenextraktion"""
        try:
            if not self.file_handler.is_pdf_file(input_path):
                raise ValueError("Only PDF files are supported for metadata extraction")

            worker = MetadataExtractorWorker(self.model.pdf_processor)
            worker.setup(input_path)
            
            # Signale verbinden
            worker.signals.started.connect(self.on_extraction_started)
            worker.signals.result.connect(self.view.show_metadata)
            worker.signals.finished.connect(self.on_extraction_finished)
            worker.signals.error.connect(self.view.show_error)
            
            self._start_worker(worker)
            logger.info(f"Started metadata extraction: {input_path}")
            
        except Exception as e:
            logger.error(f"Error starting metadata extraction: {str(e)}")
            self.view.show_error(str(e))

    def on_extraction_started(self):
        """Handler für den Start der Extraktion"""
        self.view.set_extracting_state(True)
        self.view.update_status("Extraktion läuft...")

    def on_extraction_finished(self):
        """Handler für das Ende der Extraktion"""
        self.view.set_extracting_state(False)
        self.view.update_status("Extraktion abgeschlossen")
        self.current_worker = None

    def handle_file_drop(self, file_path: str):
        """Verarbeitet gedropte Dateien"""
        if self.file_handler.is_pdf_file(file_path):
            self.view.set_input_path(file_path)