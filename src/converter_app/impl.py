# Author: Leon Gajtner
# Datum 15.10.2024
# Project: PDF Magic Implementation file

from header import PDFConverterInterface, DropAreaInterface
from PyQt5.QtWidgets import QTextEdit, QPushButton, QProgressBar, QFileDialog, QVBoxLayout, QLabel
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from PyQt5.QtCore import Qt 
from pdf2docx import Converter
import docx

class PDFConverter(PDFConverterInterface):
    """
    Concrete implementation of the PDF converter.
    """
    def run(self):
        """
        Main method to convert PDF files to DOCX.
        Processes each PDF file, updates progress, and emits status messages.
        """
        total_files = len(self.pdf_files)
        for index, pdf_file in enumerate(self.pdf_files, start=1):
            try:
                # Generate output filename
                docx_file = pdf_file.rsplit('.', 1)[0] + '.docx'
                
                # Convert PDF to DOCX
                cv = Converter(pdf_file)
                cv.convert(docx_file)
                cv.close()

                # Adjust formatting of the converted document
                doc = docx.Document(docx_file)
                for paragraph in doc.paragraphs:
                    paragraph.style.font.name = 'Arial'
                    paragraph.style.font.size = docx.shared.Pt(11)

                # Adjust formatting for tables
                for table in doc.tables:
                    for row in table.rows:
                        for cell in row.cells:
                            for paragraph in cell.paragraphs:
                                paragraph.style.font.name = 'Arial'
                                paragraph.style.font.size = docx.shared.Pt(11)

                # Save the formatted document
                doc.save(docx_file)
                self.update_log.emit(f"Erfolgreich konvertiert: {pdf_file}")
            except Exception as e:
                self.update_log.emit(f"Fehler bei der Konvertierung von {pdf_file}: {str(e)}")
            
            # Update progress
            progress = int((index / total_files) * 100)
            self.update_progress.emit(progress)

class DropArea(DropAreaInterface):
    """
    Concrete implementation of the drop area widget.
    """
    def __init__(self):
        """
        Initialize the drop area with a label.
        """
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("PDF-Dateien hier hineinziehen")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """
        Handle drag enter events.
        Accept the event if it contains URLs (potential file paths).
        
        :param event: The drag enter event
        """
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        """
        Handle drag move events.
        Allow copy action if the event contains URLs.
        
        :param event: The drag move event
        """
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        """
        Handle drop events.
        Process dropped files if they are PDFs and emit a signal with the file list.
        
        :param event: The drop event
        """
        files = [url.toLocalFile() for url in event.mimeData().urls() if url.toLocalFile().lower().endswith('.pdf')]
        if files:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            self.files_dropped.emit(files)
        else:
            event.ignore()