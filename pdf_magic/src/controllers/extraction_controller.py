# pdf_magic/controllers/extraction_controller.py

from PyQt5.QtCore import QObject, pyqtSlot
from src.workers.text_extractor_worker import TextExtractorWorker
from src.workers.metadata_extractor_worker import MetadataExtractorWorker

class ExtractionController(QObject):
    def __init__(self, model, view, thread_pool):
        super().__init__()
        self.model = model
        self.view = view
        self.thread_pool = thread_pool
        self.current_worker = None

    @pyqtSlot(str, str)
    def start_extraction(self, file_path, extraction_type):
        if extraction_type == "TEXT":
            self.current_worker = TextExtractorWorker(file_path, self.model.get_output_directory())
        elif extraction_type == "METADATA":
            self.current_worker = MetadataExtractorWorker(file_path, self.model.get_output_directory())
        else:
            raise ValueError(f"Unsupported extraction type: {extraction_type}")

        self.current_worker.signals.progress.connect(self.view.update_progress)
        self.current_worker.signals.finished.connect(self.extraction_finished)
        self.current_worker.signals.error.connect(self.view.show_error)
        self.current_worker.signals.cancelled.connect(self.extraction_cancelled)

        self.thread_pool.start(self.current_worker)

    @pyqtSlot()
    def cancel_extraction(self):
        if self.current_worker:
            self.current_worker.cancel()

    def extraction_finished(self):
        self.current_worker = None

    def extraction_cancelled(self):
        self.view.show_cancelled_message()
        self.current_worker = None