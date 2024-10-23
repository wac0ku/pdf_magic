from .base_worker import BaseWorker

class ImageToPDFWorker(BaseWorker):
    def __init__(self, pdf_processor):
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

            self.pdf_processor.convert_image_to_pdf(
                self.input_path, 
                self.output_path
            )
            
            self.signals.finished.emit()
            
        except Exception as e:
            self.signals.error.emit(str(e))