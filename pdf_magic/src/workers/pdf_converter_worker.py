from PyQt5.QtCore import QRunnable
from .base_worker import BaseWorker
import fitz  # PyMuPDF

class PDFConverterWorker(QRunnable, BaseWorker):
    def __init__(self, pdf_path, output_format):
        QRunnable.__init__(self)
        BaseWorker.__init__(self)
        self.pdf_path = pdf_path
        self.output_format = output_format

    def run(self):
        try:
            doc = fitz.open(self.pdf_path)
            total_pages = len(doc)

            for page_num in range(total_pages):
                page = doc.load_page(page_num)
                
                if self.output_format == 'docx':
                    # Convert to DOCX (simplified, you might need a more complex solution)
                    text = page.get_text()
                    # Here you would save the text to a .docx file
                elif self.output_format == 'image':
                    pix = page.get_pixmap()
                    pix.save(f"page_{page_num + 1}.png")

                progress = int((page_num + 1) / total_pages * 100)
                self.progress.emit(progress)

            doc.close()
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))