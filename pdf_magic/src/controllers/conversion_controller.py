from PyQt5.QtCore import QObject, pyqtSlot
from workers.pdf_converter_worker import PDFConverterWorker
from workers.image_to_pdf_worker import ImageToPDFWorker

class ConversionController(QObject):
    def __init__(self, model, view, thread_pool):
        super().__init__()
        self.model = model
        self.view = view
        self.thread_pool = thread_pool
        self.current_worker = None

    @pyqtSlot(list, str)
    def start_conversion(self, file_paths, conversion_type):
        if conversion_type == "PDF_TO_DOCX":
            self.current_worker = PDFConverterWorker(file_paths, self.model.get_output_directory())
        elif conversion_type == "IMAGE_TO_PDF":
            self.current_worker = ImageToPDFWorker(file_paths, self.model.get_output_directory())
        else:
            raise ValueError(f"Unsupported conversion type: {conversion_type}")

        self.current_worker.signals.progress.connect(self.view.update_progress)
        self.current_worker.signals.finished.connect(self.conversion_finished)
        self.current_worker.signals.error.connect(self.view.show_error)
        self.current_worker.signals.cancelled.connect(self.conversion_cancelled)

        self.thread_pool.start(self.current_worker)

    @pyqtSlot()
    def cancel_conversion(self):
        if self.current_worker:
            self.current_worker.cancel()

    def conversion_finished(self):
        self.current_worker = None
         
    def conversion_cancelled(self):
        self.view.show_cancelled_message()
        self.current_worker = None