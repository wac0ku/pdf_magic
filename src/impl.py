# Autor: Leon Gajtner
# Datum: 15.10.2024
# Projekt: PDF Magic impl file

import logging
from header import PDFConverterInterface
from PyQt5.QtCore import pyqtSignal
from pdf2docx import Converter
import docx
import os
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

class PDFConverter(PDFConverterInterface):
    """
    Konkrete Implementierung des PDF-Konverters mit einheitlichem Logging.
    """
    update_progress = pyqtSignal(int)
    update_log = pyqtSignal(str)

    def __init__(self, pdf_files, save_dir):
        super().__init__(pdf_files)
        self.save_dir = save_dir
        self.logger = logging.getLogger(__name__)
        self.setup_logging()

    def setup_logging(self):
        """
        Richtet das Logging für die Klasse ein.
        """
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # File handler
        file_handler = logging.FileHandler('pdf_converter.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Custom handler for GUI updates
        gui_handler = GUILogHandler(self.update_log)
        gui_handler.setFormatter(formatter)
        self.logger.addHandler(gui_handler)

    def log_info(self, message):
        """
        Protokolliert eine Informationsnachricht.
        """
        self.logger.info(message)

    def log_error(self, message):
        """
        Protokolliert eine Fehlermeldung.
        """
        self.logger.error(message)

    def run(self):
        """
        Hauptmethode zur Konvertierung von PDF-Dateien in DOCX.
        """
        total_files = len(self.pdf_files)
        for index, pdf_file in enumerate(self.pdf_files, start=1):
            try:
                # PDF in DOCX konvertieren
                docx_file = self.convert_pdf_to_docx(pdf_file)
                if docx_file:
                    # Formatierung des konvertierten Dokuments anpassen
                    self.format_docx(docx_file)

                    # PDF in Bilder konvertieren
                    self.convert_pdf_to_images(pdf_file)

                    # Text aus PDF extrahieren
                    self.extract_text_from_pdf(pdf_file)

                    self.log_info(f"Erfolgreich konvertiert und formatiert: {pdf_file}")
                else:
                    self.log_error(f"Fehler bei der Konvertierung von {pdf_file}")
            except Exception as e:
                self.log_error(f"Fehler bei der Konvertierung von {pdf_file}: {str(e)}")
            
            # Fortschritt aktualisieren
            progress = int((index / total_files) * 100)
            self.update_progress.emit(progress)

    def convert_pdf_to_docx(self, pdf_file):
        """
        Konvertiere eine PDF-Datei in DOCX-Format.
        """
        try:
            # Ausgabe-Dateiname mit dem ausgewählten Speicherort generieren
            docx_file = os.path.join(self.save_dir, os.path.basename(pdf_file).rsplit('.', 1)[0] + '.docx')

            # PDF in DOCX konvertieren
            cv = Converter(pdf_file)
            cv.convert(docx_file)
            cv.close()

            return docx_file
        except Exception as e:
            self.log_error(f"Fehler bei der Konvertierung von PDF zu DOCX: {str(e)}")
            return None

    def format_docx(self, docx_file):
        """
        Passe die Formatierung des konvertierten DOCX-Dokuments an.
        """
        try:
            # Öffne das konvertierte DOCX-Dokument
            doc = docx.Document(docx_file)

            # Formatierung für alle Absätze anpassen
            for paragraph in doc.paragraphs:
                paragraph.style.font.name = 'Arial'
                paragraph.style.font.size = docx.shared.Pt(11)

            # Formatierung für Tabellen anpassen
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            paragraph.style.font.name = 'Arial'
                            paragraph.style.font.size = docx.shared.Pt(11)

            # Formatiertes Dokument speichern
            doc.save(docx_file)

            self.log_info(f"Dokument formatiert und gespeichert: {docx_file}")
        except Exception as e:
            self.log_error(f"Fehler bei der Formatierung des Dokuments {docx_file}: {str(e)}")

    def convert_pdf_to_images(self, pdf_file):
        """
        Konvertiere eine PDF-Datei in Bilder (PNG).
        """
        try:
            images = convert_from_path(pdf_file)
            output_dir = os.path.join(self.save_dir, 'images', os.path.basename(pdf_file).rsplit('.', 1)[0])
            os.makedirs(output_dir, exist_ok=True)
            for i, image in enumerate(images):
                image_file = os.path.join(output_dir, f"page_{i + 1}.png")
                image.save(image_file, 'PNG')
            self.log_info(f"PDF in Bilder konvertiert: {pdf_file}")
        except Exception as e:
            self.log_error(f"Fehler bei der Konvertierung von PDF zu Bildern: {str(e)}")
    
    def extract_text_from_pdf(self, pdf_file):
        """
        Extrahiert den Text aus der PDF und speichert ihn in einer .txt-Datei.
        """
        try:
            text = pytesseract.image_to_string(pdf_file)
            text_file = os.path.join(self.save_dir, os.path.basename(pdf_file).rsplit('.', 1)[0] + '.txt')
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write(text)
            self.log_info(f"Text aus PDF extrahiert: {pdf_file}")
        except Exception as e:
            self.log_error(f"Fehler bei der Textextraktion aus PDF: {str(e)}")
    
    def convert_from_file(self, file):
        """
        Konvertiere eine beliebige Datei (z. B. PDF oder Bild) in ein anderes Format.
        """
        try:
            if file.lower().endswith('.pdf'):
                self.convert_pdf_to_docx(file)
            elif file.lower().endswith((".png", ".jpg", ".jpeg")):
                output_pdf = os.path.join(self.save_dir, os.path.basename(file).rsplit('.', 1)[0] + '.pdf')
                image = Image.open(file)
                image.convert('RGB').save(output_pdf)
                self.log_info(f"Bild in PDF konvertiert: {file}")
            else:
                self.log_error(f"Dateiformat wird nicht unterstützt: {file}")
        except Exception as e:
            self.log_error(f"Fehler bei der Dateikonvertierung: {str(e)}")

class GUILogHandler(logging.Handler):
    """
    Benutzerdefinierter Log-Handler zur Aktualisierung der GUI.
    """
    def __init__(self, signal):
        super().__init__()
        self.signal = signal

    def emit(self, record):
        log_entry = self.format(record)
        self.signal.emit(log_entry)