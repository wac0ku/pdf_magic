# Autor: Leon Gajtner
# Datum: 15.10.2024
# Projekt: PDF Magic Header file

import logging
from PyQt5.QtCore import pyqtSignal, QThread

# Logging einrichten
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PDFConverterInterface(QThread):
    """
    Schnittstelle für den PDF-Konverter-Thread.
    Erbt von QThread, um Hintergrundverarbeitung zu ermöglichen.
    """
    update_progress = pyqtSignal(int)
    update_log = pyqtSignal(str)

    def __init__(self, pdf_files):
        """
        Initialisiere den PDF-Konverter mit einer Liste von PDF-Dateien.

        :param pdf_files: Liste von Pfaden zu PDF-Dateien zur Konvertierung
        """
        super().__init__()
        self.pdf_files = pdf_files
        logger.info("PDFConverterInterface initialisiert.")

    def run(self):
        """
        Abstrakte Methode, die in abgeleiteten Klassen implementiert werden muss.
        Diese Methode enthält die Hauptlogik zur Konvertierung.
        """
        raise NotImplementedError("Methode 'run' muss in der abgeleiteten Klasse implementiert werden.")