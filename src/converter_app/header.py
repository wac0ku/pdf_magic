# Autor: Leon Gajtner
# Datum: 15.10.2024
# Projekt: PDF Magic Header Datei

import logging
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QDropEvent, QDragEnterEvent

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

class DropAreaInterface(QWidget):
    """
    Schnittstelle für ein Drop-Bereich-Widget.
    Ermöglicht Drag-and-Drop-Funktionalität für Dateien.
    """
    files_dropped = pyqtSignal(list)

    def __init__(self):
        """
        Initialisiere das Drop-Bereich-Widget.
        Konfiguriert das Widget, um Drop-Ereignisse zu akzeptieren.
        """
        super().__init__()
        self.setAcceptDrops(True)
        logger.info("DropAreaInterface initialisiert.")

    def dragEnterEvent(self, event: QDragEnterEvent):
        """
        Abstrakte Methode zur Handhabung von Drag-Eingabe-Ereignissen.
        Muss in abgeleiteten Klassen implementiert werden.

        :param event: Das Drag-Eingabe-Ereignis
        """
        raise NotImplementedError("Methode 'dragEnterEvent' muss in der abgeleiteten Klasse implementiert werden.")

    def dragMoveEvent(self, event):
        """
        Abstrakte Methode zur Handhabung von Drag-Bewegungs-Ereignissen.
        Muss in abgeleiteten Klassen implementiert werden.

        :param event: Das Drag-Bewegungs-Ereignis
        """
        raise NotImplementedError("Methode 'dragMoveEvent' muss in der abgeleiteten Klasse implementiert werden.")

    def dropEvent(self, event: QDropEvent):
        """
        Abstrakte Methode zur Handhabung von Drop-Ereignissen.
        Muss in abgeleiteten Klassen implementiert werden.

        :param event: Das Drop-Ereignis
        """
        raise NotImplementedError("Methode 'dropEvent' muss in der abgeleiteten Klasse implementiert werden.")