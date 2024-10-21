# Autor: Leon Gajtner
# Datum: 15.10.2024
# Projekt: PDF Magic main file

import logging
from impl import PDFConverter
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QPushButton, QProgressBar, QTextEdit, 
                             QFileDialog, QLabel, QMessageBox)
from PyQt5.QtGui import QColor, QDragEnterEvent, QDropEvent
from PyQt5.QtCore import Qt
import sys
import os
import subprocess
import pkg_resources

# Logging einrichten
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Requirements installieren
def install_requirements(requirements_file=r"src\requirements.txt"):
    try:
        with open(requirements_file) as f:
            requirements = f.read().splitlines()

        installed_packages = {pkg.key for pkg in pkg_resources.working_set}
        missing_packages = [pkg for pkg in requirements if pkg.split('==')[0] not in installed_packages]

        if missing_packages:
            print(f"Installiere fehlende Pakete: {', '.join(missing_packages)}")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing_packages])
        else:
            print("Alle Anforderungen sind bereits erfüllt")
    except Exception as e:
        print(f"Fehler beim Installieren der Anforderungen: {str(e)}")
        sys.exit(1)

install_requirements()

class ModernButton(QPushButton):
    def __init__(self, text, color):
        super().__init__(text)
        try:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    border: none;
                    color: white;
                    padding: 10px 20px;
                    text-align: center;
                    font-size: 16px;
                    border-radius: 8px;
                }}
                QPushButton:hover {{
                    background-color: {QColor(color).lighter(110).name()};
                }}
                QPushButton:pressed {{
                    background-color: {QColor(color).darker(110).name()};
                }}
            """)
        except Exception as e:
            logger.error(f"Fehler beim Einrichten des Button-Stils: {str(e)}")

class EnhancedDropArea(QWidget):
    """
    Schnittstelle für ein Drop-Bereich-Widget.
    Ermöglicht Drag-and-Drop-Funktionalität für Dateien.
    """
    def __init__(self, parent=None):
        """
        Initialisiere das Drop-Bereich-Widget.
        Konfiguriert das Widget, um Drop-Ereignisse zu akzeptieren.
        """
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setMinimumSize(400, 200)
        self.files = []

        layout = QVBoxLayout(self)
        self.label = QLabel("PDF-Dateien hier hineinziehen oder klicken, um auszuwählen")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            color: #666;
            font-size: 18px;
        """)
        layout.addWidget(self.label)

        self.setStyleSheet("""
            EnhancedDropArea {
                border: 2px dashed #aaa;
                border-radius: 10px;
                background-color: #f8f8f8;
            }
            EnhancedDropArea:hover {
                border-color: #4A90E2;
            }
        """)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """
        Abstrakte Methode zur Handhabung von Drag-Eingabe-Ereignissen.
        Muss in abgeleiteten Klassen implementiert werden.

        :param event: Das Drag-Eingabe-Ereignis
        """
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        """
        Abstrakte Methode zur Handhabung von Drag-Bewegungs-Ereignissen.
        Muss in abgeleiteten Klassen implementiert werden.

        :param event: Das Drag-Bewegungs-Ereignis
        """
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        """
        Abstrakte Methode zur Handhabung von Drop-Ereignissen.
        Muss in abgeleiteten Klassen implementiert werden.

        :param event: Das Drop-Ereignis
        """
        files = [url.toLocalFile() for url in event.mimeData().urls() if url.toLocalFile().lower().endswith('.pdf')]
        if files:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            self.files.extend(files)
            self.update_label()
        else:
            event.ignore()

    def mousePressEvent(self, event):
        files, _ = QFileDialog.getOpenFileNames(self, "PDF-Dateien auswählen", "", "PDF-Dateien (*.pdf)")
        if files:
            self.files.extend(files)
            self.update_label()

    def update_label(self):
        if self.files:
            self.label.setText(f"{len(self.files)} PDF-Datei(en) ausgewählt")
        else:
            self.label.setText("PDF-Dateien hier hineinziehen oder klicken, um auszuwählen")

    def get_files(self):
        return self.files

    def clear_files(self):
        self.files.clear()
        self.update_label()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            self.setWindowTitle("PDF Magic")
            self.setGeometry(100, 100, 800, 600)

            self.save_dir = os.path.expanduser("~")

            self.colors = {
                'background': '#F0F4F8',
                'primary': '#4A90E2',
                'secondary': '#50C878',
                'text': '#333333',
                'accent': '#FF6B6B',
                'button1': '#3498db',
                'button2': '#2ecc71',
                'button3': '#e74c3c',
                'button4': '#f39c12',
                'button5': '#9b59b6'
            }

            self.converter = None

            self.setStyleSheet(f"QMainWindow {{background-color: {self.colors['background']};}}")

            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            layout = QVBoxLayout(central_widget)

            title_label = QLabel("PDF Magic Converter")
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setStyleSheet(f"""
                font-size: 24px;
                color: {self.colors['primary']};
                margin-bottom: 20px;
                font-weight: bold;
            """)
            layout.addWidget(title_label)

            self.drop_area = EnhancedDropArea()
            layout.addWidget(self.drop_area)

            button_layout = QHBoxLayout()

            self.save_dir_button = ModernButton("Speicherort festlegen", self.colors['button1'])
            self.save_dir_button.clicked.connect(self.set_save_directory)
            button_layout.addWidget(self.save_dir_button)

            self.convert_button = ModernButton("Konvertieren", self.colors['button2'])
            self.convert_button.clicked.connect(self.start_conversion)
            button_layout.addWidget(self.convert_button)

            self.pdf_to_img_button = ModernButton("PDF zu Bild", self.colors['button3'])
            self.pdf_to_img_button.clicked.connect(self.start_pdf_to_image_conversion)
            button_layout.addWidget(self.pdf_to_img_button)

            self.extract_text_button = ModernButton("Text extrahieren", self.colors['button4'])
            self.extract_text_button.clicked.connect(self.start_text_extraction)
            button_layout.addWidget(self.extract_text_button)

            self.convert_file_button = ModernButton("Konvertiere Datei", self.colors['button5'])
            self.convert_file_button.clicked.connect(self.start_file_conversion)
            button_layout.addWidget(self.convert_file_button)

            layout.addLayout(button_layout)

            self.progress_bar = QProgressBar()
            layout.addWidget(self.progress_bar)

            self.log_text = QTextEdit()
            self.log_text.setReadOnly(True)
            layout.addWidget(self.log_text)

        except Exception as e:
            logger.error(f"Fehler beim Initialisieren des Hauptfensters: {str(e)}")

    @staticmethod
    def setup_logging(log_dir='logs', log_file='pdf_converter.log'):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_path = os.path.join(log_dir, log_file)
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            handlers=[
                                logging.FileHandler(log_path, mode='a'),
                                logging.StreamHandler()
                            ])
        logging.info("Logging in Datei initialisiert: %s", log_path)

    def set_save_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Speicherort auswählen", self.save_dir)
        if directory:
            self.save_dir = directory
            self.log_text.append(f"<span style='color: {self.colors['secondary']};'>Speicherort festgelegt: {self.save_dir}</span>")
            logger.info(f"Speicherort festgelegt: {self.save_dir}")

    def start_conversion(self):
        pdf_files = self.drop_area.get_files()
        if not pdf_files:
            self.log_text.append(f"<span style='color: #FF6B6B;'>Keine PDF-Dateien ausgewählt.</span>")
            return
        self.converter = PDFConverter(pdf_files, self.save_dir)
        self.converter.update_progress.connect(self.update_progress_bar)
        self.converter.update_log.connect(self.update_log_text)
        self.convert_button.setEnabled(False)
        self.converter.run()
        self.drop_area.clear_files()

    def update_progress_bar(self, progress):
        self.progress_bar.setValue(progress)

    def update_log_text(self, log_entry):
        self.log_text.append(log_entry)

    def start_pdf_to_image_conversion(self):
        pdf_files = self.drop_area.get_files()
        if not pdf_files:
            self.log_text.append(f"<span style='color: #FF6B6B;'>Keine PDF-Dateien ausgewählt.</span>")
            return
        self.converter = PDFConverter(pdf_files, self.save_dir)
        self.converter.convert_pdf_to_images(pdf_files)
        self.drop_area.clear_files()

    def start_text_extraction(self):
        pdf_files = self.drop_area.get_files()
        if not pdf_files:
            self.log_text.append(f"<span style='color: #FF6B6B;'>Keine PDF-Dateien ausgewählt.</span>")
            return
        self.converter = PDFConverter(pdf_files, self.save_dir)
        self.converter.extract_text_from_pdf(pdf_files)
        self.drop_area.clear_files()

    def start_file_conversion(self):
        file, _ = QFileDialog.getOpenFileName(self, "Datei auswählen", "", "Alle Dateien (*)")
        if file:
            self.converter = PDFConverter([file], self.save_dir)
            self.converter.convert_from_file(file)

    def conversion_finished(self):
        """
        Handhabe den Abschluss des Konvertierungsprozesses.
        """
        try:
            self.convert_button.setEnabled(True)
            self.select_button.setEnabled(True)

            # Frage User, ob er die Konbvertierten Dateien öffnen möchte
            reply = QMessageBox.question(self, 'Datei öffnen',
                                         "Möchten Sie die konvertierten Dateien jetzt öffnen?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.open_converted_files()

            self.log_text.append(f"<span style='color: {self.colors['secondary']};'>Konvertierung abgeschlossen.</span>")
            logger.info("Konvertierung abgeschlossen.")

        except Exception as e:
            logger.error(f"Fehler beim Abschluss der Konvertierung: {str(e)}")

if __name__ == "__main__":
    MainWindow.setup_logging(log_dir='logs', log_file='pdf_converter.log')
    try:
        app = QApplication(sys.argv)
        app.setStyle("Fusion")
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        logger.error(f"Fehler beim Start der Anwendung: {str(e)}")