# Autor: Leon Gajtner
# Datum: 22.10.2024
# PDF Magic - PDF Processor file

import os
from PyQt5.QtCore import QThread, pyqtSignal
from pdf2docx import Converter
import fitz
from PIL import Image
import json
from utils.logger import logger

class PDFProcessor(QThread):
    progress_changed = pyqtSignal(int)
    log_changed = pyqtSignal(str)
    process_completed = pyqtSignal()

    def __init__(self, input_files, save_dir, operation):
        super().__init__()
        self.input_files = input_files
        self.save_dir = save_dir
        self.operation = operation

    def stop(self):
        logger.info("Stopping PDFProcessor thread...")
        try:
            self.requestInterruption()
            self.wait()  # Warte, bis der Thread beendet ist
        except Exception as e:
            logger.error(f"Error stopping thread: {e}")

    def run(self):
        operation_methods = {
            'convert': self.convert_to_docx,
            'extract': self.extract_text,
            'metadata': self.extract_metadata,
            'image_to_pdf': self.images_to_pdf,
            'merge': self.merge_pdfs,
            'split': self.split_pdf
        }
        
        method = operation_methods.get(self.operation)
        if method:
            method()
        else:
            self.log_changed.emit(f"Ungültige Operation: {self.operation}")

        self.process_completed.emit()

    def convert_to_docx(self):
        logger.info("Start PDF zu DOCX Konvertierung...")
        total_files = len(self.input_files)
        for i, pdf_file in enumerate(self.input_files):
            if self.isInterruptionRequested():
                self.log_changed.emit("Konvertierung abgebrochen")
                break
            try:
                output_file = os.path.join(self.save_dir, f"{os.path.splitext(os.path.basename(pdf_file))[0]}.docx")
                cv = Converter(pdf_file)
                cv.convert(output_file)
                cv.close()
                self.log_changed.emit(f"Konvertiert: {pdf_file} zu {output_file}")
            except Exception as e:
                self.log_changed.emit(f"Fehler bei der Konvertierung von {pdf_file}: {str(e)}")
                logger.error(f"Error in convert_to_docx of {pdf_file}: {str(e)}")
            
            progress = int((i + 1) / total_files * 100)
            self.progress_changed.emit(progress)

    def extract_text(self):
        logger.info("Start Text-Extraktion...")
        total_files = len(self.input_files)
        for i, pdf_file in enumerate(self.input_files):
            if self.isInterruptionRequested():
                self.log_changed.emit("Textextraktion abgebrochen")
                break
            try:
                doc = fitz.open(pdf_file)
                text = ""
                for page in doc:
                    text += page.get_text()
                
                output_file = os.path.join(self.save_dir, f"{os.path.splitext(os.path.basename(pdf_file))[0]}_text.txt")
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(text)
                self.log_changed.emit(f"Text extrahiert: {pdf_file} zu {output_file}")
            except Exception as e:
                self.log_changed.emit(f"Fehler bei der Textextraktion von {pdf_file}: {str(e)}")
                logger.error(f"Error in extract_text of {pdf_file}: {str(e)}")

            
            progress = int((i + 1) / total_files * 100)
            self.progress_changed.emit(progress)

    def extract_metadata(self):
        logger.info("Start Metadaten-Extraktion...")
        total_files = len(self.input_files)
        for i, pdf_file in enumerate(self.input_files):
            if self.isInterruptionRequested():
                self.log_changed.emit("Metadatenextraktion abgebrochen")
                break
            try:
                doc = fitz.open(pdf_file)
                metadata = {
                    "author": doc.metadata["author"], "creator": doc.metadata["creator"], 
                    "creation_date": doc.metadata["creation_date"], 
                    "modification_date": doc.metadata["modification_date"], 
                    "producer": doc.metadata["producer"], 
                    "subject": doc.metadata["subject"], 
                    "title": doc.metadata["title"]
                }
                output_file = os.path.join(self.save_dir, f"{os.path.splitext(os.path.basename(pdf_file))[0]}_metadata.json")
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(metadata, f, indent=4)
                self.log_changed.emit(f"Metadaten extrahiert: {pdf_file} zu {output_file}")
            except Exception as e:
                self.log_changed.emit(f"Fehler bei der Metadatenextraktion von {pdf_file}: {str(e)}")
                logger.error(f"Error in extract_metadata of {pdf_file}: {str(e)}")
            
            progress = int((i + 1) / total_files * 100)
            self.progress_changed.emit(progress)
            logger.info("Metadatenextraktion erfolgreich abgeschlossen.")

    def images_to_pdf(self):
        logger.info("Start Bildextraktion...")

        total_files = len(self.input_files)
        for i, image_file in enumerate(self.input_files):
            if self.isInterruptionRequested():
                self.log_changed.emit("Bild zu PDF-Konvertierung abgebrochen")
                break
            try:
                image = Image.open(image_file)
                output_file = os.path.join(self.save_dir, f"{os.path.splitext(os.path.basename(image_file))[0]}.pdf")
                image.save(output_file, "PDF", resolution=100.0)
                self.log_changed.emit(f"Bild konvertiert: {image_file} zu {output_file}")
            except Exception as e:
                self.log_changed.emit(f"Fehler bei der Bildkonvertierung von {image_file}: {str(e)}")
                logger.error(f"Error in images_to_pdf of {image_file}: {str(e)}")

            
            progress = int((i + 1) / total_files * 100)
            self.progress_changed.emit(progress)
            logger.info("Bildextraktion erfolgreich abgeschlossen.")

    def merge_pdfs(self):
        logger.info("Start PDF-Vereinigung...")
        try:
            output_file = os.path.join(self.save_dir, "Merged.pdf")
            merger = fitz.open()
            for pdf_file in self.input_files:
                with fitz.open(pdf_file) as doc:
                    merger.append_doc(doc)
            merger.save(output_file)
            merger.close()
            self.log_changed.emit(f"PDF-Dateien zusammengeführt: {', '.join(self.input_files)} zu {output_file}")
            logger.info(f"PDF-Dateien zusammengeführt: {', '.join(self.input_files)} zu {output_file}")
        except Exception as e:
            self.log_changed.emit(f"Fehler bei der Zusammenführung von {', '.join(self.input_files)}: {str(e)}")

    def split_pdf(self):
        logger.info("Start PDF-Spaltung...")

        total_files = len(self.input_files)
        for i, pdf_file in enumerate(self.input_files):
            if self.isInterruptionRequested():
                self.log_changed.emit("PDF-Aufteilung abgebrochen")
                break
            try:
                doc = fitz.open(pdf_file)
                for page in range(doc.page_count):
                    output_file = os.path.join(self.save_dir, f"{os.path.splitext(os.path.basename(pdf_file))[0]}_page{page+1}.pdf")
                    with fitz.open() as new_doc:
                        new_doc.insert_pdf(doc, from_page=page, to_page=page)
                        new_doc.save(output_file)
                    self.log_changed.emit(f"PDF aufgeteilt: {pdf_file} zu {output_file}")
                    logger.info(f"PDF aufgeteilt: {pdf_file} zu {output_file}")
            except Exception as e:
                self.log_changed.emit(f"Fehler bei der Aufteilung von {pdf_file}: {str(e)}")
                logger.error(f"Error in split_pdf of {pdf_file}: {str(e)}")

            
            progress = int((i + 1) / total_files * 100)
            self.progress_changed.emit(progress)
            logger.info(f"Aufteilung von {pdf_file} zu {output_file} erfolgreich abgeschlossen.")