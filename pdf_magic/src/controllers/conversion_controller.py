from PyQt5.QtCore import QObject, pyqtSlot
from models.conversion_model import ConversionModel
from workers.pdf_converter_worker import PDFConverterWorker
from workers.image_to_pdf_worker import ImageToPDFWorker
from utils.file_handler import FileHandler
from .base_controller import BaseController
from utils.logger import logger

class ConversionController(BaseController):
    def __init__(self, model: ConversionModel, view, thread_pool, file_handler: FileHandler):
        super().__init__(thread_pool, file_handler)
        self.model = model
        self.view = view
        self.setup_connections()

    def setup_connections(self):
        """Richtet die Signal-Verbindungen ein"""
        # View Verbindungen
        self.view.start_conversion_signal.connect(self.start_conversion)
        self.view.cancel_conversion_signal.connect(self.cancel_current_task)
        self.view.file_dropped_signal.connect(self.handle_file_drop)

    @pyqtSlot(str, str)
    def start_conversion(self, input_path: str, output_path: str):
        """Startet die PDF-Konvertierung"""
        try:
            # Überprüfe Dateitypen
            input_type = self.file_handler.get_file_type(input_path)
            
            if input_type == 'pdf':
                worker = PDFConverterWorker(self.model.pdf_processor)
            elif input_type in ['jpg', 'jpeg', 'png']:
                worker = ImageToPDFWorker(self.model.pdf_processor)
            else:
                raise ValueError(f"Unsupported file type: {input_type}")

            # Worker einrichten
            worker.setup(input_path, output_path)
            
            # Signale verbinden
            worker.signals.started.connect(self.on_conversion_started)
            worker.signals.progress.connect(self.view.update_progress)
            worker.signals.finished.connect(self.on_conversion_finished)
            worker.signals.error.connect(self.view.show_error)
            
            # Worker starten
            self._start_worker(worker)
            logger.info(f"Started conversion: {input_path} -> {output_path}")
            
        except Exception as e:
            logger.error(f"Error starting conversion: {str(e)}")
            self.view.show_error(str(e))

    def on_conversion_started(self):
        """Handler für den Start der Konvertierung"""
        self.view.set_converting_state(True)
        self.view.update_status("Konvertierung läuft...")

    def on_conversion_finished(self):
        """Handler für das Ende der Konvertierung"""
        self.view.set_converting_state(False)
        self.view.update_status("Konvertierung abgeschlossen")
        self.current_worker = None

    def handle_file_drop(self, file_path: str):
        """Verarbeitet gedropte Dateien"""
        if self.file_handler.is_valid_input_file(file_path):
            self.view.set_input_path(file_path)