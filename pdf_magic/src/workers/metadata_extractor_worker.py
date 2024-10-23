from .base_worker import BaseWorker

class MetadataExtractorWorker(BaseWorker):
    def __init__(self, pdf_processor):
        super().__init__()
        self.pdf_processor = pdf_processor
        self.input_path = None

    def setup(self, input_path: str):
        self.input_path = input_path

    def run(self):
        try:
            self.signals.started.emit()
            
            if not self.input_path:
                raise ValueError("Input path must be set")

            metadata = self.pdf_processor.extract_metadata(self.input_path)
            self.signals.result.emit(metadata)
            self.signals.finished.emit()
            
        except Exception as e:
            self.signals.error.emit(str(e))