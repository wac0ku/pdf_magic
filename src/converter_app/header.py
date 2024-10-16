# Author: Leon Gajtner
# Datum 15.10.2024
# Project: PDF Magic header file

from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QDropEvent, QDragEnterEvent

class PDFConverterInterface(QThread):
    """
    Interface for PDF converter thread.
    Inherits from QThread to allow background processing.
    """
    update_progress = pyqtSignal(int)
    update_log = pyqtSignal(str)
    
    def __init__(self, pdf_files):
        """
        Initialize the PDF converter with a list of PDF files.
        
        :param pdf_files: List of paths to PDF files for conversion
        """
        super().__init__()
        self.pdf_files = pdf_files

    def run(self):
        """
        Abstract method to be implemented in derived classes.
        This method will contain the main conversion logic.
        """
        raise NotImplementedError("Methode 'run' muss in der abgeleiteten Klasse implementiert werden.")


class DropAreaInterface(QWidget):
    """
    Interface for a drop area widget.
    Allows drag and drop functionality for files.
    """
    files_dropped = pyqtSignal(list)

    def __init__(self):
        """
        Initialize the drop area widget.
        Sets up the widget to accept drop events.
        """
        super().__init__()
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """
        Abstract method to handle drag enter events.
        To be implemented in derived classes.
        
        :param event: The drag enter event
        """
        raise NotImplementedError("Methode 'dragEnterEvent' muss in der abgeleiteten Klasse implementiert werden.")

    def dragMoveEvent(self, event):
        """
        Abstract method to handle drag move events.
        To be implemented in derived classes.
        
        :param event: The drag move event
        """
        raise NotImplementedError("Methode 'dragMoveEvent' muss in der abgeleiteten Klasse implementiert werden.")

    def dropEvent(self, event: QDropEvent):
        """
        Abstract method to handle drop events.
        To be implemented in derived classes.
        
        :param event: The drop event
        """
        raise NotImplementedError("Methode 'dropEvent' muss in der abgeleiteten Klasse implementiert werden.")