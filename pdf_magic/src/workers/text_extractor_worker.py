import os
from PyQt5.QtCore import QRunnable, pyqtSlot
from PyQt5.QtCore import QObject, pyqtSignal
import fitz  # PyMuPDF
from utils.error_handler import ErrorHandler

class TextExtractorWorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    result = pyqtSignal(str, str)  # Emits extracted text and output file path

class TextExtractorWorker(QRunnable):
    def __init__(self, pdf_path, output_dir):
        super(TextExtractorWorker, self).__init__()
        self.pdf_path = pdf_path
        self.output_dir = output_dir
        self.signals = TextExtractorWorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            doc = fitz.open(self.pdf_path)
            total_pages = len(doc)
            extracted_text = ""

            for page_num in range(total_pages):
                page = doc.load_page(page_num)
                extracted_text += page.get_text()

                progress = int((page_num + 1) / total_pages * 100)
                self.signals.progress.emit(progress)

            doc.close()

            # Create output filename
            base_name = os.path.splitext(os.path.basename(self.pdf_path))[0]
            output_path = os.path.join(self.output_dir, f"{base_name}_extracted.txt")

            # Save extracted text to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(extracted_text)

            self.signals.result.emit(extracted_text, output_path)
            self.signals.finished.emit()

        except Exception as e:
            error_message = f"Error extracting text from {self.pdf_path}: {str(e)}"
            ErrorHandler.handle_error(error_message)
            self.signals.error.emit(error_message)

    def extract_text_from_page(self, page):
        """
        Extract text from a single page.
        This method can be extended to handle different text extraction methods.
        """
        return page.get_text()

    @staticmethod
    def clean_text(text):
        """
        Clean and format the extracted text.
        This method can be extended to include more text processing if needed.
        """
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Add more text cleaning operations as needed
        return text

    def extract_text_with_ocr(self, page):
        """
        Extract text using OCR for pages where normal extraction fails.
        This is a placeholder and would require integration with an OCR library.
        """
        # Placeholder for OCR implementation
        # You would need to integrate with an OCR library like Tesseract here
        pass