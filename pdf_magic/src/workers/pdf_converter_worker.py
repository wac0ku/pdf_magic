from .base_worker import BaseWorker
from utils.pdf_processor import PDFProcessor

class PDFConverterWorker(BaseWorker):
    def __init__(self, pdf_processor: PDFProcessor):
        super().__init__()
        self.pdf_processor = pdf_processor
        self.input_path = None
        self.output_path = None

    def setup(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path

    def run(self):
        try:
            self.signals.started.emit()
            
            if not self.input_path or not self.output_path:
                raise ValueError("Input and output paths must be set")

            # Konvertierung in Schritten durchführen
            total_pages = self.pdf_processor.get_page_count(self.input_path)
            
            for i in range(total_pages):
                if self.is_cancelled:
                    return
                
                # Seite konvertieren
                self.pdf_processor.convert_page(
                    self.input_path, 
                    self.output_path, 
                    page_number=i
                )
                
                # Fortschritt berechnen und Signal senden
                progress = int((i + 1) / total_pages * 100)
                self.signals.progress.emit(progress)

            self.signals.finished.emit()
            
        except Exception as e:
            self.signals.error.emit(str(e))