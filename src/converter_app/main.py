# Autor: Leon Gajtner
# Datum: 15.10.2024
# Projekt: PDF Magic Hauptdatei

import logging
from impl import PDFConverter, DropArea
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QProgressBar, QTextEdit, QFileDialog, QLabel
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import sys
import os

# Logging einrichten
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ModernButton(QPushButton):
    """
    Benutzerdefinierte Schaltflächenklasse mit modernem Stil.
    """
    def __init__(self, text, color):
        """
        Initialisiere eine ModernButton.

        :param text: Der auf der Schaltfläche angezeigte Text.
        :param color: Die Hintergrundfarbe der Schaltfläche.
        """
        super().__init__(text)
        try:
            # Schaltflächenstil mit CSS festlegen
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    border: none;
                    color: white;
                    padding: 10px 20px;
                    text-align: center;
                    text-decoration: none;
                    font-size: 16px;
                    margin: 4px 2px;
                    border-radius: 8px;
                }}
                QPushButton:hover {{
                    background-color: {QColor(color).darker(110).name()};
                }}
                QPushButton:pressed {{
                    background-color: {QColor(color).darker(120).name()};
                }}
            """)
        except Exception as e:
            logger.error(f"Fehler beim Einrichten des Button-Stils: {str(e)}")

class MainWindow(QMainWindow):
    """
    Hauptfenster der Anwendung für den PDF-zu-DOCX-Konverter.
    """
    def __init__(self):
        """
        Initialisiere das Hauptfenster und richte die Benutzeroberfläche ein.
        """
        super().__init__()
        try:
            self.setWindowTitle("PDF zu DOCX Konverter")
            self.setGeometry(100, 100, 800, 600)

            # Definiere eine moderne Farbpalette
            self.colors = {
                'background': '#F0F4F8',
                'primary': '#4A90E2',
                'secondary': '#50C878',
                'text': '#333333',
                'accent': '#FF6B6B'
            }

            # Stil des Hauptfensters festlegen
            self.setStyleSheet(f"""
                QMainWindow {{
                    background-color: {self.colors['background']};
                }}
                QLabel, QTextEdit {{
                    color: {self.colors['text']};
                }}
            """)

            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            layout = QVBoxLayout(central_widget)

            title_label = QLabel("PDF zu DOCX Konverter")
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setStyleSheet(f"""
                font-size: 24px;
                color: {self.colors['primary']};
                margin-bottom: 20px;
                font-weight: bold;
            """)
            layout.addWidget(title_label)

            # Drop-Bereich hinzufügen
            self.drop_area = DropArea()
            self.drop_area.setStyleSheet(f"""
                QWidget {{
                    border: 2px dashed {self.colors['primary']};
                    border-radius: 12px;
                    background-color: {QColor(self.colors['primary']).lighter(180).name()};
                    min-height: 150px;
                }}
                QWidget:hover {{
                    background-color: {QColor(self.colors['primary']).lighter(170).name()};
                }}
            """)
            self.drop_area.files_dropped.connect(self.add_files)
            layout.addWidget(self.drop_area)

            # Schaltflächen für Dateiauswahl und Konvertierung
            button_layout = QHBoxLayout()
            self.select_button = ModernButton("PDFs auswählen", self.colors['primary'])
            self.select_button.clicked.connect(self.select_files)
            button_layout.addWidget(self.select_button)

            self.convert_button = ModernButton("Konvertieren", self.colors['secondary'])
            self.convert_button.clicked.connect(self.start_conversion)
            button_layout.addWidget(self.convert_button)

            layout.addLayout(button_layout)

            # Fortschrittsanzeige hinzufügen
            self.progress_bar = QProgressBar()
            self.progress_bar.setStyleSheet(f"""
                QProgressBar {{
                    border: 2px solid {self.colors['primary']};
                    border-radius: 5px;
                    text-align: center;
                }}
                QProgressBar::chunk {{
                    background-color: {self.colors['secondary']};
                    width: 10px;
                    margin: 0.5px;
                }}
            """)
            layout.addWidget(self.progress_bar)

            # Protokolltextbereich hinzufügen
            self.log_text = QTextEdit()
            self.log_text.setReadOnly(True)
            self.log_text.setStyleSheet(f"""
                background-color: white;
                border: 1px solid {self.colors['primary']};
                border-radius: 5px;
                padding: 5px;
            """)
            layout.addWidget(self.log_text)

            self.pdf_files = []

            logger.info("Hauptfenster initialisiert.")
        except Exception as e:
            logger.error(f"Fehler beim Initialisieren des Hauptfensters: {str(e)}")

    def select_files(self):
        """
        Öffne ein Dateidialogfeld zur Auswahl von PDF-Dateien und füge sie der Konvertierungsliste hinzu.
        """
        try:
            files, _ = QFileDialog.getOpenFileNames(self, "PDFs auswählen", "", "PDF Dateien (*.pdf)")
            self.add_files(files)
        except Exception as e:
            logger.error(f"Fehler bei der Dateiauswahl: {str(e)}")

    def add_files(self, files):
        """
        Füge neue PDF-Dateien zur Konvertierungsliste hinzu und aktualisiere die Benutzeroberfläche.

        :param files: Liste von Dateipfaden, die hinzugefügt werden sollen.
        """
        try:
            new_files = [f for f in files if f not in self.pdf_files]
            self.pdf_files.extend(new_files)
            self.log_text.append(f"<span style='color: {self.colors['secondary']};'>{len(new_files)} neue PDF(s) hinzugefügt.</span>")
            logger.info(f"{len(new_files)} neue PDF(s) zur Konvertierung hinzugefügt.")
            self.update_drop_area_label()
        except Exception as e:
            logger.error(f"Fehler beim Hinzufügen von Dateien: {str(e)}")

    def update_drop_area_label(self):
        """
        Aktualisiere das Label des Drop-Bereichs, um die Anzahl der ausgewählten PDFs anzuzeigen.
        """
        try:
            if self.pdf_files:
                self.drop_area.label.setText(f"<span style='font-size: 18px;'>{len(self.pdf_files)} PDF(s) ausgewählt</span>")
            else:
                self.drop_area.label.setText("<span style='font-size: 18px;'>PDF-Dateien hier hineinziehen</span>")
            self.drop_area.label.setStyleSheet(f"color: {self.colors['primary']};")
        except Exception as e:
            logger.error(f"Fehler beim Aktualisieren des Drop-Bereich-Labels: {str(e)}")

    def start_conversion(self):
        """
        Starte den Konvertierungsprozess von PDF zu DOCX.
        """
        try:
            if not self.pdf_files:
                self.log_text.append(f"<span style='color: {self.colors['accent']};'>Keine PDF-Dateien ausgewählt.</span>")
                return

            self.converter = PDFConverter(self.pdf_files)
            self.converter.update_progress.connect(self.update_progress)
            self.converter.update_log.connect(self.update_log)
            self.converter.finished.connect(self.conversion_finished)
            self.converter.start()

            self.convert_button.setEnabled(False)
            self.select_button.setEnabled(False)
        except Exception as e:
            logger.error(f"Fehler beim Starten der Konvertierung: {str(e)}")

    def update_progress(self, value):
        """
        Aktualisiere den Wert der Fortschrittsanzeige.

        :param value: Der neue Fortschrittswert (0-100).
        """
        self.progress_bar.setValue(value)

    def update_log(self, message):
        """
        Füge dem Protokolltextbereich eine Nachricht hinzu und protokolliere sie.

        :param message: Die hinzuzufügende Nachricht.
        """
        self.log_text.append(f"<span style='color: {self.colors['text']};'>{message}</span>")
        logger.info(message)

    def conversion_finished(self):
        """
        Handhabe den Abschluss des Konvertierungsprozesses.
        """
        try:
            self.convert_button.setEnabled(True)
            self.select_button.setEnabled(True)
            self.pdf_files = []
            self.update_drop_area_label()
            self.log_text.append(f"<span style='color: {self.colors['secondary']};'>Konvertierung abgeschlossen.</span>")
            logger.info("Konvertierung abgeschlossen.")
        except Exception as e:
            logger.error(f"Fehler beim Abschluss der Konvertierung: {str(e)}")

    
    def setup_logging(log_dir='logs', log_file='application.log'):
        """
        Set up logging to a file.
        If the log directory doesn't exist, create it.

        :param log_dir: The directory where the log file should be stored
        :param log_file: The log file name
        """
        # Erstelle das Verzeichnis, falls es nicht existiert
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Pfad zur Log-Datei
        log_path = os.path.join(log_dir, log_file)

        # Setze Logging mit FileHandler
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            handlers=[
                                logging.FileHandler(log_path, mode='a'),  # 'a' für append (anhängen)
                                logging.StreamHandler()  # Optional: Konsolen-Logging
                            ])

        logging.info("Logging in Datei initialisiert: %s", log_path)

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
